# UFO³ Galaxy - 分布式 AI 代理系统 🛸

**版本**: v4.2 (2026-01-24)  
**总节点数**: 96 个（93 个基础节点 + 3 个增强节点）

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20Android-lightgrey.svg)](https://github.com/DannyFish-11/ufo-galaxy)

**让 AI 拥有身体** - 一个通过自然语言命令协调多设备完成复杂任务的分布式 AI 代理系统。

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

---

## 🏗️ 架构设计

UFO³ Galaxy 采用分布式、多层级的架构，由 79 个功能节点组成，通过 AIP/1.0 协议进行通信。

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        UFO Galaxy 79-Core Matrix                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐        │
│  │ Windows PC      │   │ Huawei Cloud    │   │ Android Device  │        │
│  │ (主控 + 79节点) │ ← │ (子 Agent)      │ ← │ (子 Agent)      │        │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 傻瓜式一键启动指南

**在开始之前，请确保您已在所有设备上安装并登录了 [Tailscale](https://tailscale.com/download)。**

### 1. 拉取最新代码

在您的 Windows PC 上打开 PowerShell，执行：

```powershell
# 切换到 E 盘
cd E:\

# 克隆仓库
git clone https://github.com/DannyFish-11/ufo-galaxy.git

# 进入目录
cd ufo-galaxy
```

### 2. 配置环境变量

1.  复制 `.env.example` 为 `.env`。
2.  打开 `.env` 文件，填入您的所有 API Keys。

### 3. 启动系统

1.  右键点击 `INSTALL_AND_START.bat` 文件。
2.  选择 **“以管理员身份运行”**。

脚本会自动完成所有操作。现在，您可以按 **`F12`** 键呼出侧边栏，开始发号施令了！

---

## 详细节点功能清单

请查看 [FINAL_NODE_STATUS.md](FINAL_NODE_STATUS.md) 获取完整的 79 个节点功能清单。

---

## 🎉 v4.1 架构重构 (2026-01-22)

### 视觉能力统一到 Node_90

为了符合项目的“节点化”设计原则，我们对视觉理解模块进行了全面重构：

1. **统一视觉节点**：所有视觉任务现由 `Node_90_MultimodalVision` 统一处理
2. **多 VLM 支持**：集成了 Qwen3-VL (via OpenRouter) 和 Gemini 两种 VLM Provider
3. **Gateway 简化**：`galaxy_gateway` 不再包含具体执行逻辑，只负责路由
4. **弃用文件**：`vlm_node.py`, `qwen_vl_api.py`, `vision_understanding.py` 已移至 `.deprecated/`

详细的架构分析请查看 [CODEBASE_AUDIT_REPORT.md](CODEBASE_AUDIT_REPORT.md)。

---

## 🎉 v2.0 重大更新 (2026-01-22)

### 新增核心功能

1. **Node 79: Local LLM** - 本地大模型推理
   - 支持 Qwen2.5, DeepSeek-Coder
   - 智能模型选择
   - 降低 90% API 成本

2. **Node 80: Memory System** - 四层记忆架构
   - 短期记忆（对话上下文）
   - 长期记忆（笔记文档）
   - 用户画像（偏好设置）

3. **Node 81: Orchestrator** - 统一任务编排
   - 简单/顺序/并行/条件任务
   - 智能任务分解
   - 工作流管理

4. **Node 82-85: 实时信息流**
   - 网络监控
   - 新闻聚合
   - 股票追踪
   - 提示词库

5. **Dashboard: Web 管理界面**
   - 系统概览
   - 节点管理
   - 日志查看
   - 任务管理

### 性能提升

- 启动时间：60s → 10s (-83%)
- 内存占用：4GB → 500MB (-87%)
- 智能化水平：⭐⭐⭐☆☆ → ⭐⭐⭐⭐⭐ (+40%)

### 快速开始

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull deepseek-coder:6.7b-instruct-q4_K_M

# 启动系统
python galaxy_launcher.py --mode core

# 启动 Dashboard
cd dashboard/backend && python main.py
```

访问 Dashboard: http://localhost:3000

详细文档：[OPTIMIZATION_COMPLETE_REPORT.md](OPTIMIZATION_COMPLETE_REPORT.md)
