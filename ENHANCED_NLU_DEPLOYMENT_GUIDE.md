# UFO³ Galaxy - 增强版 NLU 部署指南

## 📋 概述

**增强版 NLU v2.0** 已经完成开发，现在可以部署到您的 UFO³ Galaxy 系统中。

**主要改进：**
- ✅ 精确识别多设备（手机 A、手机 B、平板、电脑）
- ✅ 支持设备别名（"我的手机"、"工作手机"）
- ✅ LLM 驱动的意图识别（支持复杂场景）
- ✅ 复杂任务自动分解
- ✅ 跨设备协同和数据传递
- ✅ 上下文管理和多轮对话
- ✅ 主动澄清机制
- ✅ 混合策略（规则 + LLM）优化性能

---

## 🎯 新增功能

### 1. 多设备精确识别

**之前：**
```
用户："在手机B上打开微信"
系统：❌ 无法区分手机A和手机B
```

**现在：**
```
用户："在手机B上打开微信"
系统：✅ 准确识别手机B，只在手机B上执行
```

---

### 2. 复杂任务自动分解

**之前：**
```
用户："把手机上的照片发到电脑，然后用PS打开"
系统：❌ 无法理解多步任务
```

**现在：**
```
用户："把手机上的照片发到电脑，然后用PS打开"
系统：✅ 自动分解为3步：
  1. 手机：读取照片
  2. 电脑：接收照片
  3. 电脑：用PS打开照片
```

---

### 3. 多设备并行操控

**示例：**
```
用户："在手机A上打开微信，在手机B上打开QQ，在平板上播放音乐"
系统：✅ 三个设备同时执行，互不干扰
```

---

### 4. 智能上下文理解

**示例：**
```
用户："打开微信"
系统："在哪个设备上打开？"
用户："手机B"
系统：✅ 在手机B上打开微信

用户："关闭它"
系统：✅ 自动理解"它"指的是手机B上的微信
```

---

## 📦 新增文件

所有新文件都在 `galaxy_gateway/` 目录下：

| 文件 | 说明 |
|------|------|
| `enhanced_nlu_v2.py` | 增强版 NLU 引擎（核心） |
| `task_router.py` | 任务路由和调度模块 |
| `task_decomposer.py` | 复杂任务分解模块 |
| `gateway_service_v2.py` | 集成增强 NLU 的 Gateway 主服务 |
| `start_gateway_v2.sh` | 启动脚本 |
| `test_nlu_v2.py` | NLU 测试脚本 |

---

## 🚀 部署步骤

### 步骤 1：安装依赖

```bash
cd /home/ubuntu/ufo-galaxy-api-integration/galaxy_gateway

# 安装 Python 依赖
pip3 install fastapi uvicorn aiohttp websockets pydantic
```

---

### 步骤 2：配置 LLM

**选项 A：使用本地 Ollama（推荐，免费）**

```bash
# 安装 Ollama（如果还没安装）
curl -fsSL https://ollama.com/install.sh | sh

# 启动 Ollama 服务
ollama serve &

# 下载 Qwen2.5 模型（约 4.7GB）
ollama pull qwen2.5:7b

# 设置环境变量
export LLM_PROVIDER=ollama
export LLM_API_BASE=http://localhost:11434
```

**选项 B：使用云端 API（更强大，需要 API Key）**

```bash
# 使用 Groq（免费额度）
export LLM_PROVIDER=groq
export LLM_API_BASE=https://api.groq.com/openai/v1
export LLM_API_KEY=your_groq_api_key

# 或使用 DeepSeek（便宜）
export LLM_PROVIDER=deepseek
export LLM_API_BASE=https://api.deepseek.com/v1
export LLM_API_KEY=your_deepseek_api_key
```

---

### 步骤 3：启动 Gateway v2.0

```bash
cd /home/ubuntu/ufo-galaxy-api-integration/galaxy_gateway

# 使用启动脚本
./start_gateway_v2.sh

# 或直接启动
python3 gateway_service_v2.py
```

**启动成功后，您会看到：**
```
======================================================================
UFO³ Galaxy Gateway v2.0
======================================================================
启动时间: 2026-01-22 10:00:00
LLM 提供商: ollama
设备数量: 4
======================================================================
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

### 步骤 4：测试 NLU

**方法 1：使用测试脚本**

```bash
cd /home/ubuntu/ufo-galaxy-api-integration/galaxy_gateway

python3 test_nlu_v2.py
```

这会运行所有测试用例并生成报告。

**方法 2：使用 HTTP API**

```bash
# 测试基础指令
curl -X POST http://localhost:8000/api/test/nlu \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在手机B上打开微信",
    "session_id": "test_session",
    "user_id": "test_user"
  }'

# 测试复杂指令
curl -X POST http://localhost:8000/api/test/nlu \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在手机A上打开微信，在平板上播放音乐，在电脑上打开Chrome",
    "session_id": "test_session",
    "user_id": "test_user"
  }'
```

**方法 3：使用 Python**

```python
import requests

response = requests.post(
    "http://localhost:8000/api/test/nlu",
    json={
        "user_input": "在手机B上打开微信",
        "session_id": "test_session",
        "user_id": "test_user"
    }
)

print(response.json())
```

---

### 步骤 5：配置设备

**每个设备需要注册到 Gateway：**

```bash
# 注册手机 A
curl -X POST http://localhost:8000/api/devices/register \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "phone_a",
    "device_name": "手机A",
    "device_type": "android",
    "aliases": ["手机A", "我的手机", "主手机"],
    "capabilities": ["wechat", "qq", "browser", "camera"],
    "ip_address": "192.168.1.100"
  }'

# 注册手机 B
curl -X POST http://localhost:8000/api/devices/register \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "phone_b",
    "device_name": "手机B",
    "device_type": "android",
    "aliases": ["手机B", "工作手机", "备用手机"],
    "capabilities": ["wechat", "qq", "browser", "camera"],
    "ip_address": "192.168.1.101"
  }'

# 注册平板
curl -X POST http://localhost:8000/api/devices/register \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "tablet",
    "device_name": "平板",
    "device_type": "android",
    "aliases": ["平板", "iPad", "平板电脑"],
    "capabilities": ["wechat", "qq", "browser", "youtube", "music"],
    "ip_address": "192.168.1.102"
  }'

# 注册电脑
curl -X POST http://localhost:8000/api/devices/register \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "pc",
    "device_name": "电脑",
    "device_type": "windows",
    "aliases": ["电脑", "PC", "台式机", "主机"],
    "capabilities": ["chrome", "edge", "notepad", "vscode", "photoshop"],
    "ip_address": "192.168.1.10"
  }'
```

---

### 步骤 6：执行命令

**使用 HTTP API：**

```bash
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在手机B上打开微信，在平板上播放音乐",
    "session_id": "my_session",
    "user_id": "danny"
  }'
```

**响应示例：**

```json
{
  "success": true,
  "nlu": {
    "confidence": 0.95,
    "method": "llm",
    "processing_time": 0.523,
    "context_used": false
  },
  "execution": {
    "summary": {
      "total_tasks": 2,
      "completed": 2,
      "failed": 0,
      "success_rate": 1.0,
      "total_duration": 3.2
    },
    "by_device": {
      "phone_b": {"total": 1, "completed": 1, "failed": 0},
      "tablet": {"total": 1, "completed": 1, "failed": 0}
    },
    "errors": [],
    "results": [
      {
        "task_id": "task_1",
        "device_id": "phone_b",
        "status": "completed",
        "result": {"app": "wechat", "status": "opened"},
        "duration": 2.1
      },
      {
        "task_id": "task_2",
        "device_id": "tablet",
        "status": "completed",
        "result": {"app": "music", "status": "playing"},
        "duration": 1.5
      }
    ]
  }
}
```

---

## 🧪 测试场景

### 场景 1：基础操作

```bash
# 在手机A上打开微信
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{"user_input": "在手机A上打开微信"}'

# 在平板上播放音乐
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{"user_input": "在平板上播放音乐"}'
```

---

### 场景 2：多设备并行

```bash
# 三个设备同时操作
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在手机A上打开微信，在手机B上打开QQ，在平板上播放YouTube"
  }'
```

---

### 场景 3：复杂任务

```bash
# 跨设备文件传输
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "把手机A上的照片发到电脑"
  }'

# 多步操作
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在电脑上打开Chrome并搜索Python教程"
  }'
```

---

### 场景 4：设备别名

```bash
# 使用别名
curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在我的手机上打开微信"
  }'

curl -X POST http://localhost:8000/api/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "在工作手机上打开QQ"
  }'
```

---

## 📊 API 端点

### 1. 执行命令（主要 API）

**端点：** `POST /api/command`

**请求：**
```json
{
  "user_input": "在手机B上打开微信",
  "session_id": "my_session",
  "user_id": "danny"
}
```

**响应：**
```json
{
  "success": true,
  "nlu": {...},
  "execution": {...}
}
```

---

### 2. 测试 NLU（不执行）

**端点：** `POST /api/test/nlu`

**请求：**
```json
{
  "user_input": "在手机B上打开微信"
}
```

**响应：**
```json
{
  "success": true,
  "confidence": 0.95,
  "method": "llm",
  "tasks": [...]
}
```

---

### 3. 列出设备

**端点：** `GET /api/devices`

**响应：**
```json
{
  "devices": [
    {
      "device_id": "phone_a",
      "device_name": "手机A",
      "device_type": "android",
      "status": "online",
      "aliases": ["手机A", "我的手机"],
      "capabilities": ["wechat", "qq"]
    }
  ]
}
```

---

### 4. 注册设备

**端点：** `POST /api/devices/register`

**请求：**
```json
{
  "device_id": "phone_a",
  "device_name": "手机A",
  "device_type": "android",
  "aliases": ["手机A", "我的手机"],
  "capabilities": ["wechat", "qq"],
  "ip_address": "192.168.1.100"
}
```

---

### 5. 获取状态

**端点：** `GET /api/status`

**响应：**
```json
{
  "status": "online",
  "uptime_seconds": 3600,
  "devices": {
    "total": 4,
    "online": 4
  },
  "connections": 4,
  "stats": {
    "total_requests": 100,
    "total_tasks": 150,
    "successful_tasks": 145,
    "failed_tasks": 5
  }
}
```

---

## 🔧 配置选项

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `LLM_PROVIDER` | LLM 提供商（ollama/groq/deepseek/openrouter） | `ollama` |
| `LLM_API_BASE` | LLM API 基础 URL | `http://localhost:11434` |
| `LLM_API_KEY` | LLM API 密钥（云端 API 需要） | - |

---

### NLU 引擎配置

在 `gateway_service_v2.py` 中修改：

```python
# NLU 引擎
self.nlu_engine = EnhancedNLUEngineV2(
    device_registry=self.device_registry,
    llm_client=self.llm_client,
    use_llm=True,              # 是否使用 LLM
    confidence_threshold=0.7   # 置信度阈值
)
```

---

## 📈 性能优化

### 1. 混合策略

系统自动使用混合策略：
- 简单指令 → 规则引擎（快速，<0.1秒）
- 复杂指令 → LLM（准确，0.5-2秒）

### 2. 本地 LLM vs 云端 API

| 方案 | 优点 | 缺点 |
|------|------|------|
| 本地 Ollama | 免费、隐私、无网络延迟 | 需要 GPU、模型较小 |
| 云端 API | 强大、无需硬件 | 需要网络、有成本 |

**推荐：**
- 开发/测试：本地 Ollama
- 生产环境：云端 API（DeepSeek 或 Groq）

---

## 🐛 故障排查

### 问题 1：Ollama 无法启动

**解决：**
```bash
# 检查 Ollama 是否安装
ollama --version

# 重新安装
curl -fsSL https://ollama.com/install.sh | sh

# 启动服务
ollama serve
```

---

### 问题 2：NLU 识别不准确

**解决：**
1. 检查设备是否已注册
2. 检查设备别名是否配置
3. 尝试使用更强大的 LLM（如 DeepSeek）
4. 查看 NLU 测试报告

---

### 问题 3：任务执行失败

**解决：**
1. 检查设备是否在线
2. 检查设备 IP 地址是否正确
3. 检查设备是否支持该应用
4. 查看 Gateway 日志

---

## 📚 下一步

1. **集成到 Android Agent**
   - 修改 Android Agent 连接到 Gateway v2.0
   - 使用新的 WebSocket 协议

2. **集成到 Windows Client**
   - 修改 Windows Client 连接到 Gateway v2.0
   - 实现任务执行接口

3. **完整部署**
   - 在您的 Windows PC 上部署 Gateway v2.0
   - 在所有设备上安装和配置 Agent
   - 测试完整的多设备操控流程

4. **持续优化**
   - 收集用户输入数据
   - 优化 NLU 准确率
   - 添加更多应用支持

---

## 📞 支持

如有问题，请查看：
- `NLU_ANALYSIS.md` - NLU 问题分析
- `test_nlu_v2.py` - 测试脚本
- GitHub Issues: https://github.com/DannyFish-11/ufo-galaxy/issues

---

**文档版本：** 1.0  
**最后更新：** 2026-01-22  
**作者：** Manus AI
