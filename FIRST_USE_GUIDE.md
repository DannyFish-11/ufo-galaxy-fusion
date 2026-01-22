# UFO³ Galaxy 首次使用指南

**欢迎来到 UFO³ Galaxy 的世界！**

您已经成功部署了这个强大的跨设备 AI 增强系统。现在，让我们一起体验它的核心功能，感受自然语言控制多设备的魔力。

---

## 🎯 核心理念

UFO³ Galaxy 的设计理念是**超级增益器**（Super Enhancer）。它能够通过自然语言理解您的意图，并自动调用合适的模型、协议和设备来完成任务。您不需要记住复杂的命令，只需要像和朋友聊天一样，告诉系统您想做什么。

---

## 🌟 第一个指令：测试连接

在开始更复杂的任务之前，让我们先确认所有设备都已正确连接。

### 在 PC 端测试

打开命令行，进入 `ufo-galaxy` 目录，运行以下命令：

```bash
curl http://localhost:8888/health
```

如果系统正常运行，您会看到类似以下的 JSON 响应：

```json
{
  "status": "healthy",
  "version": "3.0.0",
  "nodes": {
    "node_01": "running",
    "node_50": "running",
    "node_67": "running"
  }
}
```

### 在安卓端测试

在您的小米 14 或 OPPO 平板上，打开 `UFO³ Galaxy` 应用。您应该看到灵动岛的**折叠态**，状态指示器呈现**绿色**（表示已连接）。单击灵动岛，它会展开为**概览态**，显示"CONNECTED"字样。

---

## 📱 第二个指令：跨设备截图

现在，让我们尝试一个简单但实用的跨设备操作：在 PC 上通过自然语言指令，截取小米 14 的屏幕。

### 方法 A：通过 PC 端命令行

在 PC 的命令行中，运行：

```bash
curl -X POST http://localhost:8888/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"截图小米 14 的屏幕\"}"
```

系统会自动识别您的意图，调用 Node_67（安卓设备管理节点），通过 Scrcpy 或 ADB 协议连接到小米 14，执行截图操作，并将截图保存到 PC 的 `Downloads` 目录。

### 方法 B：通过安卓端悬浮窗

在小米 14 上，单击灵动岛两次，完全展开为**极客终端模式**。在底部的输入框中，输入或语音说出：

```
截图我的屏幕
```

系统会立即执行截图，并在历史记录区显示：

```
[12:34:56] [USER] 截图我的屏幕
[12:34:57] [SYSTEM] 正在执行截图任务...
[12:34:58] [SYSTEM] 截图完成，已保存到 /sdcard/Pictures/screenshot_20260122_123458.png
```

---

## 🔄 第三个指令：文件传输

UFO³ Galaxy 支持在 PC 和安卓设备之间无缝传输文件。让我们尝试将小米 14 上的一张照片传输到 PC。

### 从安卓传输到 PC

在 PC 的命令行中，运行：

```bash
curl -X POST http://localhost:8888/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"将小米 14 上最新的照片传输到我的 PC\"}"
```

系统会自动：

1. 连接到小米 14。
2. 扫描 `/sdcard/DCIM/Camera/` 目录，找到最新的照片。
3. 通过 ADB 或 Tailscale 网络将照片传输到 PC 的 `Downloads` 目录。
4. 在命令行中返回传输结果。

### 从 PC 传输到安卓

同样，您也可以反向操作：

```bash
curl -X POST http://localhost:8888/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"将 PC 上的 report.pdf 发送到 OPPO 平板\"}"
```

系统会将 `report.pdf` 传输到 OPPO 平板的 `/sdcard/Download/` 目录。

---

## 🤖 第四个指令：自动化操作

UFO³ Galaxy 的核心能力之一是在安卓设备上执行自动化操作。让我们尝试在小米 14 上自动打开微信。

### 打开应用

在 PC 的命令行中，运行：

```bash
curl -X POST http://localhost:8888/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"在小米 14 上打开微信\"}"
```

系统会通过无障碍服务（Accessibility Service）自动识别微信图标并点击，打开微信应用。

### 更复杂的操作

您甚至可以执行更复杂的多步骤操作：

```bash
curl -X POST http://localhost:8888/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"在小米 14 上打开微信，进入我的收藏，截图第一条内容\"}"
```

系统会自动分解这个任务为多个步骤，并依次执行。

---

## 🧠 第五个指令：调用 AI 模型

UFO³ Galaxy 集成了多个 AI 模型，包括 Qwen3-VL（视觉理解）、DeepSeek（文本/代码）等。让我们尝试使用视觉模型分析小米 14 的屏幕内容。

### 视觉理解

在 PC 的命令行中，运行：

```bash
curl -X POST http://localhost:8888/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"看看小米 14 的屏幕上显示了什么内容\"}"
```

系统会：

1. 截取小米 14 的屏幕。
2. 将截图发送到 Qwen3-VL 模型。
3. 返回模型的分析结果，例如："屏幕上显示的是微信的聊天界面，最新的一条消息是..."

---

## 🔬 第六个指令：量子计算（进阶）

如果您对量子计算感兴趣，UFO³ Galaxy 还集成了量子计算功能。让我们尝试运行一个简单的量子算法。

### 运行 Bell 态

在 PC 的命令行中，运行：

```bash
curl -X POST http://localhost:8057/bell_state?shots=1024
```

系统会通过 Node_57（量子云接口）连接到 IBM Quantum Cloud（或本地 Qiskit 模拟器），运行 Bell 态生成算法，并返回测量结果。

### 自然语言量子编程

您甚至可以用自然语言描述量子算法：

```bash
curl -X POST http://localhost:8051/dispatch \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"找到 5 个城市的最短路径\", \"problem_type\": \"optimization\", \"max_qubits\": 10, \"shots\": 1024}"
```

系统会自动将您的自然语言描述转换为量子电路，并执行。

---

## 🎨 第七个指令：自定义您的体验

UFO³ Galaxy 高度可定制。让我们尝试调整安卓端的 UI 主题。

### 修改强调色

在您的 PC 上，打开文件 `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/ui/theme/GeekTheme.kt`。

找到以下代码：

```kotlin
val AccentBlue = Color(0xFF00BFFF)      // 科技蓝
```

将其修改为您喜欢的颜色，例如紫色：

```kotlin
val AccentBlue = Color(0xFF9370DB)      // 紫色
```

保存文件，重新打包并安装 APK，您就会看到新的主题效果。

---

## 🚀 更多可能性

UFO³ Galaxy 的功能远不止这些。以下是一些您可以探索的方向：

### 多设备协同

同时控制小米 14 和 OPPO 平板，例如：

```
在小米 14 上打开微信，在 OPPO 平板上打开钉钉，同时截图两台设备的屏幕
```

### 智能传输路由

系统会根据设备状态、网络质量、任务类型，自动选择最优的传输协议（ADB、Scrcpy、WebRTC、Tailscale）。

### 节点推送

您可以在 PC 端开发新的节点，并通过 WebSocket 实时推送到安卓设备，无需重新打包 APK。

### MCP 集成

系统已经集成了多个 MCP 服务器（Notion、PayPal、MiniMax），您可以通过自然语言调用这些服务。

---

## 💡 使用技巧

### 技巧 1：善用自然语言

不要担心措辞是否精确，系统会理解您的意图。例如，以下表达都是等价的：

- "截图小米 14"
- "给我的小米 14 拍个屏幕快照"
- "把小米 14 的屏幕内容保存下来"

### 技巧 2：查看历史记录

在安卓端的极客终端模式中，您可以滚动查看所有历史对话，每条消息都带有时间戳和语法高亮。

### 技巧 3：使用语音输入

在安卓端，点击输入框右侧的麦克风图标，您可以直接用语音说出指令，系统会自动识别并执行。

### 技巧 4：拖拽灵动岛

长按灵动岛，您可以将它拖动到屏幕的任意位置，找到最舒适的操作区域。

---

## ❓ 常见问题

**Q: 为什么安卓端显示"连接失败"？**

A: 检查以下几点：

1. PC 和安卓设备是否都在 Tailscale 网络中？
2. PC 端的 UFO³ Galaxy 系统是否正在运行？
3. APK 中配置的 PC IP 地址是否正确？

**Q: 为什么自动化操作没有执行？**

A: 确认您已经在安卓设备上开启了**无障碍服务**权限。这是最重要的权限，没有它，系统无法执行自动化操作。

**Q: 如何查看系统日志？**

A: 在 PC 端，系统日志会实时输出到启动脚本的命令行窗口中。您也可以查看 `logs/` 目录下的日志文件。

---

## 🎉 开始您的探索之旅

现在，您已经掌握了 UFO³ Galaxy 的基本使用方法。这个系统的潜力是无限的，它会随着您的使用而不断学习和进化。

**尽情探索，享受跨设备 AI 增强的魔力吧！**

如果您有任何问题或建议，欢迎在 GitHub 仓库中提交 Issue，或直接联系开发团队。

---

**祝您使用愉快！** 🚀
