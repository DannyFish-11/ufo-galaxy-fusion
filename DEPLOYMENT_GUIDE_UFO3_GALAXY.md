# UFO³ Galaxy 部署指南 (华为 MateBook + 小米 14 + OPPO 平板)

**版本**: 1.0  
**日期**: 2026-01-22  
**作者**: Manus AI

---

## 1. 概述

本指南将引导您在以下设备上完整部署 UFO³ Galaxy 系统：

- **PC 端**: 华为 MateBook (Windows)
- **手机端**: 小米 14 (Android)
- **平板端**: OPPO 平板 (Android)

部署完成后，您将能够通过自然语言在 PC 上控制所有设备，并利用多模态 AI 能力进行跨设备协同。

## 2. 部署架构

| 设备 | 角色 | 运行的组件 |
|---|---|---|
| **华为 MateBook (PC)** | **主控端 (Master)** | - `galaxy_launcher.py` (所有核心节点)
- `Node_95_WebRTC_Receiver`
- `Node_34_Scrcpy`
- `Node_33_ADB`
- 量子计算节点 (51, 52, 57, 60)
- `SmartTransportRouter` (Node_96) |
| **小米 14 (手机)** | **被控端 (Agent)** | - UFO³ Galaxy Android 客户端 |
| **OPPO 平板** | **被控端 (Agent)** | - UFO³ Galaxy Android 客户端 |
| **所有设备** | **网络层** | - Tailscale VPN |

## 3. 环境准备

在开始之前，请确保在相应设备上安装好以下软件。

### 3.1. 华为 MateBook (PC - Windows)

1.  **Git**: 用于克隆代码仓库。
    - [https://git-scm.com/download/win](https://git-scm.com/download/win)

2.  **Python 3.11**: 项目的主要运行环境。
    - [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)
    - **重要**: 安装时请务必勾选 `Add Python to PATH`。

3.  **ADB (Android Debug Bridge)**: 用于控制安卓设备。
    - 包含在 Android Studio 的 Platform Tools 中。
    - 下载地址: [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)
    - 下载后，请将 `platform-tools` 目录的路径添加到系统的 `Path` 环境变量中。

4.  **Tailscale**: 用于构建跨设备的虚拟专用网络。
    - [https://tailscale.com/download/windows](https://tailscale.com/download/windows)
    - 安装后，使用您的 Google/Microsoft/GitHub 账号登录。

### 3.2. 小米 14 & OPPO 平板 (Android)

1.  **Tailscale**: 
    - 在 Google Play 或设备自带的应用商店中搜索 `Tailscale` 并安装。
    - 安装后，使用与 PC 端**相同的账号**登录。

2.  **开启开发者模式和 USB 调试**:
    - **小米 14**: 
        - `设置` -> `我的设备` -> `全部参数`
        - 连续点击 `MIUI 版本` 7 次，直到提示“您现在处于开发者模式”。
        - 返回 `设置` -> `更多设置` -> `开发者选项`
        - 开启 `开发者选项`、`USB 调试` 和 `USB 调试（安全设置）`。
    - **OPPO 平板**: 
        - `设置` -> `关于平板电脑` -> `版本信息`
        - 连续点击 `版本号` 7 次，直到提示“您正处于开发者模式”。
        - 返回 `设置` -> `其他设置` -> `开发者选项`
        - 开启 `开发者选项` 和 `USB 调试`。

## 4. PC 端部署 (华为 MateBook)

### 4.1. 克隆代码仓库

打开 `Git Bash` 或 `CMD`，执行以下命令：

```bash
git clone https://github.com/DannyFish-11/ufo-galaxy.git
cd ufo-galaxy
```

### 4.2. 安装 Python 依赖

在 `ufo-galaxy` 目录下，执行以下命令安装所有必需的 Python 包：

```bash
# 安装核心依赖
python -m pip install -r galaxy_gateway/requirements.txt

# 安装量子计算依赖 (可选，但建议安装)
sudo pip3 install qiskit qiskit-aer qiskit-ibm-runtime

# 安装其他节点依赖 (为了完整性)
for /d %%i in (nodes\*) do (
    if exist "%%i\requirements.txt" (
        pip install -r "%%i\requirements.txt"
    )
)
```

### 4.3. 配置环境变量

创建 `.env` 文件，用于存放环境变量。在 `ufo-galaxy` 根目录下创建一个名为 `.env` 的文件，并填入以下内容：

```env
# .env

# -- 网络配置 --
# 设置为 true 以启用 Tailscale
TAILSCALE_ENABLED=true

# -- 量子计算配置 (可选) --
# 如果您有 IBM Quantum 账号，可以填入 Token
# IBM_QUANTUM_TOKEN="your_ibm_quantum_token_here"

# -- AI API Keys (如果需要) --
# OPENAI_API_KEY="sk-..."
# DEEPSEEK_API_KEY="sk-..."

# -- 节点 URL (通常保持默认) --
NODE_95_URL=http://localhost:8095
NODE_34_URL=http://localhost:8034
NODE_33_URL=http://localhost:8033
NODE_41_URL=http://localhost:8041
```

### 4.4. 验证 Tailscale 连接

1.  确保 PC 和两台安卓设备都已安装并登录 Tailscale。
2.  在 PC 的命令行中，执行 `tailscale status`，您应该能看到您的三台设备都在列表中。
3.  记下您的 PC 在 Tailscale 网络中的 IP 地址（通常是 `100.x.x.x` 格式）。

## 5. 安卓端部署 (小米 14 & OPPO 平板)

### 5.1. 构建 APK 文件

在 PC 上，导航到安卓客户端的目录并使用 Gradle 构建 APK。

```bash
cd enhancements/clients/android_client

# Windows
.\gradlew.bat assembleDebug

# Linux/macOS
# ./gradlew assembleDebug
```

构建成功后，APK 文件会位于 `app/build/outputs/apk/debug/app-debug.apk`。

### 5.2. 安装 APK

将两台安卓设备通过 USB 连接到 PC，并确保已开启 USB 调试。

为每台设备执行以下命令：

```bash
# 检查设备是否连接
adb devices

# 安装 APK (将 <device_id> 替换为实际的设备 ID)
adb -s <device_id> install -r enhancements/clients/android_client/app/build/outputs/apk/debug/app-debug.apk
```

### 5.3. 配置安卓客户端

1.  在每台安卓设备上打开新安装的 `UFO³ Galaxy` 应用。
2.  进入设置界面。
3.  在 `Gateway IP` 或 `Master IP` 字段中，填入您在 **步骤 4.4** 中记下的 PC 的 **Tailscale IP 地址**。
4.  保存设置并重启应用。

## 6. 系统启动和验证

### 6.1. 启动 UFO³ Galaxy 系统

回到 PC 端，在 `ufo-galaxy` 根目录下，运行智能启动器 `galaxy_launcher.py`。

我们建议启动**核心 (core)** 和 **扩展 (extended)** 组的节点，以获得完整的功能体验。

```bash
python galaxy_launcher.py --include-groups core extended
```

启动器会自动启动所有必要的节点，包括：
- 核心服务 (StateMachine, Router, ...)
- 设备控制节点 (ADB, Scrcpy, WebRTC)
- 智能路由 (SmartTransportRouter)
- 量子计算节点 (如果依赖已安装)

### 6.2. 端到端测试

1.  **检查节点健康状态**: 
    - 打开浏览器，访问 `http://localhost:8000/dashboard` (如果 Dashboard 节点已启动)。
    - 或者通过 `galaxy_launcher.py` 的输出来确认所有节点都已成功启动。

2.  **测试跨设备截图**: 
    - 打开一个新的命令行窗口。
    - 使用 `curl` 或 Python 脚本向 Gateway 发送一个截图指令。

    **cURL 示例**:
    ```bash
    # 将 <your_phone_device_id> 替换为 adb devices 中显示的手机 ID
    curl -X POST http://localhost:8001/v1/control/screenshot \
      -H "Content-Type: application/json" \
      -d '{
        "device_id": "<your_phone_device_id>",
        "save_path": "C:/Users/YourUser/Desktop/test_screenshot.png"
      }'
    ```

3.  **验证结果**: 
    - 如果一切正常，您应该能在桌面上看到一张来自您小米 14 或 OPPO 平板的截图。
    - 这证明了从 PC 主控端到安卓被控端的完整通信链路（包括 Tailscale 网络、ADB 控制和 Gateway 服务）是通畅的。

## 7. 常见问题 (FAQ)

- **Q: 启动节点时报错 `Address already in use`?**
  A: 端口被占用了。请使用 `netstat -ano | findstr <port_number>` (Windows) 或 `lsof -i :<port_number>` (Linux) 找到占用端口的进程并结束它。

- **Q: `adb devices` 看不到我的设备?**
  A: 请检查 USB 连接是否稳固，USB 调试是否已开启，以及驱动程序是否正确安装。

- **Q: 安卓应用无法连接到 PC?**
  A: 请确认：
    1. PC 和安卓设备在同一个 Tailscale 网络中。
    2. 安卓应用中填写的 IP 地址是 PC 的 Tailscale IP。
    3. PC 的防火墙没有阻止来自 Tailscale 网络的连接。

- **Q: 量子计算节点启动失败?**
  A: 请确保 `qiskit` 相关的库已正确安装 (`pip install qiskit qiskit-aer qiskit-ibm-runtime`)。

---

部署完成！现在您可以开始探索 UFO³ Galaxy 的强大功能了。
