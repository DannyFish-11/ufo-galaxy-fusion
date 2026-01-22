# AgentCPM 和 Memos 集成现状报告

**日期**: 2026-01-22  
**作者**: Manus AI  
**项目**: UFO³ Galaxy

---

## 📊 现状评估

### ✅ AgentCPM

**状态**: ⭐⭐⭐⭐⭐ 已有完整分析，但**未集成**

| 项目 | 状态 | 说明 |
|-----|------|------|
| **分析文档** | ✅ 已完成 | `AGENTCPM_ANALYSIS.md` |
| **源代码研究** | ✅ 已完成 | GitHub 仓库已访问 |
| **集成节点** | ❌ 未实现 | 需要创建 Node_104 |
| **AgentDock 部署** | ❌ 未部署 | 需要 Docker 部署 |
| **API 测试** | ❌ 未测试 | 需要验证可用性 |

**关键发现**:
1. AgentCPM-Explore（4B 参数）- 深度搜索智能体
2. AgentCPM-Report（8B 参数）- 深度研究报告生成
3. AgentDock - 统一工具沙盒（MCP 协议）
4. 完全开源（Apache-2.0）
5. 支持 Docker 一键部署

---

### ✅ Memos

**状态**: ⭐⭐⭐⭐ 已集成到 Node_80，但**功能未充分利用**

| 项目 | 状态 | 说明 |
|-----|------|------|
| **集成节点** | ✅ 已实现 | `nodes/Node_80_MemorySystem` |
| **部署方案** | ✅ 已完成 | Podman/Docker 部署 |
| **API 文档** | ✅ 已获取 | REST + gRPC API |
| **实际使用** | ⚠️ 部分使用 | 仅作为长期记忆存储 |
| **学术功能** | ❌ 未开发 | 未用于学术笔记管理 |

**关键发现**:
1. Memos 已集成到 Node_80 的长期记忆层
2. 支持 REST API（`/api/v1`）
3. Bearer Token 认证
4. 支持标签、全文搜索、Markdown
5. 55.3k GitHub Stars，非常成熟

---

## 🎯 集成方案

### 方案 A：AgentCPM 集成（高优先级）

#### 目标

将 AgentCPM-Explore 和 AgentCPM-Report 集成到 UFO³ Galaxy，提供深度搜索和研究报告生成能力。

#### 实施步骤

**第一阶段：部署 AgentDock（1-2 天）**

1. 克隆 AgentCPM 仓库
2. 使用 Docker Compose 部署 AgentDock
3. 验证 MCP 工具服务（http://localhost:8000）
4. 配置工具参数（`config.toml`）

**部署命令**:
```bash
# 克隆仓库
git clone https://github.com/OpenBMB/AgentCPM.git
cd AgentCPM/AgentCPM-Explore/AgentDock

# 启动 AgentDock
docker compose up -d

# 验证服务
curl http://localhost:8000/health
```

**第二阶段：创建 Node_104_AgentCPM（2-3 天）**

1. 创建节点目录结构
2. 实现 AgentCPM-Explore 接口
3. 实现 AgentCPM-Report 接口
4. 集成 AgentDock MCP 服务
5. 提供统一的 REST API

**API 设计**:
```python
# 深度搜索
POST /deep_search
{
  "query": "量子机器学习的最新进展",
  "max_turns": 100,
  "tools": ["search", "arxiv", "scholar"]
}

# 深度研究报告
POST /deep_research
{
  "topic": "量子计算在机器学习中的应用",
  "depth": "deep",  # deep|medium|shallow
  "output_format": "markdown"
}
```

**第三阶段：集成到 Galaxy Gateway（1 天）**

1. 在 Gateway 中添加 AgentCPM 路由
2. 实现任务分发逻辑（长程任务 → AgentCPM）
3. 实现结果缓存
4. 添加监控和日志

**第四阶段：测试和验证（1-2 天）**

1. 测试深度搜索功能
2. 测试研究报告生成
3. 测试 100+ 轮交互
4. 性能基准测试
5. 反复核实可用性

**第五阶段：文档和推送（1 天）**

1. 编写使用文档
2. 编写部署指南
3. 推送到 GitHub
4. 更新 README

---

### 方案 B：Memos 学术增强（中优先级）

#### 目标

充分利用 Memos 的能力，将其打造为学术笔记和文献管理系统。

#### 实施步骤

**第一阶段：增强 Node_80（1-2 天）**

1. 添加学术笔记专用 API
2. 实现论文笔记模板
3. 实现标签自动分类
4. 实现引用链接管理

**API 设计**:
```python
# 添加论文笔记
POST /academic/paper_note
{
  "paper_id": "arxiv:2401.12345",
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "abstract": "摘要",
  "notes": "我的笔记",
  "tags": ["深度学习", "计算机视觉"],
  "citations": ["arxiv:2301.11111", "arxiv:2302.22222"]
}

# 搜索论文笔记
GET /academic/paper_notes?query=深度学习&tags=计算机视觉

# 获取引用网络
GET /academic/citation_network/{paper_id}
```

**第二阶段：集成到学术搜索（1 天）**

1. 将搜索到的论文自动保存到 Memos
2. 生成论文摘要并保存
3. 自动提取关键概念作为标签

**第三阶段：可视化和导出（1 天）**

1. 实现笔记可视化（时间线、标签云）
2. 实现引用网络可视化
3. 实现导出功能（Markdown、PDF、BibTeX）

---

### 方案 C：AgentCPM + Memos 融合（最高优先级）

#### 目标

将 AgentCPM 的深度研究能力与 Memos 的笔记管理能力融合，打造完整的学术研究工作流。

#### 工作流

```
用户输入研究主题
    ↓
AgentCPM-Explore 深度搜索
    ↓
自动保存到 Memos（论文列表）
    ↓
AgentCPM-Report 生成研究报告
    ↓
保存到 Memos（完整报告）
    ↓
用户查看和编辑
```

#### 实施步骤

**第一阶段：打通数据流（1 天）**

1. AgentCPM 搜索结果 → Memos 笔记
2. Memos 笔记 → AgentCPM 上下文
3. AgentCPM 报告 → Memos 长文档

**第二阶段：实现自动化工作流（2 天）**

1. 一键触发：研究主题 → 完整报告
2. 自动标签：根据内容自动打标签
3. 自动链接：自动建立论文之间的引用关系

**第三阶段：增强交互（1 天）**

1. 在 Memos 中直接触发 AgentCPM 搜索
2. 在 Memos 中直接生成报告
3. 在 Memos 中查看搜索进度

---

## 🔧 技术细节

### AgentCPM 部署要求

| 组件 | 要求 | 说明 |
|-----|------|------|
| **Docker** | 必需 | 用于部署 AgentDock |
| **GPU** | 可选 | 本地部署模型时需要 |
| **内存** | 8GB+ | AgentDock + 模型 |
| **存储** | 10GB+ | 模型权重 + 工具数据 |
| **网络** | 必需 | 访问 API 或下载模型 |

### Memos API 使用

**认证**:
```bash
# 获取 Access Token（在 Memos 设置中生成）
export MEMOS_TOKEN="your_access_token"

# 使用 Token
curl -H "Authorization: Bearer $MEMOS_TOKEN" \
  https://localhost:5230/api/v1/memos
```

**创建笔记**:
```bash
curl -X POST https://localhost:5230/api/v1/memos \
  -H "Authorization: Bearer $MEMOS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# 论文笔记\n\n**标题**: ...\n\n**摘要**: ...",
    "visibility": "PRIVATE"
  }'
```

**搜索笔记**:
```bash
curl -X GET "https://localhost:5230/api/v1/memos?filter=content contains '深度学习'" \
  -H "Authorization: Bearer $MEMOS_TOKEN"
```

---

## 📊 优先级排序

| 方案 | 优先级 | 预计时间 | 价值 |
|-----|--------|---------|------|
| **方案 C（融合）** | ⭐⭐⭐⭐⭐ | 4-5 天 | 最高 |
| **方案 A（AgentCPM）** | ⭐⭐⭐⭐⭐ | 6-8 天 | 很高 |
| **方案 B（Memos 增强）** | ⭐⭐⭐⭐ | 3-4 天 | 高 |

**建议**: 先实现方案 A（AgentCPM 集成），然后实现方案 B（Memos 增强），最后实现方案 C（融合）。

---

## 🎯 反复核实清单

### AgentCPM 核实项

- [ ] AgentDock 是否成功启动？
- [ ] MCP 工具服务是否可访问？
- [ ] AgentCPM-Explore 是否能执行深度搜索？
- [ ] AgentCPM-Report 是否能生成报告？
- [ ] 100+ 轮交互是否稳定？
- [ ] API 响应时间是否可接受？
- [ ] 错误处理是否完善？

### Memos 核实项

- [ ] Memos 服务是否正常运行？
- [ ] REST API 是否可访问？
- [ ] Bearer Token 认证是否有效？
- [ ] 创建笔记是否成功？
- [ ] 搜索功能是否正常？
- [ ] 标签功能是否正常？
- [ ] 全文搜索是否准确？

### 集成核实项

- [ ] Node_104 是否成功启动？
- [ ] Gateway 路由是否正确？
- [ ] 数据流是否打通？
- [ ] 自动化工作流是否正常？
- [ ] 性能是否满足要求？
- [ ] 文档是否完整？
- [ ] 代码是否已推送到 GitHub？

---

## 📝 总结

### 现状

1. **AgentCPM**: 已有完整分析，但**未集成**
2. **Memos**: 已集成到 Node_80，但**功能未充分利用**

### 建议

1. **立即开始**: 部署 AgentDock 和创建 Node_104
2. **系统推进**: 按照方案 A → 方案 B → 方案 C 的顺序实施
3. **反复核实**: 每个阶段完成后进行全面测试
4. **节点推送**: 每完成一个节点立即推送到 GitHub

### 预期效果

完成后，UFO³ Galaxy 将具备：

1. **深度搜索能力**: 通过 AgentCPM-Explore 实现 100+ 轮交互的深度搜索
2. **研究报告生成**: 通过 AgentCPM-Report 自动生成高质量研究报告
3. **学术笔记管理**: 通过 Memos 管理论文笔记和文献
4. **完整工作流**: 从搜索到报告的一站式学术研究工作流

---

**下一步**: 开始实施方案 A（AgentCPM 集成）
