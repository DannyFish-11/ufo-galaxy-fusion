#!/usr/bin/env python3
"""
UFO³ Galaxy 端到端测试脚本
测试从 PC 到安卓设备的完整通信链路

版本: 1.0
日期: 2026-01-22
"""

import asyncio
import httpx
import sys
import time
from pathlib import Path

# 测试配置
GATEWAY_URL = "http://localhost:8001"  # Gateway 地址
TIMEOUT = 30  # 超时时间（秒）

class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    """打印测试名称"""
    print(f"\n{Colors.BLUE}[测试] {name}{Colors.END}")

def print_success(message):
    """打印成功信息"""
    print(f"{Colors.GREEN}  ✓ {message}{Colors.END}")

def print_error(message):
    """打印错误信息"""
    print(f"{Colors.RED}  ✗ {message}{Colors.END}")

def print_warning(message):
    """打印警告信息"""
    print(f"{Colors.YELLOW}  ⚠️  {message}{Colors.END}")

async def test_node_health(node_id: int, node_name: str):
    """测试节点健康状态"""
    print_test(f"节点健康检查: Node_{node_id:02d}_{node_name}")
    
    url = f"http://localhost:{8000 + node_id}/health"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")
                
                if status in ["healthy", "ok"]:
                    print_success(f"{node_name} 运行正常")
                    return True
                else:
                    print_warning(f"{node_name} 状态异常: {status}")
                    return False
            else:
                print_error(f"{node_name} 返回错误: HTTP {response.status_code}")
                return False
    
    except httpx.ConnectError:
        print_error(f"{node_name} 连接失败 (节点可能未启动)")
        return False
    except Exception as e:
        print_error(f"{node_name} 测试失败: {e}")
        return False

async def test_smart_transport_router():
    """测试智能传输路由"""
    print_test("智能传输路由 (SmartTransportRouter)")
    
    url = "http://localhost:8096/route"
    
    payload = {
        "device_id": "test_device",
        "task_type": "dynamic",
        "quality": "high",
        "realtime": True
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                method = data.get("method")
                network = data.get("network")
                signal = data.get("signal")
                
                print_success(f"路由成功")
                print(f"    传输方式: {method}")
                print(f"    网络层: {network}")
                print(f"    信令: {signal}")
                return True
            else:
                print_error(f"路由失败: HTTP {response.status_code}")
                return False
    
    except httpx.ConnectError:
        print_error(f"连接失败 (Node_96 可能未启动)")
        return False
    except Exception as e:
        print_error(f"测试失败: {e}")
        return False

async def test_adb_connection():
    """测试 ADB 连接"""
    print_test("ADB 设备连接")
    
    import subprocess
    
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        devices = [line for line in result.stdout.split('\n') if '\tdevice' in line]
        
        if devices:
            print_success(f"检测到 {len(devices)} 台设备:")
            for device in devices:
                device_id = device.split()[0]
                print(f"    - {device_id}")
            return True, [d.split()[0] for d in devices]
        else:
            print_warning("未检测到连接的设备")
            print("    请确保:")
            print("    1. 设备已通过 USB 连接到 PC")
            print("    2. 设备已开启 USB 调试")
            print("    3. 已授权 PC 的 USB 调试请求")
            return False, []
    
    except FileNotFoundError:
        print_error("ADB 未安装")
        return False, []
    except Exception as e:
        print_error(f"测试失败: {e}")
        return False, []

async def test_adb_screenshot(device_id: str):
    """测试 ADB 截图"""
    print_test(f"ADB 截图测试 (设备: {device_id})")
    
    import subprocess
    import tempfile
    
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        
        # 执行截图命令
        result = subprocess.run(
            ["adb", "-s", device_id, "exec-out", "screencap", "-p"],
            capture_output=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            # 保存截图
            with open(tmp_path, 'wb') as f:
                f.write(result.stdout)
            
            # 检查文件大小
            size = Path(tmp_path).stat().st_size
            
            if size > 1000:  # 至少 1KB
                print_success(f"截图成功 (大小: {size / 1024:.1f} KB)")
                print(f"    保存位置: {tmp_path}")
                return True
            else:
                print_error(f"截图文件过小 ({size} 字节)")
                return False
        else:
            print_error(f"截图失败")
            return False
    
    except subprocess.TimeoutExpired:
        print_error("截图超时")
        return False
    except Exception as e:
        print_error(f"测试失败: {e}")
        return False

async def test_quantum_dispatcher():
    """测试量子任务调度器"""
    print_test("量子任务调度器 (Node_51)")
    
    url = "http://localhost:8051/dispatch"
    
    payload = {
        "prompt": "Find the shortest path for 5 cities",
        "problem_type": "optimization",
        "max_qubits": 10,
        "shots": 1024
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                algorithm = data.get("recommended_algorithm")
                
                print_success(f"量子任务调度成功")
                print(f"    推荐算法: {algorithm}")
                return True
            else:
                print_error(f"调度失败: HTTP {response.status_code}")
                return False
    
    except httpx.ConnectError:
        print_warning(f"连接失败 (Node_51 可能未启动或量子功能未启用)")
        return False
    except Exception as e:
        print_error(f"测试失败: {e}")
        return False

async def main():
    """主测试流程"""
    print("=" * 60)
    print("  UFO³ Galaxy 端到端测试")
    print("=" * 60)
    
    results = {}
    
    # 1. 测试核心节点
    print("\n" + "=" * 60)
    print("  第一部分: 核心节点健康检查")
    print("=" * 60)
    
    core_nodes = [
        (0, "StateMachine"),
        (1, "OneAPI"),
        (33, "ADB"),
        (96, "SmartTransportRouter"),
    ]
    
    for node_id, node_name in core_nodes:
        results[f"Node_{node_id:02d}"] = await test_node_health(node_id, node_name)
        await asyncio.sleep(0.5)
    
    # 2. 测试智能传输路由
    print("\n" + "=" * 60)
    print("  第二部分: 智能传输路由测试")
    print("=" * 60)
    
    results["SmartTransportRouter"] = await test_smart_transport_router()
    
    # 3. 测试 ADB 连接
    print("\n" + "=" * 60)
    print("  第三部分: ADB 设备连接测试")
    print("=" * 60)
    
    adb_ok, devices = await test_adb_connection()
    results["ADB_Connection"] = adb_ok
    
    # 4. 测试 ADB 截图
    if adb_ok and devices:
        print("\n" + "=" * 60)
        print("  第四部分: ADB 截图测试")
        print("=" * 60)
        
        for device_id in devices[:1]:  # 只测试第一台设备
            results[f"ADB_Screenshot_{device_id}"] = await test_adb_screenshot(device_id)
    
    # 5. 测试量子计算（可选）
    print("\n" + "=" * 60)
    print("  第五部分: 量子计算测试 (可选)")
    print("=" * 60)
    
    results["QuantumDispatcher"] = await test_quantum_dispatcher()
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("  测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n通过: {passed}/{total}\n")
    
    for name, result in results.items():
        status = "✓" if result else "✗"
        color = Colors.GREEN if result else Colors.RED
        print(f"  {color}{status}{Colors.END} {name}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 所有测试通过！系统运行正常。{Colors.END}")
        return 0
    elif passed >= total * 0.7:
        print(f"\n{Colors.YELLOW}⚠️  大部分测试通过，系统基本可用。{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}❌ 多项测试失败，请检查系统配置。{Colors.END}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}测试已中断{Colors.END}")
        sys.exit(1)
