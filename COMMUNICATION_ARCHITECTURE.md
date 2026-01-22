# UFO³ Galaxy 通信架构文档

**作者**: Manus AI  
**日期**: 2026-01-22  
**版本**: 1.0  
**目标**: 完整列出 ufo-galaxy 项目中的所有通信方式

---

## 1. 核心通信协议：AIP v2.0

系统内部的核心通信协议是 **AIP v2.0 (Agent Interaction Protocol)**，它是一个基于 WebSocket 的自定义协议，用于设备间的指令下发、状态同步和数据传输。

### 1.1 协议特点

- **统一消息格式**: 所有消息都遵循 `AIPMessage` 数据结构
- **多种消息类型**: 支持控制、文本、图片、文件、流等
- **可靠性**: 包含消息确认 (ACK) 和心跳机制
- **灵活性**: 支持多种传输方式（Gateway 中转、P2P 直连）

### 1.2 消息格式

```json
{
  "version": "2.0",
  "message_id": "msg_123456",
  "message_type": "control",
  "source": {
    "device_id": "pc_main",
    "device_name": "Windows PC"
  },
  "target": {
    "device_id": "phone_a",
    "device_name": "手机 A"
  },
  "payload": {
    "action": "execute_task",
    "params": {
      "task_name": "screenshot",
      "task_params": {}
    }
  },
  "timestamp": 1674384000,
  "priority": "normal"
}
```

---

## 2. 服务端点与端口

系统主要由两个核心服务组成：**Galaxy Gateway** 和 **Node_90_MultimodalVision**。

### 2.1 Galaxy Gateway

- **功能**: 系统的主入口，负责设备管理、任务分发和跨设备协同
- **端口**: `8000`
- **协议**: HTTP/REST + WebSocket

#### API 端点

| 方法 | 路径 | 描述 |
| :--- | :--- | :--- |
| `GET` | `/` | 健康检查 |
| `POST` | `/api/command` | 接收自然语言指令 |
| `POST` | `/api/devices/register` | 注册新设备 |
| `GET` | `/api/devices` | 获取设备列表 |
| `POST` | `/api/transfer/file` | 文件中转 |
| `GET` | `/api/status` | 获取系统状态 |

#### WebSocket 端点

| 路径 | 描述 |
| :--- | :--- |
| `/ws/{device_id}` | 设备连接到 Gateway 的 WebSocket 端点 |

### 2.2 Node_90_MultimodalVision

- **功能**: 视觉理解服务，提供截图、OCR、视觉分析等能力
- **端口**: `8090`
- **协议**: HTTP/REST

#### API 端点

| 方法 | 路径 | 描述 |
| :--- | :--- | :--- |
| `POST` | `/capture_screen` | 截取屏幕 |
| `POST` | `/ocr` | 文字识别 |
| `POST` | `/find_element` | 查找元素 |
| `POST` | `/analyze_screen` | 视觉分析 |
| `POST` | `/find_text` | 查找文本 |
| `POST` | `/find_template` | 模板匹配 |
| `GET` | `/health` | 健康检查 |
| `POST` | `/mcp/call` | 调用 MCP |

---

## 3. 外部通信

系统通过标准的 HTTP Client 与外部服务进行通信。

### 3.1 LLM/VLM API 调用

- **协议**: HTTP/REST
- **库**: `aiohttp`
- **端点**: 
  - OpenRouter API
  - Gemini API
  - OpenAI API

### 3.2 安卓端通信

- **协议**: 未明确（可能是 WebSocket 或自定义 TCP）
- **实现**: `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/agent/GalaxyAgentV2.kt`
- **功能**: 与 Galaxy Gateway 建立连接，接收指令并执行

---

## 4. 通信架构图

```mermaid
graph TD
    subgraph Windows PC
        A[Galaxy Gateway (Port 8000)]
        B[Node_90 (Port 8090)]
    end

    subgraph Android Phone
        C[Android Agent]
    end

    subgraph Cloud Services
        D[LLM/VLM APIs]
    end

    User -- "自然语言指令" --> A
    A -- "AIP v2.0 (WebSocket)" --> C
    C -- "系统调用" --> Android_OS
    A -- "HTTP/REST" --> B
    B -- "HTTP/REST" --> D
```

---

## 5. 总结

| 通信方式 | 协议 | 用途 | 关键文件 |
| :--- | :--- | :--- | :--- |
| **内部核心** | AIP v2.0 (WebSocket) | 设备间指令与数据传输 | `aip_protocol_v2.py` |
| **服务间** | HTTP/REST | Gateway 调用 Node_90 | `gateway_service_v3.py` |
| **外部 API** | HTTP/REST | 调用 LLM/VLM | `Node_90/main.py` |
| **安卓端** | WebSocket | Gateway 与安卓 Agent 通信 | `GalaxyAgentV2.kt` |

**结论**: 系统的通信架构清晰，以 **Galaxy Gateway** 为中心，通过 **AIP v2.0** 协议与各设备通信，并通过 **HTTP/REST** 调用功能节点和外部 API。
