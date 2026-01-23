# UFO³ Galaxy - 从零开始部署指南

**版本**: 2.0.0  
**日期**: 2026-01-23  
**作者**: Manus AI

---

## 概述

本指南将引导您在一台**全新的 Windows 10/11** 计算机上，从零开始完整部署 UFO³ Galaxy 系统。

---

## 1. 前置环境准备

在开始之前，您需要安装以下核心软件。所有软件都推荐使用默认设置进行安装。

### 1.1 Git (必需)

**用途**: 用于从 GitHub 下载和更新 UFO³ Galaxy 的代码。

| 步骤 | 操作 | 验证 |
|:----|:-----|:-----|
| **1** | **下载**: 访问 [git-scm.com/download/win](https://git-scm.com/download/win) 下载适用于 Windows 的最新版本。 | - |
| **2** | **安装**: 运行下载的安装程序，使用默认选项完成安装。 | - |
| **3** | **验证**: 打开**命令提示符 (CMD)** 或 **PowerShell**，输入以下命令： | `git version x.x.x` |
| | `git --version` | |

### 1.2 Python 3.11+ (必需)

**用途**: UFO³ Galaxy 系统的核心运行环境。

| 步骤 | 操作 | 验证 |
|:----|:-----|:-----|
| **1** | **下载**: 访问 [python.org/downloads](https://www.python.org/downloads/) 下载 Python 3.11 或更高版本。 | - |
| **2** | **安装**: 运行安装程序。**关键：请务必勾选 `Add Python to PATH`** 选项，然后选择 `Install Now`。 | - |
| **3** | **验证**: 重新打开**命令提示符**，输入以下两个命令： | `Python 3.11.x` <br> `pip x.x.x` |
| | `python --version` <br> `pip --version` | |

### 1.3 Tailscale (强烈推荐)

**用途**: 用于实现 PC 与手机/平板之间的跨设备安全通信。

| 步骤 | 操作 | 验证 |
|:----|:-----|:-----|
| **1** | **下载**: 访问 [tailscale.com/download](https://tailscale.com/download) 下载适用于 Windows 的版本。 | - |
| **2** | **安装与登录**: 安装后，按照提示使用您的 Google/Microsoft/GitHub 账户登录。 | - |
| **3** | **验证**: 在**命令提示符**中输入： | `100.x.x.x` |
| | `tailscale ip -4` | |

### 1.4 Android Debug Bridge (ADB) (可选)

**用途**: 用于在 PC 上控制您的安卓设备（小米 14、OPPO 平板）。

| 步骤 | 操作 | 验证 |
|:----|:-----|:-----|
| **1** | **下载**: 访问 [developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools) 下载 "SDK Platform-Tools for Windows"。 | - |
| **2** | **解压**: 将下载的 `platform-tools` 压缩包解压到一个固定的位置，例如 `C:\platform-tools`。 | - |
| **3** | **配置环境变量**: 将 `C:\platform-tools` 添加到系统的 `Path` 环境变量中。 | - |
| **4** | **验证**: 重新打开**命令提示符**，输入： | `Android Debug Bridge version x.x.x` |
| | `adb --version` | |

---

## 2. 系统部署

完成所有前置环境准备后，您可以开始部署 UFO³ Galaxy 系统。

### 2.1 下载代码

打开**命令提示符**，执行以下命令将代码下载到您的电脑：

```bash
# 切换到你希望存放项目的目录，例如 C 盘根目录
cd C:\

# 从 GitHub 下载代码
git clone https://github.com/DannyFish-11/ufo-galaxy.git

# 进入项目目录
cd ufo-galaxy
```

### 2.2 一键部署

在 `ufo-galaxy` 目录中，找到并双击运行 `deploy.bat` 脚本。

```bash
# 在文件浏览器中双击运行
deploy.bat
```

此脚本会自动：
- 检查您的环境是否完整。
- 安装运行系统所需的核心 Python 包。
- 提示您下一步操作。

### 2.3 启动系统

部署完成后，双击运行 `start_system.bat` 脚本。

```bash
# 在文件浏览器中双击运行
start_system.bat
```

脚本会提供一个菜单，让您选择启动模式：

| 选项 | 描述 | 推荐场景 |
|:----|:-----|:---------|
| **1** | **核心系统** | 仅运行最基础的功能。 |
| **2** | **学术研究系统** | 运行学术搜索、报告生成等功能。 |
| **3** | **开发工作流系统** | 运行 GitHub 自动化、代码生成等功能。 |
| **4** | **完整系统** | 启动所有 18 个核心节点，功能最全。 | **首次使用推荐** |

首次使用，建议选择 **选项 4** 启动完整系统。

---

## 3. 验证部署

系统启动后，您可以验证部署是否成功。

### 3.1 启动健康监控

在 `ufo-galaxy` 目录中，找到并运行 `health_monitor.py`。

```bash
# 在命令提示符中运行
python health_monitor.py
```

### 3.2 访问 Web 仪表板

打开您的浏览器（Chrome, Edge, Firefox），访问以下地址：

**http://localhost:9000**

如果您能看到一个标题为 `🛸 UFO³ Galaxy Health Monitor` 的动态仪表板，并且大部分节点状态显示为 `✅ 健康`，那么恭喜您，系统已成功部署！

---

## 4. 下一步

- **安卓端配置**: 请参考 `ANDROID_QUICK_INSTALL.md` 为您的小米 14 和 OPPO 平板打包并安装客户端。
- **功能探索**: 请参考 `FIRST_USE_GUIDE.md` 探索系统的各项强大功能。

---

**UFO³ Galaxy** | 从零开始部署指南 | 2026-01-23
