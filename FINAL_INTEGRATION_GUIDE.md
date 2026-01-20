# UFO³ Galaxy 增强模块 - 最终集成指南

**版本**: v3.1  
**更新时间**: 2025-01-20  
**GitHub 仓库**: https://github.com/DannyFish-11/ufo-galaxy

---

## 项目概述

本项目是对**微软 UFO** 的全面增强，旨在通过分布式节点架构、跨平台协同和自然语言控制，将 AI Agent 的能力扩展到真实世界的硬件设备和云计算资源。

### 核心增强功能

| 功能模块 | 说明 | 状态 |
|:--------|:-----|:-----|
| **Node 50 - NLU 引擎** | 智能任务分发，支持 OneAPI 多模型调用 | ✅ 完成 |
| **Node 48 - 视频生成** | PixVerse API 集成，自动生成和下载 AI 视频 | ✅ 完成 |
| **Node 60 - 异构计算** | 量子计算（IBM Quantum）+ AI 加速（昇腾 Atlas） | ✅ 完成 |
| **Windows 客户端** | 侧边栏 UI + F12 热键 + 桌面自动化 | ✅ 完成 |
| **Android 客户端** | 悬浮窗 + 语音输入 + 自然语言控制 | ✅ 完成 |
| **云节点部署** | 华为云一键部署脚本 + systemd 服务 | ✅ 完成 |

---

## 集成方案

### 方案 A：一键自动集成（推荐）

适用于希望快速集成所有增强功能的用户。

#### 步骤 1：进入您的微软 UFO 项目目录

```powershell
cd E:\UFO  # 请替换为您实际的路径
```

#### 步骤 2：下载并运行一键集成脚本

```powershell
# 下载集成脚本
curl -O https://raw.githubusercontent.com/DannyFish-11/ufo-galaxy/master/INTEGRATE_ENHANCEMENT.bat

# 运行集成脚本
.\INTEGRATE_ENHANCEMENT.bat
```

脚本会自动完成以下操作：
1. 克隆 UFO³ Galaxy 增强模块仓库
2. 复制所有核心文件到您的 UFO 项目中
3. 清理临时文件

#### 步骤 3：启动增强系统

```powershell
# 以管理员身份运行
.\INSTALL_AND_START.bat
```

---

### 方案 B：手动选择性集成

适用于只需要特定增强功能的用户。

#### 步骤 1：克隆增强模块仓库

```powershell
cd E:\UFO  # 您的 UFO 项目目录
git clone https://github.com/DannyFish-11/ufo-galaxy.git ufo-galaxy-enhancement
```

#### 步骤 2：选择需要的模块

**如果您需要 Windows 客户端（侧边栏 + F12 热键）**:
```powershell
xcopy /E /I ufo-galaxy-enhancement\windows_client .\windows_client
```

**如果您需要云节点（量子计算 + 异构计算）**:
```powershell
xcopy /E /I ufo-galaxy-enhancement\node_60_cloud .\node_60_cloud
```

**如果您需要特定的节点（如 Node 48 视频生成）**:
```powershell
xcopy /E /I ufo-galaxy-enhancement\nodes\Node_48_MediaGen .\nodes\Node_48_MediaGen
```

**如果您需要 Podman 容器配置**:
```powershell
copy ufo-galaxy-enhancement\podman-compose.yml .
xcopy /E /I ufo-galaxy-enhancement\nodes .\nodes
```

#### 步骤 3：清理临时文件

```powershell
rd /s /q ufo-galaxy-enhancement
```

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Tailscale 虚拟私有网络 (VPN)                       │
│                     零配置、点对点、加密通信                           │
└─────────────────────────────────────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────────┐      ┌──────────────┐          ┌──────────────┐
│   Windows PC      │      │   Android    │          │  华为云服务器  │
│   (主控中心)       │      │   (移动端)    │          │  (计算节点)    │
├───────────────────┤      ├──────────────┤          ├──────────────┤
│ Node 50 (大脑)    │◄────►│  悬浮窗客户端 │          │  Node 60     │
│ - NLU 引擎        │      │  - 语音输入   │          │  - 量子计算   │
│ - 任务分发        │      │  - 文本输入   │          │  - AI 加速    │
│                   │      │  - 命令发送   │          │  - 路径优化   │
│ Node 43 (工匠)    │      └──────────────┘          └──────────────┘
│ - 3D 打印控制     │
│                   │
│ Node 48 (艺术家)  │
│ - AI 视频生成     │
│                   │
│ Windows 客户端    │
│ - 侧边栏 UI       │
│ - F12 热键        │
│ - 桌面自动化      │
└───────────────────┘
```

### 通信协议：AIP/1.0

所有节点和客户端之间通过自定义的 **AIP/1.0** (Agent Interaction Protocol) 协议进行通信。

**消息格式示例**:
```json
{
  "protocol": "AIP/1.0",
  "message_id": "win-client_1737336000123",
  "timestamp": "2025-01-20T12:00:00Z",
  "from": "Windows_Client",
  "to": "Node_50",
  "type": "command",
  "payload": {
    "command": "打印一个警告标志",
    "context": {
      "platform": "windows",
      "user_id": "user_001"
    }
  }
}
```

---

## 使用指南

### Windows 客户端

#### 启动客户端

```powershell
cd windows_client
.\START_CLIENT.bat
```

#### 使用侧边栏

1. 按 **F12** 键唤醒侧边栏（再次按下隐藏）
2. 在输入框中输入自然语言命令
3. 按 **回车** 发送命令

#### 示例命令

```
"打印一个警告标志"
→ 系统自动调用 Node 43 启动 Bambu Lab 3D 打印机

"生成一个关于宇宙探索的视频"
→ 系统调用 Node 48 (PixVerse) 生成 AI 视频

"优化从北京到上海的路线"
→ 系统调用 Node 60 使用量子算法优化路径

"打开浏览器搜索最新的 AI 新闻"
→ 系统在 Windows 上自动执行桌面操作
```

### Android 客户端

#### 构建和安装

```bash
cd ufo-galaxy-android
./build_configured_apk.sh
# 根据提示输入 Windows PC 的 Tailscale IP
# 将生成的 APK 安装到 Android 设备
```

#### 使用悬浮窗

1. 打开应用并授予悬浮窗权限
2. 点击悬浮窗图标
3. 使用语音或文本输入命令

### 云节点

#### 部署到华为云

```bash
cd node_60_cloud
./DEPLOY_CLOUD.sh
# 根据提示输入 Windows PC 的 Tailscale IP
```

#### 启动云节点

```bash
./start_node60.sh
```

#### 设置开机自启（可选）

```bash
sudo cp node60.service /etc/systemd/system/
sudo systemctl enable node60
sudo systemctl start node60
```

---

## 系统测试

运行自动测试脚本验证所有组件：

```bash
python TEST_SYSTEM.py
```

测试内容包括：
- Node 50 HTTP 接口
- Node 50 健康检查
- WebSocket 连接
- 命令处理流程

---

## 故障排除

### 问题 1：无法连接到 Node 50

**症状**: Windows 客户端或 Android 客户端显示"连接失败"

**解决方案**:
1. 确认 Podman 容器是否正在运行：`podman ps`
2. 确认 Tailscale 是否已登录：`tailscale status`
3. 确认防火墙是否允许端口 8050

### 问题 2：PixVerse 视频生成失败

**症状**: Node 48 返回错误或视频无法下载

**解决方案**:
1. 检查 `PIXVERSE_API_KEY` 环境变量是否正确设置
2. 确认 PixVerse API 配额是否充足
3. 查看 Node 48 的日志：`podman logs ufo_node_48`

### 问题 3：量子计算任务失败

**症状**: Node 60 无法执行量子算法

**解决方案**:
1. 检查 `IBM_QUANTUM_TOKEN` 是否已配置
2. 确认网络可以访问 IBM Quantum 服务
3. 如果没有 IBM Quantum 账号，系统会自动使用本地模拟器

---

## 技术亮点

### 1. 分布式架构
- 64 个节点，分为 4 层（Kernel、Gateway、Tools、Physical）
- 每个节点独立运行在 Podman 容器中
- 通过 Tailscale 实现零配置 VPN

### 2. 真实硬件集成
- Bambu Lab 3D 打印机控制
- 摄像头、传感器、串口设备
- 支持 MQTT、CAN-bus、MAVLink 等工业协议

### 3. AI 内容生成
- PixVerse API 集成
- 文本生成视频 (Text-to-Video)
- 图片生成视频 (Image-to-Video)
- 自动下载和管理生成的视频

### 4. 异构计算
- 量子计算（IBM Quantum、华为 HiQ）
- AI 加速（昇腾 Atlas）
- 路径优化算法
- 自定义量子电路执行

### 5. 跨平台协同
- Windows PC（后端 + 客户端）
- Android 设备（悬浮窗客户端）
- 华为云服务器（异构计算节点）
- 所有设备通过自然语言命令协同工作

---

## 许可证

本项目采用 MIT 许可证。

---

## 联系方式

- **GitHub**: [@DannyFish-11](https://github.com/DannyFish-11)
- **项目地址**: [https://github.com/DannyFish-11/ufo-galaxy](https://github.com/DannyFish-11/ufo-galaxy)

---

**为极客松 AI & Robotics 竞赛而生 🏆**
