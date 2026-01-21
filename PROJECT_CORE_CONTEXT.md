# UFO³ Galaxy 项目核心上下文文档

**⚠️ 重要：本文档记录项目的核心目标和架构，任何 AI Agent 在开始工作前必须先阅读此文档**

**创建日期:** 2026-01-22  
**最后更新:** 2026-01-22  
**版本:** 1.0

---

## 🎯 项目核心目标

**本项目的唯一目标：为用户已部署的 Microsoft UFO³ Galaxy 系统提供增强、强化、延展和扩展。**

### 关键原则

1. **这是一个增强项目，不是独立项目**
   - 用户的 Windows PC 上已经部署了 Microsoft UFO³ Galaxy 系统
   - 我们所做的一切都是为了增强这个现有系统
   - 不要创建与现有系统脱节的独立模块

2. **整合优先于创造**
   - 优先整合现有代码和模块
   - 不要轻易创建新的独立组件
   - 确保所有组件都能协同工作

3. **真实可用优先于功能丰富**
   - 每个功能都必须在真实环境中验证
   - 不接受模拟测试
   - 文档必须与实际代码一致

---

## 🏗️ 系统架构（架构 A - 已确认）

### 核心组件

```
用户的 Windows PC
├── Microsoft UFO³ Galaxy (基础系统)
│   ├── 79 个功能节点 (Podman 容器)
│   └── Node 50: Transformer (NLU 引擎 - 系统大脑)
│
└── Galaxy Gateway (我们创建的增强模块)
    ├── 端口: 8888
    ├── 功能: 超级网关，统一调用所有节点和 API
    ├── WebSocket 支持: /ws/agent
    └── 设备路由和跨设备协同
        ↓
    Android Agent (移动端增强)
    ├── 灵动岛 UI
    ├── 语音控制
    ├── 自主操纵 (AccessibilityService)
    └── 通过 Tailscale 连接到 Galaxy Gateway
```

### 关键决策

1. **Galaxy Gateway 是增强模块，不是替代品**
   - 它运行在用户的 Windows PC 上
   - 它与 Microsoft UFO³ 的 79 个节点协同工作
   - 它提供额外的功能（10 个 API 集成、跨设备协同等）

2. **Android Agent 连接到 Galaxy Gateway**
   - 不是直接连接到 Microsoft UFO³ Server
   - 通过 Galaxy Gateway 间接访问所有节点
   - 使用简化的 WebSocket 协议（不必完全遵循 AIP）

3. **通信路径**
   ```
   用户语音输入 (Android)
       ↓
   Galaxy Gateway (Windows PC, 端口 8888)
       ↓
   Node 50: Transformer (NLU 引擎)
       ↓
   任务分解和路由
       ↓
   相关节点执行 (79 个节点中的任意一个或多个)
       ↓
   结果返回给 Android Agent
   ```

---

## 📦 现有资产清单

### 后端 (Windows PC)

**已完成:**
- ✅ 79 个功能节点 (在 `nodes/` 目录)
- ✅ Galaxy Gateway (在 `galaxy_gateway/` 目录)
  - main.py (主服务)
  - websocket_handler.py (WebSocket 处理)
  - device_router.py (设备路由)
  - cross_device_coordinator.py (跨设备协同)
- ✅ Podman Compose 配置 (podman-compose.yml)
- ✅ 10 个 API Keys 配置 (.env)
- ✅ 一键启动脚本 (INSTALL_AND_START.bat)

**状态:** 功能完整，可以运行

### 前端 (Android)

**已完成:**
- ✅ 灵动岛 UI (DynamicIsland.kt, DynamicIslandPremium.kt)
- ✅ 极简极客主题 (GeekTheme.kt, GeekThemePremium.kt)
- ✅ 悬浮窗服务 (FloatingWindowService.kt)
- ✅ API 客户端 (GalaxyApiClient.kt)
- ✅ 触觉反馈和音效 (FeedbackManager.kt)
- ✅ 高级动画效果 (AnimationEffects.kt)
- ✅ AccessibilityService (AutonomyService.kt)
- ✅ 动作执行器 (ActionExecutor.kt)
- ✅ UI 树可视化 (UITreeVisualizer.kt)

**问题:** 这些模块之间的集成不完整，需要整合

---

## 🚨 常见问题和陷阱

### 问题 1: 创建独立的新系统

**错误做法:**
- 创建一个新的 "UFO³ Server"
- 实现完整的 AIP 协议栈
- 创建与现有系统脱节的独立架构

**正确做法:**
- 使用现有的 Galaxy Gateway
- 简化协议，只要能工作即可
- 确保与现有 79 个节点协同

### 问题 2: 过度设计

**错误做法:**
- 实现复杂的 5 阶段注册流程
- 创建完整的设备管理系统
- 实现所有可能的功能

**正确做法:**
- 实现最小可用功能
- 先让基本流程跑通
- 逐步添加功能

### 问题 3: 模拟测试

**错误做法:**
- 创建模拟的测试脚本
- 在文档中描述"模拟的设备连接"
- 没有真实环境验证

**正确做法:**
- 在真实设备上测试
- 提供真实的部署步骤
- 记录真实的测试结果

---

## 📋 当前任务：整合 Android Agent

### 目标

让 Android Agent 能够真正连接到 Galaxy Gateway，接收任务并执行。

### 具体步骤

1. **整合现有模块**
   - 将 GalaxyAgentV2, TaskExecutor, AutonomyManager 整合到 MainActivity
   - 移除重复和冲突的代码
   - 确保启动流程清晰

2. **简化连接协议**
   - Android Agent 连接到 ws://YOUR_TAILSCALE_IP:8888/ws/agent
   - 发送简单的 JSON 消息（不必完全遵循 AIP）
   - 实现心跳、任务接收、结果回传

3. **实现核心流程**
   ```
   用户在 Android 上说: "打开微信"
       ↓
   Android Agent 发送消息到 Galaxy Gateway
       ↓
   Galaxy Gateway 转发给 Node 50 (NLU)
       ↓
   Node 50 理解意图，生成任务
       ↓
   Galaxy Gateway 将任务发送回 Android Agent
       ↓
   Android Agent 的 AutonomyService 执行任务
       ↓
   返回执行结果
   ```

4. **真实环境测试**
   - 在用户的 Windows PC 上运行 Galaxy Gateway
   - 在用户的 Android 手机上安装 APK
   - 通过 Tailscale 连接
   - 测试完整流程

---

## 🔄 更新记录

### 2026-01-22
- 创建本文档
- 确认架构 A
- 明确当前任务：整合 Android Agent

---

## 📞 重要提醒

**每次开始工作前，必须：**
1. 阅读本文档
2. 检查 COMPLETE_STATUS_ANALYSIS.md
3. 确认当前任务和目标
4. 不要创建新的独立模块，除非绝对必要

**每次完成工作后，必须：**
1. 更新本文档（如果有架构变更）
2. 推送代码到 GitHub
3. 在真实环境中验证功能

---

**文档结束**
