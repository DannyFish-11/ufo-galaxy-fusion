# UFO³ Galaxy - 傻瓜式一键启动指南

**版本**: 1.1 (一键安装版)

---

## 简介

本指南将帮助您在 3 个步骤内启动整个 UFO³ Galaxy 系统。无需任何复杂配置，只需点击几下即可。

**在开始之前，请确保您已在所有设备上安装并登录了 [Tailscale](https://tailscale.com/download)。**

---

## 步骤 1: 启动后端服务 (Windows PC)

1.  进入 `ufo-galaxy-podman` 目录。
2.  右键点击 `INSTALL_AND_START.bat` 文件。
3.  选择 **“以管理员身份运行”**。

脚本会自动完成以下所有操作：
- 检查您的环境（Python, Podman）
- 安装所有必要的依赖
- 启动所有后端节点容器（Node 50, 43, 48）

**完成后，请保持此窗口打开。**

---

## 步骤 2: 启动 Windows 客户端

1.  进入 `windows_client` 目录。
2.  双击 `START_CLIENT.bat` 文件。

客户端会自动连接到后端服务。现在您可以按 **`F12`** 键唤醒或隐藏侧边栏，并通过它发送命令。

---

## 步骤 3: 启动其他设备

### A. Android 客户端

1.  在 `ufo-galaxy-android` 目录中，运行 `build_configured_apk.sh` 脚本，根据提示输入您的 Windows PC 的 Tailscale IP 地址。
2.  脚本会自动生成一个预配置好的 APK 文件。
3.  将此 APK 文件传输到您的 Android 设备并安装。
4.  打开应用，并授予**悬浮窗**和**麦克风**权限。

### B. 华为云节点

1.  将 `node_60_cloud` 目录上传到您的华为云服务器。
2.  在服务器上运行 `DEPLOY_CLOUD.sh` 脚本。
3.  根据提示输入您的 Windows PC 的 Tailscale IP 地址。
4.  脚本会自动配置并启动云节点。

---

## 系统已启动！

现在，您的 UFO³ Galaxy 系统已完全启动并准备就绪。您可以开始通过 Windows 侧边栏或 Android 悬浮窗发送命令了。

**示例命令**:
- `"打印一个警告标志"`
- `"生成一个关于宇宙探索的视频"`
- `"打开浏览器搜索最新的 AI 新闻"`

### 系统测试

如果您想验证所有组件是否正常工作，可以运行 `ufo-galaxy-podman` 目录下的 `TEST_SYSTEM.py` 脚本。

```bash
cd ufo-galaxy-podman
python TEST_SYSTEM.py
```
