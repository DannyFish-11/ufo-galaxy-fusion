# Android Agent 集成文档

## 概述

本文档描述了如何将 UFO³ Galaxy Android Agent 集成到主系统中，实现跨设备协同。

## Android Agent 仓库

**GitHub**: https://github.com/DannyFish-11/ufo-galaxy-android

## 已实现功能

### 1. 通信层 (892 行代码)

- ✅ **WebSocketClient.kt** (290 行) - WebSocket 客户端
  - 连接到 Galaxy Gateway
  - 自动重连机制（最多 10 次）
  - 心跳保持（每 30 秒）
  - 连接状态管理

- ✅ **AIPMessage.kt** (309 行) - AIP v2.0 协议封装
  - 支持 10 种消息类型
  - 消息验证和解析
  - JSON 序列化和反序列化

- ✅ **DeviceManager.kt** (293 行) - 设备管理器
  - 设备注册
  - 心跳机制
  - 任务接收和执行
  - 工具注册

### 2. UI 层

- ✅ **FloatingWindowService.kt** (494 行) - 浮动窗口服务
  - 黑白渐变 UI
  - Dynamic Island 风格
  - 语音和文字双输入
  - 快捷操作（截图、剪贴板、任务）

### 3. 无障碍服务

- ✅ **UFOAccessibilityService.kt** (494 行) - 无障碍服务
  - 10 个核心操作（点击、滑动、输入等）
  - 与豆包手机类似的系统级控制能力

### 4. 屏幕截图

- ✅ **ScreenshotHelper.kt** - 截图辅助类
  - 支持 Android 11+ 的截图功能

## 集成步骤

### 1. 启动 Galaxy Gateway

确保 Galaxy Gateway 正在运行：

```bash
cd /path/to/ufo-galaxy
python galaxy_gateway/main.py
```

Gateway 默认监听：
- WebSocket: `ws://0.0.0.0:8000/ws`
- HTTP API: `http://0.0.0.0:8000`

### 2. 配置 Android Agent

在 Android Agent 的 `MainActivity.kt` 中配置 Gateway URL：

```kotlin
val gatewayUrl = "ws://192.168.1.100:8000/ws" // 替换为实际 IP
```

### 3. 安装 Android APK

```bash
adb install app-debug.apk
```

### 4. 启动 Android Agent

1. 打开 UFO Galaxy 应用
2. 授予必要权限：
   - 悬浮窗权限
   - 无障碍服务权限
   - 录音权限（语音输入）
3. 点击"启动浮动窗口"按钮
4. 点击"连接到 Galaxy"按钮

### 5. 验证连接

在 Galaxy Gateway 的日志中应该看到：

```
[INFO] Device registered: android_<device_id>
[INFO] Device type: android
[INFO] Capabilities: screen_capture, input_control, accessibility, voice_input
```

## 通信协议

### 设备注册消息

Android Agent 连接后会自动发送：

```json
{
  "version": "2.0",
  "type": "device_register",
  "device_id": "android_<device_id>",
  "timestamp": 1706112000000,
  "payload": {
    "device_type": "android",
    "capabilities": {
      "screen_capture": true,
      "input_control": true,
      "accessibility": true,
      "voice_input": true,
      "app_management": true
    }
  }
}
```

### 任务请求消息

Galaxy Gateway 可以发送任务请求：

```json
{
  "version": "2.0",
  "type": "task_request",
  "device_id": "android_<device_id>",
  "timestamp": 1706112000000,
  "payload": {
    "task_id": "task_001",
    "task_type": "screenshot",
    "data": {
      "save_path": "/sdcard/screenshot.png"
    }
  }
}
```

### 任务响应消息

Android Agent 会返回：

```json
{
  "version": "2.0",
  "type": "task_response",
  "device_id": "android_<device_id>",
  "timestamp": 1706112000000,
  "payload": {
    "task_id": "task_001",
    "success": true,
    "result": {
      "file_path": "/sdcard/screenshot.png",
      "file_size": 1024000
    }
  }
}
```

## 跨设备协同示例

### 示例 1：跨设备截图

**场景**：从 Windows 端触发 Android 端截图

**步骤**：

1. Windows 端发送任务请求到 Galaxy Gateway：
```python
import requests

response = requests.post(
    "http://192.168.1.100:8000/api/task",
    json={
        "target_device": "android_<device_id>",
        "task_type": "screenshot",
        "data": {}
    }
)
```

2. Galaxy Gateway 路由任务到 Android Agent

3. Android Agent 执行截图并返回结果

4. Galaxy Gateway 将结果返回给 Windows 端

### 示例 2：跨设备输入

**场景**：从 Windows 端控制 Android 端输入文本

**步骤**：

1. Windows 端发送命令：
```python
response = requests.post(
    "http://192.168.1.100:8000/api/command",
    json={
        "target_device": "android_<device_id>",
        "command_type": "input_text",
        "data": {
            "text": "Hello from Windows!"
        }
    }
)
```

2. Android Agent 通过无障碍服务输入文本

3. 返回执行结果

### 示例 3：跨设备任务编排

**场景**：在 Windows 上编辑文档，在 Android 上发送邮件

**步骤**：

1. Galaxy Gateway 接收任务：
```json
{
  "task_name": "edit_and_send",
  "steps": [
    {
      "device": "windows_<device_id>",
      "action": "edit_document",
      "data": {"file": "report.docx"}
    },
    {
      "device": "android_<device_id>",
      "action": "send_email",
      "data": {
        "to": "boss@company.com",
        "subject": "Report",
        "attachment": "report.docx"
      }
    }
  ]
}
```

2. Galaxy Gateway 按顺序执行任务

3. 返回整体执行结果

## 支持的操作

### 1. 屏幕操作

- `screenshot` - 截图
- `screen_record` - 录屏（需要实现）

### 2. 输入操作

- `tap` - 点击
- `long_tap` - 长按
- `swipe` - 滑动
- `input_text` - 输入文本
- `key_event` - 按键事件

### 3. 应用操作

- `launch_app` - 启动应用
- `close_app` - 关闭应用
- `install_app` - 安装应用
- `uninstall_app` - 卸载应用

### 4. 系统操作

- `get_device_info` - 获取设备信息
- `get_running_apps` - 获取运行中的应用
- `get_clipboard` - 获取剪贴板内容
- `set_clipboard` - 设置剪贴板内容

## 性能优化

### 1. 连接优化

- 使用 WSS (WebSocket Secure) 加密通信
- 启用消息压缩（gzip）
- 使用连接池复用

### 2. 消息优化

- 批量发送消息
- 使用二进制格式传输大文件
- 启用断点续传

### 3. 心跳优化

根据网络环境调整心跳间隔：
- 稳定网络：60 秒
- 不稳定网络：30 秒
- 移动网络：20 秒

## 故障排除

### 1. 连接失败

**问题**：Android Agent 无法连接到 Galaxy Gateway

**解决方案**：
- 检查 Gateway URL 是否正确
- 检查网络连接（同一局域网）
- 检查防火墙设置
- 检查 Gateway 是否正在运行

### 2. 消息未接收

**问题**：发送消息后没有收到响应

**解决方案**：
- 检查设备是否已注册
- 检查消息格式是否正确
- 检查 Gateway 日志

### 3. 权限问题

**问题**：无障碍服务或悬浮窗权限未授予

**解决方案**：
- 在设置中手动授予权限
- 重启应用

## 安全性

### 1. 使用 WSS

```kotlin
val gatewayUrl = "wss://your-domain.com/ws"
```

### 2. 设备认证

在设备注册时添加认证信息：

```kotlin
val message = AIPMessage.createDeviceRegister(
    deviceId = deviceId,
    deviceType = "android",
    capabilities = mapOf(
        "auth_token" to "your_auth_token"
    )
)
```

### 3. 消息加密

对敏感数据进行加密：

```kotlin
val encryptedData = encrypt(sensitiveData)
val message = AIPMessage.createDataTransfer(
    deviceId = deviceId,
    dataType = "encrypted",
    data = encryptedData
)
```

## 未来增强

1. **WebRTC 集成** - 低延迟屏幕共享
2. **P2P 连接** - 设备间直连
3. **离线队列** - 离线时缓存消息
4. **多媒体传输** - 图片、视频、音频传输
5. **断点续传** - 大文件传输

## 相关文档

- [Android 通信层文档](https://github.com/DannyFish-11/ufo-galaxy-android/blob/main/COMMUNICATION_LAYER.md)
- [Android 浮动窗口文档](https://github.com/DannyFish-11/ufo-galaxy-android/blob/main/FLOATING_WINDOW_DEVELOPMENT.md)
- [Android 无障碍服务文档](https://github.com/DannyFish-11/ufo-galaxy-android/blob/main/ACCESSIBILITY_SERVICE_VERIFICATION.md)
- [Galaxy Gateway 文档](../galaxy_gateway/README.md)
- [AIP v2.0 协议文档](../galaxy_gateway/aip_protocol_v2.py)

## 版本历史

- **v2.0.0** (2026-01-24)
  - 完整实现通信层
  - 完整实现 UI 层
  - 完整实现无障碍服务
  - 支持跨设备协同

## 贡献者

- UFO Galaxy Team

## 许可证

MIT License
