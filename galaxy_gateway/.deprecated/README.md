# 已废弃的模块

本目录包含在架构重构过程中被废弃的模块。这些文件已不再被系统使用，但保留以供参考。

## 废弃原因

在 2026-01-22 的架构重构中，我们统一了视觉理解能力到 `Node_90_MultimodalVision`，以符合项目的"节点化"设计原则。

## 废弃的文件

| 文件名 | 原功能 | 废弃原因 |
| :--- | :--- | :--- |
| `vlm_node.py` | VLM 任务执行节点 | 违反了节点化架构，Gateway 不应包含具体执行逻辑 |
| `qwen_vl_api.py` | Qwen3-VL API 客户端 | 功能已整合到 Node_90 中 |
| `vision_understanding.py` | 视觉理解模块 | 与 Node_90 功能重叠，已统一到 Node_90 |

## 新的架构

所有视觉理解任务现在由 `nodes/Node_90_MultimodalVision` 统一处理：
- 支持 Gemini 和 Qwen3-VL 两种 VLM Provider
- 集成了 OCR、屏幕截图、元素查找等功能
- 作为独立的 FastAPI 微服务运行

Gateway (`galaxy_gateway/gateway_service_v3.py`) 通过 HTTP 调用 Node_90，而不是直接执行视觉任务。

---

**如需恢复这些文件，请从 Git 历史中检出。**
