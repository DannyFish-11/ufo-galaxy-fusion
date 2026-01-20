# UFO³ Galaxy 完整部署指南

欢迎来到 UFO³ Galaxy 的世界！本指南将一步一步教您如何部署和使用这个强大的多设备智能体系统。

---

## 目录

1. **准备工作**
2. **获取代码**
3. **Windows 端部署**
4. **Android 端部署**
5. **测试与使用**

---

## 第 1 步：准备工作

在开始之前，请确保您的 Windows 电脑上已安装以下软件。

### 1.1 Git

Git 是一个版本控制系统，用于从 GitHub 下载项目代码。

- **下载地址**：[https://git-scm.com/download/win](https://git-scm.com/download/win)
- **安装选项**：在安装过程中，请使用默认选项。

### 1.2 Python

Python 是我们系统的主要编程语言。

- **下载地址**：[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
- **推荐版本**：Python 3.10 或更高版本
- **安装选项**：在安装时，请务必勾选 **"Add Python to PATH"** 选项。

### 1.3 Podman Desktop

Podman Desktop 用于管理我们系统的后端服务容器。

- **下载地址**：[https://podman-desktop.io/downloads](https://podman-desktop.io/downloads)
- **安装选项**：下载并运行安装程序，按照默认选项安装。

### 1.4 Android Studio (可选)

如果您想自行修改和构建 Android 客户端，则需要安装 Android Studio。

- **下载地址**：[https://developer.android.com/studio](https://developer.android.com/studio)
- **安装选项**：按照默认选项安装即可。

---

## 第 2 步：获取代码

现在，让我们从您的 GitHub 仓库获取所有项目代码。

### 2.1 打开命令行工具

在 Windows 上，您可以使用 **PowerShell** 或 **Git Bash**。

- **PowerShell**：在开始菜单中搜索 "PowerShell" 并打开。
- **Git Bash**：在开始菜单中搜索 "Git Bash" 并打开。

### 2.2 选择一个工作目录

选择一个您想存放项目的位置，例如 `E:\projects`。

```powershell
# 切换到 E 盘
E:

# 创建一个项目目录（如果不存在）
mkdir projects

# 进入项目目录
cd projects
```

### 2.3 克隆项目

运行以下命令，将您的 UFO³ Galaxy 项目从 GitHub 克隆到本地。

```powershell
git clone https://github.com/DannyFish-11/ufo-galaxy.git
```

### 2.4 进入项目目录

克隆完成后，进入项目目录。

```powershell
cd ufo-galaxy
```

**恭喜！** 您已经完成了所有的准备工作。接下来，我们将开始部署 Windows 端的后端服务和客户端。


---

## 第 3 步：Windows 端部署

现在，我们将在您的 Windows 电脑上部署后端服务和客户端。

### 3.1 启动 Podman Desktop

- 打开您刚刚安装的 Podman Desktop。
- 第一次启动时，它会自动初始化。请耐心等待几分钟。

### 3.2 启动后端服务

在您的 PowerShell 或 Git Bash 中，确保您仍然在 `ufo-galaxy` 项目目录下，然后运行以下命令：

```powershell
# 启动所有后端服务容器
podman-compose up -d
```

这个命令会：
- 自动下载所有必需的镜像
- 构建所有节点容器
- 在后台启动所有服务

您可以在 Podman Desktop 的 **Containers** 标签页中看到所有正在运行的容器。

### 3.3 配置第三方服务

如果您想使用 3D 打印、视频生成等高级功能，需要配置 API Key 和设备信息。

1. **复制配置文件**
   ```powershell
   copy config\services_config.example.json config\services_config.json
   ```

2. **编辑配置文件**
   - 使用记事本或任何文本编辑器打开 `config\services_config.json`。
   - 填入您的 API Key 和设备信息。

3. **重启服务**
   ```powershell
   podman-compose restart
   ```

### 3.4 启动 Windows 客户端

现在，让我们启动极简极客风格的侧边栏客户端。

1. **进入客户端目录**
   ```powershell
   cd enhancements\clients\windows_client
   ```

2. **安装依赖**
   ```powershell
   pip install -r requirements.txt
   ```

3. **运行客户端**
   ```powershell
   python client_ui_minimalist.py
   ```

4. **唤起侧边栏**
   - 按下 **F12** 键，您会看到一个黑白渐变的侧边栏从屏幕右侧滑出。
   - 再次按下 F12 键可以隐藏它。

**恭喜！** 您的 Windows 端已经部署完成！接下来，我们将部署 Android 客户端。


---

## 第 4 步：Android 端部署

现在，我们将在您的 Android 手机上部署悬浮窗客户端。

### 4.1 查找您电脑的 IP 地址

Android 客户端需要连接到您电脑上运行的后端服务，所以需要知道您电脑的 IP 地址。

1. 在您的 Windows 电脑上，打开 PowerShell。
2. 运行以下命令：
   ```powershell
   ipconfig
   ```
3. 找到您的 **IPv4 地址**，通常是 `192.168.x.x` 的形式。请记下这个地址。

### 4.2 构建预配置的 APK

我们提供了一个脚本，可以自动将您的 IP 地址配置到 APK 中。

1. **进入 Android 客户端目录**
   在您的 PowerShell 或 Git Bash 中，回到 `ufo-galaxy` 的根目录，然后进入 Android 客户端目录。
   ```powershell
   cd ..\..\enhancements\clients\android_client
   ```

2. **运行构建脚本**
   ```powershell
   bash build_configured_apk.sh
   ```

3. **输入 IP 地址**
   脚本会提示您输入电脑的 IP 地址。请输入您刚刚记下的 IPv4 地址，然后按 Enter。

4. **等待构建完成**
   脚本会自动构建 APK。完成后，您会在以下路径找到它：
   `app/build/outputs/apk/debug/app-debug.apk`

### 4.3 安装 APK 到手机

1. **连接手机**
   使用 USB 数据线将您的 Android 手机连接到电脑。

2. **开启 USB 调试**
   在手机的“开发者选项”中，开启“USB 调试”功能。

3. **安装 APK**
   在您的 PowerShell 或 Git Bash 中，运行以下命令：
   ```powershell
   adb install app/build/outputs/apk/debug/app-debug.apk
   ```

### 4.4 授予权限

1. **悬浮窗权限**
   - 在手机的“设置”中，找到“应用管理”，然后找到“UFO³ Galaxy”。
   - 授予“悬浮窗”或“在其他应用上层显示”的权限。

2. **无障碍服务权限**
   - 在手机的“设置”中，找到“无障碍”或“辅助功能”。
   - 找到“UFO³ Galaxy”并开启服务。

### 4.5 启动应用

- 在手机上打开“UFO³ Galaxy”应用。
- 您会看到一个黑白渐变的悬浮窗出现在屏幕上。

**恭喜！** 您的 Android 端也部署完成了！接下来，让我们测试一下整个系统。


---

## 第 5 步：测试与使用

现在，让我们来测试一下整个系统的连通性和核心功能。

### 5.1 检查连接状态

- **Windows 侧边栏**：按下 F12 唤起侧边栏，底部的状态栏应该显示 **“● CONNECTED”**（绿色）。
- **Android 悬浮窗**：底部的状态栏应该显示 **“READY”**。

如果状态不正确，请检查您的网络连接和 IP 地址配置。

### 5.2 发送第一条命令

让我们从一个简单的命令开始。

- 在 **Android 悬浮窗** 的输入框中，输入：
  ```
  在我的 Windows 电脑上打开记事本，然后输入“你好，UFO³ Galaxy！”
  ```
- 点击发送按钮。

您应该会看到：
1. 您的 Windows 电脑自动打开了记事本。
2. 记事本中自动输入了“你好，UFO³ Galaxy！”
3. Windows 侧边栏和 Android 悬浮窗的消息历史中都显示了任务的执行过程。

### 5.3 测试跨设备协同

现在，让我们测试一个更复杂的跨设备任务。

- 在 **Windows 侧边栏** 的输入框中，输入：
  ```
  让我的手机打开摄像头拍照，然后把照片发送到我的电脑桌面
  ```
- 按下 Enter 发送。

您应该会看到：
1. 您的 Android 手机自动打开了摄像头应用。
2. 拍摄一张照片。
3. 照片自动发送到您 Windows 电脑的桌面上。

### 5.4 探索更多功能

现在，您可以自由探索 UFO³ Galaxy 的所有强大功能了！

**试试这些命令：**
- “生成一个猫在弹钢琴的视频”
- “让 3D 打印机打印一个测试模型”
- “无人机起飞，悬停 10 秒”
- “我的知识库里有哪些关于 AI 的知识？”
- “在 51World 中模拟一次无人机飞行任务”

---

## 常见问题

### 1. 连接失败怎么办？
- 检查您电脑和手机是否在同一个 Wi-Fi 网络下。
- 检查您在构建 APK 时输入的 IP 地址是否正确。
- 检查防火墙设置，确保允许 Podman 和 Python 通过。

### 2. F12 键没反应？
- 确保 `client_ui_minimalist.py` 脚本正在运行。
- 尝试以管理员身份运行脚本。

### 3. 悬浮窗不显示？
- 检查是否已授予悬浮窗权限。

---

**恭喜您！** 您已经成功部署并掌握了 UFO³ Galaxy 系统。现在，开始您的极客松之旅吧！🚀
