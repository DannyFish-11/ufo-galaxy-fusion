# UFO³ Galaxy - 开发者指南

**版本**: 1.0
**作者**: Manus AI

---

## 1. 简介

本指南旨在帮助开发者理解 UFO³ Galaxy 的内部工作原理，并指导如何扩展系统功能，例如添加新节点、增强 NLU 能力或自定义通信协议。

## 2. 项目结构

```
/ufo_galaxy_package
├── ufo-galaxy-podman/      # 后端容器化节点
│   ├── nodes/
│   │   ├── Node_43_BambuLab/ # 3D 打印机节点
│   │   ├── Node_48_MediaGen/ # 视频生成节点
│   │   └── Node_50_Transformer/ # NLU 核心节点
│   ├── podman-compose.yml  # 容器编排文件
│   └── ...
├── windows_client/         # Windows 客户端 (UI 侧边栏)
│   ├── client.py
│   ├── ui_sidebar.py
│   └── key_listener.py
├── ufo-galaxy-android/     # Android 客户端 (悬浮窗)
│   └── app/
├── node_60_cloud/          # 华为云异构计算节点
│   ├── main.py
│   └── quantum_adapters/
├── UFO3_Galaxy_Complete_Deployment_Guide.md # 部署指南
└── UFO3_Galaxy_Developer_Guide.md           # 本文档
```

## 3. AIP/1.0 通信协议

AIP (Agent Interaction Protocol) 是系统内所有节点和客户端之间通信的标准。它是一个基于 WebSocket 和 JSON 的简单协议。

### 3.1. 消息结构

所有 AIP 消息都遵循以下 JSON 结构：

```json
{
    "protocol": "AIP/1.0",
    "message_id": "unique_string_identifier",
    "timestamp": "ISO8601_datetime_string",
    "from": "source_device_id",
    "to": "target_device_id",
    "type": "command | response | event | heartbeat | registration",
    "payload": {}
}
```

### 3.2. 消息类型

| 类型 | 方向 | 描述 |
| :--- | :--- | :--- |
| `registration` | `Node -> Node 50` | 节点启动时向 Node 50 注册自身能力 |
| `command` | `Client -> Node 50` 或 `Node 50 -> Node` | 发送需要执行的命令 |
| `response` | `Node -> Node 50 -> Client` | 对 `command` 的执行结果响应 |
| `event` | `Node -> Node 50 -> All` | 广播重要事件（如打印完成、检测到异常） |
| `heartbeat` | `Node <-> Node 50` | 维持 WebSocket 连接，检查节点健康状态 |

## 4. 如何添加一个新节点

假设您想添加一个 `Node_77_Weather` 用于查询天气。请遵循以下步骤：

### 步骤 1：创建节点主程序

1.  在 `ufo-galaxy-podman/nodes/` 目录下创建一个新文件夹 `Node_77_Weather`。
2.  在其中创建一个 `main.py` 文件，实现一个基本的 WebSocket 客户端，该客户端需能连接到 Node 50。
3.  **核心逻辑**：
    *   **连接**：连接到 `ws://<node-50-ip>:8050/ws/ufo3/Node_77_Weather`。
    *   **注册**：连接成功后，发送一个 `registration` 消息，声明自己的能力。
        ```json
        {
            "type": "registration",
            "payload": {
                "device_type": "Weather_Agent",
                "capabilities": ["query_weather", "get_forecast"]
            }
        }
        ```
    *   **监听命令**：循环等待来自 Node 50 的 `command` 消息。
    *   **执行动作**：当收到 `action` 为 `query_weather` 的命令时，调用天气 API。
    *   **发送响应**：将执行结果通过 `response` 消息发回给 Node 50，并附带 `source_device` 字段，以便 Node 50 将结果转发给原始请求者。

### 步骤 2：在 Podman 中配置新节点

1.  打开 `podman-compose.yml` 文件。
2.  在 `services` 下添加一个新的服务 `node_77`。

    ```yaml
    node_77:
      build:
        context: ./nodes/Node_77_Weather
      container_name: ufo3-node77-weather
      environment:
        - TAILSCALE_IP=${TAILSCALE_IP}
        - WEATHER_API_KEY=${WEATHER_API_KEY}
      restart: unless-stopped
    ```

### 步骤 3：增强 NLU 引擎

1.  打开 `ufo-galaxy-podman/nodes/Node_50_Transformer/main.py`。
2.  在 `NLUEngine` 类的 `_understand_with_rules` 方法（或 `_understand_with_ai` 的 system prompt）中添加新的规则/说明。

    ```python
    # 在 _understand_with_rules 中
    elif any(kw in command_lower for kw in ["天气", "weather"]):
        return {
            "intent": "query_weather",
            "target_nodes": ["Node_77_Weather"],
            "tasks": [{
                "node": "Node_77_Weather",
                "action": "query_weather",
                "parameters": {"city": "北京"} # 参数可以从命令中提取
            }],
            "workflow": "sequential"
        }
    ```

### 步骤 4：重启系统

在 Podman Desktop 中重启 Compose 项目，新节点将自动加入 UFO³ Galaxy 系统。

## 5. 调试与测试

- **独立测试节点**：在每个节点的 `main.py` 中，使用 `if __name__ == "__main__":` 来编写独立的测试代码，模拟来自 Node 50 的命令，确保节点逻辑正确。
- **查看实时日志**：
    - **Podman 节点**：在 Podman Desktop 中直接查看容器日志。
    - **Windows/Android 客户端**：日志会直接打印在终端或 Logcat 中。
- **使用 `websocat`**：这是一个强大的 WebSocket 命令行工具，可以用来模拟任何节点或客户端，直接与 Node 50 交互，发送自定义的 AIP 消息。
  ```bash
  # 模拟一个客户端连接到 Node 50
  websocat ws://<node-50-ip>:8050/ws/ufo3/debug-client
  
  # 发送一个命令
  {"protocol":"AIP/1.0","message_id":"debug1","from":"debug-client","to":"Node_50","type":"command","payload":{"command":"打印一个测试模型"}}
  ```

## 6. 未来扩展方向

- **实现任务持久化**：将 Node 50 接收到的任务存入数据库，以便在节点离线后重新执行。
- **增强 AI 理解能力**：完全依赖 AI 模型进行任务规划，实现更复杂的、多步骤的、并行的工作流。
- **实现 MCP 集成**：将某些功能（如 Notion、PayPal）通过 MCP（Model Context Protocol）暴露给 AI，让 AI 可以直接调用外部工具。
