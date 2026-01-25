"""
UFO Galaxy Fusion - AIP Topology Extensions

扩展微软 AIP 协议以支持拓扑概念

新增消息类型和字段:
1. TopologyInfo - 拓扑信息
2. TopologyRoutingHint - 拓扑路由提示
3. 扩展 ClientMessage 和 ServerMessage

作者: Manus AI
日期: 2026-01-25
"""

from typing import List, Optional, Tuple
from pydantic import BaseModel, Field


# ============================================================================
# Topology Data Structures
# ============================================================================

class TopologyInfo(BaseModel):
    """
    拓扑信息 - 三层球体拓扑
    
    描述节点在三层球体拓扑中的位置和关系
    """
    
    # 层级 (Layer)
    layer: str = Field(..., description="层级: core, cognitive, perception")
    layer_index: int = Field(..., description="层级索引: 0, 1, 2", ge=0, le=2)
    
    # 域 (Domain)
    domain: str = Field(..., description="域: vision, nlu, state_management, etc.")
    
    # 球面坐标 (Spherical Coordinates)
    # 用于可视化和路径优化
    theta: float = Field(..., description="极角 [0, π]", ge=0.0, le=3.14159)
    phi: float = Field(..., description="方位角 [0, 2π]", ge=0.0, le=6.28318)
    radius: float = Field(..., description="半径 (层级决定)", gt=0.0)
    
    # 拓扑关系
    neighbors: List[str] = Field(
        default_factory=list,
        description="邻居节点 ID 列表"
    )
    parent_nodes: Optional[List[str]] = Field(
        default=None,
        description="父节点 (上层) ID 列表"
    )
    child_nodes: Optional[List[str]] = Field(
        default=None,
        description="子节点 (下层) ID 列表"
    )
    
    # 路由权重
    routing_weight: float = Field(
        default=1.0,
        description="路由权重",
        ge=0.0
    )
    load_capacity: int = Field(
        default=100,
        description="负载容量",
        gt=0
    )
    
    # 当前状态
    current_load: float = Field(
        default=0.0,
        description="当前负载 [0.0, 1.0]",
        ge=0.0,
        le=1.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "layer": "core",
                "layer_index": 0,
                "domain": "state_management",
                "theta": 0.5236,
                "phi": 1.5708,
                "radius": 1.0,
                "neighbors": ["Node_04", "Node_02"],
                "parent_nodes": None,
                "child_nodes": ["Node_16", "Node_20"],
                "routing_weight": 1.0,
                "load_capacity": 100,
                "current_load": 0.3
            }
        }


class TopologyRoutingHint(BaseModel):
    """
    拓扑路由提示
    
    用于指导任务路由到最佳节点
    """
    
    # 首选层级
    preferred_layer: Optional[str] = Field(
        default=None,
        description="首选层级: core, cognitive, perception"
    )
    
    # 首选域
    preferred_domain: Optional[str] = Field(
        default=None,
        description="首选域: vision, nlu, state_management, etc."
    )
    
    # 源节点 (用于路径优化)
    source_node_id: Optional[str] = Field(
        default=None,
        description="源节点 ID，用于计算最短路径"
    )
    
    # 路由策略
    routing_strategy: str = Field(
        default="load_balanced",
        description="路由策略: load_balanced, shortest_path, domain_affinity, layer_priority"
    )
    
    # 约束条件
    exclude_nodes: List[str] = Field(
        default_factory=list,
        description="排除的节点 ID 列表"
    )
    required_capabilities: List[str] = Field(
        default_factory=list,
        description="必需的能力列表"
    )
    
    # 性能要求
    max_latency_ms: Optional[int] = Field(
        default=None,
        description="最大延迟 (毫秒)",
        gt=0
    )
    min_reliability: Optional[float] = Field(
        default=None,
        description="最小可靠性 [0.0, 1.0]",
        ge=0.0,
        le=1.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "preferred_layer": "cognitive",
                "preferred_domain": "vision",
                "source_node_id": "Node_00",
                "routing_strategy": "shortest_path",
                "exclude_nodes": ["Node_10", "Node_11"],
                "required_capabilities": ["image_processing", "ocr"],
                "max_latency_ms": 1000,
                "min_reliability": 0.95
            }
        }


class DeviceMetadataExtended(BaseModel):
    """
    扩展的设备元数据
    
    在原有元数据基础上添加拓扑信息
    """
    
    # 原有字段 (兼容微软)
    os: Optional[str] = Field(default=None, description="操作系统")
    capabilities: List[str] = Field(
        default_factory=list,
        description="能力列表"
    )
    
    # 新增拓扑字段
    topology: Optional[TopologyInfo] = Field(
        default=None,
        description="拓扑信息"
    )
    
    # 性能指标
    cpu_cores: int = Field(default=1, description="CPU 核心数", gt=0)
    memory_mb: int = Field(default=1024, description="内存 (MB)", gt=0)
    current_load: float = Field(
        default=0.0,
        description="当前负载 [0.0, 1.0]",
        ge=0.0,
        le=1.0
    )
    
    # 网络信息
    network_latency_ms: Optional[float] = Field(
        default=None,
        description="网络延迟 (毫秒)",
        ge=0.0
    )
    bandwidth_mbps: Optional[float] = Field(
        default=None,
        description="带宽 (Mbps)",
        ge=0.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "os": "linux",
                "capabilities": ["state_management", "lock_management"],
                "topology": {
                    "layer": "core",
                    "layer_index": 0,
                    "domain": "state_management",
                    "theta": 0.5236,
                    "phi": 1.5708,
                    "radius": 1.0,
                    "neighbors": ["Node_04", "Node_02"],
                    "routing_weight": 1.0,
                    "load_capacity": 100,
                    "current_load": 0.3
                },
                "cpu_cores": 4,
                "memory_mb": 8192,
                "current_load": 0.3,
                "network_latency_ms": 5.2,
                "bandwidth_mbps": 1000.0
            }
        }


class TopologyStats(BaseModel):
    """
    拓扑统计信息
    
    用于监控和可视化
    """
    
    total_nodes: int = Field(..., description="总节点数")
    
    # 层级统计
    core_nodes: int = Field(..., description="核心层节点数")
    cognitive_nodes: int = Field(..., description="认知层节点数")
    perception_nodes: int = Field(..., description="感知层节点数")
    
    # 域统计
    domains: List[str] = Field(..., description="域列表")
    domain_distribution: dict = Field(
        default_factory=dict,
        description="域分布 {domain: count}"
    )
    
    # 负载统计
    average_load: float = Field(..., description="平均负载")
    max_load: float = Field(..., description="最大负载")
    min_load: float = Field(..., description="最小负载")
    
    # 连接统计
    total_edges: int = Field(..., description="总边数")
    average_degree: float = Field(..., description="平均度数")
    
    # 健康状态
    healthy_nodes: int = Field(..., description="健康节点数")
    unhealthy_nodes: int = Field(default=0, description="不健康节点数")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_nodes": 102,
                "core_nodes": 16,
                "cognitive_nodes": 45,
                "perception_nodes": 41,
                "domains": ["vision", "nlu", "state_management"],
                "domain_distribution": {
                    "vision": 10,
                    "nlu": 8,
                    "state_management": 5
                },
                "average_load": 0.35,
                "max_load": 0.85,
                "min_load": 0.05,
                "total_edges": 256,
                "average_degree": 5.02,
                "healthy_nodes": 100,
                "unhealthy_nodes": 2
            }
        }


# ============================================================================
# Extended Message Types
# ============================================================================

class ClientMessageWithTopology(BaseModel):
    """
    带拓扑信息的客户端消息
    
    扩展原有的 ClientMessage，添加拓扑相关字段
    
    注意: 这是一个扩展类，实际使用时应该将这些字段
    添加到原有的 ClientMessage 中，或者通过 metadata 字段传递
    """
    
    # 拓扑元数据
    topology_metadata: Optional[TopologyInfo] = Field(
        default=None,
        description="节点的拓扑信息"
    )
    
    # 路由提示
    routing_hint: Optional[TopologyRoutingHint] = Field(
        default=None,
        description="任务路由提示"
    )


class ServerMessageWithTopology(BaseModel):
    """
    带拓扑信息的服务器消息
    
    扩展原有的 ServerMessage，添加拓扑相关字段
    """
    
    # 路由提示
    routing_hint: Optional[TopologyRoutingHint] = Field(
        default=None,
        description="任务路由提示"
    )
    
    # 选择的节点路径
    selected_node_path: Optional[List[str]] = Field(
        default=None,
        description="选择的节点路径 (用于多跳路由)"
    )
    
    # 拓扑统计
    topology_stats: Optional[TopologyStats] = Field(
        default=None,
        description="拓扑统计信息"
    )


# ============================================================================
# Helper Functions
# ============================================================================

def create_topology_metadata(
    layer: str,
    domain: str,
    coordinates: Tuple[float, float, float],
    neighbors: List[str],
    **kwargs
) -> DeviceMetadataExtended:
    """
    创建拓扑元数据
    
    Args:
        layer: 层级
        domain: 域
        coordinates: 球面坐标 (theta, phi, radius)
        neighbors: 邻居节点列表
        **kwargs: 其他参数
    
    Returns:
        扩展的设备元数据
    """
    layer_index = {"core": 0, "cognitive": 1, "perception": 2}[layer]
    theta, phi, radius = coordinates
    
    topology_info = TopologyInfo(
        layer=layer,
        layer_index=layer_index,
        domain=domain,
        theta=theta,
        phi=phi,
        radius=radius,
        neighbors=neighbors,
        **{k: v for k, v in kwargs.items() if k in TopologyInfo.__fields__}
    )
    
    return DeviceMetadataExtended(
        topology=topology_info,
        **{k: v for k, v in kwargs.items() if k in DeviceMetadataExtended.__fields__}
    )


def create_routing_hint(
    preferred_layer: Optional[str] = None,
    preferred_domain: Optional[str] = None,
    strategy: str = "load_balanced",
    **kwargs
) -> TopologyRoutingHint:
    """
    创建路由提示
    
    Args:
        preferred_layer: 首选层级
        preferred_domain: 首选域
        strategy: 路由策略
        **kwargs: 其他参数
    
    Returns:
        拓扑路由提示
    """
    return TopologyRoutingHint(
        preferred_layer=preferred_layer,
        preferred_domain=preferred_domain,
        routing_strategy=strategy,
        **kwargs
    )


# ============================================================================
# Validation Functions
# ============================================================================

def validate_topology_info(topology: TopologyInfo) -> bool:
    """
    验证拓扑信息
    
    Args:
        topology: 拓扑信息
    
    Returns:
        True 如果有效，否则 False
    """
    # 验证层级
    if topology.layer not in ["core", "cognitive", "perception"]:
        return False
    
    # 验证层级索引
    layer_index_map = {"core": 0, "cognitive": 1, "perception": 2}
    if topology.layer_index != layer_index_map[topology.layer]:
        return False
    
    # 验证坐标范围
    if not (0 <= topology.theta <= 3.14159):
        return False
    if not (0 <= topology.phi <= 6.28318):
        return False
    if topology.radius <= 0:
        return False
    
    # 验证负载
    if not (0.0 <= topology.current_load <= 1.0):
        return False
    
    return True


def validate_routing_hint(hint: TopologyRoutingHint) -> bool:
    """
    验证路由提示
    
    Args:
        hint: 路由提示
    
    Returns:
        True 如果有效，否则 False
    """
    # 验证层级
    if hint.preferred_layer and hint.preferred_layer not in ["core", "cognitive", "perception"]:
        return False
    
    # 验证路由策略
    valid_strategies = ["load_balanced", "shortest_path", "domain_affinity", "layer_priority"]
    if hint.routing_strategy not in valid_strategies:
        return False
    
    # 验证可靠性
    if hint.min_reliability is not None and not (0.0 <= hint.min_reliability <= 1.0):
        return False
    
    return True
