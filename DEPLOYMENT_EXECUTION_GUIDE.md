# UFO³ Galaxy - 部署执行指南

**版本**: 2.1.0  
**日期**: 2026-01-23  
**作者**: Manus AI

---

## 概述

本指南将引导您完成 UFO³ Galaxy 系统的完整部署流程，包括 PC 端和安卓端。

---

## 1. PC 端部署

### 1.1 检查前置环境

在开始之前，请运行 `check_prerequisites.py` 脚本，确保所有必需环境已就绪。

```bash
python check_prerequisites.py
```

**预期输出**:
```
✅ 所有必需环境已就绪，可以开始部署！
```

### 1.2 一键部署

运行 `deploy.bat` 脚本，自动安装核心依赖。

```bash
deploy.bat
```

### 1.3 启动系统

使用 `smart_launcher.py` 启动系统。推荐启动完整系统。

```bash
python smart_launcher.py start all
```

**预期输出**:
```
================================================================================
启动 核心系统
================================================================================

✓ Node_00_StateMachine (端口 8000) - 状态机节点，管理系统状态
✓ Node_01_OneAPI (端口 8001) - 统一 API 接口
...

================================================================================
启动完成！
================================================================================

查看状态: python smart_launcher.py status
启动监控: python smart_launcher.py monitor
停止所有节点: python smart_launcher.py stop
```

### 1.4 验证部署

#### 1.4.1 查看状态

```bash
python smart_launcher.py status
```

**预期输出**:
```
Node_00_StateMachine                ✓ 运行中 (运行时间: 10s)
Node_01_OneAPI                      ✓ 运行中 (运行时间: 8s)
...
```

#### 1.4.2 访问 Web 仪表板

```bash
python health_monitor.py
```

打开浏览器，访问 **http://localhost:9000**

---

## 2. 安卓端部署

### 2.1 一键打包 APK

运行 `build_android_apk.bat` 脚本，为您的设备打包 APK。

```bash
build_android_apk.bat
```

脚本会引导您：
1. 确认 PC 的 Tailscale IP
2. 选择设备类型（小米 14 / OPPO 平板）
3. 自动构建 APK

**预期输出**:
```
================================================================================
构建成功！
================================================================================

APK 文件: UFO3_Galaxy_xiaomi-14_20260123.apk
设备: 小米14
PC IP: 100.111.222.333
```

### 2.2 安装和配置

1. **传输 APK**: 将生成的 APK 文件传输到您的安卓设备。
2. **安装 APK**: 在设备上安装 APK。
3. **授予权限**: 打开应用，授予以下权限：
   - **无障碍服务权限**（必需）
   - **悬浮窗权限**（必需）
   - **存储权限**（可选）

### 2.3 验证连接

1. **确保网络连接**: 确保 PC 和安卓设备在同一个 Tailscale 网络中。
2. **查看 PC 端日志**: PC 端节点的日志中应该会显示安卓设备的连接信息。
3. **测试悬浮窗**: 在安卓设备上点击悬浮窗，尝试发送自然语言指令。

---

## 3. 核心命令

| 命令 | 描述 |
|:-----|:-----|
| `python check_prerequisites.py` | 检查前置环境 |
| `deploy.bat` | 一键部署（安装依赖） |
| `python smart_launcher.py start all` | 启动完整系统 |
| `python smart_launcher.py status` | 查看节点状态 |
| `python smart_launcher.py stop` | 停止所有节点 |
| `python smart_launcher.py monitor` | 监控所有节点（自动重启） |
| `python health_monitor.py` | 启动 Web 仪表板 |
| `build_android_apk.bat` | 一键打包安卓 APK |

---

## 4. 故障排查

### 4.1 PC 端

- **端口冲突**: 如果某个节点启动失败，请检查端口是否被占用。
- **依赖问题**: 运行 `pip install -r requirements_full.txt` 安装所有依赖。
- **防火墙**: 确保防火墙允许 Python 和 Tailscale 通信。

### 4.2 安卓端

- **连接失败**: 
  - 检查 PC 的 Tailscale IP 是否正确。
  - 检查 PC 和设备是否在同一个 Tailscale 网络中。
  - 检查 PC 端的 UFO³ Galaxy 是否正在运行。
- **应用闪退**: 
  - 检查**无障碍服务**权限是否已开启。
  - 检查 APK 是否是为当前设备打包的。

---

**UFO³ Galaxy** | 部署执行指南 | 2026-01-23
