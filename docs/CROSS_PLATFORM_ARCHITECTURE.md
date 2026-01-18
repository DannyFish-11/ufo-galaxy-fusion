# UFO Galaxy 跨平台子 Agent 架构

## 🌍 支持的平台

| 平台 | 实现方式 | 状态 |
|------|---------|------|
| **Android** | 原生 Kotlin App | ✅ 已实现 |
| **iOS** | 原生 Swift App | 📋 规划中 |
| **Windows** | Python + PyQt/Electron | ✅ 可用 |
| **macOS** | Python + PyQt/Electron | ✅ 可用 |
| **Linux** | Python + PyQt/Electron | ✅ 可用 |
| **Web** | PWA (Progressive Web App) | 📋 规划中 |

---

## 🏗️ 统一架构设计

### 核心原则

1. **统一协议**: 所有平台使用相同的工具发现协议
2. **模块化设计**: 核心节点可跨平台复用
3. **轻量级**: 最小化依赖，快速启动
4. **自适应**: 根据平台能力自动调整功能

### 架构层次

```
┌─────────────────────────────────────────────────────────┐
│                  统一通信层 (MQTT/HTTP)                   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐       ┌───────▼────────┐
│  主 Agent       │       │  子 Agent       │
│  (PC/Server)    │       │  (移动/嵌入式)   │
└────────┬────────┘       └────────┬────────┘
         │                         │
    ┌────┴────┐              ┌────┴────┐
    │ 70 节点  │              │ 5-10 节点│
    └─────────┘              └─────────┘
```

---

## 📱 各平台实现方案

### 1. Android (已实现)

**技术栈**:
- Kotlin + Jetpack Compose
- Ktor (HTTP 客户端)
- Eclipse Paho (MQTT)
- WorkManager (后台任务)

**核心节点**:
- Node 00: 状态机
- Node 04: 工具路由
- Node 33: ADB 自控
- Node 41: MQTT 通信
- Node 58: 模型路由

**特殊能力**:
- 无障碍服务 (Accessibility Service)
- Shizuku 集成 (免 root ADB)
- Termux 集成

---

### 2. iOS

**技术栈**:
- Swift + SwiftUI
- URLSession (HTTP)
- CocoaMQTT (MQTT)
- Background Tasks Framework

**核心节点**:
- Node 00: 状态机
- Node 04: 工具路由
- Node 41: MQTT 通信
- Node 58: 模型路由
- Node 70: Shortcuts 集成

**特殊能力**:
- Shortcuts 自动化
- Siri 集成
- iCloud 同步

**实现文件结构**:
```
ufo-galaxy-ios/
├── UFOGalaxy/
│   ├── Core/
│   │   ├── AgentCore.swift
│   │   └── NodeBase.swift
│   ├── Nodes/
│   │   ├── Node00_StateMachine.swift
│   │   ├── Node04_Router.swift
│   │   └── Node41_MQTT.swift
│   ├── Services/
│   │   └── BackgroundService.swift
│   └── Views/
│       └── ContentView.swift
└── Info.plist
```

---

### 3. Windows 桌面

**技术栈**:
- Python 3.11+
- PyQt6 / Electron (可选)
- pywin32 (Windows API)
- paho-mqtt

**核心节点**:
- Node 00: 状态机
- Node 04: 工具路由 (增强版)
- Node 06: 文件系统
- Node 36: UI Automation
- Node 41: MQTT 通信
- Node 45: 桌面自动化
- Node 58: 模型路由

**特殊能力**:
- Windows UI Automation
- COM 对象调用
- 注册表操作
- 任务计划程序集成

**实现文件结构**:
```
ufo-galaxy-windows/
├── main.py
├── core/
│   ├── agent_core.py
│   └── node_base.py
├── nodes/
│   ├── node_00_state.py
│   ├── node_04_router.py
│   └── node_36_uia.py
├── ui/
│   └── tray_icon.py
└── installer/
    └── setup.iss (Inno Setup)
```

---

### 4. macOS 桌面

**技术栈**:
- Python 3.11+ / Swift (可选)
- PyQt6 / Electron
- pyobjc (macOS API)
- paho-mqtt

**核心节点**:
- Node 00: 状态机
- Node 04: 工具路由 (增强版)
- Node 06: 文件系统
- Node 35: AppleScript 集成
- Node 41: MQTT 通信
- Node 45: 桌面自动化
- Node 58: 模型路由

**特殊能力**:
- AppleScript 自动化
- Shortcuts 集成
- Accessibility API
- Automator 集成

**实现文件结构**:
```
ufo-galaxy-macos/
├── main.py
├── core/
│   ├── agent_core.py
│   └── node_base.py
├── nodes/
│   ├── node_00_state.py
│   ├── node_04_router.py
│   └── node_35_applescript.py
├── ui/
│   └── menu_bar.py
└── installer/
    └── build_dmg.sh
```

---

### 5. Linux 桌面

**技术栈**:
- Python 3.11+
- PyQt6 / Electron
- python-dbus (D-Bus)
- paho-mqtt

**核心节点**:
- Node 00: 状态机
- Node 04: 工具路由 (增强版)
- Node 06: 文件系统
- Node 37: D-Bus 集成
- Node 41: MQTT 通信
- Node 45: 桌面自动化
- Node 58: 模型路由

**特殊能力**:
- D-Bus 服务调用
- systemd 集成
- X11/Wayland 自动化
- 桌面环境集成 (GNOME/KDE)

**实现文件结构**:
```
ufo-galaxy-linux/
├── main.py
├── core/
│   ├── agent_core.py
│   └── node_base.py
├── nodes/
│   ├── node_00_state.py
│   ├── node_04_router.py
│   └── node_37_dbus.py
├── ui/
│   └── system_tray.py
└── installer/
    ├── ufo-galaxy.desktop
    └── ufo-galaxy.service
```

---

### 6. Web (PWA)

**技术栈**:
- React / Vue.js
- WebSocket / MQTT over WebSocket
- Service Worker
- IndexedDB

**核心节点**:
- Node 00: 状态机 (浏览器存储)
- Node 04: 工具路由 (受限)
- Node 41: WebSocket 通信
- Node 58: 模型路由

**特殊能力**:
- 离线工作
- 推送通知
- 文件系统 API (受限)
- Web Automation (Puppeteer)

---

## 🔧 统一工具发现协议

所有平台共享相同的协议文件: `config/tool_discovery_protocol.yaml`

### 平台特定扩展

```yaml
# Android 扩展
android:
  package_manager: true
  accessibility_service: true
  shizuku: true
  termux: true

# iOS 扩展
ios:
  shortcuts: true
  siri: true
  url_schemes: true

# Windows 扩展
windows:
  registry: true
  com_objects: true
  uia: true
  powershell: true

# macOS 扩展
macos:
  applescript: true
  shortcuts: true
  automator: true
  accessibility: true

# Linux 扩展
linux:
  dbus: true
  systemd: true
  desktop_files: true
  x11: true
```

---

## 📦 打包与分发

### Android
```bash
# APK
./gradlew assembleRelease

# AAB (Google Play)
./gradlew bundleRelease
```

### iOS
```bash
# 使用 Xcode
xcodebuild -scheme UFOGalaxy -archivePath build/UFOGalaxy.xcarchive archive
```

### Windows
```bash
# 使用 PyInstaller
pyinstaller --onefile --windowed main.py

# 或使用 Inno Setup 创建安装程序
iscc installer/setup.iss
```

### macOS
```bash
# 使用 py2app
python setup.py py2app

# 创建 DMG
./installer/build_dmg.sh
```

### Linux
```bash
# AppImage
./build_appimage.sh

# Snap
snapcraft

# Flatpak
flatpak-builder build com.ufo.galaxy.yml
```

---

## 🌐 跨平台通信

### MQTT 主题规范

```
ufo/galaxy/{device_id}/status       # 设备状态
ufo/galaxy/{device_id}/task/request # 任务请求
ufo/galaxy/{device_id}/task/response # 任务响应
ufo/galaxy/{device_id}/tools        # 工具列表
ufo/galaxy/broadcast                # 广播消息
```

### HTTP API 规范

所有平台子 Agent 提供统一的 REST API:

```
GET  /health              # 健康检查
GET  /tools               # 工具列表
POST /tools/invoke        # 调用工具
GET  /status              # 状态查询
POST /task                # 提交任务
```

---

## 🎯 实现优先级

1. **Android** ✅ (已完成)
2. **Windows 桌面** (高优先级)
3. **macOS 桌面** (高优先级)
4. **Linux 桌面** (中优先级)
5. **iOS** (中优先级)
6. **Web PWA** (低优先级)

---

## 📝 开发指南

### 创建新平台子 Agent

1. 复制 `ufo-galaxy-android` 项目结构
2. 替换平台特定代码
3. 实现核心节点 (Node 00, 04, 41, 58)
4. 添加平台特定节点
5. 配置工具发现规则
6. 测试与主 Agent 的通信
7. 打包与分发

### 最小可行子 Agent

只需实现 3 个核心节点即可与主 Agent 通信:
- Node 00: 状态机
- Node 04: 工具路由
- Node 41: MQTT 通信

---

## 🔮 未来扩展

- [ ] 嵌入式设备 (Raspberry Pi, ESP32)
- [ ] 智能手表 (Wear OS, watchOS)
- [ ] 车载系统 (Android Automotive)
- [ ] 游戏主机 (Switch, Steam Deck)
- [ ] VR/AR 设备 (Quest, Vision Pro)

---

**所有平台共享相同的核心理念：智能工具发现 + AI 驱动路由**
