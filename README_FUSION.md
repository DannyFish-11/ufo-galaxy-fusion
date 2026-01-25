# 🚀 UFO Galaxy Fusion

**深度融合系统 - 将 103 节点三层球体拓扑与微软 UFO³ Galaxy 框架进行代码级集成**

---

## 📋 项目概述

这是一个**真正的融合系统**，不是简单的桥接或适配。我们将：

- ✅ **你的系统**: 103 个功能节点，三层球体拓扑（Core, Cognitive, Perception）
- ✅ **微软 UFO³ Galaxy**: 跨设备编排框架，动态 DAG 任务分配
- ✅ **深度融合**: 代码级集成，让微软 Galaxy 原生理解和使用三层拓扑

---

## 🏗️ 架构

```
GalaxyClient (微软的，轻度扩展)
    ↓
TopologyAwareConstellationClient (拓扑感知)
    ↓ 统一 AIP 协议
┌────────────────┬────────────────┬────────────────┐
│  Core Layer    │ Cognitive Layer│ Perception     │
│  (16 nodes)    │ (45 nodes)     │ Layer          │
│                │                │ (41 nodes)     │
└────────────────┴────────────────┴────────────────┘
```

---

## 📂 目录结构

```
ufo-galaxy-fusion/
├── nodes/                       # 103 个功能节点
├── galaxy_gateway/              # Galaxy 网关
├── enhancements/                # 增强组件
├── microsoft-ufo/               # 微软 UFO³ Galaxy (子模块)
├── fusion/                      # 🆕 融合层
│   ├── topology_manager.py      # 拓扑管理器
│   ├── topology_aware_client.py # 拓扑感知客户端
│   ├── node_adapter.py          # 节点适配器基类
│   └── adapters/                # 具体节点适配器
├── config/                      # 配置文件
│   └── topology.json            # 拓扑配置 (102 节点)
└── README_FUSION.md             # 本文档
```

---

## 🎯 核心组件

### 1. TopologyManager
- 管理三层球体拓扑
- 4 种路由策略：负载均衡、最短路径、域亲和、层级优先
- 负载跟踪和监控

### 2. TopologyAwareConstellationClient
- 扩展微软的 ConstellationClient
- 基于拓扑的智能任务分配
- 自动域和层级推断

### 3. Node Adapters
- 将 FastAPI 节点适配为微软 AIP Device Agent
- 支持健康检查、命令执行、结果返回

### 4. AIP Topology Extensions
- 扩展微软 AIP 协议
- 添加拓扑信息、路由提示、统计数据

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/DannyFish-11/ufo-galaxy-fusion.git
cd ufo-galaxy-fusion
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置

```bash
cp .env.example .env
# 编辑 .env 文件
```

### 4. 启动融合系统

```bash
python fusion/start_fusion.py
```

---

## 📊 拓扑配置

拓扑配置文件：`config/topology.json`

- **102 个节点**
- **三层分布**:
  - Core Layer: 16 节点
  - Cognitive Layer: 45 节点
  - Perception Layer: 41 节点
- **15 个域**: vision, nlu, state_management, task_management, security, storage, network, media, knowledge, monitoring, search, notification, device_control, sandbox, general

---

## 🔧 开发

### 创建新的节点适配器

```python
from fusion.node_adapter import UFONodeAdapter

class MyNodeAdapter(UFONodeAdapter):
    def __init__(self, server_url):
        super().__init__(
            node_id="Node_XX",
            node_name="MyNode",
            layer="cognitive",
            domain="my_domain",
            server_url=server_url,
            node_api_url="http://localhost:8XXX"
        )
    
    async def execute_command(self, command):
        # 实现命令执行逻辑
        ...
    
    def get_capabilities(self):
        return ["my_capability"]
```

---

## 📖 文档

- [深度融合架构设计](DEEP_FUSION_PLAN_A.md)
- [拓扑管理器文档](docs/topology_manager.md)
- [节点适配器指南](docs/node_adapter_guide.md)
- [API 参考](docs/api_reference.md)

---

## 🧪 测试

```bash
# 运行测试
pytest tests/

# 测试拓扑管理器
python -m pytest tests/test_topology_manager.py

# 测试节点适配器
python -m pytest tests/test_node_adapter.py
```

---

## 📈 状态

- ✅ 拓扑管理器 (完成)
- ✅ 拓扑配置生成 (完成)
- ✅ 节点适配器基类 (完成)
- ✅ AIP 协议扩展 (完成)
- ✅ 拓扑感知客户端 (完成)
- 🔄 具体节点适配器 (进行中)
- 🔄 统一启动脚本 (进行中)
- ⏳ 测试和验证 (待开始)
- ⏳ 容器化部署 (待开始)

---

## 🤝 贡献

这是一个实验性项目，欢迎贡献！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- **Microsoft UFO³ Galaxy**: 跨设备编排框架
- **UFO Galaxy Unified**: 103 节点三层球体拓扑系统

---

**作者**: Manus AI  
**日期**: 2026-01-25  
**版本**: 0.1.0 (Alpha)
