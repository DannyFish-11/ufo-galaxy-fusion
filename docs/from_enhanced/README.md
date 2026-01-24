# UFO³ Galaxy Enhanced Nodes

---

## 📝 **最新状态 (2026-01-24)**

- **最新提交:** `7f9a8b9 Add basic unit test for node_108_metacognition`
- **静态代码检查:** ✅ 通过
- **已知问题:** 无

---




**融合性增强外骨骼 - 新增节点包**

本仓库包含为 UFO³ Galaxy 系统开发的 5 个增强节点，旨在提升系统的智能化水平和工具集成能力。

---

## 📦 节点清单

### 阶段二：智能增强节点

| 节点编号 | 节点名称 | 端口 | 智能化水平 | 状态 |
| :--- | :--- | :---: | :---: | :---: |
| **Node_108** | MetaCognition | 9100 | L3.5 | ✅ 已完成 |
| **Node_109** | ProactiveSensing | 9101 | L3.5 | ✅ 已完成 |

### 阶段三：工具集成节点

| 节点编号 | 节点名称 | 端口 | 智能化水平 | 状态 |
| :--- | :--- | :---: | :---: | :---: |
| **Node_113** | ExternalToolWrapper | 9102 | L3 | ✅ 已完成 |
| **Node_114** | OpenCode | 9103 | L3 | ✅ 已完成 |
| **Node_115** | NodeFactory | 9104 | L4 | ✅ 已完成 |

---

## 🎯 节点功能概述

### Node_108_MetaCognition（元认知节点）

**核心能力**: 让系统能够反思自己的思考过程，评估决策质量，并持续优化策略。

**关键特性**:
- 思维过程追踪与分析
- 决策质量评估（置信度匹配、推理质量）
- 策略优化建议
- 认知偏差检测（确认偏差、锚定偏差、过度自信等5种）

**API 端点**:
- `POST /api/v1/track_thought` - 追踪思维
- `POST /api/v1/track_decision` - 追踪决策
- `POST /api/v1/evaluate_decision` - 评估决策
- `POST /api/v1/reflect` - 反思
- `POST /api/v1/optimize_strategy` - 优化策略
- `GET /api/v1/cognitive_state` - 获取认知状态

**依赖节点**: Node_01_OneAPI, Node_103_KnowledgeGraph, Node_73_Learning

**文档**: [nodes/node_108_metacognition/README.md](nodes/node_108_metacognition/README.md)

---

### Node_109_ProactiveSensing（主动感知节点）

**核心能力**: 主动发现环境变化、潜在问题和优化机会，而不是被动等待指令。

**关键特性**:
- 环境状态监控（自定义监控器注册）
- 异常模式识别（性能、错误、模式、资源）
- 机会发现（优化、集成、学习、自动化）
- 主动预警（三级预警：INFO/WARNING/CRITICAL）

**API 端点**:
- `POST /api/v1/scan_environment` - 扫描环境
- `POST /api/v1/detect_anomalies` - 检测异常
- `POST /api/v1/discover_opportunities` - 发现机会
- `POST /api/v1/create_alert` - 创建预警
- `POST /api/v1/acknowledge_alert` - 确认预警
- `GET /api/v1/alerts` - 获取预警列表

**依赖节点**: Node_22_BraveSearch, Node_25_GoogleSearch, Node_108_MetaCognition

**文档**: [nodes/node_109_proactive_sensing/README.md](nodes/node_109_proactive_sensing/README.md)

---

### Node_113_ExternalToolWrapper（通用工具包装器）

**核心能力**: 动态学习和使用任何 CLI 工具，无需预先编写集成代码。

**关键特性**:
- 工具自动发现（搜索 + LLM 理解）
- 文档理解与解析
- 动态命令生成
- 自动安装和验证（支持6种安装方法）
- 执行结果验证

**API 端点**:
- `POST /api/v1/use_tool` - 使用工具
- `POST /api/v1/learn_tool` - 手动教授工具
- `POST /api/v1/discover_tool` - 自动发现工具
- `GET /api/v1/known_tools` - 获取已知工具
- `GET /api/v1/tool_knowledge/{tool_name}` - 获取工具知识
- `DELETE /api/v1/forget_tool` - 忘记工具

**依赖节点**: Node_22_BraveSearch, Node_01_OneAPI, Node_09_Sandbox, Node_73_Learning

**文档**: [nodes/node_113_external_tool_wrapper/README.md](nodes/node_113_external_tool_wrapper/README.md)

---

### Node_114_OpenCode（OpenCode 专用节点）

**核心能力**: 深度集成 OpenCode AI 编程工具，提供高效可靠的代码生成能力。

**关键特性**:
- 多模型支持（OpenAI, Anthropic, DeepSeek, Groq, Local）
- 自动配置管理（~/.opencode.json）
- 代码质量验证（语法检查 + 质量评分）
- 与系统其他节点深度协同

**API 端点**:
- `POST /api/v1/generate_code` - 生成代码
- `POST /api/v1/configure` - 配置 OpenCode
- `POST /api/v1/install` - 安装 OpenCode
- `GET /api/v1/status` - 获取状态
- `GET /api/v1/supported_models` - 获取支持的模型
- `GET /api/v1/generation_history` - 获取生成历史

**依赖节点**: Node_03_SecretVault, Node_102_DebugOptimize, Node_113_ExternalToolWrapper

**文档**: [nodes/node_114_opencode/README.md](nodes/node_114_opencode/README.md)

---

### Node_115_NodeFactory（节点工厂）

**核心能力**: 自主编写和加载新节点，让系统能够"自我进化"。

**关键特性**:
- 动态节点生成（从规格或自然语言描述）
- 自动代码生成（引擎、服务器、文档、测试）
- 代码质量验证
- 自动部署

**API 端点**:
- `POST /api/v1/generate_node` - 生成节点（从规格）
- `POST /api/v1/generate_node_from_description` - 生成节点（从描述）
- `GET /api/v1/generation_history` - 获取生成历史

**依赖节点**: Node_114_OpenCode, Node_108_MetaCognition, Node_109_ProactiveSensing, Node_01_OneAPI

**文档**: [nodes/node_115_node_factory/README.md](nodes/node_115_node_factory/README.md)

---

## 🚀 安装与部署

### 前置要求

- UFO³ Galaxy 主系统已部署
- Python 3.11+
- Redis（用于节点间通信）
- 所需 API Keys（OpenAI, Anthropic, 等）

### 部署步骤

1. **克隆本仓库**
```bash
git clone https://github.com/DannyFish-11/ufo-galaxy-enhanced-nodes.git
cd ufo-galaxy-enhanced-nodes
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 创建 .env 文件
cat > .env << EOF
# Node_108_MetaCognition
NODE_108_PORT=9100
OPENAI_API_KEY=sk-...

# Node_109_ProactiveSensing
NODE_109_PORT=9101
BRAVE_API_KEY=...

# Node_113_ExternalToolWrapper
NODE_113_PORT=9102

# Node_114_OpenCode
NODE_114_PORT=9103
ANTHROPIC_API_KEY=sk-ant-...
DEEPSEEK_API_KEY=...

# Node_115_NodeFactory
NODE_115_PORT=9104
EOF
```

4. **启动节点**
```bash
# 方式一：单独启动各节点
cd nodes/node_108_metacognition && python server.py &
cd nodes/node_109_proactive_sensing && python server.py &
cd nodes/node_113_external_tool_wrapper && python server.py &
cd nodes/node_114_opencode && python server.py &
cd nodes/node_115_node_factory && python server.py &

# 方式二：集成到主系统的 smart_launcher.py（推荐）
# 将 config/node_dependencies_additions.json 合并到主系统配置
```

5. **验证运行**
```bash
curl http://localhost:9100/health  # Node_108
curl http://localhost:9101/health  # Node_109
curl http://localhost:9102/health  # Node_113
curl http://localhost:9103/health  # Node_114
curl http://localhost:9104/health  # Node_115
```

---

## 📊 系统架构

```
UFO³ Galaxy System
├── Phase 1: 基础系统（91个节点）
│   ├── Node_01_OneAPI (LLM 接口)
│   ├── Node_03_SecretVault (密钥管理)
│   ├── Node_09_Sandbox (沙箱执行)
│   ├── Node_22_BraveSearch (搜索)
│   ├── Node_73_Learning (学习)
│   └── ...
│
├── Phase 2: 智能增强（本项目）
│   ├── Node_108_MetaCognition ──┐
│   │   └── 反思、评估、优化    │
│   │                           ├─→ 增强系统自我认知
│   └── Node_109_ProactiveSensing ┘
│       └── 监控、检测、预警
│
└── Phase 3: 工具集成与自我扩展（本项目）
    ├── Node_113_ExternalToolWrapper ──┐
    │   └── 动态学习任何工具          │
    │                                 │
    ├── Node_114_OpenCode ────────────┤
    │   └── AI 代码生成              ├─→ 实现系统自我扩展
    │                                 │
    └── Node_115_NodeFactory ─────────┘
        └── 自主创建新节点
```

---

## 🧪 测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个节点测试
pytest tests/test_node_108.py -v
pytest tests/test_node_109.py -v
pytest tests/test_node_113.py -v
pytest tests/test_node_114.py -v
pytest tests/test_node_115.py -v
```

---

## 📈 智能化水平

| 级别 | 描述 | 节点 |
| :---: | :--- | :--- |
| **L4** | 完全自主智能 | Node_115 |
| **L3.5** | 条件自主智能（增强版） | Node_108, Node_109 |
| **L3** | 条件自主智能 | Node_113, Node_114 |

---

## 🎯 典型应用场景

### 场景一：用户询问"能用 OpenCode 吗？"

```
1. Node_109 检测到工具集成需求
2. Node_113 自动发现并学习 OpenCode
3. Node_114 深度集成 OpenCode
4. Node_108 评估集成质量
5. 系统回复："✅ OpenCode 已就绪！"
```

### 场景二：系统自我优化

```
1. Node_109 检测到性能异常
2. Node_108 反思并发现缺少缓存机制
3. Node_115 自动生成 Node_116_CacheManager
4. 自动部署并集成
5. 性能提升 50%
```

### 场景三：批量工具集成

```
用户："我需要使用 ffmpeg, jq, curl"

1. Node_113 并行学习 3 个工具
2. 自动安装和配置
3. 生成使用示例
4. 系统回复："✅ 所有工具已就绪！"
```

---

## 📚 文档

- [Node_108 完整文档](nodes/node_108_metacognition/README.md)
- [Node_109 完整文档](nodes/node_109_proactive_sensing/README.md)
- [Node_113 完整文档](nodes/node_113_external_tool_wrapper/README.md)
- [Node_114 完整文档](nodes/node_114_opencode/README.md)
- [Node_115 完整文档](nodes/node_115_node_factory/README.md)
- [配置文件说明](config/node_dependencies_additions.json)

---

## 🔄 开发进度

- [x] 项目初始化
- [x] 架构设计
- [x] Node_108_MetaCognition 开发
- [x] Node_109_ProactiveSensing 开发
- [x] Node_113_ExternalToolWrapper 开发
- [x] Node_114_OpenCode 开发
- [x] Node_115_NodeFactory 开发
- [x] 配置文件更新
- [x] 文档完善
- [ ] 集成测试
- [ ] 部署验证

---

## 📝 版本历史

### v0.1.0 (2026-01-24)
- ✅ 完成所有 5 个节点开发
- ✅ 核心引擎实现
- ✅ FastAPI 服务器实现
- ✅ 完整 API 文档
- ✅ 配置文件更新
- ⏳ 待进行集成测试

---

## 🔧 系统要求

- **Python**: >=3.11
- **UFO³ Galaxy**: >=3.0.0
- **操作系统**: Linux / macOS / Windows
- **内存**: 建议 8GB+
- **磁盘**: 建议 10GB+

---

## 📄 许可证

本项目为私有仓库，仅供 UFO³ Galaxy 系统使用。

---

**作者**: Manus AI  
**最后更新**: 2026-01-24  
**状态**: ✅ 所有节点开发完成，待集成测试

