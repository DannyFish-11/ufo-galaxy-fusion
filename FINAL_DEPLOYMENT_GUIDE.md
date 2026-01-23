# UFO³ Galaxy - 最终部署指南

**版本**: 2.0.0  
**日期**: 2026-01-23  
**作者**: Manus AI

---

## 概述

本指南提供 UFO³ Galaxy 系统的最终部署方案，包括一键部署、系统管理、健康监控和安卓端配置。

---

## 快速开始

### 1. 一键部署

**Windows**:
```bash
deploy.bat
```

此脚本将自动检查环境、安装依赖，并提供下一步操作指引。

### 2. 启动系统

**Windows**:
```bash
start_system.bat
```

此脚本提供多种启动模式：
- **核心系统**: 启动最基础的节点
- **学术研究系统**: 启动学术相关的节点
- **开发工作流系统**: 启动开发相关的节点
- **完整系统**: 启动所有节点

### 3. 健康监控

**启动监控服务**:
```bash
python health_monitor.py
```

**访问 Web 仪表板**:
- URL: http://localhost:9000

---

## 核心组件

### 1. 系统管理器 (`system_manager.py`)

- **功能**: 统一管理所有节点的启动、停止、监控和健康检查
- **使用**:
  - `python system_manager.py start --group core`
  - `python system_manager.py stop`
  - `python system_manager.py status`
  - `python system_manager.py monitor`
  - `python system_manager.py report`

### 2. 健康监控器 (`health_monitor.py`)

- **功能**: 实时监控所有节点，提供 Web 仪表板
- **Web 仪表板**: http://localhost:9000

### 3. 部署脚本 (`deploy.bat`)

- **功能**: 一键检查环境、安装依赖

### 4. 启动脚本 (`start_system.bat`)

- **功能**: 提供多种启动模式

---

## 安卓端配置

请参考 `ANDROID_QUICK_INSTALL.md` 和 `ANDROID_SETUP_GUIDE.md`。

**核心步骤**:

1. 运行 `enhancements/clients/android_client/build_configured_apk.bat`
2. 输入 PC 的 Tailscale IP 和设备 ID
3. 等待构建完成
4. 安装 APK
5. 授予无障碍服务权限

---

## 依赖管理

- **核心依赖**: `requirements.txt`
- **完整依赖**: `requirements_full.txt`

**安装所有依赖**:
```bash
pip install -r requirements_full.txt
```

---

## 故障排查

### 问题 1: 节点无法启动

**原因**: 依赖未安装或端口被占用

**解决**:
1. 运行 `deploy.bat` 检查环境
2. 检查端口占用

### 问题 2: Web 仪表板无法访问

**原因**: `health_monitor.py` 未启动

**解决**:
```bash
python health_monitor.py
```

### 问题 3: 安卓端连接失败

**原因**: Tailscale 未配置或 PC 端未运行

**解决**:
1. 确保 PC 和安卓设备在同一个 Tailscale 网络中
2. 确保 PC 端的 UFO³ Galaxy 正在运行

---

## 总结

通过本指南，您可以轻松部署和管理 UFO³ Galaxy 系统。

**推荐流程**:

1. 运行 `deploy.bat`
2. 运行 `start_system.bat`
3. 运行 `python health_monitor.py`
4. 访问 http://localhost:9000

---

**UFO³ Galaxy** | 最终部署指南 | 2026-01-23
