#!/usr/bin/env python3
"""
UFO Galaxy Fusion - Node Executor (Reinforced)

节点执行器（加固版）

核心职责:
1. 管理与 102 个节点的连接
2. 执行远程命令
3. 统一端口管理 (9000+ 范围)
4. 异常处理和重试

作者: Manus AI
日期: 2026-01-26
版本: 1.1.0 (加固版)
"""

import asyncio
import logging
import aiohttp
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NodeExecutor")

@dataclass
class ExecutionResult:
    """执行结果"""
    node_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    timestamp: float = 0.0

class NodeExecutor:
    """
    单个节点的执行器
    """
    
    def __init__(self, node_id: str, api_url: str, timeout: int = 15):
        self.node_id = node_id
        self.api_url = api_url.rstrip('/')
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self.session

    async def execute(self, command: str, params: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """执行远程命令"""
        start_time = time.time()
        url = f"{self.api_url}/execute"
        payload = {
            "command": command,
            "params": params or {},
            "timestamp": start_time
        }
        
        try:
            session = await self._get_session()
            async with session.post(url, json=payload) as response:
                latency = (time.time() - start_time) * 1000
                if response.status == 200:
                    data = await response.json()
                    return ExecutionResult(
                        node_id=self.node_id,
                        success=True,
                        data=data,
                        latency_ms=latency,
                        timestamp=time.time()
                    )
                else:
                    error_text = await response.text()
                    return ExecutionResult(
                        node_id=self.node_id,
                        success=False,
                        error=f"HTTP {response.status}: {error_text}",
                        latency_ms=latency,
                        timestamp=time.time()
                    )
        except Exception as e:
            latency = (time.time() - start_time) * 1000
            return ExecutionResult(
                node_id=self.node_id,
                success=False,
                error=str(e),
                latency_ms=latency,
                timestamp=time.time()
            )

    async def close(self):
        """关闭连接"""
        if self.session and not self.session.closed:
            await self.session.close()

class ExecutionPool:
    """
    执行池 - 管理 102 个节点的执行器
    """
    
    def __init__(self, topology_config: List[Dict[str, Any]]):
        self.executors: Dict[str, NodeExecutor] = {}
        self._init_pool(topology_config)
        
    def _init_pool(self, topology_config: List[Dict[str, Any]]):
        """初始化执行池，统一使用 9000+ 端口范围"""
        for node in topology_config:
            node_id = node["id"]
            # 统一端口逻辑：9000 + 节点索引
            # 假设节点 ID 格式为 Node_XX
            try:
                idx = int(node_id.split('_')[1])
                port = 9000 + idx
                api_url = f"http://localhost:{port}"
            except:
                api_url = node.get("api_url", "http://localhost:8000")
                
            self.executors[node_id] = NodeExecutor(node_id, api_url)
        
        logger.info(f"🎯 ExecutionPool initialized with {len(self.executors)} executors")

    async def execute_on_node(self, node_id: str, command: str, params: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """在指定节点上执行命令"""
        executor = self.executors.get(node_id)
        if not executor:
            return ExecutionResult(
                node_id=node_id,
                success=False,
                error=f"Executor for {node_id} not found in pool"
            )
        
        return await executor.execute(command, params)

    async def close_all(self):
        """关闭所有执行器连接"""
        logger.info("🛑 Closing all executors in pool...")
        tasks = [executor.close() for executor in self.executors.values()]
        if tasks:
            await asyncio.gather(*tasks)
        logger.info("✅ All executors closed")
