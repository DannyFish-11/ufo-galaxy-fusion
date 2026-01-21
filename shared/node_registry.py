"""
UFO³ Galaxy - 节点注册和发现机制
管理所有节点的注册、发现和调用
"""

import httpx
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class NodeCategory(Enum):
    """节点类别"""
    CORE = "core"  # 核心系统
    LLM = "llm"  # LLM 相关
    DATABASE = "database"  # 数据库
    SEARCH = "search"  # 搜索
    COMMUNICATION = "communication"  # 通信
    HARDWARE = "hardware"  # 硬件控制
    INTELLIGENCE = "intelligence"  # 智能推理
    SYSTEM = "system"  # 系统管理
    MEDIA = "media"  # 媒体生成
    TOOLS = "tools"  # 工具类


@dataclass
class NodeInfo:
    """节点信息"""
    node_id: str  # 节点 ID (e.g., "node_01")
    name: str  # 节点名称
    description: str  # 节点描述
    category: NodeCategory  # 节点类别
    url: str  # 节点 URL
    port: int  # 端口
    methods: List[str] = field(default_factory=list)  # 可用方法
    status: str = "unknown"  # 状态: online, offline, unknown
    priority: int = 5  # 优先级 (1-10, 10 最高)


class NodeRegistry:
    """
    节点注册中心
    管理所有节点的注册、发现和调用
    """
    
    def __init__(self):
        self.nodes: Dict[str, NodeInfo] = {}
        self.client = httpx.AsyncClient(timeout=10.0)
        self._register_default_nodes()
    
    def _register_default_nodes(self):
        """注册默认节点"""
        default_nodes = [
            # 核心系统
            NodeInfo(
                node_id="node_00",
                name="State Machine",
                description="状态机和锁管理",
                category=NodeCategory.CORE,
                url="http://localhost:8000",
                port=8000,
                methods=["acquire_lock", "release_lock", "get_state"],
                priority=10
            ),
            NodeInfo(
                node_id="node_01",
                name="One-API",
                description="LLM 统一网关",
                category=NodeCategory.LLM,
                url="http://localhost:8001",
                port=8001,
                methods=["chat_completions", "list_models", "health"],
                priority=10
            ),
            NodeInfo(
                node_id="node_02",
                name="Tasker",
                description="任务调度",
                category=NodeCategory.CORE,
                url="http://localhost:8002",
                port=8002,
                methods=["create_task", "execute_task", "get_status"],
                priority=9
            ),
            
            # LLM 相关
            NodeInfo(
                node_id="node_79",
                name="Local LLM",
                description="本地大模型",
                category=NodeCategory.LLM,
                url="http://localhost:8079",
                port=8079,
                methods=["generate", "chat", "list_models"],
                priority=10
            ),
            NodeInfo(
                node_id="node_80",
                name="Memory System",
                description="记忆系统",
                category=NodeCategory.LLM,
                url="http://localhost:8080",
                port=8080,
                methods=["save_memory", "recall", "get_profile"],
                priority=9
            ),
            NodeInfo(
                node_id="node_81",
                name="Orchestrator",
                description="任务编排器",
                category=NodeCategory.INTELLIGENCE,
                url="http://localhost:8081",
                port=8081,
                methods=["execute_task", "decompose_task", "get_plan"],
                priority=9
            ),
            NodeInfo(
                node_id="node_85",
                name="Prompt Library",
                description="提示词库",
                category=NodeCategory.LLM,
                url="http://localhost:8085",
                port=8085,
                methods=["get_prompt", "save_prompt", "optimize"],
                priority=7
            ),
            
            # 数据库
            NodeInfo(
                node_id="node_12",
                name="Postgres",
                description="PostgreSQL 数据库",
                category=NodeCategory.DATABASE,
                url="http://localhost:8012",
                port=8012,
                methods=["query", "execute", "transaction"],
                priority=8
            ),
            NodeInfo(
                node_id="node_13",
                name="SQLite",
                description="SQLite 数据库",
                category=NodeCategory.DATABASE,
                url="http://localhost:8013",
                port=8013,
                methods=["query", "execute", "backup"],
                priority=7
            ),
            
            # 搜索
            NodeInfo(
                node_id="node_22",
                name="Brave Search",
                description="Brave 搜索",
                category=NodeCategory.SEARCH,
                url="http://localhost:8022",
                port=8022,
                methods=["search", "news_search"],
                priority=8
            ),
            NodeInfo(
                node_id="node_25",
                name="Google Search",
                description="Google 搜索",
                category=NodeCategory.SEARCH,
                url="http://localhost:8025",
                port=8025,
                methods=["search", "image_search"],
                priority=7
            ),
            
            # 通信
            NodeInfo(
                node_id="node_10",
                name="Slack",
                description="Slack 消息",
                category=NodeCategory.COMMUNICATION,
                url="http://localhost:8010",
                port=8010,
                methods=["send_message", "get_messages"],
                priority=6
            ),
            NodeInfo(
                node_id="node_16",
                name="Email",
                description="邮件发送",
                category=NodeCategory.COMMUNICATION,
                url="http://localhost:8016",
                port=8016,
                methods=["send_email", "read_email"],
                priority=7
            ),
            
            # 硬件控制
            NodeInfo(
                node_id="node_33",
                name="ADB",
                description="Android 调试桥",
                category=NodeCategory.HARDWARE,
                url="http://localhost:8033",
                port=8033,
                methods=["execute_command", "install_app", "screenshot"],
                priority=8
            ),
            NodeInfo(
                node_id="node_34",
                name="SSH",
                description="SSH 远程控制",
                category=NodeCategory.HARDWARE,
                url="http://localhost:8034",
                port=8034,
                methods=["execute", "upload", "download"],
                priority=8
            ),
            
            # 媒体生成
            NodeInfo(
                node_id="node_71",
                name="Media Generation",
                description="媒体生成",
                category=NodeCategory.MEDIA,
                url="http://localhost:8071",
                port=8071,
                methods=["generate_image", "generate_video", "generate_audio"],
                priority=7
            ),
            
            # 系统管理
            NodeInfo(
                node_id="node_65",
                name="Logger Central",
                description="日志中心",
                category=NodeCategory.SYSTEM,
                url="http://localhost:8065",
                port=8065,
                methods=["log", "query_logs", "get_stats"],
                priority=9
            ),
            NodeInfo(
                node_id="node_67",
                name="Health Monitor",
                description="健康监控",
                category=NodeCategory.SYSTEM,
                url="http://localhost:8067",
                port=8067,
                methods=["check_health", "get_metrics", "restart_node"],
                priority=9
            ),
            NodeInfo(
                node_id="node_82",
                name="Network Guard",
                description="网络监控",
                category=NodeCategory.SYSTEM,
                url="http://localhost:8082",
                port=8082,
                methods=["check_network", "get_traffic", "check_vpn"],
                priority=7
            ),
            NodeInfo(
                node_id="node_83",
                name="News Aggregator",
                description="新闻聚合",
                category=NodeCategory.TOOLS,
                url="http://localhost:8083",
                port=8083,
                methods=["get_news", "search_news", "subscribe"],
                priority=6
            ),
            NodeInfo(
                node_id="node_84",
                name="Stock Tracker",
                description="股票追踪",
                category=NodeCategory.TOOLS,
                url="http://localhost:8084",
                port=8084,
                methods=["get_quote", "get_chart", "add_watchlist"],
                priority=6
            ),
        ]
        
        for node in default_nodes:
            self.nodes[node.node_id] = node
    
    def register_node(self, node: NodeInfo):
        """
        注册节点
        
        Args:
            node: 节点信息
        """
        self.nodes[node.node_id] = node
    
    def get_node(self, node_id: str) -> Optional[NodeInfo]:
        """
        获取节点信息
        
        Args:
            node_id: 节点 ID
        
        Returns:
            节点信息，如果不存在则返回 None
        """
        return self.nodes.get(node_id)
    
    def list_nodes(
        self,
        category: Optional[NodeCategory] = None,
        status: Optional[str] = None
    ) -> List[NodeInfo]:
        """
        列出节点
        
        Args:
            category: 按类别筛选
            status: 按状态筛选
        
        Returns:
            节点列表
        """
        nodes = list(self.nodes.values())
        
        if category:
            nodes = [n for n in nodes if n.category == category]
        
        if status:
            nodes = [n for n in nodes if n.status == status]
        
        return sorted(nodes, key=lambda n: n.priority, reverse=True)
    
    async def check_node_health(self, node_id: str) -> bool:
        """
        检查节点健康状态
        
        Args:
            node_id: 节点 ID
        
        Returns:
            是否在线
        """
        node = self.get_node(node_id)
        if not node:
            return False
        
        try:
            response = await self.client.get(f"{node.url}/health", timeout=5.0)
            is_healthy = response.status_code == 200
            node.status = "online" if is_healthy else "offline"
            return is_healthy
        except:
            node.status = "offline"
            return False
    
    async def call_node(
        self,
        node_id: str,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        调用节点方法
        
        Args:
            node_id: 节点 ID
            method: 方法名
            params: 参数
        
        Returns:
            调用结果
        """
        node = self.get_node(node_id)
        if not node:
            return {"error": f"Node {node_id} not found"}
        
        if method not in node.methods:
            return {"error": f"Method {method} not available in {node_id}"}
        
        try:
            response = await self.client.post(
                f"{node.url}/{method}",
                json=params or {}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()


# 全局单例
_node_registry: Optional[NodeRegistry] = None


def get_node_registry() -> NodeRegistry:
    """
    获取全局节点注册中心单例
    
    Returns:
        NodeRegistry 实例
    """
    global _node_registry
    if _node_registry is None:
        _node_registry = NodeRegistry()
    return _node_registry
