# UFO³ Galaxy 安卓端打包与配置指南

**版本**: 1.1  
**日期**: 2026-01-22  
**作者**: Manus AI

---

## 1. 概述

是的，您需要为您的安卓设备（小米 14 和 OPPO 平板）打包并安装 APK 客户端。项目中没有提供预编译的 APK，因为每个 APK 都需要**预先配置**您的 PC 主控端的 IP 地址才能正常工作。

本指南将为您提供两种打包方法，并详细说明如何配置和安装。

## 2. 准备工作

在开始之前，请确保您已完成 PC 端的环境准备：

- ✅ **Java Development Kit (JDK)**: 安卓构建需要 JDK 11 或更高版本。
- ✅ **Android SDK**: 确保已安装 Android SDK 和 `platform-tools` (ADB)。
- ✅ **Tailscale**: 确保 PC 端已安装并登录 Tailscale。

## 3. 打包 APK：两种方法

### 方法 A：使用自动化脚本（推荐）

这是最简单、最推荐的方法。我们提供了一个脚本，可以自动完成 IP 配置、打包和重命名。

#### 步骤：

1.  **获取 PC 的 Tailscale IP**
    在您的华为 MateBook 上打开命令行，运行：
    ```bash
    tailscale status
    ```
    记下您的 PC 的 IP 地址（例如 `100.111.222.333`）。

2.  **运行打包脚本**
    在 `ufo-galaxy` 项目的根目录下，进入安卓客户端目录：
    ```bash
    cd enhancements/clients/android_client
    ```
    运行脚本：
    ```bash
    ./build_configured_apk.sh
    ```

3.  **输入配置信息**
    脚本会提示您输入：
    - **PC 的 Tailscale IP 地址**: 输入您刚刚记下的 IP。
    - **设备 ID**: 为您的设备起一个名字，例如 `xiaomi-14` 或 `oppo-tablet`。这有助于在系统中区分它们。

4.  **等待构建完成**
    脚本会自动修改配置文件、清理旧的构建并打包新的 APK。首次构建可能需要 5-10 分钟。

5.  **获取 APK 文件**
    构建成功后，您会在 `enhancements/clients/android_client` 目录下找到一个以设备 ID 命名的 APK 文件，例如：
    - `UFO3_Galaxy_xiaomi-14_20260122.apk`

**为另一台设备打包**: 
重复步骤 2-5，为您的 OPPO 平板创建另一个 APK，只需在第 3 步输入不同的设备 ID（例如 `oppo-tablet`）。

---

### 方法 B：手动打包（使用 Android Studio）

如果您安装了 Android Studio，也可以手动打包。

#### 步骤：

1.  **打开项目**
    - 启动 Android Studio。
    - 选择 `File` -> `Open`，然后导航到 `ufo-galaxy/enhancements/clients/android_client` 目录并打开。

2.  **修改服务器 IP**
    - 在 Android Studio 的项目视图中，找到并打开以下文件：
      `app/src/main/java/com/ufo/galaxy/client/AIPClient.kt`
    - 找到 `NODE50_URL` 这一行。
    - 将 IP 地址和设备 ID 修改为您的配置：
      ```kotlin
      // 将 100.x.x.x 替换为您的 PC 的 Tailscale IP
      // 将 your-device-id 替换为您为设备设定的唯一 ID
      private val NODE50_URL = "ws://100.x.x.x:8050/ws/ufo3/your-device-id"
      ```
      例如，对于小米 14，您可以这样设置：
      ```kotlin
      private val NODE50_URL = "ws://100.111.222.333:8050/ws/ufo3/xiaomi-14"
      ```

3.  **构建 APK**
    - 在 Android Studio 的菜单栏中，选择 `Build` -> `Build Bundle(s) / APK(s)` -> `Build APK(s)`。
    - 等待构建完成。

4.  **定位 APK**
    - 构建成功后，Android Studio 右下角会弹出通知。
    - 点击通知中的 `locate` 链接，即可在文件浏览器中找到 `app-debug.apk` 文件。

## 4. 安装与配置

### 4.1. 安装 APK

1.  将打包好的 APK 文件（例如 `UFO3_Galaxy_xiaomi-14_20260122.apk`）传输到您的安卓设备上。
2.  在安卓设备上，使用文件管理器找到并点击 APK 文件进行安装。
    - 如果系统提示“禁止安装来自未知来源的应用”，请在弹出的设置中允许安装。

### 4.2. 授予必要权限

为了让 UFO³ Galaxy 正常工作，您需要授予以下权限：

1.  **无障碍服务 (Accessibility Service)**
    - **这是最重要的权限**，用于识别屏幕上的元素和执行点击操作。
    - 打开 `设置` -> `无障碍` -> `已安装的应用`。
    - 找到 `UFO³ Galaxy` 并开启服务。

2.  **显示在其他应用上层 (Overlay)**
    - 用于显示控制悬浮窗。
    - 通常在首次启动应用时会提示授权。
    - 如果没有，请到 `设置` -> `应用管理` -> `UFO³ Galaxy` -> `权限管理` 中手动开启。

3.  **屏幕录制**
    - 用于 WebRTC 和 Scrcpy 传输屏幕内容。
    - 当 PC 端请求屏幕数据时，系统会弹出授权提示，请选择“允许”。

## 5. 验证连接

1.  确保您的 PC 端 UFO³ Galaxy 系统正在运行 (`python galaxy_launcher.py --include-groups core extended`)。
2.  确保您的安卓设备和 PC 都已连接到 Tailscale。
3.  打开您在安卓设备上安装的 `UFO³ Galaxy` 应用。
4.  如果配置正确，应用界面上会显示“已连接到网关”或类似的成功状态。

## 6. 故障排查

- **Q: 构建失败，提示 `SDK location not found`?**
  A: 请在 `enhancements/clients/android_client` 目录下创建一个名为 `local.properties` 的文件，并填入您的 Android SDK 路径，例如：
  `sdk.dir=C:\Users\YourUser\AppData\Local\Android\Sdk`

- **Q: 应用安装后闪退？**
  A: 最大的可能是权限问题。请务必检查**无障碍服务**和**显示在其他应用上层**权限是否都已开启。

- **Q: 应用显示“连接失败”？**
  A: 请检查：
    1. PC 的 Tailscale IP 是否填写正确。
    2. PC 和安卓设备是否在同一个 Tailscale 网络中。
    3. PC 端的防火墙是否允许 `galaxy_launcher.py` 的网络连接。
    4. PC 端的 UFO³ Galaxy 系统是否已启动。

---

**总结**: 推荐使用**方法 A（自动化脚本）** 来为您的每台设备生成专属的 APK，这样最简单且不易出错。安装后，关键是授予**无障碍服务**权限。
