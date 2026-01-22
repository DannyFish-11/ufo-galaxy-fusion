# UFO³ Galaxy 协议融合地图

**版本**: 1.0.0  
**日期**: 2026-01-22  
**状态**: ✅ 已完成扫描和融合

## 概述

本文档记录了 UFO³ Galaxy 项目中所有通信协议的融合情况，包括协议类型、使用场景、相关文件和融合状态。

## 协议统计

| 协议类型 | 文件数量 | 融合状态 | 优先级 |
|---------|---------|---------|--------|
| **HTTP/REST** | 112 | ✅ 已融合 | 高 |
| **WebSocket** | 34 | ✅ 已融合 | 高 |
| **ADB** | 21 | ✅ 已融合 | 高 |
| **TCP/UDP** | 18 | ⚠️ 部分融合 | 中 |
| **Tailscale** | 12 | ✅ 已融合 | 高 |
| **MQTT** | 9 | ✅ 已融合 | 中 |
| **Scrcpy** | 6 | ✅ 已融合 | 高 |
| **WebRTC** | 4 | ✅ 已融合 | 高 |
| **gRPC** | 0 | ❌ 未使用 | 低 |

## 协议详情

### 1. HTTP/REST (112 个文件)

**用途**: 基础 API 通信、健康检查、配置管理

**关键文件**:
- `dashboard/backend/main.py` - Dashboard 后端
- `galaxy_gateway/gateway_service_v3.py` - Gateway 服务
- `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/api/GalaxyApiClient.kt` - Android 客户端

**融合状态**: ✅ 已完全融合到 Gateway 和各节点

**使用场景**:
- 节点健康检查
- 任务提交和状态查询
- 配置获取和更新
- 文件上传下载

---

### 2. WebSocket (34 个文件)

**用途**: 实时双向通信、AIP 协议、设备控制

**关键文件**:
- `galaxy_gateway/aip_protocol_v2.py` - AIP v2.0 协议实现
- `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/agent/AgentWebSocket.kt` - Android WebSocket 客户端
- `dashboard/backend/main.py` - Dashboard WebSocket 接口

**融合状态**: ✅ 已完全融合到 AIP v2.0 协议

**使用场景**:
- 设备间实时消息传递
- 任务状态实时推送
- 屏幕控制指令
- 日志流式传输

---

### 3. ADB (21 个文件)

**用途**: Android 设备控制、截图、文件传输

**关键文件**:
- `nodes/Node_33_ADB/main.py` - ADB 节点
- `galaxy_gateway/adb_manager.py` - ADB 管理器
- `enhancements/nodes/Node_52_KnowledgeBase/knowledge_base_system.py` - 知识库系统

**融合状态**: ✅ 已融合到 SmartTransportRouter

**使用场景**:
- 设备截图（静态内容）
- 应用安装和卸载
- 文件推送和拉取
- Shell 命令执行

---

### 4. TCP/UDP (18 个文件)

**用途**: 底层网络通信、Socket 连接

**关键文件**:
- `dashboard/backend/main.py`
- `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/agent/AgentWebSocket.kt`

**融合状态**: ⚠️ 部分融合（主要作为 WebSocket 和 HTTP 的底层）

**使用场景**:
- WebSocket 底层传输
- HTTP 底层传输
- 自定义协议（如有）

---

### 5. Tailscale (12 个文件)

**用途**: 跨设备 VPN、安全通信

**关键文件**:
- `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/network/TailscaleAdapter.kt` - Tailscale 适配器
- `TEST_SYSTEM.py` - 测试系统

**融合状态**: ✅ 已融合到 SmartTransportRouter

**使用场景**:
- 跨网络设备通信
- 安全的远程访问
- 多设备协同

**配置**:
```bash
export TAILSCALE_ENABLED=true
export TAILSCALE_DOMAIN=your-machine.tailnet-name.ts.net
```

---

### 6. MQTT (9 个文件)

**用途**: 轻量级消息队列、IoT 设备通信

**关键文件**:
- `nodes/Node_41_MQTT/main.py` - MQTT 节点
- `enhancements/nodes/Node_43_BambuLab/enhanced_bambu_controller.py` - BambuLab 3D 打印机控制

**融合状态**: ✅ 已融合到 SmartTransportRouter

**使用场景**:
- IoT 设备控制（如 3D 打印机）
- 低功耗设备通信
- 发布/订阅模式消息传递

---

### 7. Scrcpy (6 个文件)

**用途**: 高帧率屏幕镜像、实时控制

**关键文件**:
- `nodes/Node_34_Scrcpy/main.py` - Scrcpy 节点
- `nodes/Node_04_Router/main.py` - 路由节点

**融合状态**: ✅ 已融合到 SmartTransportRouter

**使用场景**:
- 高帧率屏幕捕获（动态内容）
- 实时设备控制
- 游戏和视频场景

---

### 8. WebRTC (4 个文件)

**用途**: 实时音视频流、低延迟屏幕共享

**关键文件**:
- `nodes/Node_95_WebRTC_Receiver/main.py` - WebRTC 接收器
- `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/webrtc/WebRTCManager.kt` - Android WebRTC 管理器
- `enhancements/clients/android_client/app/src/main/java/com/ufo/galaxy/webrtc/ScreenCaptureService.kt` - 屏幕捕获服务

**融合状态**: ✅ 已融合到 SmartTransportRouter

**使用场景**:
- 实时屏幕共享（最低延迟）
- 交互式任务
- 视频通话

---

## SmartTransportRouter 融合架构

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    SmartTransportRouter                      │
│                      (Node_96)                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 智能路由
                              ▼
        ┌─────────────────────────────────────────┐
        │         传输方式选择逻辑                 │
        │                                         │
        │  任务类型 + 质量需求 + 实时性 + 设备状态  │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   WebRTC     │      │   Scrcpy     │      │     ADB      │
│  (Node_95)   │      │  (Node_34)   │      │  (Node_33)   │
│              │      │              │      │              │
│ 实时、低延迟  │      │ 高帧率、动态  │      │ 静态、低功耗  │
└──────────────┘      └──────────────┘      └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   网络层选择     │
                    │                  │
                    │ Tailscale / 直连 │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   信令选择       │
                    │                  │
                    │ MQTT/WS/HTTP     │
                    └──────────────────┘
```

### 路由决策表

| 任务类型 | 质量需求 | 实时性 | 首选方式 | 回退方式 |
|---------|---------|--------|---------|---------|
| 动态内容 | 高 | 是 | WebRTC | Scrcpy |
| 动态内容 | 高 | 否 | Scrcpy | ADB |
| 动态内容 | 中/低 | 是 | WebRTC | Scrcpy |
| 动态内容 | 中/低 | 否 | Scrcpy | ADB |
| 静态内容 | 高 | - | Scrcpy | ADB |
| 静态内容 | 中/低 | - | ADB | HTTP |
| 交互式 | 任意 | 是 | WebRTC | Scrcpy |

## 使用示例

### 1. 自动选择传输方式

```python
from smart_transport_router import SmartTransportRouter, TransportRequest

router = SmartTransportRouter()

# 请求路由
request = TransportRequest(
    device_id="phone_a",
    task_type="dynamic",  # static/dynamic/interactive
    quality="high",
    realtime=True
)

response = await router.route(request)
print(f"选择的方式: {response.method}")
print(f"端点: {response.endpoint}")
```

### 2. 指定首选方式

```python
request = TransportRequest(
    device_id="phone_a",
    task_type="dynamic",
    quality="high",
    realtime=True,
    preferred_method="webrtc"  # 首选 WebRTC
)

response = await router.route(request)
```

### 3. 集成到 Gateway

```python
# 在 gateway_service_v3.py 中
from smart_transport_router import SmartTransportRouter

router = SmartTransportRouter()

async def capture_screen(device_id: str, task_type: str):
    request = TransportRequest(
        device_id=device_id,
        task_type=task_type,
        quality="high",
        realtime=True
    )
    
    response = await router.route(request)
    
    # 使用选择的端点
    async with httpx.AsyncClient() as client:
        result = await client.get(response.endpoint)
        return result.content
```

## 验证清单

- [x] 扫描所有协议类型
- [x] 分析协议使用场景
- [x] 创建 SmartTransportRouter
- [x] 实现智能路由逻辑
- [x] 支持 Tailscale 网络层
- [x] 支持多种信令方式
- [x] 创建 Node_96 节点
- [x] 编写文档和示例
- [ ] 端到端测试（待推送后进行）
- [ ] 性能基准测试
- [ ] 多设备协同测试

## 下一步

1. **推送到 GitHub**: 将 Node_96 和协议融合文档推送到仓库
2. **端到端测试**: 在实际设备上测试智能路由
3. **性能优化**: 根据测试结果优化路由逻辑
4. **文档完善**: 补充更多使用示例和最佳实践

## 参考文档

- [COMMUNICATION_ARCHITECTURE.md](./COMMUNICATION_ARCHITECTURE.md) - 通信架构文档
- [WEBRTC_INTEGRATION_COMPLETE.md](./WEBRTC_INTEGRATION_COMPLETE.md) - WebRTC 集成文档
- [MULTIMODAL_TRANSPORT_OPTIMIZATION_PLAN.md](./MULTIMODAL_TRANSPORT_OPTIMIZATION_PLAN.md) - 多模态传输优化计划
- [Node_96_SmartTransportRouter/README.md](./nodes/Node_96_SmartTransportRouter/README.md) - Node_96 详细文档
