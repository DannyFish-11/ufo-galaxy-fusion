# UFO³ Galaxy - 所有 API 和模型清单

**最后更新:** 2026-01-22  
**Node 01 版本:** 2.1.0  
**支持的提供商:** 7 个（6 云端 + 1 本地）

---

## 📊 总览

### 支持的 API 提供商

| 提供商 | 类型 | 状态 | 成本 | 特点 |
|--------|------|------|------|------|
| **Local LLM** | 本地 | ✅ | 免费 | DeepSeek-Coder, Qwen2.5 系列 |
| **Groq** | 云端 | ✅ | 免费 | Llama 3.3, Mixtral, 超快速度 |
| **Together AI** | 云端 | ✅ | 低成本 | 多种开源模型，Llama 3.3, DeepSeek-V3 |
| **智谱 AI** | 云端 | ✅ | 低成本 | GLM-4, 中文优秀 |
| **OpenRouter** | 云端 | ✅ | 中等 | 聚合多个提供商 |
| **Claude** | 云端 | ✅ | 高成本 | Claude 3.5, 最强推理 |
| **OpenWeather** | 工具 | ✅ | 免费 | 天气查询 |
| **Brave Search** | 工具 | ✅ | 免费 | 实时搜索 |

---

## 🤖 LLM 模型清单

### 1. 本地 LLM (Node 79)

**提供商:** Ollama  
**成本:** 免费  
**优势:** 隐私保护、离线可用、零成本

| 模型 ID | 参数 | 内存需求 | 适用场景 | 推荐度 |
|---------|------|----------|---------|--------|
| `local/deepseek-coder:6.7b-instruct-q4_K_M` | 6.7B | 4GB | 代码生成、调试 | ⭐⭐⭐⭐⭐ |
| `local/qwen2.5:14b-instruct-q4_K_M` | 14B | 8-9GB | 复杂推理、规划 | ⭐⭐⭐⭐⭐ |
| `local/qwen2.5:7b-instruct-q4_K_M` | 7B | 4-5GB | 常规对话、问答 | ⭐⭐⭐⭐☆ |
| `local/qwen2.5:3b-instruct-q4_K_M` | 3B | 2GB | 快速响应、简单任务 | ⭐⭐⭐☆☆ |

**使用示例:**
```python
# 自动选择（代码任务自动用 DeepSeek）
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "auto",
    "messages": [{"role": "user", "content": "Write a Python function"}]
})

# 指定模型
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "local/deepseek-coder:6.7b-instruct-q4_K_M",
    "messages": [{"role": "user", "content": "Explain recursion"}]
})
```

---

### 2. Groq (免费)

**提供商:** Groq  
**成本:** 免费  
**优势:** 超快速度（LPU 加速）、免费额度大

| 模型 ID | 参数 | 上下文 | 特点 | 推荐度 |
|---------|------|--------|------|--------|
| `groq/llama-3.3-70b-versatile` | 70B | 32K | 通用任务，速度快 | ⭐⭐⭐⭐⭐ |
| `groq/mixtral-8x7b-32768` | 47B (MoE) | 32K | 多语言，推理强 | ⭐⭐⭐⭐☆ |

**使用示例:**
```python
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "groq/llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Explain quantum computing"}]
})
```

**配置:**
```bash
export GROQ_API_KEY="your_groq_api_key"
```

---

### 3. Together AI (低成本) ⭐ 新增

**提供商:** Together AI  
**成本:** 低成本（$0.0001-0.0008/1K tokens）  
**优势:** 多种开源模型、价格便宜、速度快

| 模型 ID | 参数 | 上下文 | 成本 | 特点 | 推荐度 |
|---------|------|--------|------|------|--------|
| `together/meta-llama/Llama-3.3-70B-Instruct-Turbo` | 70B | 128K | 低 | 通用任务，Turbo 加速 | ⭐⭐⭐⭐⭐ |
| `together/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo` | 405B | 128K | 中 | 最强开源模型 | ⭐⭐⭐⭐⭐ |
| `together/Qwen/Qwen2.5-72B-Instruct-Turbo` | 72B | 128K | 低 | 中文优秀，Turbo 加速 | ⭐⭐⭐⭐⭐ |
| `together/deepseek-ai/DeepSeek-V3` | 671B (MoE) | 64K | 低 | 最新 DeepSeek，推理强 | ⭐⭐⭐⭐⭐ |

**使用示例:**
```python
# Llama 3.3 70B Turbo
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "together/meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "messages": [{"role": "user", "content": "Analyze market trends"}]
})

# DeepSeek-V3 (最新最强)
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "together/deepseek-ai/DeepSeek-V3",
    "messages": [{"role": "user", "content": "Solve complex math problem"}]
})
```

**配置:**
```bash
export TOGETHER_API_KEY="tgp_v1_UNn83XywlRbucbXVq9lEU9esuHQMseXOKVTla36eEvE"
```

**价格对比:**
| 模型 | 输入成本 | 输出成本 | 对比 GPT-4 |
|------|---------|---------|-----------|
| Llama 3.3 70B Turbo | $0.00018/1K | $0.00018/1K | **便宜 95%** |
| Llama 3.1 405B Turbo | $0.0005/1K | $0.0005/1K | **便宜 90%** |
| Qwen2.5 72B Turbo | $0.00018/1K | $0.00018/1K | **便宜 95%** |
| DeepSeek-V3 | $0.00027/1K | $0.0011/1K | **便宜 90%** |

---

### 4. 智谱 AI (中文优秀)

**提供商:** 智谱 AI (GLM)  
**成本:** 低成本  
**优势:** 中文理解和生成能力强

| 模型 ID | 参数 | 上下文 | 特点 | 推荐度 |
|---------|------|--------|------|--------|
| `zhipu/glm-4-flash` | - | 128K | 快速响应，低成本 | ⭐⭐⭐⭐⭐ |
| `zhipu/glm-4` | - | 128K | 标准版，中文强 | ⭐⭐⭐⭐☆ |

**使用示例:**
```python
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "zhipu/glm-4-flash",
    "messages": [{"role": "user", "content": "写一篇关于人工智能的文章"}]
})
```

**配置:**
```bash
export ZHIPU_API_KEY="your_zhipu_api_key"
```

---

### 5. OpenRouter (聚合平台)

**提供商:** OpenRouter  
**成本:** 中等（取决于具体模型）  
**优势:** 聚合多个提供商，一个 API 访问所有模型

| 模型 ID | 提供商 | 成本 | 特点 | 推荐度 |
|---------|--------|------|------|--------|
| `openrouter/openai/gpt-4` | OpenAI | 中 | GPT-4，强大 | ⭐⭐⭐⭐⭐ |
| `openrouter/openai/gpt-3.5-turbo` | OpenAI | 低 | GPT-3.5，快速 | ⭐⭐⭐⭐☆ |
| `openrouter/anthropic/claude-3-opus` | Anthropic | 高 | Claude 3 Opus | ⭐⭐⭐⭐⭐ |

**使用示例:**
```python
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "openrouter/openai/gpt-4",
    "messages": [{"role": "user", "content": "Complex reasoning task"}]
})
```

**配置:**
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

---

### 6. Claude (最强推理)

**提供商:** Anthropic  
**成本:** 高成本  
**优势:** 最强推理能力、长上下文、安全性高

| 模型 ID | 参数 | 上下文 | 特点 | 推荐度 |
|---------|------|--------|------|--------|
| `claude/claude-3-5-sonnet-20241022` | - | 200K | 最新版，推理强 | ⭐⭐⭐⭐⭐ |
| `claude/claude-3-haiku-20240307` | - | 200K | 快速版，低成本 | ⭐⭐⭐⭐☆ |

**使用示例:**
```python
response = requests.post("http://localhost:8001/v1/chat/completions", json={
    "model": "claude/claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Deep analysis of philosophical question"}]
})
```

**配置:**
```bash
export CLAUDE_API_KEY="your_claude_api_key"
```

---

## 🛠️ 工具 API

### 1. OpenWeather (天气查询)

**提供商:** OpenWeather  
**成本:** 免费（1000 次/天）  
**功能:** 实时天气、预报、历史数据

**使用示例:**
```python
response = requests.post("http://localhost:8001/weather", json={
    "city": "Beijing",
    "units": "metric"
})
```

**配置:**
```bash
export OPENWEATHER_API_KEY="your_openweather_api_key"
```

---

### 2. Brave Search (实时搜索)

**提供商:** Brave  
**成本:** 免费（2000 次/月）  
**功能:** 实时网页搜索、新闻搜索

**使用示例:**
```python
response = requests.post("http://localhost:8001/search", json={
    "query": "latest AI news",
    "count": 10
})
```

**配置:**
```bash
export BRAVE_API_KEY="your_brave_api_key"
```

---

## 🎯 智能路由策略

### 策略 1: 本地优先（推荐，零成本）

**配置:**
```bash
LOCAL_LLM_ENABLED=true
LOCAL_LLM_PRIORITY=1
```

**路由顺序:**
```
请求 → One-API
  ├─> 本地 LLM (免费)
  │   ├─> 成功 ✅ → 返回
  │   └─> 失败 ✗ → Fallback 云端
  │       ├─> Groq (免费)
  │       ├─> Together AI (低成本)
  │       ├─> 智谱 AI (中文)
  │       ├─> OpenRouter
  │       └─> Claude (最强)
  └─> 返回结果
```

### 策略 2: 云端优先（高质量）

**配置:**
```bash
LOCAL_LLM_ENABLED=true
LOCAL_LLM_PRIORITY=0
```

**路由顺序:**
```
请求 → One-API
  ├─> Groq (免费，快)
  ├─> Together AI (低成本，强)
  ├─> 智谱 AI (中文)
  ├─> OpenRouter
  ├─> Claude (最强)
  └─> 本地 LLM (备用)
```

---

## 💰 成本对比

### 日常开发场景（1000 次调用/天）

| 提供商 | 成本/天 | 成本/月 | 成本/年 | 节省 |
|--------|---------|---------|---------|------|
| **本地 LLM** | $0 | $0 | $0 | - |
| **Groq** | $0 | $0 | $0 | - |
| **Together AI** | $0.18 | $5.4 | $65.7 | **vs GPT-4: 95%** |
| **智谱 AI** | $1 | $30 | $365 | **vs GPT-4: 90%** |
| **OpenRouter (GPT-4)** | $10 | $300 | $3,650 | - |
| **Claude 3.5** | $15 | $450 | $5,475 | - |

### 生产环境（10,000 次调用/天）

| 提供商 | 成本/天 | 成本/月 | 成本/年 | 节省 |
|--------|---------|---------|---------|------|
| **本地 LLM** | $0 | $0 | $0 | **100%** |
| **Groq** | $0 | $0 | $0 | **100%** |
| **Together AI** | $1.8 | $54 | $657 | **95%** |
| **智谱 AI** | $10 | $300 | $3,650 | **90%** |
| **OpenRouter (GPT-4)** | $100 | $3,000 | $36,500 | - |
| **Claude 3.5** | $150 | $4,500 | $54,750 | - |

---

## 📋 模型选择建议

### 按任务类型

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| **代码生成** | `local/deepseek-coder:6.7b` | 专门优化，免费 |
| **代码生成（云端）** | `together/deepseek-ai/DeepSeek-V3` | 最新最强，低成本 |
| **中文对话** | `zhipu/glm-4-flash` | 中文优秀，低成本 |
| **中文对话（本地）** | `local/qwen2.5:7b` | 免费，隐私 |
| **复杂推理** | `claude/claude-3-5-sonnet` | 最强推理 |
| **复杂推理（低成本）** | `together/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo` | 405B，便宜 |
| **快速响应** | `groq/llama-3.3-70b-versatile` | 超快，免费 |
| **通用任务** | `auto` | 自动选择 |

### 按成本优先级

| 优先级 | 模型 | 成本 | 质量 |
|--------|------|------|------|
| 1️⃣ **免费** | 本地 LLM, Groq | $0 | ⭐⭐⭐⭐☆ |
| 2️⃣ **低成本** | Together AI, 智谱 AI | $0.0001-0.001/1K | ⭐⭐⭐⭐⭐ |
| 3️⃣ **中等** | OpenRouter (GPT-3.5) | $0.001-0.01/1K | ⭐⭐⭐⭐⭐ |
| 4️⃣ **高成本** | Claude 3.5, GPT-4 | $0.01-0.03/1K | ⭐⭐⭐⭐⭐ |

---

## 🚀 快速开始

### 1. 配置环境变量

创建 `.env` 文件：

```bash
# ===== 本地 LLM =====
LOCAL_LLM_ENABLED=true
LOCAL_LLM_URL=http://localhost:8079
LOCAL_LLM_PRIORITY=1

# ===== 云端 API Keys =====
# 免费提供商
GROQ_API_KEY=your_groq_key

# 低成本提供商
TOGETHER_API_KEY=tgp_v1_UNn83XywlRbucbXVq9lEU9esuHQMseXOKVTla36eEvE
ZHIPU_API_KEY=your_zhipu_key

# 聚合平台
OPENROUTER_API_KEY=your_openrouter_key

# 高级提供商
CLAUDE_API_KEY=your_claude_key

# ===== 工具 API =====
OPENWEATHER_API_KEY=your_openweather_key
BRAVE_API_KEY=your_brave_key
```

### 2. 启动服务

```bash
# 启动 Ollama
ollama serve

# 下载模型
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull deepseek-coder:6.7b-instruct-q4_K_M

# 启动 Node 79 (Local LLM)
cd nodes/Node_79_LocalLLM
python main.py  # 8079 端口

# 启动 Node 01 (One-API)
cd nodes/Node_01_OneAPI
python main.py  # 8001 端口
```

### 3. 测试调用

```python
import requests

# 自动选择（本地优先）
response = requests.post(
    "http://localhost:8001/v1/chat/completions",
    json={
        "model": "auto",
        "messages": [
            {"role": "user", "content": "Hello, world!"}
        ]
    }
)

print(response.json())
```

---

## 📊 总结

**UFO³ Galaxy 现在支持:**
- ✅ **7 个 API 提供商** (6 云端 + 1 本地)
- ✅ **20+ 个模型** (涵盖免费、低成本、高性能)
- ✅ **智能路由** (自动选择最优提供商)
- ✅ **成本优化** (本地优先，降低 90%+ 成本)
- ✅ **高可用** (自动 Fallback，保证可用性)

**推荐配置:**
- 日常开发: 本地 LLM + Groq (免费)
- 生产环境: Together AI + 智谱 AI (低成本)
- 高质量需求: Claude 3.5 (最强)

---

**项目仓库:** https://github.com/DannyFish-11/ufo-galaxy  
**最后更新:** 2026-01-22  
**Node 01 版本:** 2.1.0
