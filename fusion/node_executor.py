"""
UFO Galaxy Fusion - Node Executor

节点执行层 - 拓扑原生的执行框架

这是融合系统的执行层，负责：
1. 与 102 个节点的实际通信
2. 命令执行和结果收集
3. 健康检查和故障恢复
4. 性能监控和日志记录

作者: Manus AI
日期: 2026-01-25
版本: 1.0.0
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time
import aiohttp

logger = logging.getLogger(__name__)


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
    节点执行器
    
    负责与单个节点的实际通信和命令执行
    """
    
    def __init__(
        self,
        node_id: str,
        node_url: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        初始化节点执行器
        
        Args:
            node_id: 节点 ID
            node_url: 节点 API URL
            timeout: 超时时间（秒）
            max_retries: 最大重试次数
        """
        self.node_id = node_id
        self.node_url = node_url
        self.timeout = timeout
        self.max_retries = max_retries
        
        # HTTP 客户端
        self.session: Optional[aiohttp.ClientSession] = None
        
        # 统计信息
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_latency_ms": 0.0,
            "average_latency_ms": 0.0
        }
    
    async def initialize(self):
        """初始化执行器"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
            logger.debug(f"🔌 NodeExecutor initialized: {self.node_id}")
    
    async def close(self):
        """关闭执行器"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.debug(f"🔌 NodeExecutor closed: {self.node_id}")
    
    async def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            是否健康
        """
        try:
            await self.initialize()
            
            async with self.session.get(f"{self.node_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("status") == "healthy"
                return False
        
        except Exception as e:
            logger.debug(f"⚠️  Health check failed for {self.node_id}: {e}")
            return False
    
    async def execute_command(
        self,
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> ExecutionResult:
        """
        执行命令
        
        Args:
            command: 命令名称
            params: 命令参数
        
        Returns:
            执行结果
        """
        start_time = time.time()
        
        try:
            await self.initialize()
            
            # 准备请求
            payload = {
                "command": command,
                "params": params or {}
            }
            
            # 发送请求（带重试）
            for attempt in range(self.max_retries):
                try:
                    async with self.session.post(
                        f"{self.node_url}/execute",
                        json=payload
                    ) as response:
                        latency_ms = (time.time() - start_time) * 1000
                        
                        if response.status == 200:
                            data = await response.json()
                            
                            # 更新统计
                            self._update_stats(latency_ms, success=True)
                            
                            return ExecutionResult(
                                node_id=self.node_id,
                                success=True,
                                data=data,
                                latency_ms=latency_ms,
                                timestamp=time.time()
                            )
                        else:
                            error_text = await response.text()
                            logger.warning(
                                f"⚠️  Command failed on {self.node_id}: "
                                f"status={response.status}, error={error_text}"
                            )
                            
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(0.5 * (attempt + 1))
                                continue
                            
                            # 最后一次重试失败
                            self._update_stats(latency_ms, success=False)
                            
                            return ExecutionResult(
                                node_id=self.node_id,
                                success=False,
                                error=f"HTTP {response.status}: {error_text}",
                                latency_ms=latency_ms,
                                timestamp=time.time()
                            )
                
                except asyncio.TimeoutError:
                    logger.warning(
                        f"⚠️  Command timeout on {self.node_id} "
                        f"(attempt {attempt + 1}/{self.max_retries})"
                    )
                    
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(1.0 * (attempt + 1))
                        continue
                    
                    # 超时
                    latency_ms = (time.time() - start_time) * 1000
                    self._update_stats(latency_ms, success=False)
                    
                    return ExecutionResult(
                        node_id=self.node_id,
                        success=False,
                        error="Timeout",
                        latency_ms=latency_ms,
                        timestamp=time.time()
                    )
        
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self._update_stats(latency_ms, success=False)
            
            logger.error(f"❌ Command execution failed on {self.node_id}: {e}")
            
            return ExecutionResult(
                node_id=self.node_id,
                success=False,
                error=str(e),
                latency_ms=latency_ms,
                timestamp=time.time()
            )
    
    def _update_stats(self, latency_ms: float, success: bool):
        """更新统计信息"""
        self.stats["total_requests"] += 1
        self.stats["total_latency_ms"] += latency_ms
        
        if success:
            self.stats["successful_requests"] += 1
        else:
            self.stats["failed_requests"] += 1
        
        if self.stats["total_requests"] > 0:
            self.stats["average_latency_ms"] = (
                self.stats["total_latency_ms"] / self.stats["total_requests"]
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_requests"] / self.stats["total_requests"]
                if self.stats["total_requests"] > 0 else 0.0
            )
        }


class ExecutionPool:
    """
    执行池
    
    管理所有节点的执行器，提供统一的执行接口
    """
    
    def __init__(self, topology_config: Dict[str, Any]):
        """
        初始化执行池
        
        Args:
            topology_config: 拓扑配置
        """
        self.topology_config = topology_config
        self.executors: Dict[str, NodeExecutor] = {}
        
        # 从拓扑配置创建执行器
        for node in topology_config.get("nodes", []):
            node_id = node["id"]
            node_url = node.get("api_url", f"http://localhost:{8000 + int(node_id.split('_')[1])}")
            
            self.executors[node_id] = NodeExecutor(
                node_id=node_id,
                node_url=node_url
            )
        
        logger.info(f"🎯 ExecutionPool initialized with {len(self.executors)} executors")
    
    async def initialize_all(self):
        """初始化所有执行器"""
        tasks = [executor.initialize() for executor in self.executors.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("✅ All executors initialized")
    
    async def close_all(self):
        """关闭所有执行器"""
        tasks = [executor.close() for executor in self.executors.values()]
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("✅ All executors closed")
    
    async def health_check_all(self) -> Dict[str, bool]:
        """
        对所有节点进行健康检查
        
        Returns:
            节点 ID -> 健康状态
        """
        tasks = {
            node_id: executor.health_check()
            for node_id, executor in self.executors.items()
        }
        
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        health_status = {}
        for node_id, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                health_status[node_id] = False
            else:
                health_status[node_id] = result
        
        healthy_count = sum(1 for status in health_status.values() if status)
        logger.info(
            f"📊 Health check: {healthy_count}/{len(health_status)} nodes healthy"
        )
        
        return health_status
    
    async def execute_on_node(
        self,
        node_id: str,
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> ExecutionResult:
        """
        在指定节点上执行命令
        
        Args:
            node_id: 节点 ID
            command: 命令名称
            params: 命令参数
        
        Returns:
            执行结果
        """
        if node_id not in self.executors:
            return ExecutionResult(
                node_id=node_id,
                success=False,
                error=f"Node not found: {node_id}",
                timestamp=time.time()
            )
        
        executor = self.executors[node_id]
        return await executor.execute_command(command, params)
    
    async def execute_on_nodes(
        self,
        node_ids: List[str],
        command: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[ExecutionResult]:
        """
        在多个节点上执行命令（并行）
        
        Args:
            node_ids: 节点 ID 列表
            command: 命令名称
            params: 命令参数
        
        Returns:
            执行结果列表
        """
        tasks = [
            self.execute_on_node(node_id, command, params)
            for node_id in node_ids
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常
        final_results = []
        for node_id, result in zip(node_ids, results):
            if isinstance(result, Exception):
                final_results.append(ExecutionResult(
                    node_id=node_id,
                    success=False,
                    error=str(result),
                    timestamp=time.time()
                ))
            else:
                final_results.append(result)
        
        return final_results
    
    def get_executor(self, node_id: str) -> Optional[NodeExecutor]:
        """获取节点执行器"""
        return self.executors.get(node_id)
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """获取所有执行器的统计信息"""
        return {
            node_id: executor.get_stats()
            for node_id, executor in self.executors.items()
        }
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """获取汇总统计信息"""
        all_stats = self.get_all_stats()
        
        total_requests = sum(s["total_requests"] for s in all_stats.values())
        successful_requests = sum(s["successful_requests"] for s in all_stats.values())
        failed_requests = sum(s["failed_requests"] for s in all_stats.values())
        total_latency = sum(s["total_latency_ms"] for s in all_stats.values())
        
        return {
            "total_nodes": len(self.executors),
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (
                successful_requests / total_requests if total_requests > 0 else 0.0
            ),
            "average_latency_ms": (
                total_latency / total_requests if total_requests > 0 else 0.0
            )
        }
