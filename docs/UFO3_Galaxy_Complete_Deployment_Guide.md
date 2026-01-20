# UFO³ Galaxy - 完整部署指南

**版本**: 1.0 (UI & 核心功能增强版)
**作者**: Manus AI

---

## 1. 系统概述

UFO³ Galaxy 是一个为极客松竞赛设计的分布式 AI 代理系统。它通过自然语言命令，协同多个异构设备（Windows PC、Android 设备、云服务器）完成复杂任务，例如 3D 打印、AI 视频生成、桌面自动化和量子计算。

### 1.1. 核心组件

| 节点/客户端 | 设备/平台 | 功能 |
| :--- | :--- | :--- |
| **Node 50 (大脑)** | Windows (Podman 容器) | 核心 NLU 引擎，负责任务理解与分发 |
| **Node 43 (工匠)** | Windows (Podman 容器) | 控制 Bambu Lab 3D 打印机 |
| **Node 48 (艺术家)** | Windows (Podman 容器) | 调用 PixVerse API 生成 AI 视频 |
| **Node 60 (学者)** | 华为云服务器 | 执行异构计算（量子计算、AI 推理） |
| **Windows 客户端** | Windows 桌面 | 提供 UI 侧边面板，用于命令输入和桌面自动化 |
| **Android 客户端** | Android 手机/平板 | 提供悬浮窗，用于语音/文本命令输入 |

### 1.2. 技术架构

- **网络**: 所有设备通过 **Tailscale** 组成一个安全的虚拟私有网络。
- **通信**: 节点间使用基于 WebSocket 的 **AIP/1.0** 协议进行通信。
- **容器化**: 核心后端节点在 Windows PC 上通过 **Podman Desktop** 进行容器化管理。
- **AI 能力**: 通过 **OneAPI** 统一管理和调用多种大语言模型（DeepSeek, Gemini, GPT-4 等）。

---

## 2. 环境准备

在开始部署前，请确保您已安装并配置好以下软件。

### 2.1. 必备软件

| 软件 | 平台 | 用途 | 安装说明 |
| :--- | :--- | :--- | :--- |
| **Tailscale** | 所有设备 | 组建虚拟局域网 | [tailscale.com](https://tailscale.com/download) |
| **Podman Desktop** | Windows PC | 运行后端容器节点 | [podman-desktop.io](https://podman-desktop.io/downloads) |
| **Python 3.10+** | Windows PC, 华为云 | 运行客户端和节点 | [python.org](https://www.python.org/downloads/) |
| **Android Studio** | Windows PC | 编译 Android 客户端 | [developer.android.com](https://developer.android.com/studio) |
| **Git** | Windows PC | 克隆项目代码 | [git-scm.com](https://git-scm.com/downloads) |

### 2.2. API 密钥配置

您需要准备以下 API 密钥，并将其配置为环境变量或直接写入代码中。

| 服务 | 环境变量 | 用途 | 获取地址 |
| :--- | :--- | :--- | :--- |
| **OneAPI** | `ONEAPI_API_KEY` | 访问所有 LLM 模型 | 您自己的 OneAPI 实例 |
| **PixVerse** | `PIXVERSE_API_KEY` | 生成 AI 视频 | `sk-f5c7177f35ee6cceab5d97d6ffae26d0` (用户提供) |
| **IBM Quantum** | `IBM_QUANTUM_TOKEN` | 运行量子计算任务 | [quantum-computing.ibm.com](https://quantum-computing.ibm.com/) |

---

## 3. 部署步骤

请严格按照以下步骤进行部署。

### 步骤 1：网络配置 (所有设备)

1. 在您的 **所有设备**（Windows PC, Android 手机/平板, 华为云服务器）上安装并登录同一个 Tailscale 账号。
2. 确保所有设备都出现在 Tailscale 管理后台的设备列表中，并处于“已连接”状态。
3. 在 **Windows PC** 上打开命令行，执行 `tailscale ip -4`，记下显示的 `100.x.x.x` IP 地址。**这个 IP 将作为 Node 50 的地址，在所有其他节点的配置中都会用到。**

### 步骤 2：后端节点部署 (Windows PC)

1. **克隆项目**:
   ```powershell
   git clone <your-repo-url> F:\ufo-galaxy
   cd F:\ufo-galaxy\ufo-galaxy-podman
   ```

2. **配置环境变量**:
   - 打开 `podman-compose.yml` 文件。
   - 找到 `environment` 部分，填入您的 API 密钥和 Tailscale IP。

   ```yaml
   services:
     node_50:
       environment:
         - ONEAPI_API_KEY=sk-your-oneapi-key
         - ONEAPI_BASE_URL=http://<your-oneapi-ip>:3000/v1
     node_48:
       environment:
         - PIXVERSE_API_KEY=sk-f5c7177f35ee6cceab5d97d6ffae26d0
         - TAILSCALE_IP=<windows-pc-tailscale-ip> # 替换为步骤1中获取的IP
     # ... 其他节点
   ```

3. **启动容器**:
   - 打开 **Podman Desktop**。
   - 导航到 **Compose** 部分。
   - 点击 **"Play"** 按钮，选择 `podman-compose.yml` 文件，启动所有容器。
   - 检查日志，确保 Node 50, 43, 48 都已成功启动并显示 `Listening on port...`。

### 步骤 3：Windows 客户端部署

1. **安装依赖**:
   ```powershell
   cd F:\ufo-galaxy\windows_client
   pip install -r requirements.txt
   ```

2. **配置连接**:
   - 打开 `client.py` 文件。
   - 确认 `NODE50_URL` 指向 `localhost`，因为客户端和 Podman 在同一台机器上。
   ```python
   NODE50_URL = "ws://localhost:8050"
   ```

3. **启动客户端**:
   ```powershell
   python client.py
   ```
   - 终端会显示 `Press F12 to toggle the sidebar.`。
   - 按 `F12` 键即可唤醒或隐藏侧边面板。

### 步骤 4：Android 客户端部署

1. **打开项目**:
   - 在 Android Studio 中打开 `F:\ufo-galaxy\ufo-galaxy-android` 项目。

2. **配置连接**:
   - 打开 `app/src/main/java/com/ufo/galaxy/client/AIPClient.kt`。
   - 修改 `NODE50_URL`，将其中的 IP 地址替换为 **Windows PC 的 Tailscale IP**。
   ```kotlin
   private val NODE50_URL = "ws://100.123.215.126:8050/ws/ufo3/android-xiaomi-24030PN60C"
   ```

3. **编译并安装**:
   - 点击 **Build** -> **Build Bundle(s) / APK(s)** -> **Build APK(s)**。
   - 将生成的 APK 文件传输到您的 Android 设备并安装。

4. **授予权限**:
   - 首次打开应用时，系统会提示您授予“**显示在其他应用上层**”（即悬浮窗）的权限。请务必允许。
   - 如果需要，同时授予“**麦克风**”权限用于语音输入。

### 步骤 5：云节点部署 (华为云服务器)

1. **上传代码**:
   - 将 `F:\ufo-galaxy\node_60_cloud` 目录上传到您的华为云服务器的 `/home/ubuntu/` 目录下。

2. **安装依赖**:
   ```bash
   cd /home/ubuntu/node_60_cloud
   pip install -r requirements.txt
   # 安装量子计算库
   pip install qiskit qiskit-ibm-runtime
   ```

3. **配置环境变量**:
   ```bash
   export TAILSCALE_IP="<windows-pc-tailscale-ip>"  # 替换为 Windows PC 的 Tailscale IP
   export IBM_QUANTUM_TOKEN="<your-ibm-quantum-token>"
   ```

4. **启动节点**:
   ```bash
   python main.py
   ```
   - 终端会显示 `Connecting to Node 50 at ws://...`。

---

## 4. 使用指南

- **Windows**: 按 `F12` 唤醒侧边栏，在输入框中输入命令，按回车发送。
- **Android**: 点击屏幕上的悬浮麦克风图标，说出您的命令。

**示例命令**:
- `"打印一个警告标志"`
- `"生成一个关于宇宙探索的视频"`
- `"使用量子算法优化从北京到上海的路线"`
- `"打开浏览器搜索最新的 AI 新闻"`

---

## 5. 故障排除

- **无法连接到 Node 50**:
  - **检查 Tailscale**: 在所有设备上运行 `tailscale status`，确保它们都在线且 IP 正确。
  - **检查防火墙**: 确保 Windows 防火墙允许 Podman 和 Python 应用的入站连接。
  - **检查 Podman**: 在 Podman Desktop 中查看 Node 50 的日志，确认它正在监听 `0.0.0.0:8050`。

- **Android 悬浮窗不显示**:
  - 确保已在系统“设置”中为“UFO³ Galaxy Agent”应用授予了悬浮窗权限。

- **命令没有反应**:
  - **检查 Node 50 日志**: 查看 Node 50 容器的日志，确认它是否收到了命令，以及 NLU 引擎的解析结果是否正确。
  - **检查目标节点日志**: 如果任务已分发，请检查相应节点（如 Node 43, 48）的日志，看是否有错误信息。

- **API Key 错误**:
  - 检查 `podman-compose.yml` 和 `node_60_cloud` 的环境变量，确保 API 密钥填写正确且未过期。
