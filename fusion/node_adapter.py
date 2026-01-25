"""
UFO Galaxy Fusion - Node Adapter Base Class

节点适配器基类

将你的 FastAPI 节点适配为微软 UFO 的 Device Agent，
实现 AIP 协议接口，使节点能够：
1. 注册到微软 Galaxy
2. 接收任务请求
3. 执行命令
4. 返回结果

作者: Manus AI
日期: 2026-01-25
"""

import asyncio
import logging
import sys
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path

# 添加微软 UFO 到 Python 路径
MICROSOFT_UFO_PATH = Path(__file__).parent.parent / "microsoft-ufo"
if str(MICROSOFT_UFO_PATH) not in sys.path:
    sys.path.insert(0, str(MICROSOFT_UFO_PATH))

try:
    from aip.endpoints.client_endpoint import DeviceClientEndpoint
    from aip.messages import (
        ClientMessage, ServerMessage, Command, Result,
        ResultStatus, TaskStatus, ClientMessageType, ClientType
    )
    AIP_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️  Microsoft UFO AIP not available: {e}")
    AIP_AVAILABLE = False
    # 创建模拟类
    class DeviceClientEndpoint:
        def __init__(self, device_id, server_url): pass
        async def connect(self): pass
        async def disconnect(self): pass
    class Command: pass
    class Result: pass
    class ResultStatus:
        SUCCESS = "success"
        FAILURE = "failure"

logger = logging.getLogger(__name__)


class UFONodeAdapter(DeviceClientEndpoint if AIP_AVAILABLE else object, ABC):
    """
    UFO 节点适配器基类
    
    将你的 FastAPI 节点适配为微软 UFO 的 Device Agent
    
    子类需要实现:
    - execute_command(): 执行具体命令
    - get_capabilities(): 返回节点能力
    - get_tools(): 返回节点提供的工具列表
    
    使用示例:
    ```python
    class Node00Adapter(UFONodeAdapter):
        def __init__(self, server_url):
            super().__init__(
                node_id="Node_00",
                node_name="StateMachine",
                layer="core",
                domain="state_management",
                server_url=server_url,
                node_api_url="http://localhost:8000"
            )
        
        async def execute_command(self, command):
            # 实现具体的命令执行逻辑
            ...
    ```
    """
    
    def __init__(
        self,
        node_id: str,
        node_name: str,
        layer: str,
        domain: str,
        server_url: str,
        node_api_url: str,
        capabilities: Optional[List[str]] = None
    ):
        """
        初始化节点适配器
        
        Args:
            node_id: 节点 ID (如 "Node_00")
            node_name: 节点名称 (如 "StateMachine")
            layer: 层级 ("core", "cognitive", "perception")
            domain: 域 ("state_management", "vision", etc.)
            server_url: 微软 Galaxy 服务器 URL
            node_api_url: 节点的 FastAPI URL
            capabilities: 能力列表（可选，默认从 get_capabilities() 获取）
        """
        # 初始化 DeviceClientEndpoint (如果可用)
        if AIP_AVAILABLE:
            super().__init__(
                device_id=node_id,
                server_url=server_url
            )
        
        self.node_id = node_id
        self.node_name = node_name
        self.layer = layer
        self.domain = domain
        self.server_url = server_url
        self.node_api_url = node_api_url
        self._capabilities = capabilities or self.get_capabilities()
        
        # HTTP 客户端 (用于调用节点的 FastAPI)
        self.http_session: Optional[Any] = None
        
        # 状态跟踪
        self.is_connected = False
        self.current_task: Optional[str] = None
        
        logger.info(
            f"🔌 Node adapter initialized: {self.node_id} ({self.node_name}) "
            f"[{self.layer}/{self.domain}]"
        )
    
    async def start(self):
        """启动适配器"""
        try:
            # 创建 HTTP 客户端
            import aiohttp
            self.http_session = aiohttp.ClientSession()
            
            # 测试节点连接
            await self.health_check()
            
            # 注册到微软 Galaxy (如果 AIP 可用)
            if AIP_AVAILABLE:
                await self.connect()
                self.is_connected = True
                logger.info(f"✅ Node adapter started and connected: {self.node_id}")
            else:
                logger.warning(f"⚠️  AIP not available, running in standalone mode: {self.node_id}")
        
        except Exception as e:
            logger.error(f"❌ Failed to start node adapter {self.node_id}: {e}")
            raise
    
    async def stop(self):
        """停止适配器"""
        try:
            # 关闭 HTTP 客户端
            if self.http_session:
                await self.http_session.close()
            
            # 断开连接 (如果 AIP 可用)
            if AIP_AVAILABLE and self.is_connected:
                await self.disconnect()
                self.is_connected = False
            
            logger.info(f"🛑 Node adapter stopped: {self.node_id}")
        
        except Exception as e:
            logger.error(f"❌ Failed to stop node adapter {self.node_id}: {e}")
    
    async def health_check(self) -> bool:
        """
        健康检查 - 测试节点是否可访问
        
        Returns:
            True 如果节点健康，否则 False
        """
        try:
            url = f"{self.node_api_url}/health"
            async with self.http_session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    logger.debug(f"✅ Node {self.node_id} health check passed")
                    return True
                else:
                    logger.warning(f"⚠️  Node {self.node_id} health check failed: {resp.status}")
                    return False
        except Exception as e:
            logger.warning(f"⚠️  Node {self.node_id} health check failed: {e}")
            return False
    
    async def on_task_received(self, message: 'ServerMessage'):
        """
        接收任务 (来自微软 Galaxy)
        
        这是 DeviceClientEndpoint 的回调方法
        
        Args:
            message: 服务器消息
        """
        if not AIP_AVAILABLE:
            logger.warning("⚠️  AIP not available, cannot process task")
            return
        
        logger.info(
            f"📥 Task received by {self.node_id}: {message.user_request}"
        )
        
        self.current_task = message.task_name
        
        try:
            # 执行任务
            result = await self.execute_task(message)
            
            # 发送结果
            await self.send_task_result(result)
            
            logger.info(f"✅ Task completed by {self.node_id}: {message.task_name}")
        
        except Exception as e:
            logger.error(f"❌ Task execution failed in {self.node_id}: {e}")
            await self.send_error(str(e))
        
        finally:
            self.current_task = None
    
    async def execute_task(self, message: 'ServerMessage') -> Dict[str, Any]:
        """
        执行任务
        
        将微软的任务转换为节点 API 调用
        
        Args:
            message: 服务器消息
        
        Returns:
            任务执行结果
        """
        # 提取命令列表
        commands = message.actions or []
        
        if not commands:
            logger.warning(f"⚠️  No commands in task for {self.node_id}")
            return {
                "status": "completed",
                "results": []
            }
        
        # 执行每个命令
        results = []
        for cmd in commands:
            try:
                result = await self.execute_command(cmd)
                results.append(result)
            except Exception as e:
                logger.error(f"❌ Command execution failed: {e}")
                results.append({
                    "status": ResultStatus.FAILURE if AIP_AVAILABLE else "failure",
                    "error": str(e)
                })
        
        return {
            "status": "completed",
            "results": results
        }
    
    @abstractmethod
    async def execute_command(self, command: 'Command') -> 'Result':
        """
        执行单个命令
        
        子类必须实现此方法
        
        Args:
            command: 命令对象
        
        Returns:
            命令执行结果
        """
        pass
    
    async def call_node_api(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        调用节点的 FastAPI
        
        Args:
            endpoint: API 端点 (如 "/execute")
            method: HTTP 方法 (GET, POST, PUT, DELETE)
            data: 请求数据 (JSON body)
            params: URL 参数
        
        Returns:
            API 响应 (JSON)
        """
        url = f"{self.node_api_url}{endpoint}"
        
        try:
            if method == "POST":
                async with self.http_session.post(url, json=data, params=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            
            elif method == "GET":
                async with self.http_session.get(url, params=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            
            elif method == "PUT":
                async with self.http_session.put(url, json=data, params=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            
            elif method == "DELETE":
                async with self.http_session.delete(url, params=params) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        
        except Exception as e:
            logger.error(f"❌ Node API call failed ({method} {url}): {e}")
            raise
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        返回节点能力列表
        
        子类必须实现此方法
        
        Returns:
            能力列表，如 ["state_management", "lock_management"]
        """
        pass
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """
        返回节点提供的工具列表
        
        子类可以重写此方法以提供更详细的工具信息
        
        Returns:
            工具列表，每个工具包含 name, description, parameters 等
        """
        return []
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        返回节点元数据
        
        Returns:
            元数据字典
        """
        return {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "layer": self.layer,
            "domain": self.domain,
            "capabilities": self._capabilities,
            "api_url": self.node_api_url,
            "is_connected": self.is_connected,
            "current_task": self.current_task
        }
    
    def __repr__(self) -> str:
        return (
            f"<UFONodeAdapter {self.node_id} "
            f"layer={self.layer} domain={self.domain} "
            f"connected={self.is_connected}>"
        )


class SimpleNodeAdapter(UFONodeAdapter):
    """
    简单节点适配器
    
    用于快速创建适配器，无需子类化
    
    使用示例:
    ```python
    async def my_command_handler(command):
        # 处理命令
        return {"status": "success", "result": "..."}
    
    adapter = SimpleNodeAdapter(
        node_id="Node_00",
        node_name="StateMachine",
        layer="core",
        domain="state_management",
        server_url="ws://localhost:5000",
        node_api_url="http://localhost:8000",
        capabilities=["state_management"],
        command_handler=my_command_handler
    )
    ```
    """
    
    def __init__(
        self,
        node_id: str,
        node_name: str,
        layer: str,
        domain: str,
        server_url: str,
        node_api_url: str,
        capabilities: List[str],
        command_handler=None
    ):
        """
        初始化简单节点适配器
        
        Args:
            command_handler: 命令处理函数 async def handler(command) -> result
        """
        super().__init__(
            node_id=node_id,
            node_name=node_name,
            layer=layer,
            domain=domain,
            server_url=server_url,
            node_api_url=node_api_url,
            capabilities=capabilities
        )
        
        self.command_handler = command_handler
    
    async def execute_command(self, command: 'Command') -> 'Result':
        """执行命令"""
        if self.command_handler:
            try:
                result = await self.command_handler(command)
                
                if AIP_AVAILABLE:
                    return Result(
                        status=ResultStatus.SUCCESS,
                        result=result,
                        namespace=self.domain,
                        call_id=command.call_id if hasattr(command, 'call_id') else None
                    )
                else:
                    return result
            
            except Exception as e:
                if AIP_AVAILABLE:
                    return Result(
                        status=ResultStatus.FAILURE,
                        error=str(e),
                        namespace=self.domain,
                        call_id=command.call_id if hasattr(command, 'call_id') else None
                    )
                else:
                    return {"status": "failure", "error": str(e)}
        else:
            logger.warning(f"⚠️  No command handler for {self.node_id}")
            if AIP_AVAILABLE:
                return Result(
                    status=ResultStatus.FAILURE,
                    error="No command handler",
                    namespace=self.domain
                )
            else:
                return {"status": "failure", "error": "No command handler"}
    
    def get_capabilities(self) -> List[str]:
        """返回能力"""
        return self._capabilities
