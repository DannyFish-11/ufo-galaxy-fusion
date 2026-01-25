# 🚀 方案 A：深度融合架构 - 完整实施方案

**日期**: 2026-01-25  
**环境**: fusion-experiment (安全实验环境)  
**目标**: 代码级深度集成，实现真正的融合性增强

---

## 📋 目录

1. [架构概览](#架构概览)
2. [核心设计原则](#核心设计原则)
3. [系统架构对比](#系统架构对比)
4. [融合架构设计](#融合架构设计)
5. [详细实施步骤](#详细实施步骤)
6. [代码实现](#代码实现)
7. [配置和部署](#配置和部署)
8. [测试验证](#测试验证)
9. [时间规划](#时间规划)

---

## 🎯 架构概览

### 融合后的系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        GalaxyClient                              │
│                    (微软的，轻度扩展)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│              TopologyAwareConstellationClient                    │
│                  (新增，拓扑感知的客户端)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  ConstellationClient (微软的基础功能)                    │  │
│  │  + TopologyManager (拓扑管理)                            │  │
│  │  + TopologyRouter (拓扑路由)                             │  │
│  │  + LoadBalancer (负载均衡)                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │  AIP Protocol   │
                    │   (统一扩展)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────┴────────┐  ┌────────┴────────┐  ┌───────┴────────┐
│ Core Layer     │  │ Cognitive Layer │  │ Perception     │
│ (16 nodes)     │  │ (46 nodes)      │  │ Layer          │
│                │  │                 │  │ (31 nodes)     │
│ Node_00        │  │ Node_16         │  │ Node_62        │
│ Node_04        │  │ Node_20         │  │ Node_70        │
│ ...            │  │ ...             │  │ ...            │
└────────────────┘  └─────────────────┘  └────────────────┘
```

---

## 💡 核心设计原则

### 1. 最小侵入性

**原则**: 尽量少修改微软 UFO 的核心代码

**实施**:
- ✅ 通过**继承**扩展 ConstellationClient
- ✅ 通过**组合**添加拓扑管理功能
- ✅ 通过**配置**启用/禁用拓扑功能
- ❌ 不直接修改微软的核心类

### 2. 协议统一

**原则**: 统一微软 AIP 和你的 AIP v2.0

**实施**:
- 扩展微软 AIP 消息，添加拓扑字段
- 保持向后兼容
- 支持协议版本协商

### 3. 拓扑原生化

**原则**: 让微软 Galaxy 原生理解三层球体拓扑

**实施**:
- 拓扑信息作为设备元数据
- 路由算法基于拓扑
- 负载均衡考虑拓扑结构

### 4. 渐进式融合

**原则**: 分阶段实施，每个阶段都可独立运行

**实施**:
- 阶段 1: 基础适配（1-2 周）
- 阶段 2: 拓扑集成（2-3 周）
- 阶段 3: 深度优化（3-4 周）

---

## 📊 系统架构对比

### 微软 UFO³ Galaxy

```python
# 架构特点
- 轻量级 Device Agent
- 动态 DAG 编排 (TaskConstellation)
- WebSocket + JSON-RPC
- 设备注册 + 心跳机制
- 跨设备任务分发

# 核心组件
GalaxyClient
  └─ ConstellationClient
      ├─ DeviceManager
      │   ├─ DeviceRegistry
      │   ├─ ConnectionManager
      │   └─ HeartbeatManager
      └─ TaskQueueManager
```

### 你的 ufo-galaxy-unified

```python
# 架构特点
- 重量级功能节点 (103 个)
- 三层球体拓扑 (Core, Cognitive, Perception)
- AIP v2.0 多媒体协议
- FastAPI + Redis
- 域驱动设计 (vision, nlu, state_management, etc.)

# 核心组件
System Manager
  └─ Galaxy Gateway
      ├─ Task Router (基于域)
      ├─ Device Router (基于拓扑)
      ├─ NLU Engine
      └─ Cross-Device Coordinator
```

### 关键差异

| 维度 | 微软 UFO³ | 你的系统 | 融合策略 |
|------|-----------|----------|----------|
| **节点模型** | 轻量级 Agent | 重量级 Node | 节点实现 AIP 接口 |
| **拓扑** | 平面结构 | 三层球体 | 扩展 AIP 支持拓扑 |
| **协议** | WebSocket + JSON-RPC | AIP v2.0 多媒体 | 统一为扩展 AIP |
| **路由** | 基于能力 | 基于域+拓扑 | 拓扑感知路由 |
| **编排** | 动态 DAG | 静态拓扑 | 混合模式 |

---

## 🏗️ 融合架构设计

### 1. 扩展 AIP 协议

#### 1.1 拓扑元数据

```python
# 在 microsoft-ufo/aip/messages.py 中添加

from typing import Tuple, List
from pydantic import BaseModel

@dataclass
class TopologyInfo(BaseModel):
    """拓扑信息 - 三层球体拓扑"""
    
    # 层级 (Layer)
    layer: str  # "core", "cognitive", "perception"
    layer_index: int  # 0, 1, 2
    
    # 域 (Domain)
    domain: str  # "vision", "nlu", "state_management", etc.
    
    # 球面坐标 (Spherical Coordinates)
    # 用于可视化和路径优化
    theta: float  # 极角 [0, π]
    phi: float    # 方位角 [0, 2π]
    radius: float  # 半径 (层级决定)
    
    # 拓扑关系
    neighbors: List[str]  # 邻居节点 ID
    parent_nodes: List[str]  # 父节点 (上层)
    child_nodes: List[str]   # 子节点 (下层)
    
    # 路由权重
    routing_weight: float = 1.0  # 路由权重
    load_capacity: int = 100     # 负载容量

@dataclass
class DeviceMetadataExtended(BaseModel):
    """扩展的设备元数据"""
    
    # 原有字段 (兼容微软)
    os: Optional[str] = None
    capabilities: List[str] = []
    
    # 新增拓扑字段
    topology: Optional[TopologyInfo] = None
    
    # 性能指标
    cpu_cores: int = 1
    memory_mb: int = 1024
    current_load: float = 0.0

# 扩展 ClientMessage
class ClientMessage(BaseModel):
    # ... 原有字段 ...
    
    # 新增字段
    topology_metadata: Optional[TopologyInfo] = None
```

#### 1.2 拓扑路由消息

```python
@dataclass
class TopologyRoutingHint(BaseModel):
    """拓扑路由提示"""
    
    # 首选层级
    preferred_layer: Optional[str] = None
    
    # 首选域
    preferred_domain: Optional[str] = None
    
    # 源节点 (用于路径优化)
    source_node_id: Optional[str] = None
    
    # 路由策略
    routing_strategy: str = "shortest_path"  # "shortest_path", "load_balanced", "domain_affinity"
    
    # 约束条件
    exclude_nodes: List[str] = []
    required_capabilities: List[str] = []

# 扩展 ServerMessage
class ServerMessage(BaseModel):
    # ... 原有字段 ...
    
    # 新增字段
    routing_hint: Optional[TopologyRoutingHint] = None
    selected_node_path: Optional[List[str]] = None  # 选择的节点路径
```

---

### 2. 拓扑管理器 (TopologyManager)

#### 2.1 核心职责

```python
"""
TopologyManager - 拓扑管理器

职责:
1. 加载和管理三层球体拓扑
2. 提供拓扑查询接口
3. 计算最优路由路径
4. 负载均衡
5. 拓扑可视化
"""
```

#### 2.2 实现

```python
# 创建 fusion-experiment/ufo-galaxy-unified/fusion/topology_manager.py

import json
import logging
import networkx as nx
from typing import Dict, List, Optional, Tuple, Set
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class NodeInfo:
    """节点信息"""
    node_id: str
    node_name: str
    layer: str
    domain: str
    coordinates: Tuple[float, float, float]  # (theta, phi, radius)
    capabilities: List[str]
    neighbors: List[str]
    metadata: Dict


class TopologyManager:
    """
    三层球体拓扑管理器
    
    功能:
    - 加载拓扑配置
    - 构建拓扑图 (NetworkX)
    - 路由算法 (最短路径、负载均衡、域亲和)
    - 负载监控
    """
    
    def __init__(self, topology_config_path: str):
        self.config_path = Path(topology_config_path)
        self.graph = nx.DiGraph()  # 有向图
        self.nodes: Dict[str, NodeInfo] = {}
        self.layers: Dict[str, List[str]] = {
            "core": [],
            "cognitive": [],
            "perception": []
        }
        self.domains: Dict[str, List[str]] = {}
        self.load_tracker: Dict[str, float] = {}  # 节点负载
        
        self._load_topology()
    
    def _load_topology(self):
        """加载拓扑配置"""
        logger.info(f"📊 Loading topology from {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 加载节点
        for node_data in config['nodes']:
            node = NodeInfo(
                node_id=node_data['id'],
                node_name=node_data['name'],
                layer=node_data['layer'],
                domain=node_data['domain'],
                coordinates=(
                    node_data['coordinates']['theta'],
                    node_data['coordinates']['phi'],
                    node_data['coordinates']['radius']
                ),
                capabilities=node_data.get('capabilities', []),
                neighbors=node_data.get('neighbors', []),
                metadata=node_data.get('metadata', {})
            )
            
            self.nodes[node.node_id] = node
            self.layers[node.layer].append(node.node_id)
            
            if node.domain not in self.domains:
                self.domains[node.domain] = []
            self.domains[node.domain].append(node.node_id)
            
            # 添加到图
            self.graph.add_node(
                node.node_id,
                layer=node.layer,
                domain=node.domain,
                coordinates=node.coordinates
            )
            
            # 初始化负载
            self.load_tracker[node.node_id] = 0.0
        
        # 添加边 (基于邻居关系)
        for node_id, node in self.nodes.items():
            for neighbor_id in node.neighbors:
                if neighbor_id in self.nodes:
                    self.graph.add_edge(node_id, neighbor_id, weight=1.0)
        
        logger.info(f"✅ Topology loaded: {len(self.nodes)} nodes, {len(self.graph.edges)} edges")
        logger.info(f"   Layers: {[(k, len(v)) for k, v in self.layers.items()]}")
        logger.info(f"   Domains: {[(k, len(v)) for k, v in self.domains.items()]}")
    
    def find_best_node(
        self,
        domain: Optional[str] = None,
        layer: Optional[str] = None,
        capabilities: Optional[List[str]] = None,
        source_node: Optional[str] = None,
        strategy: str = "load_balanced"
    ) -> Optional[str]:
        """
        查找最佳节点
        
        Args:
            domain: 目标域
            layer: 目标层级
            capabilities: 所需能力
            source_node: 源节点 (用于路径优化)
            strategy: 路由策略
                - "load_balanced": 负载均衡
                - "shortest_path": 最短路径
                - "domain_affinity": 域亲和
        
        Returns:
            最佳节点 ID
        """
        # 1. 筛选候选节点
        candidates = self._filter_candidates(domain, layer, capabilities)
        
        if not candidates:
            logger.warning(f"⚠️  No candidates found for domain={domain}, layer={layer}")
            return None
        
        # 2. 根据策略选择
        if strategy == "load_balanced":
            return self._select_by_load(candidates)
        elif strategy == "shortest_path" and source_node:
            return self._select_by_path(candidates, source_node)
        elif strategy == "domain_affinity":
            return self._select_by_domain(candidates, domain)
        else:
            # 默认: 负载均衡
            return self._select_by_load(candidates)
    
    def _filter_candidates(
        self,
        domain: Optional[str],
        layer: Optional[str],
        capabilities: Optional[List[str]]
    ) -> List[str]:
        """筛选候选节点"""
        candidates = list(self.nodes.keys())
        
        # 按域筛选
        if domain and domain in self.domains:
            candidates = [n for n in candidates if n in self.domains[domain]]
        
        # 按层级筛选
        if layer and layer in self.layers:
            candidates = [n for n in candidates if n in self.layers[layer]]
        
        # 按能力筛选
        if capabilities:
            candidates = [
                n for n in candidates
                if all(cap in self.nodes[n].capabilities for cap in capabilities)
            ]
        
        return candidates
    
    def _select_by_load(self, candidates: List[str]) -> str:
        """按负载选择"""
        return min(candidates, key=lambda n: self.load_tracker.get(n, 0.0))
    
    def _select_by_path(self, candidates: List[str], source_node: str) -> str:
        """按路径长度选择"""
        if source_node not in self.graph:
            return self._select_by_load(candidates)
        
        # 计算到每个候选节点的最短路径
        paths = {}
        for candidate in candidates:
            try:
                path_length = nx.shortest_path_length(
                    self.graph, source_node, candidate
                )
                paths[candidate] = path_length
            except nx.NetworkXNoPath:
                paths[candidate] = float('inf')
        
        # 选择最短路径
        return min(paths, key=paths.get)
    
    def _select_by_domain(self, candidates: List[str], domain: Optional[str]) -> str:
        """按域亲和选择"""
        if domain:
            # 优先选择同域节点
            same_domain = [n for n in candidates if self.nodes[n].domain == domain]
            if same_domain:
                return self._select_by_load(same_domain)
        
        return self._select_by_load(candidates)
    
    def get_node_info(self, node_id: str) -> Optional[NodeInfo]:
        """获取节点信息"""
        return self.nodes.get(node_id)
    
    def get_layer_nodes(self, layer: str) -> List[str]:
        """获取指定层级的所有节点"""
        return self.layers.get(layer, [])
    
    def get_domain_nodes(self, domain: str) -> List[str]:
        """获取指定域的所有节点"""
        return self.domains.get(domain, [])
    
    def update_load(self, node_id: str, load: float):
        """更新节点负载"""
        if node_id in self.load_tracker:
            self.load_tracker[node_id] = load
    
    def get_topology_stats(self) -> Dict:
        """获取拓扑统计信息"""
        return {
            "total_nodes": len(self.nodes),
            "layers": {k: len(v) for k, v in self.layers.items()},
            "domains": {k: len(v) for k, v in self.domains.items()},
            "total_edges": len(self.graph.edges),
            "average_load": sum(self.load_tracker.values()) / len(self.load_tracker) if self.load_tracker else 0.0
        }
```

---

### 3. 拓扑感知的 ConstellationClient

#### 3.1 继承扩展

```python
# 创建 fusion-experiment/ufo-galaxy-unified/fusion/topology_aware_client.py

import logging
from typing import Dict, List, Optional, Any

from microsoft-ufo.galaxy.client.constellation_client import ConstellationClient
from microsoft-ufo.galaxy.client.config_loader import ConstellationConfig
from microsoft-ufo.aip.messages import ClientMessage, ServerMessage

from .topology_manager import TopologyManager

logger = logging.getLogger(__name__)


class TopologyAwareConstellationClient(ConstellationClient):
    """
    拓扑感知的 ConstellationClient
    
    扩展微软的 ConstellationClient，添加:
    1. 拓扑管理
    2. 拓扑路由
    3. 负载均衡
    """
    
    def __init__(
        self,
        config: Optional[ConstellationConfig] = None,
        task_name: Optional[str] = None,
        topology_config_path: Optional[str] = None,
        enable_topology: bool = True
    ):
        """
        初始化拓扑感知客户端
        
        Args:
            config: Constellation 配置
            task_name: 任务名称
            topology_config_path: 拓扑配置文件路径
            enable_topology: 是否启用拓扑功能
        """
        # 调用父类初始化
        super().__init__(config, task_name)
        
        self.enable_topology = enable_topology
        self.topology_manager: Optional[TopologyManager] = None
        
        # 如果启用拓扑，加载拓扑管理器
        if enable_topology and topology_config_path:
            logger.info("🌐 Initializing TopologyManager...")
            self.topology_manager = TopologyManager(topology_config_path)
            logger.info("✅ TopologyManager initialized")
    
    async def assign_task_with_topology(
        self,
        task: Dict[str, Any],
        domain: Optional[str] = None,
        layer: Optional[str] = None,
        source_node: Optional[str] = None,
        strategy: str = "load_balanced"
    ) -> Optional[str]:
        """
        基于拓扑分配任务
        
        Args:
            task: 任务描述
            domain: 目标域
            layer: 目标层级
            source_node: 源节点
            strategy: 路由策略
        
        Returns:
            目标节点 ID
        """
        if not self.enable_topology or not self.topology_manager:
            # 回退到标准分配
            logger.warning("⚠️  Topology not enabled, using standard assignment")
            return await self._standard_assign(task)
        
        # 1. 从任务中提取域和层级 (如果未指定)
        if not domain:
            domain = task.get('domain') or self._infer_domain(task)
        
        if not layer:
            layer = task.get('layer') or self._infer_layer(task)
        
        # 2. 使用拓扑管理器查找最佳节点
        target_node = self.topology_manager.find_best_node(
            domain=domain,
            layer=layer,
            capabilities=task.get('required_capabilities', []),
            source_node=source_node,
            strategy=strategy
        )
        
        if not target_node:
            logger.error(f"❌ No suitable node found for task: {task}")
            return None
        
        logger.info(f"✅ Task assigned to node: {target_node} (domain={domain}, layer={layer})")
        
        # 3. 分配任务到目标节点
        return await self._send_task_to_node(target_node, task)
    
    def _infer_domain(self, task: Dict[str, Any]) -> str:
        """从任务描述推断域"""
        description = task.get('description', '').lower()
        
        # 简单的关键词匹配
        if any(kw in description for kw in ['image', 'vision', 'visual', 'see']):
            return 'vision'
        elif any(kw in description for kw in ['text', 'language', 'understand', 'nlu']):
            return 'nlu'
        elif any(kw in description for kw in ['state', 'manage', 'track']):
            return 'state_management'
        else:
            return 'general'
    
    def _infer_layer(self, task: Dict[str, Any]) -> str:
        """从任务描述推断层级"""
        description = task.get('description', '').lower()
        
        # 简单的层级推断
        if any(kw in description for kw in ['perceive', 'detect', 'capture']):
            return 'perception'
        elif any(kw in description for kw in ['analyze', 'understand', 'process']):
            return 'cognitive'
        elif any(kw in description for kw in ['coordinate', 'manage', 'control']):
            return 'core'
        else:
            return 'perception'  # 默认从感知层开始
    
    async def _standard_assign(self, task: Dict[str, Any]) -> Optional[str]:
        """标准任务分配 (回退方案)"""
        # 使用父类的设备管理器
        devices = self.device_manager.device_registry.get_all_devices()
        
        if not devices:
            logger.error("❌ No devices available")
            return None
        
        # 简单选择第一个可用设备
        for device_id, device in devices.items():
            if device.status == "IDLE":
                return device_id
        
        # 如果没有空闲设备，选择第一个
        return list(devices.keys())[0] if devices else None
    
    async def _send_task_to_node(self, node_id: str, task: Dict[str, Any]) -> str:
        """发送任务到指定节点"""
        # 这里需要调用父类的设备管理器
        # 实际实现需要根据微软 UFO 的 API
        
        logger.info(f"📤 Sending task to node {node_id}: {task.get('description', 'N/A')}")
        
        # TODO: 实现实际的任务发送逻辑
        # 这里需要使用 device_manager 发送任务
        
        return node_id
    
    def get_topology_stats(self) -> Optional[Dict]:
        """获取拓扑统计信息"""
        if self.topology_manager:
            return self.topology_manager.get_topology_stats()
        return None
```

---

### 4. 扩展 GalaxyClient

#### 4.1 集成拓扑功能

```python
# 修改 microsoft-ufo/galaxy/galaxy_client.py

# 在文件顶部添加导入
try:
    from fusion.topology_aware_client import TopologyAwareConstellationClient
    TOPOLOGY_AVAILABLE = True
except ImportError:
    TOPOLOGY_AVAILABLE = False
    logger.warning("⚠️  Topology fusion not available")


class GalaxyClient:
    def __init__(
        self,
        session_name: Optional[str] = None,
        task_name: Optional[str] = None,
        max_rounds: int = 10,
        log_level: str = "WARNING",
        output_dir: Optional[str] = None,
        # 新增参数
        enable_topology: bool = False,
        topology_config: Optional[str] = None
    ):
        """
        Initialize Galaxy client.
        
        :param enable_topology: 是否启用拓扑融合功能
        :param topology_config: 拓扑配置文件路径
        """
        # ... 原有代码 ...
        
        self.enable_topology = enable_topology
        self.topology_config = topology_config
    
    async def initialize(self) -> None:
        """
        Initialize all Galaxy framework components.
        """
        try:
            with self.display.show_initialization_progress() as progress:
                task = progress.add_task(
                    "[cyan]Initializing UFO3 Framework...", total=None
                )
                
                self.logger.info("🚀 Initializing UFO3 Framework components...")
                
                # Initialize constellation client
                progress.update(
                    task, description="[cyan]Setting up Constellation Client..."
                )
                
                # 根据配置选择客户端类型
                if self.enable_topology and TOPOLOGY_AVAILABLE and self.topology_config:
                    self.display.print_info("🌐 Enabling topology fusion...")
                    self._client = TopologyAwareConstellationClient(
                        config=self._device_config,
                        task_name=self.task_name,
                        topology_config_path=self.topology_config,
                        enable_topology=True
                    )
                    self.display.print_success("✅ TopologyAwareConstellationClient initialized")
                else:
                    self._client = ConstellationClient(
                        config=self._device_config,
                        task_name=self.task_name
                    )
                    self.display.print_success("✅ ConstellationClient initialized")
                
                await self._client.initialize()
                
                # ... 其余代码保持不变 ...
```

---

### 5. 节点适配 AIP 接口

#### 5.1 AIP 适配器基类

```python
# 创建 fusion-experiment/ufo-galaxy-unified/fusion/node_adapter.py

import asyncio
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

# 导入微软的 AIP
import sys
sys.path.insert(0, '/home/ubuntu/fusion-experiment/ufo-galaxy-unified/microsoft-ufo')

from aip.endpoints.client_endpoint import DeviceClientEndpoint
from aip.messages import (
    ClientMessage, ServerMessage, Command, Result,
    ResultStatus, TaskStatus, ClientMessageType
)

logger = logging.getLogger(__name__)


class UFONodeAdapter(DeviceClientEndpoint, ABC):
    """
    UFO 节点适配器基类
    
    将你的节点适配为微软 AIP 的 Device Agent
    
    子类需要实现:
    - execute_command(): 执行具体命令
    - get_capabilities(): 返回节点能力
    """
    
    def __init__(
        self,
        node_id: str,
        node_name: str,
        layer: str,
        domain: str,
        server_url: str,
        node_api_url: str
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
        """
        # 初始化 DeviceClientEndpoint
        super().__init__(
            device_id=node_id,
            server_url=server_url
        )
        
        self.node_id = node_id
        self.node_name = node_name
        self.layer = layer
        self.domain = domain
        self.node_api_url = node_api_url
        
        # HTTP 客户端 (用于调用节点的 FastAPI)
        import aiohttp
        self.http_session: Optional[aiohttp.ClientSession] = None
    
    async def start(self):
        """启动适配器"""
        import aiohttp
        self.http_session = aiohttp.ClientSession()
        
        # 注册到微软 Galaxy
        await self.connect()
        
        logger.info(f"✅ Node adapter started: {self.node_id}")
    
    async def stop(self):
        """停止适配器"""
        if self.http_session:
            await self.http_session.close()
        
        await self.disconnect()
        
        logger.info(f"🛑 Node adapter stopped: {self.node_id}")
    
    async def on_task_received(self, message: ServerMessage):
        """
        接收任务 (来自微软 Galaxy)
        
        这是 DeviceClientEndpoint 的回调
        """
        logger.info(f"📥 Task received: {message.user_request}")
        
        try:
            # 执行任务
            result = await self.execute_task(message)
            
            # 发送结果
            await self.send_task_result(result)
            
        except Exception as e:
            logger.error(f"❌ Task execution failed: {e}")
            await self.send_error(str(e))
    
    async def execute_task(self, message: ServerMessage) -> Dict[str, Any]:
        """
        执行任务
        
        将微软的任务转换为节点 API 调用
        """
        # 1. 提取命令
        commands = message.actions or []
        
        results = []
        for cmd in commands:
            result = await self.execute_command(cmd)
            results.append(result)
        
        return {
            "status": "completed",
            "results": results
        }
    
    @abstractmethod
    async def execute_command(self, command: Command) -> Result:
        """
        执行单个命令
        
        子类必须实现此方法
        """
        pass
    
    async def call_node_api(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        调用节点的 FastAPI
        
        Args:
            endpoint: API 端点 (如 "/execute")
            method: HTTP 方法
            data: 请求数据
        
        Returns:
            API 响应
        """
        url = f"{self.node_api_url}{endpoint}"
        
        try:
            if method == "POST":
                async with self.http_session.post(url, json=data) as resp:
                    return await resp.json()
            elif method == "GET":
                async with self.http_session.get(url) as resp:
                    return await resp.json()
            else:
                raise ValueError(f"Unsupported method: {method}")
        
        except Exception as e:
            logger.error(f"❌ Node API call failed: {e}")
            raise
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        返回节点能力列表
        
        子类必须实现此方法
        """
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """返回节点元数据"""
        return {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "layer": self.layer,
            "domain": self.domain,
            "capabilities": self.get_capabilities()
        }
```

#### 5.2 具体节点适配器示例

```python
# 创建 fusion-experiment/ufo-galaxy-unified/fusion/adapters/node_00_adapter.py

from ..node_adapter import UFONodeAdapter
from aip.messages import Command, Result, ResultStatus


class Node00Adapter(UFONodeAdapter):
    """
    Node_00 (StateMachine) 适配器
    """
    
    def __init__(self, server_url: str):
        super().__init__(
            node_id="Node_00",
            node_name="StateMachine",
            layer="core",
            domain="state_management",
            server_url=server_url,
            node_api_url="http://localhost:8000"  # Node_00 的 FastAPI 端口
        )
    
    async def execute_command(self, command: Command) -> Result:
        """执行命令"""
        tool_name = command.tool_name
        parameters = command.parameters or {}
        
        try:
            if tool_name == "acquire_lock":
                # 调用 Node_00 的锁接口
                response = await self.call_node_api(
                    "/lock/acquire",
                    method="POST",
                    data={
                        "node_id": parameters.get("node_id"),
                        "resource_id": parameters.get("resource_id"),
                        "timeout_seconds": parameters.get("timeout", 30)
                    }
                )
                
                return Result(
                    status=ResultStatus.SUCCESS if response["success"] else ResultStatus.FAILURE,
                    result=response,
                    namespace="state_management",
                    call_id=command.call_id
                )
            
            elif tool_name == "release_lock":
                response = await self.call_node_api(
                    "/lock/release",
                    method="POST",
                    data={
                        "node_id": parameters.get("node_id"),
                        "resource_id": parameters.get("resource_id"),
                        "token": parameters.get("token")
                    }
                )
                
                return Result(
                    status=ResultStatus.SUCCESS if response["success"] else ResultStatus.FAILURE,
                    result=response,
                    namespace="state_management",
                    call_id=command.call_id
                )
            
            else:
                return Result(
                    status=ResultStatus.FAILURE,
                    error=f"Unknown command: {tool_name}",
                    namespace="state_management",
                    call_id=command.call_id
                )
        
        except Exception as e:
            return Result(
                status=ResultStatus.FAILURE,
                error=str(e),
                namespace="state_management",
                call_id=command.call_id
            )
    
    def get_capabilities(self) -> List[str]:
        """返回能力"""
        return [
            "state_management",
            "lock_management",
            "node_registry",
            "global_state"
        ]
```

---

### 6. 拓扑配置文件

#### 6.1 创建拓扑配置

```json
// 创建 fusion-experiment/ufo-galaxy-unified/config/topology.json

{
  "version": "1.0",
  "topology_type": "three_layer_sphere",
  "layers": [
    {
      "name": "core",
      "index": 0,
      "radius": 1.0,
      "description": "核心层 - 系统管理和协调"
    },
    {
      "name": "cognitive",
      "index": 1,
      "radius": 2.0,
      "description": "认知层 - 智能处理和分析"
    },
    {
      "name": "perception",
      "index": 2,
      "radius": 3.0,
      "description": "感知层 - 数据采集和感知"
    }
  ],
  "domains": [
    "state_management",
    "vision",
    "nlu",
    "task_management",
    "security",
    "storage",
    "network",
    "sandbox",
    "general"
  ],
  "nodes": [
    {
      "id": "Node_00",
      "name": "StateMachine",
      "layer": "core",
      "domain": "state_management",
      "coordinates": {
        "theta": 0.0,
        "phi": 0.0,
        "radius": 1.0
      },
      "capabilities": [
        "state_management",
        "lock_management",
        "node_registry"
      ],
      "api_url": "http://localhost:8000",
      "neighbors": ["Node_04", "Node_02"],
      "metadata": {
        "priority": "critical",
        "max_load": 100
      }
    },
    {
      "id": "Node_04",
      "name": "Router",
      "layer": "core",
      "domain": "task_management",
      "coordinates": {
        "theta": 0.5,
        "phi": 1.57,
        "radius": 1.0
      },
      "capabilities": [
        "routing",
        "task_distribution"
      ],
      "api_url": "http://localhost:8004",
      "neighbors": ["Node_00", "Node_02", "Node_16"],
      "metadata": {
        "priority": "high",
        "max_load": 200
      }
    }
    // ... 其他 101 个节点 ...
  ]
}
```

---

### 7. 统一启动脚本

#### 7.1 融合系统启动器

```python
# 创建 fusion-experiment/ufo-galaxy-unified/fusion/start_fusion.py

#!/usr/bin/env python3
"""
UFO Galaxy 深度融合系统启动器

启动顺序:
1. 启动你的 103 个节点 (Podman Compose)
2. 启动节点适配器
3. 启动微软 UFO³ Galaxy (带拓扑支持)
"""

import asyncio
import logging
import subprocess
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FusionSystemStarter:
    """融合系统启动器"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.nodes_started = False
        self.adapters_started = False
        self.galaxy_started = False
    
    async def start(self):
        """启动融合系统"""
        try:
            logger.info("🚀 Starting UFO Galaxy Fusion System...")
            
            # 1. 启动节点系统
            await self.start_nodes()
            
            # 2. 启动适配器
            await self.start_adapters()
            
            # 3. 启动微软 Galaxy
            await self.start_galaxy()
            
            logger.info("✅ Fusion System started successfully!")
            logger.info("🌐 Access Galaxy WebUI at: http://localhost:5000")
            
            # 保持运行
            await self.keep_alive()
        
        except KeyboardInterrupt:
            logger.info("\n⚠️  Shutting down...")
            await self.shutdown()
        except Exception as e:
            logger.error(f"❌ Startup failed: {e}")
            await self.shutdown()
            sys.exit(1)
    
    async def start_nodes(self):
        """启动 103 个节点"""
        logger.info("📦 Starting 103 nodes with Podman Compose...")
        
        compose_file = self.base_dir / "podman-compose.yml"
        
        if not compose_file.exists():
            logger.warning("⚠️  podman-compose.yml not found, skipping...")
            return
        
        # 使用 podman-compose 启动
        result = subprocess.run(
            ["podman-compose", "up", "-d"],
            cwd=self.base_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to start nodes: {result.stderr}")
        
        logger.info("✅ Nodes started, waiting for initialization...")
        await asyncio.sleep(10)  # 等待节点启动
        
        self.nodes_started = True
    
    async def start_adapters(self):
        """启动节点适配器"""
        logger.info("🔌 Starting node adapters...")
        
        # 导入适配器
        from .adapters.node_00_adapter import Node00Adapter
        # ... 导入其他适配器 ...
        
        # 启动适配器
        galaxy_server_url = "ws://localhost:5000/constellation"
        
        adapters = [
            Node00Adapter(galaxy_server_url),
            # ... 其他适配器 ...
        ]
        
        for adapter in adapters:
            await adapter.start()
            logger.info(f"✅ Adapter started: {adapter.node_id}")
        
        self.adapters_started = True
    
    async def start_galaxy(self):
        """启动微软 Galaxy"""
        logger.info("🌌 Starting Microsoft UFO³ Galaxy...")
        
        # 导入 GalaxyClient
        sys.path.insert(0, str(self.base_dir / "microsoft-ufo"))
        from galaxy.galaxy_client import GalaxyClient
        
        # 创建客户端 (启用拓扑)
        client = GalaxyClient(
            session_name="fusion_session",
            enable_topology=True,
            topology_config=str(self.base_dir / "config" / "topology.json")
        )
        
        # 初始化
        await client.initialize()
        
        logger.info("✅ Galaxy initialized with topology support")
        
        self.galaxy_started = True
        self.galaxy_client = client
    
    async def keep_alive(self):
        """保持系统运行"""
        logger.info("🔄 System running, press Ctrl+C to stop...")
        
        while True:
            await asyncio.sleep(60)
            
            # 打印状态
            if hasattr(self, 'galaxy_client'):
                stats = self.galaxy_client._client.get_topology_stats()
                if stats:
                    logger.info(f"📊 Topology stats: {stats}")
    
    async def shutdown(self):
        """关闭系统"""
        logger.info("🛑 Shutting down fusion system...")
        
        # 停止 Galaxy
        if self.galaxy_started:
            logger.info("Stopping Galaxy...")
            # TODO: 停止 Galaxy
        
        # 停止适配器
        if self.adapters_started:
            logger.info("Stopping adapters...")
            # TODO: 停止适配器
        
        # 停止节点
        if self.nodes_started:
            logger.info("Stopping nodes...")
            subprocess.run(
                ["podman-compose", "down"],
                cwd=self.base_dir
            )
        
        logger.info("✅ Shutdown complete")


async def main():
    starter = FusionSystemStarter()
    await starter.start()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📋 实施步骤总结

### 阶段 1: 基础架构 (1 周)

**任务**:
1. ✅ 创建 `fusion/` 目录结构
2. ✅ 实现 TopologyManager
3. ✅ 扩展 AIP 协议消息
4. ✅ 创建拓扑配置文件

**验证**:
- TopologyManager 能加载拓扑
- 路由算法正常工作

### 阶段 2: 客户端集成 (1 周)

**任务**:
1. ✅ 实现 TopologyAwareConstellationClient
2. ✅ 修改 GalaxyClient 集成拓扑
3. ✅ 创建节点适配器基类

**验证**:
- GalaxyClient 能启用拓扑模式
- 拓扑路由正常工作

### 阶段 3: 节点适配 (2 周)

**任务**:
1. ✅ 为核心层节点创建适配器 (16 个)
2. ✅ 为认知层节点创建适配器 (46 个)
3. ✅ 为感知层节点创建适配器 (31 个)

**验证**:
- 每个节点能注册到 Galaxy
- 节点能接收和执行任务

### 阶段 4: 测试和优化 (1 周)

**任务**:
1. ✅ 端到端测试
2. ✅ 性能优化
3. ✅ 文档完善

**验证**:
- 系统稳定运行
- 性能达标

### 阶段 5: 容器化部署 (1 周)

**任务**:
1. ✅ 创建 Podman Compose 配置
2. ✅ 创建启动脚本
3. ✅ 部署测试

**验证**:
- 一键启动
- 容器化运行正常

---

## ⏱️ 时间规划

| 阶段 | 任务 | 时间 | 累计 |
|------|------|------|------|
| 1 | 基础架构 | 1 周 | 1 周 |
| 2 | 客户端集成 | 1 周 | 2 周 |
| 3 | 节点适配 | 2 周 | 4 周 |
| 4 | 测试优化 | 1 周 | 5 周 |
| 5 | 容器化部署 | 1 周 | 6 周 |

**总计**: 6 周 (约 1.5 个月)

---

## 🎯 下一步

我现在开始实施！

**你想让我**:
1. ✅ 立即开始编写代码 (从 TopologyManager 开始)
2. ⏸️ 先回答你的问题
3. 📝 先完善某个部分的设计

**请告诉我！** 🚀
