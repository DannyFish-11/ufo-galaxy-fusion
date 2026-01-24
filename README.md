# UFO³ Galaxy Unified - 统一版本

---

## 📝 **最新状态 (2026-01-24)**

- **版本:** v5.0 Unified (三仓库合并版)
- **合并完成:** 2026-01-24
- **总节点数:** 103 个
- **静态代码检查:** ✅ 通过
- **已知问题:** 无

---

**版本**: v5.0 Unified (2026-01-24)  
**总节点数**: 103 个（来自 3 个原始仓库）

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android-lightgrey.svg)](https://github.com/DannyFish-11/ufo-galaxy-unified)

**让 AI 拥有身体** - 一个通过自然语言命令协调多设备完成复杂任务的分布式 AI 代理系统。

---

## 🎯 关于此统一版本

此仓库是以下三个仓库的**完整合并版本**：

1. **ufo-galaxy** (主仓库) - 96 个基础节点和核心功能
2. **ufo-galaxy-main** (主文档仓库) - 额外的文档和 2 个节点
3. **ufo-galaxy-enhanced-nodes** (增强节点仓库) - 5 个高级增强节点

### 合并策略

- ✅ **完整性**: 所有文件、节点、文档都已保留
- ✅ **可追溯**: 通过目录结构标注来源
- ✅ **无冲突**: 节点编号冲突已解决
- ✅ **统一管理**: 一个仓库，简化维护

详细的合并说明请查看 [MERGE_VERIFICATION_REPORT.md](MERGE_VERIFICATION_REPORT.md)。

---

## 🚀 核心特性

| 特性 | 描述 |
|:---|:---|
| 🧠 **智能任务分发** | Node 50 NLU 引擎通过 OneAPI 调用 LLM 理解自然语言命令 |
| 🖨️ **真实硬件集成** | 支持拓竹 3D 打印机、摄像头、串口、蓝牙、NFC 等 |
| 🎬 **AI 内容生成** | 集成 PixVerse API 生成高质量 AI 视频 |
| ⚛️ **异构计算** | 支持量子计算（IBM Quantum）和 AI 加速 |
| 🖥️ **跨平台控制** | Windows UI 自动化、macOS 自动化、Android 屏幕镜像 |
| 🌐 **多协议支持** | HTTP, WebSocket, MQTT, SSH, SFTP, ADB, BLE, Serial, CAN, MAVLink |
| 🧩 **元认知能力** | Node 108 提供系统自我反思和优化能力 |
| 👁️ **主动感知** | Node 109 提供主动环境监测和预测能力 |
| 🔧 **外部工具包装** | Node 116 提供统一的外部工具调用接口 |
| 📝 **开放代码生成** | Node 117 提供高级代码生成和优化能力 |
| 🏭 **节点工厂** | Node 118 支持动态创建和管理节点 |

---

## 🏗️ 架构设计

UFO³ Galaxy Unified 采用分布式、多层级的架构，由 **103 个功能节点**组成，通过 AIP/1.0 协议进行通信。

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    UFO Galaxy 103-Node Unified System                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐        │
│  │ Windows PC      │   │ Huawei Cloud    │   │ Android Device  │        │
│  │ (主控 + 103节点)│ ← │ (子 Agent)      │ ← │ (子 Agent + 无障碍)│        │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘        │
│                                                                         │
│  基础节点 (Node_00-Node_97): 96 个                                      │
│  高级节点 (Node_100-Node_107): 8 个                                     │
│  增强节点 (Node_108-Node_109, Node_112-Node_113, Node_116-Node_118): 7 个│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 节点分布

### 基础节点 (Node_00-Node_97) - 96 个

来自 **ufo-galaxy** 主仓库，包括：

- **核心节点** (Node_00-Node_09): StateMachine, OneAPI, Tasker, SecretVault, Router, Auth, Filesystem, Git, Fetch, Sandbox
- **集成节点** (Node_10-Node_25): Slack, GitHub, Postgres, SQLite, FFmpeg, OCR, Email, EdgeTTS, DeepL, Crypto, Qdrant, Notion, BraveSearch, Calendar, Time, Weather, GoogleSearch
- **硬件节点** (Node_33-Node_49): ADB, Scrcpy, AppleScript, UIAWindows, LinuxDBus, BLE, SSH, SFTP, MQTT, CANbus, MAVLink, NFC, DesktopAuto, Camera, Audio, MediaGen, Serial, OctoPrint
- **AI 节点** (Node_50-Node_59): Transformer, QuantumDispatcher, QiskitSimulator, GraphLogic, SymbolicMath, AgentSwarm, Planning, QuantumCloud, ModelRouter, CausalInference
- **推理节点** (Node_61-Node_62): GeometricReasoning, ProbabilisticProgramming
- **系统节点** (Node_64-Node_69): Telemetry, LoggerCentral, ConfigManager, HealthMonitor, Security, BackupRestore
- **应用节点** (Node_70-Node_85): BambuLab, MediaGen, KnowledgeBase, Learning, DigitalTwin, LocalLLM, MemorySystem, Orchestrator, NetworkGuard, NewsAggregator, StockTracker, PromptLibrary
- **多模态节点** (Node_90-Node_97): MultimodalVision, MultimodalAgent, AutoControl, WebRTC_Receiver, SmartTransportRouter, AcademicSearch

### 高级节点 (Node_100-Node_107) - 8 个

来自 **ufo-galaxy** 主仓库：

- Node_100_MemorySystem
- Node_101_CodeEngine
- Node_102_DebugOptimize
- Node_103_KnowledgeGraph
- Node_104_AgentCPM
- Node_105_UnifiedKnowledgeBase
- Node_106_GitHubFlow
- Node_107 (预留)

### 增强节点 (Node_108-Node_118) - 7 个

来自 **ufo-galaxy-enhanced-nodes** 和 **ufo-galaxy-main**：

- **Node_108_MetaCognition** (来自 enhanced-nodes)
  - 元认知引擎，提供系统自我反思和优化能力
  
- **Node_109_ProactiveSensing** (来自 enhanced-nodes)
  - 主动感知引擎，提供环境监测和预测能力
  
- **Node_110_SmartOrchestrator** (来自 ufo-galaxy)
  - 智能编排器
  
- **Node_111_ContextManager** (来自 ufo-galaxy)
  - 上下文管理器
  
- **Node_112_SelfHealing** (来自 main)
  - 自我修复系统
  
- **Node_113_AndroidVLM** (来自 main)
  - Android 视觉语言模型
  
- **Node_116_ExternalToolWrapper** (来自 enhanced-nodes，原 node_113)
  - 外部工具包装器，提供统一的工具调用接口
  
- **Node_117_OpenCode** (来自 enhanced-nodes，原 node_114)
  - 开放代码生成引擎
  
- **Node_118_NodeFactory** (来自 enhanced-nodes，原 node_115)
  - 节点工厂，支持动态创建节点

---

## 📁 目录结构

```
ufo-galaxy-unified/
├── README.md                          # 本文件
├── README_original.md                 # 原始 README (备份)
├── MERGE_VERIFICATION_REPORT.md       # 合并验证报告
├── LICENSE                            # MIT License
├── .gitignore                         # Git 忽略文件
├── requirements_full.txt              # 完整依赖列表
├── 
├── docs/                              # 文档目录
│   ├── from_main/                     # 来自 ufo-galaxy-main 的文档
│   └── from_enhanced/                 # 来自 ufo-galaxy-enhanced-nodes 的文档
│
├── nodes/                             # 所有 103 个节点
│   ├── Node_00_StateMachine/
│   ├── ...
│   ├── Node_108_MetaCognition/
│   ├── Node_109_ProactiveSensing/
│   ├── Node_116_ExternalToolWrapper/
│   ├── Node_117_OpenCode/
│   └── Node_118_NodeFactory/
│
├── config/                            # 配置文件
│   ├── from_main/                     # 来自 ufo-galaxy-main 的配置
│   └── from_enhanced/                 # 来自 ufo-galaxy-enhanced-nodes 的配置
│
├── tests/                             # 测试文件
│   └── from_enhanced/                 # 来自 ufo-galaxy-enhanced-nodes 的测试
│
├── enhancements/                      # 增强功能
├── galaxy_gateway/                    # Galaxy 网关
├── dashboard/                         # 仪表板
└── scripts/                           # 脚本
    └── INSTALL_AND_START.bat          # 一键启动脚本
```

---

## 🚀 傻瓜式一键启动指南

**在开始之前，请确保您已在所有设备上安装并登录了 [Tailscale](https://tailscale.com/download)。**

### 1. 拉取最新代码

在您的 Windows PC 上打开 PowerShell，执行：

```powershell
# 切换到 E 盘
cd E:\

# 克隆仓库
git clone https://github.com/DannyFish-11/ufo-galaxy-unified.git

# 进入目录
cd ufo-galaxy-unified
```

### 2. 配置环境变量

1.  复制 `.env.example` 为 `.env`。
2.  打开 `.env` 文件，填入您的所有 API Keys。

### 3. 启动系统

1.  右键点击 `INSTALL_AND_START.bat` 文件。
2.  选择 **"以管理员身份运行"**。

脚本会自动完成所有操作。现在，您可以按 **`F12`** 键呼出侧边栏，开始发号施令了！

---

## 📚 详细文档

- **节点功能清单**: [FINAL_NODE_STATUS.md](FINAL_NODE_STATUS.md)
- **合并验证报告**: [MERGE_VERIFICATION_REPORT.md](MERGE_VERIFICATION_REPORT.md)
- **原始 README**: [README_original.md](README_original.md)
- **来自 main 的文档**: [docs/from_main/](docs/from_main/)
- **来自 enhanced 的文档**: [docs/from_enhanced/](docs/from_enhanced/)
- **部署指南**: [COMPLETE_SYSTEM_DEPLOYMENT_GUIDE.md](COMPLETE_SYSTEM_DEPLOYMENT_GUIDE.md)
- **API 配置**: [API_CONFIGURATION_GUIDE.md](API_CONFIGURATION_GUIDE.md)

---

## 🎉 版本历史

### v5.0 Unified (2026-01-24)

**三仓库完整合并版本**

- ✅ 合并 ufo-galaxy, ufo-galaxy-main, ufo-galaxy-enhanced-nodes
- ✅ 统一管理 103 个节点
- ✅ 完整保留所有文件和文档
- ✅ 解决节点编号冲突
- ✅ 优化目录结构

### v4.2 (2026-01-24)

- 清理 galaxy_gateway 依赖
- 静态代码检查通过
- 96 个节点稳定运行

### v4.1 (2026-01-22)

- 架构重构
- 视觉能力统一到 Node_90

---

## 📊 系统要求

- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.10+
- **内存**: 8GB+ 推荐
- **存储**: 10GB+ 可用空间
- **网络**: Tailscale VPN (用于跨设备通信)

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- 微软 UFO 项目团队
- 所有贡献者和支持者
- 开源社区

---

## 📞 联系方式

- **GitHub**: [@DannyFish-11](https://github.com/DannyFish-11)
- **Issues**: [GitHub Issues](https://github.com/DannyFish-11/ufo-galaxy-unified/issues)

---

**让 AI 真正拥有身体，让智能触手可及！** 🚀
