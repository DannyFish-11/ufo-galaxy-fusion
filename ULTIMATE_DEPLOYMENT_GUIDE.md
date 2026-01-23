# UFO³ Galaxy - 终极部署指南 (从零开始)

**版本**: 2.2.0  
**日期**: 2026-01-23  
**作者**: Manus AI

---

## 概述

本指南是您唯一需要的部署文档。它将引导您从**零**开始，完成 UFO³ Galaxy 系统的完整部署，包括 PC 端和安卓端。

**预计总时间**: 30-60 分钟

---

## 第 0 部分：前置环境准备 (15-20 分钟)

在开始之前，请确保您的 PC (华为 MateBook) 上安装了以下软件。

| 软件 | 状态 | 用途 | 下载地址 |
|:-----|:-----|:-----|:---------|
| **Git** | 必需 | 下载和更新代码 | [git-scm.com/download/win](https://git-scm.com/download/win) |
| **Python 3.11+** | 必需 | 运行环境 | [python.org/downloads](https://www.python.org/downloads/) |
| **Tailscale** | 强烈推荐 | 跨设备通信 | [tailscale.com/download](https://tailscale.com/download/) |
| **ADB** | 可选 | 安卓设备控制 | [developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools) |

### 详细安装步骤

1.  **安装 Git**
    - 下载并运行安装程序。
    - 在安装过程中，保持默认设置即可。
    - **验证**: 打开命令行，输入 `git --version`，看到版本号即表示成功。

2.  **安装 Python 3.11+**
    - 下载并运行安装程序。
    - **重要**: 在安装界面，务必勾选 **`Add Python to PATH`**。
    - **验证**: 打开命令行，输入 `python --version`，看到版本号即表示成功。

3.  **安装 Tailscale**
    - 下载并运行安装程序。
    - 安装后，使用您的 Google/Microsoft/GitHub 账户登录。
    - **验证**: 打开命令行，输入 `tailscale ip -4`，看到 `100.x.x.x` 格式的 IP 地址即表示成功。

4.  **安装 ADB**
    - 下载并解压 `platform-tools` 压缩包 (例如，解压到 `C:\platform-tools`)。
    - 将解压后的路径 (如 `C:\platform-tools`) 添加到系统的 `Path` 环境变量中。
    - **验证**: 打开命令行，输入 `adb version`，看到版本号即表示成功。

---

## 第 1 部分：PC 端部署 (10-15 分钟)

### 步骤 1: 克隆代码

打开命令行，进入您想要存放项目的目录，然后运行以下命令：

```bash
git clone https://github.com/DannyFish-11/ufo-galaxy.git
cd ufo-galaxy
```

### 步骤 2: 检查环境

运行增强版的环境检查脚本，确保所有软件都已正确安装和配置。

```bash
python check_prerequisites.py
```

**预期输出**: 所有检查项都显示为 `[✓]` 绿色。

### 步骤 3: 一键部署

运行一键部署脚本，自动安装所有必需的 Python 包。

```bash
deploy.bat
```

### 步骤 4: 启动完整系统

使用智能启动器启动所有节点。

```bash
python smart_launcher.py start all
```

### 步骤 5: 验证系统状态

保持上一个命令行窗口**不要关闭**，另外打开一个新的命令行窗口，进入 `ufo-galaxy` 目录，运行以下命令：

```bash
# 查看所有节点状态
python smart_launcher.py status

# 启动 Web 监控仪表板
python health_monitor.py
```

然后打开浏览器，访问 **http://localhost:9000**，您应该能看到所有节点都处于“运行中”状态。

---

## 第 2 部分：安卓端部署 (10-15 分钟)

### 步骤 1: 一键打包 APK

回到 PC 端的命令行窗口，按 `Ctrl+C` 停止系统，然后运行一键打包脚本。

```bash
build_android_apk.bat
```

脚本会引导您：
1.  确认 PC 的 Tailscale IP
2.  选择设备类型 (小米 14 / OPPO 平板)
3.  自动构建 APK

构建成功后，您会在 `ufo-galaxy` 目录下找到生成的 APK 文件 (例如 `UFO3_Galaxy_xiaomi-14_20260123.apk`)。

### 步骤 2: 安装和配置

1.  **传输 APK**: 将生成的 APK 文件传输到您的安卓设备。
2.  **安装 APK**: 在设备上安装 APK。
3.  **授予权限**: 打开应用，授予以下权限：
    - **无障碍服务权限** (必需)
    - **悬浮窗权限** (必需)
    - **存储权限** (可选)

---

## 第 3 部分：系统联调 (5 分钟)

1.  **重启 PC 端系统**: 在 PC 上再次运行 `python smart_launcher.py start all`。
2.  **确保网络连接**: 确保您的 PC 和安卓设备都已连接到 Tailscale 网络。
3.  **验证连接**: 
    - 在 PC 端的 `health_monitor.py` Web 仪表板上，您应该能看到安卓设备的连接状态。
    - 在安卓设备上，点击悬浮窗，尝试发送自然语言指令，例如“你好”。
    - 在 PC 端的命令行窗口中，您应该能看到来自安卓设备的消息。

---

## 第 4 部分：日常使用

| 场景 | 命令 |
|:-----|:-----|
| **启动系统** | `python smart_launcher.py start all` |
| **查看状态** | `python smart_launcher.py status` |
| **停止系统** | `python smart_launcher.py stop` |
| **打包 APK** | `build_android_apk.bat` |

---

## 恭喜！

您已成功部署 UFO³ Galaxy 系统！现在可以开始探索它的强大功能了。🚀
