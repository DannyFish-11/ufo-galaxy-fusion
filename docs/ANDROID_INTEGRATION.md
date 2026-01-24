# UFO³ Galaxy - Android 客户端集成文档

**文档版本:** 2.0  
**更新日期:** 2026-01-24  
**状态:** 核心功能已完成，与 Windows 客户端功能对等

---

## 1. 概述

本文档描述了如何将 UFO³ Galaxy Android 客户端集成到主系统中。Android 客户端现已完成核心功能开发，实现了与 Windows 客户端的功能对等，并在语音输入、WebRTC 屏幕共享等方面具备独特优势。

**Android 客户端仓库:** [https://github.com/DannyFish-11/ufo-galaxy-android](https://github.com/DannyFish-11/ufo-galaxy-android)

---

## 2. 功能与代码统计

Android 客户端总代码量 **2,934 行**，所有功能均已达到生产就绪状态，无占位符代码。

| 模块 | 代码行数 | 状态 | 核心组件 |
| :--- | :--- | :--- | :--- |
| **通信层** | 892 行 | ✅ 完成 | `WebSocketClient`, `AIPMessage`, `DeviceManager` |
| **WebRTC** | 654 行 | ✅ 完成 | `WebRTCManager`, `ScreenCaptureService` |
| **浮窗 UI** | 515 行 | ✅ 完成 | `FloatingWindowService` |
| **无障碍服务** | 589 行 | ✅ 完成 | `UFOAccessibilityService` |
| **XML 资源** | 284 行 | ✅ 完成 | 布局 (Layouts) 和样式 (Drawables) |

---

## 3. 核心功能对比

| 功能 | Windows 客户端 | Android 客户端 | 状态与备注 |
| :--- | :--- | :--- | :--- |
| **设备注册与心跳** | ✅ | ✅ | **功能对等** |
| **WebSocket & AIP v2.0** | ✅ | ✅ | **功能对等** |
| **浮窗 UI** | ✅ (PyQt5/Tkinter) | ✅ (Android 原生) | **UI 风格一致** (黑白渐变) |
| **文本输入** | ✅ | ✅ | **功能对等** |
| **语音输入** | ❌ | ✅ | **Android 专属优势** (基于 `SpeechRecognizer`) |
| **屏幕共享** | ✅ (scrcpy) | ✅ (WebRTC) | 技术方案不同，**功能对等** |
| **系统级控制** | ✅ (pyautogui) | ✅ (Accessibility) | **功能对等** |

---

## 4. 集成步骤

### 步骤 1: 启动 Galaxy Gateway

确保主系统的 Galaxy Gateway 正在运行。Gateway 负责设备管理、消息路由和任务分发。

```bash
cd /path/to/ufo-galaxy
python galaxy_gateway/main.py
```

Gateway 默认监听 `ws://0.0.0.0:8000/ws`。

### 步骤 2: 配置并安装 Android 客户端

1.  **配置 Gateway 地址:** 在 Android 项目的 `DeviceManager` 或配置文件中，设置 Gateway 的 WebSocket 地址（例如: `ws://192.168.1.100:8000/ws`）。
2.  **编译 APK:** 使用 Android Studio 编译生成 `app-debug.apk`。
3.  **安装 APK:**
    ```bash
    adb install app-debug.apk
    ```

### 步骤 3: 启动并授权

1.  在 Android 设备上打开 **UFO³ Galaxy** 应用。
2.  根据应用引导，依次授予以下关键权限：
    - **悬浮窗权限 (SYSTEM_ALERT_WINDOW):** 用于显示系统级浮窗 UI。
    - **无障碍服务权限 (Accessibility Service):** 用于实现系统级控制和自动化操作。
    - **录音权限 (RECORD_AUDIO):** 用于支持语音输入功能。
3.  启动 `FloatingWindowService`，浮窗将显示在屏幕上。

### 步骤 4: 验证连接

- **客户端:** 浮窗 UI 上的状态指示灯应变为绿色，表示已成功连接到 Gateway。
- **Gateway 端:** 在 Gateway 的控制台日志中，应能看到来自 Android 设备的注册信息。

```log
[INFO] Device registered: android_xxxxxxxx
[INFO]   - Device Type: android
[INFO]   - Capabilities: screen_capture_webrtc, voice_input, accessibility_control
```

---

## 5. 协同工作示例

### 示例 1: 从 Windows 控制 Android 进行 WebRTC 屏幕共享

1.  **Windows 客户端** (或任何其他控制端) 通过 Gateway 的 HTTP API 发送一个任务。
2.  **Galaxy Gateway** 将任务路由到指定的 Android 设备。
3.  **Android 客户端** 的 `WebRTCManager` 收到任务，初始化 `PeerConnection`，创建并发送 Offer。
4.  信令通过 Gateway 中继到 **Windows 客户端**。
5.  双方交换 ICE Candidate，建立 WebRTC 连接，实现低延迟屏幕共享。

### 示例 2: 语音指令驱动的多设备任务

1.  **用户** 对 **Android 客户端** 的浮窗使用语音输入：“总结我电脑上打开的报告，并发送邮件给张三。”
2.  **Android 客户端** 的 `FloatingWindowService` 将语音转为文本，并通过 WebSocket 发送到 **Galaxy Gateway**。
3.  **Gateway** 解析任务，进行任务分解：
    - **步骤 A:** 指派 **Windows 客户端** 执行“获取活动窗口内容”和“文本摘要”任务。
    - **步骤 B:** 指派 **Android 客户端** 执行“发送邮件”任务，并将步骤 A 的结果作为邮件内容。
4.  两个客户端分别执行任务，并将结果报告给 Gateway。

---

## 6. 故障排除

- **连接失败:** 检查 Android 设备与 Gateway 是否在同一局域网，并确认 IP 地址和端口配置正确。
- **权限问题:** 如果浮窗不显示或无障碍操作失败，请到系统“设置”中手动检查相关权限是否已授予。
- **WebRTC 失败:** 检查 STUN/TURN 服务器配置是否正确，以及网络防火墙是否阻止了 UDP 流量。

---

## 7. 相关文档

- **Android 客户端进度报告:** [PROGRESS_REPORT.md](https://github.com/DannyFish-11/ufo-galaxy-android/blob/main/PROGRESS_REPORT.md)
- **Android 集成测试方案:** [INTEGRATION_TEST_PLAN.md](https://github.com/DannyFish-11/ufo-galaxy-android/blob/main/INTEGRATION_TEST_PLAN.md)
- **AIP v2.0 协议:** `ufo-galaxy/galaxy_gateway/aip_protocol_v2.py`
