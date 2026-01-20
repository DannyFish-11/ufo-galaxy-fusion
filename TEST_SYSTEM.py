#!/usr/bin/env python3
"""
UFO³ Galaxy 系统测试脚本
测试所有组件是否正常工作
"""

import asyncio
import json
import sys
import time
from datetime import datetime

try:
    import websockets
    import requests
except ImportError:
    print("[错误] 缺少依赖，正在安装...")
    import os
    os.system("pip install websockets requests")
    import websockets
    import requests

# 测试配置
NODE50_URL = "ws://localhost:8050"
NODE50_HTTP = "http://localhost:8050"
DEVICE_ID = "test-client"

class SystemTester:
    """系统测试器"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
    
    def test(self, name: str, func):
        """运行单个测试"""
        print(f"\n[测试] {name}...")
        try:
            result = func()
            if asyncio.iscoroutine(result):
                result = asyncio.run(result)
            
            if result:
                print(f"  ✓ 通过")
                self.tests_passed += 1
                self.test_results.append((name, True, None))
                return True
            else:
                print(f"  ✗ 失败")
                self.tests_failed += 1
                self.test_results.append((name, False, "测试返回 False"))
                return False
        except Exception as e:
            print(f"  ✗ 失败: {e}")
            self.tests_failed += 1
            self.test_results.append((name, False, str(e)))
            return False
    
    def test_node50_http(self):
        """测试 Node 50 HTTP 接口"""
        try:
            response = requests.get(f"{NODE50_HTTP}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"    Node 50 版本: {data.get('version')}")
                print(f"    活跃连接: {data.get('active_connections')}")
                return True
            return False
        except Exception as e:
            raise Exception(f"无法连接到 Node 50: {e}")
    
    def test_node50_health(self):
        """测试 Node 50 健康检查"""
        try:
            response = requests.get(f"{NODE50_HTTP}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"    状态: {data.get('status')}")
                print(f"    OneAPI: {'可用' if data.get('oneapi_available') else '不可用'}")
                return data.get('status') == 'healthy'
            return False
        except Exception as e:
            raise Exception(f"健康检查失败: {e}")
    
    async def test_websocket_connection(self):
        """测试 WebSocket 连接"""
        try:
            ws_url = f"{NODE50_URL}/ws/ufo3/{DEVICE_ID}"
            async with websockets.connect(ws_url, ping_interval=None) as websocket:
                print(f"    已连接到: {ws_url}")
                
                # 发送注册消息
                message = {
                    "protocol": "AIP/1.0",
                    "message_id": f"test_{int(time.time())}",
                    "timestamp": datetime.now().isoformat(),
                    "from": DEVICE_ID,
                    "to": "Node_50",
                    "type": "registration",
                    "payload": {
                        "device_type": "Test_Client",
                        "capabilities": ["test"]
                    }
                }
                
                await websocket.send(json.dumps(message))
                print(f"    已发送注册消息")
                
                # 等待响应（最多 5 秒）
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    print(f"    收到响应")
                    return True
                except asyncio.TimeoutError:
                    print(f"    警告: 未收到响应，但连接成功")
                    return True
        except Exception as e:
            raise Exception(f"WebSocket 连接失败: {e}")
    
    async def test_command_processing(self):
        """测试命令处理"""
        try:
            ws_url = f"{NODE50_URL}/ws/ufo3/{DEVICE_ID}"
            async with websockets.connect(ws_url, ping_interval=None) as websocket:
                # 发送测试命令
                message = {
                    "protocol": "AIP/1.0",
                    "message_id": f"test_{int(time.time())}",
                    "timestamp": datetime.now().isoformat(),
                    "from": DEVICE_ID,
                    "to": "Node_50",
                    "type": "command",
                    "payload": {
                        "command": "打印一个测试模型",
                        "context": {}
                    }
                }
                
                await websocket.send(json.dumps(message))
                print(f"    已发送测试命令")
                
                # 等待响应
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(response)
                    if data.get("type") == "response":
                        task_plan = data.get("payload", {}).get("task_plan", {})
                        intent = task_plan.get("intent", "unknown")
                        print(f"    命令理解: {intent}")
                        return True
                    return False
                except asyncio.TimeoutError:
                    raise Exception("命令处理超时")
        except Exception as e:
            raise Exception(f"命令处理失败: {e}")
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("测试摘要")
        print("=" * 60)
        
        total = self.tests_passed + self.tests_failed
        print(f"\n总计: {total} 个测试")
        print(f"通过: {self.tests_passed} ✓")
        print(f"失败: {self.tests_failed} ✗")
        
        if self.tests_failed > 0:
            print("\n失败的测试:")
            for name, passed, error in self.test_results:
                if not passed:
                    print(f"  - {name}")
                    if error:
                        print(f"    错误: {error}")
        
        print("\n" + "=" * 60)
        
        if self.tests_failed == 0:
            print("✓ 所有测试通过！系统运行正常。")
            return 0
        else:
            print("✗ 部分测试失败，请检查系统配置。")
            return 1

def main():
    """主函数"""
    print("=" * 60)
    print("UFO³ Galaxy 系统测试")
    print("=" * 60)
    print("\n请确保以下服务已启动:")
    print("  1. Podman 容器 (Node 50, 43, 48)")
    print("  2. Tailscale 网络")
    print("\n按回车键开始测试...")
    input()
    
    tester = SystemTester()
    
    # 运行测试
    tester.test("Node 50 HTTP 接口", tester.test_node50_http)
    tester.test("Node 50 健康检查", tester.test_node50_health)
    tester.test("WebSocket 连接", tester.test_websocket_connection)
    tester.test("命令处理", tester.test_command_processing)
    
    # 打印摘要
    exit_code = tester.print_summary()
    
    print("\n按回车键退出...")
    input()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试已取消")
        sys.exit(1)
