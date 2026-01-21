# 🚀 UFO³ Galaxy v2.0 - 快速部署指南

## ✅ 系统已完成配置

所有 10 个 API 提供商已经完成集成，可以立即部署使用！

---

## 📋 支持的 API 提供商

### 核心 LLM API (7个)
1. ✅ **Groq** - 免费，超快速度
2. ✅ **Together AI** - 低成本
3. ✅ **智谱 AI** - 中文优秀
4. ✅ **Perplexity** - 实时搜索
5. ✅ **OpenRouter** - 聚合平台
6. ✅ **Claude** - 最强推理
7. ✅ **本地 LLM** - 零成本

### 工具 API (3个)
8. ✅ **Brave Search** - 免费搜索
9. ✅ **OpenWeather** - 免费天气
10. ✅ **Pixverse** - 视频生成

---

## 🚀 Windows 本地部署步骤

### Step 1: 拉取最新代码

```powershell
cd E:\ufo-galaxy
git pull origin master
```

### Step 2: 配置 API Keys

```powershell
# 复制模板
copy .env.example .env

# 编辑 .env 文件
notepad .env
```

**重要：** 将您的 API Keys 填入 `.env` 文件中。所有 API Keys 的格式和获取方式请参考 `API_CONFIGURATION_GUIDE.md`。

### Step 3: 启动 Podman 容器

```powershell
# 启动 Memos (长期记忆)
podman run -d --name memos -p 5230:5230 -v E:\ufo-galaxy\data\memos:/var/opt/memos neosmemo/memos:stable

# 启动 Redis (短期记忆)
podman run -d --name redis -p 6379:6379 redis:alpine

# 验证容器状态
podman ps
```

### Step 4: 安装 Ollama 和模型

```powershell
# 1. 下载 Ollama
# 访问: https://ollama.com/download

# 2. 安装后，拉取模型
ollama pull qwen2.5:7b-instruct-q4_K_M
ollama pull deepseek-coder:6.7b-instruct-q4_K_M

# 3. 验证模型
ollama list
```

### Step 5: 启动 UFO³ Galaxy

```powershell
cd E:\ufo-galaxy

# 启动核心节点（推荐）
python galaxy_launcher.py --mode core

# 或启动所有节点
python galaxy_launcher.py --mode all
```

### Step 6: 验证部署

```powershell
# 测试 Galaxy Gateway
curl http://localhost:8888/health

# 测试 One-API
curl http://localhost:8001/health

# 访问 Dashboard
start http://localhost:8000
```

---

## 🎯 智能路由策略

系统已配置为 **cost_optimized**（成本优化）模式：

```
用户请求
    ↓
Galaxy Gateway 智能判断
    ↓
├─ 简单任务 → 本地 LLM (免费)
├─ 代码任务 → DeepSeek-Coder (免费)
├─ 中文任务 → 智谱 AI (低成本)
├─ 实时信息 → Perplexity (中等)
├─ 快速响应 → Groq (免费)
└─ 复杂推理 → Claude (高质量)
```

**预计成本节省：** 78-87%

---

## 💰 成本估算

### 日常使用 (1000 次/天)

| 场景 | 提供商 | 成本/天 | 成本/月 |
|------|--------|---------|---------|
| 日常对话 | 本地 LLM | $0 | $0 |
| 代码生成 | DeepSeek-Coder | $0 | $0 |
| 中文任务 | 智谱 AI | $0.1 | $3 |
| 实时信息 | Perplexity | $1-5 | $30-150 |
| 快速响应 | Groq | $0 | $0 |
| **总计** | **混合使用** | **$1-6** | **$30-180** |

### 优化后 vs 优化前

| 指标 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 日常任务 | $10/天 | $0/天 | **100%** |
| 中文任务 | $10/天 | $0.1/天 | **99%** |
| 实时信息 | $5/天 | $1-5/天 | **0-80%** |
| 复杂推理 | $20/天 | $5/天 | **75%** |
| **总计** | **$45/天** | **$6-10/天** | **78-87%** |

---

## 📊 API 调用示例

### 1. 使用 Galaxy Gateway（推荐）

```python
import httpx

async def chat(message: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8888/api/llm/chat",
            json={
                "messages": [{"role": "user", "content": message}],
                "model": "auto"  # 自动选择最优模型
            }
        )
        return response.json()
```

### 2. 指定提供商

```python
# 使用 Groq（免费，快速）
result = await chat_with_provider("groq", "快速回答问题")

# 使用智谱 AI（中文优秀）
result = await chat_with_provider("zhipu", "写一篇中文文章")

# 使用 Perplexity（实时搜索）
result = await chat_with_provider("perplexity", "今天的新闻")

# 使用 Claude（最强推理）
result = await chat_with_provider("claude", "复杂推理任务")
```

---

## 🔒 安全注意事项

### 1. API Keys 保护

```
✅ DO:
- 将 API Keys 保存在 .env 文件中
- 确保 .env 文件不被 Git 追踪
- 定期检查 API 使用量
- 设置使用限额

❌ DON'T:
- 不要在代码中硬编码 API Keys
- 不要将 API Keys 提交到 Git
- 不要在日志中打印 API Keys
- 不要与他人分享 API Keys
```

### 2. 网络安全

```bash
# 如果需要远程访问，使用 Tailscale VPN
# 不要直接暴露端口到公网

# 配置防火墙，只允许本地访问
GATEWAY_HOST=127.0.0.1
ONE_API_HOST=127.0.0.1
DASHBOARD_HOST=127.0.0.1
```

---

## ✅ 部署检查清单

- [ ] Git 代码已拉取到最新
- [ ] .env 文件已创建并填入 API Keys
- [ ] Podman 容器已启动（Memos + Redis）
- [ ] Ollama 已安装并拉取模型
- [ ] Galaxy 系统已启动
- [ ] 所有端口可以访问（8000, 8001, 8888）
- [ ] API Keys 已验证可用
- [ ] Dashboard 可以正常访问
- [ ] LLM 调用测试通过

---

## 🆘 故障排查

### 问题 1: 端口被占用

```powershell
# 查看端口占用
netstat -ano | findstr :8888

# 杀死进程
taskkill /PID <PID> /F

# 或修改端口
# 编辑 .env 文件
GATEWAY_PORT=8889
```

### 问题 2: Ollama 连接失败

```powershell
# 检查 Ollama 是否运行
ollama list

# 重启 Ollama
# 在任务管理器中结束 Ollama 进程
# 重新启动 Ollama
```

### 问题 3: API Key 无效

```powershell
# 检查 .env 文件中的 API Key 格式
# 确保没有多余的空格或换行

# 测试 API Key（以 Groq 为例）
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.groq.com/openai/v1/models
```

### 问题 4: 容器无法启动

```powershell
# 检查 Podman 状态
podman info

# 查看容器日志
podman logs memos
podman logs redis

# 重启容器
podman restart memos redis
```

---

## 📞 技术支持

如果遇到问题：

1. 查看日志文件：`E:\ufo-galaxy\logs\galaxy.log`
2. 访问 Dashboard：`http://localhost:8000`
3. 查看完整文档：
   - `API_CONFIGURATION_GUIDE.md` - API 配置指南
   - `FINAL_COMPLETE_REPORT.md` - 完整项目报告
   - `OPTIMIZATION_PROGRESS.md` - 优化进度
4. GitHub Issues：https://github.com/DannyFish-11/ufo-galaxy/issues

---

## 🎉 部署完成

恭喜！您的 UFO³ Galaxy v2.0 系统已经可以开始部署了。

**下一步：**
1. 按照上述步骤完成部署
2. 测试各个 API 提供商
3. 体验智能路由功能
4. 监控成本和使用情况
5. 根据需要调整路由策略

**系统状态：** ✅ 生产就绪  
**API 提供商：** 10 个全部集成完成  
**预计成本节省：** 78-87%

享受您的智能助手系统！🚀
