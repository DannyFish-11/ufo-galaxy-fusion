# UFO³ Galaxy 增强系统 - 完整部署流程

**版本:** 2.2  
**作者:** Manus AI  
**日期:** 2026-01-22

---

## 📋 系统概述

UFO³ Galaxy 增强系统是一个完整的跨设备自动化平台，包含以下组件：

### 系统架构

```
UFO³ Galaxy 增强系统
│
├── Windows PC (E:\)
│   ├── Microsoft UFO³ Galaxy (原版) - 核心系统
│   ├── ufo-galaxy (增强项目)
│   │   ├── Galaxy Gateway - 超级网关
│   │   ├── 79 个功能节点
│   │   ├── 10 个 API 提供商集成
│   │   └── Podman 容器环境
│   └── Ollama + 本地模型 (可选)
│
├── Android 设备
│   ├── 手机 A - Android Agent
│   ├── 手机 B - Android Agent
│   └── 平板 - Android Agent
│
└── Tailscale VPN - 跨设备通信
```

---

## 🎯 部署目标

完成部署后，您将能够：

1. **在任意 Android 设备上通过语音或文本控制整个系统**
2. **让系统自动操作所有设备（Windows + Android）**
3. **实现跨设备协同**（剪贴板同步、文件传输等）
4. **使用 10 个 API 提供商**（节省成本 78-87%）
5. **本地 + 云端混合**（隐私 + 能力）

---

## 📦 部署前准备

### 1. 硬件要求

- **Windows PC:**
  - Windows 10/11
  - 16GB+ RAM
  - 100GB+ 可用磁盘空间
  - 稳定的网络连接

- **Android 设备:**
  - Android 8.0+
  - 2GB+ RAM
  - 稳定的网络连接

### 2. 软件要求

- **Windows PC:**
  - Git
  - Python 3.11+
  - Podman Desktop (或 Docker Desktop)
  - Tailscale
  - Ollama (可选，用于本地模型)

- **Android 设备:**
  - Tailscale App
  - 足够的存储空间安装 APK

### 3. 账号准备

- GitHub 账号 (已有: DannyFish-11)
- Tailscale 账号
- 10 个 API 提供商的 API Keys (已配置)

---

## 🚀 部署步骤

### 第一部分：Windows PC 部署

#### 步骤 1: 克隆增强项目

```bash
# 打开 PowerShell 或 CMD
cd E:\
git clone https://github.com/DannyFish-11/ufo-galaxy.git
cd ufo-galaxy
```

#### 步骤 2: 配置 API Keys

1. 从 GitHub 仓库根目录复制 `.env.example` 为 `.env`
   ```bash
   copy .env.example .env
   ```

2. 编辑 `.env` 文件，填入您的真实 API Keys
   （您已经有一个包含所有 Keys 的 `user_env_file.txt`，直接复制内容即可）

#### 步骤 3: 安装 Tailscale

1. 下载并安装 Tailscale: https://tailscale.com/download/windows
2. 登录您的 Tailscale 账号
3. 记录您的 Windows PC 的 Tailscale IP 地址
   ```bash
   tailscale ip -4
   ```
   例如: `100.x.x.x`

#### 步骤 4: 部署 Galaxy Gateway

```bash
cd E:\ufo-galaxy\galaxy_gateway

# 安装 Python 依赖
pip install -r requirements.txt

# 启动 Galaxy Gateway
python main.py
```

您应该看到类似输出：
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**保持这个窗口运行！**

#### 步骤 5: 部署 79 个功能节点 (Podman)

打开新的 PowerShell 窗口：

```bash
cd E:\ufo-galaxy

# 启动所有容器
podman-compose up -d

# 查看运行状态
podman-compose ps
```

您应该看到 79 个容器都在运行。

#### 步骤 6: (可选) 部署 Ollama 本地模型

```bash
# 下载并安装 Ollama
# https://ollama.com/download/windows

# 安装推荐的模型
ollama pull qwen2.5:7b
ollama pull llama3.2:3b
```

---

### 第二部分：Android 设备部署

#### 步骤 1: 在 Android 设备上安装 Tailscale

1. 从 Google Play 商店安装 Tailscale
2. 登录您的 Tailscale 账号
3. 确保与 Windows PC 在同一个 Tailnet 中

#### 步骤 2: 构建 Android APK

在 Windows PC 上：

1. 安装 Android Studio
2. 打开项目
   ```
   E:\ufo-galaxy\enhancements\clients\android_client
   ```

3. 修改配置文件
   打开 `app/src/main/assets/config.properties`
   
   将 `galaxy.gateway.url` 改为您的 Windows PC 的 Tailscale IP:
   ```properties
   galaxy.gateway.url=ws://100.x.x.x:8000/ws/agent
   ```

4. 构建 APK
   - 在 Android Studio 中: `Build` → `Build Bundle(s) / APK(s)` → `Build APK(s)`
   - APK 位置: `app/build/outputs/apk/debug/app-debug.apk`

#### 步骤 3: 安装 APK 到所有 Android 设备

将 `app-debug.apk` 传输到您的：
- 手机 A
- 手机 B
- 平板

在每个设备上安装 APK。

#### 步骤 4: 配置 Android Agent

在每个 Android 设备上：

1. **授予权限**
   - 悬浮窗权限
   - 无障碍服务权限
   - 麦克风权限

2. **启动服务**
   - 打开 UFO³ Galaxy App
   - 点击 "启动 Galaxy Agent"
   - 点击 "启动悬浮窗"

3. **验证连接**
   - 在 Windows PC 的 Galaxy Gateway 日志中，您应该看到：
     ```
     INFO: Agent 'Android Agent' (ID: xxxxx) connected.
     ```

---

### 第三部分：系统验证

#### 测试 1: 基础连接

在任意 Android 设备的悬浮窗中，输入或说：
```
你好
```

在 Windows PC 的 Galaxy Gateway 日志中，您应该看到接收到的消息。

#### 测试 2: 跨设备控制

在手机 A 上说：
```
打开微信
```

手机 A 应该自动打开微信应用。

#### 测试 3: 自然语言理解

在任意设备上说：
```
帮我搜索最新的 AI 新闻
```

系统应该理解您的意图并执行相应操作。

---

## 🔧 配置优化

### 1. 多设备命名

为了区分不同的 Android 设备，您可以在每个设备的 `config.properties` 中设置不同的名称：

- 手机 A: `agent.name=Phone-A`
- 手机 B: `agent.name=Phone-B`
- 平板: `agent.name=Tablet`

### 2. API 成本优化

根据您的使用场景，调整 `.env` 文件中的 API 优先级：

- **日常对话**: 使用 Together AI (低成本)
- **复杂推理**: 使用 Claude (高质量)
- **实时信息**: 使用 Perplexity (联网搜索)
- **快速响应**: 使用 Groq (免费且快)

### 3. 本地模型优先

如果您安装了 Ollama，可以配置系统优先使用本地模型：

```env
LOCAL_LLM_ENABLED=true
LOCAL_LLM_URL=http://localhost:11434
LOCAL_LLM_MODEL=qwen2.5:7b
```

---

## 📊 系统监控

### Galaxy Gateway Dashboard

访问: `http://localhost:8000/dashboard`

您可以看到：
- 所有在线设备
- 实时任务执行状态
- API 调用统计
- 成本分析

### 日志查看

- **Galaxy Gateway 日志**: 在运行 `python main.py` 的窗口中
- **Podman 容器日志**: `podman-compose logs -f`
- **Android Agent 日志**: `adb logcat | grep "Galaxy"`

---

## ❓ 常见问题

### Q1: Android Agent 无法连接到 Galaxy Gateway

**解决方案:**
1. 确认 Windows PC 和 Android 设备都已连接到 Tailscale
2. 确认 `config.properties` 中的 IP 地址正确
3. 确认 Galaxy Gateway 正在运行
4. 检查防火墙设置

### Q2: 语音识别不工作

**解决方案:**
1. 确认已授予麦克风权限
2. 在 Android 设置中检查语音识别服务是否可用
3. 尝试重启 App

### Q3: 自主操纵功能不工作

**解决方案:**
1. 确认已开启无障碍服务
2. 在 Android 设置 → 无障碍 → UFO³ Galaxy 自主操纵 → 开启
3. 尝试重启设备

---

## 🎉 完成！

恭喜！您的 UFO³ Galaxy 增强系统已完整部署。

现在您可以：
- 📱 在手机上通过语音控制一切
- 🖥️ 让系统自动操作电脑和手机
- 🔄 实现跨设备协同工作
- 💰 使用低成本 API 节省开支
- 🔒 保护隐私的同时享受强大能力

---

**享受您的智能助手系统吧！** 🚀
