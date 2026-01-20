# UFO³ Galaxy - 分布式 AI 代理系统 🛸

**版本**: v4.0 (2026-01-21)  
**总节点数**: 79 个

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
