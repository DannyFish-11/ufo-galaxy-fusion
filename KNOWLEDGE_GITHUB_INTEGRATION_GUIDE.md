# UFO³ Galaxy - 知识库与 GitHub 集成指南

**版本**: 1.0.0  
**日期**: 2026-01-22  
**作者**: Manus AI

---

## 概述

本指南介绍如何使用 **Node_105 (Unified Knowledge Base)** 和 **Node_106 (GitHub Flow)** 实现强大的知识管理和 GitHub 工作流自动化。

---

## 快速开始

### 1. 启动节点

**Windows**:
```bash
start_knowledge_github_nodes.bat
```

**Linux/macOS**:
```bash
# 启动 Node_105
cd nodes/Node_105_UnifiedKnowledgeBase
python main.py &

# 启动 Node_106
cd nodes/Node_106_GitHubFlow
python main.py &
```

### 2. 验证节点

```bash
# 检查 Node_105
curl http://localhost:8105/health

# 检查 Node_106
curl http://localhost:8106/health
```

### 3. 运行集成测试

```bash
python test_knowledge_github_integration.py
```

---

## 核心功能

### Node_105: 统一知识库

#### 功能

1. **统一数据源**: 文件、URL、GitHub、Memos
2. **增强 RAG**: 关键词、向量、混合搜索
3. **代码知识库**: 支持多种编程语言
4. **RAG 问答**: 基于检索的问答

#### 使用示例

**添加文本知识**:
```bash
curl -X POST http://localhost:8105/add \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "content": "量子计算是一种利用量子力学原理进行计算的技术。",
    "metadata": {"category": "quantum"}
  }'
```

**搜索知识**:
```bash
curl -X POST http://localhost:8105/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "量子计算",
    "top_k": 5,
    "search_type": "hybrid"
  }'
```

**RAG 问答**:
```bash
curl -X POST http://localhost:8105/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "什么是量子计算？",
    "top_k": 3
  }'
```

### Node_106: GitHub 工作流

#### 功能

1. **Issue 驱动开发**: 自动创建 Issue
2. **自动化代码生成**: 根据 Issue 生成代码
3. **自动化代码审查**: 调用 LLM 审查代码
4. **代码知识库集成**: 与 Node_105 联动

#### 使用示例

**创建 Issue**:
```bash
curl -X POST http://localhost:8106/create_issue \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "username/repo",
    "title": "添加用户认证功能",
    "body": "需要实现基于 JWT 的用户认证系统",
    "labels": ["enhancement"]
  }'
```

**生成代码**:
```bash
curl -X POST http://localhost:8106/generate_code \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "username/repo",
    "issue_number": 1,
    "branch_name": "feature/user-auth"
  }'
```

**审查 PR**:
```bash
curl -X POST http://localhost:8106/review_pr \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "username/repo",
    "pr_number": 1
  }'
```

---

## 集成场景

### 场景 1: 学术研究工作流

**目标**: 自动化学术研究流程

**步骤**:

1. **搜索论文** (Node_97):
   ```bash
   curl -X POST http://localhost:8097/search \
     -H "Content-Type: application/json" \
     -d '{
       "query": "quantum machine learning",
       "source": "arxiv",
       "max_results": 10
     }'
   ```

2. **保存到知识库** (Node_105):
   ```bash
   curl -X POST http://localhost:8105/add \
     -H "Content-Type: application/json" \
     -d '{
       "source_type": "text",
       "content": "论文内容...",
       "metadata": {"source": "arxiv", "category": "research"}
     }'
   ```

3. **生成研究报告** (Node_104):
   ```bash
   curl -X POST http://localhost:8104/explore \
     -H "Content-Type: application/json" \
     -d '{
       "query": "量子机器学习的最新进展",
       "depth": 3
     }'
   ```

4. **创建 GitHub Issue** (Node_106):
   ```bash
   curl -X POST http://localhost:8106/create_issue \
     -H "Content-Type: application/json" \
     -d '{
       "repo": "myresearch/project",
       "title": "实现量子机器学习算法",
       "body": "根据研究报告实现 QAOA 算法"
     }'
   ```

### 场景 2: 代码知识库

**目标**: 将 GitHub 仓库作为知识库

**步骤**:

1. **索引仓库到知识库**:
   ```bash
   curl -X POST http://localhost:8106/index_repo \
     -H "Content-Type: application/json" \
     -d '{
       "repo_url": "https://github.com/myproject/backend.git"
     }'
   ```

2. **搜索代码**:
   ```bash
   curl -X POST http://localhost:8105/search \
     -H "Content-Type: application/json" \
     -d '{
       "query": "JWT authentication",
       "top_k": 5,
       "search_type": "hybrid"
     }'
   ```

3. **代码问答**:
   ```bash
   curl -X POST http://localhost:8105/ask \
     -H "Content-Type: application/json" \
     -d '{
       "question": "如何实现 JWT 认证？",
       "top_k": 3
     }'
   ```

### 场景 3: Issue 驱动开发

**目标**: 从任务到代码的自动化流程

**步骤**:

1. **从 Memos 获取任务**:
   ```bash
   # 假设 Memos 中有任务：
   # TODO: 添加用户认证功能
   ```

2. **创建 GitHub Issue**:
   ```bash
   curl -X POST http://localhost:8106/create_issue \
     -H "Content-Type: application/json" \
     -d '{
       "repo": "myproject/backend",
       "title": "添加用户认证功能",
       "body": "实现 JWT 生成和验证..."
     }'
   ```

3. **生成代码**:
   ```bash
   curl -X POST http://localhost:8106/generate_code \
     -H "Content-Type: application/json" \
     -d '{
       "repo": "myproject/backend",
       "issue_number": 1
     }'
   ```

4. **手动创建分支、提交代码、创建 PR**

5. **自动审查 PR**:
   ```bash
   curl -X POST http://localhost:8106/review_pr \
     -H "Content-Type: application/json" \
     -d '{
       "repo": "myproject/backend",
       "pr_number": 1
     }'
   ```

---

## 配置

### Mock 模式（默认）

**特点**:
- 无需任何配置
- 开箱即用
- 适合快速测试和演示

**限制**:
- 向量搜索退化为关键词搜索
- 代码生成较简单
- 无法访问真实的 GitHub API

### 真实模式

**Node_105 真实模式**:

1. 安装依赖:
   ```bash
   pip install chromadb sentence-transformers
   ```

2. 修改 `nodes/Node_105_UnifiedKnowledgeBase/main.py`:
   ```python
   self.use_mock = False
   ```

3. 重启 Node_105

**Node_106 真实模式**:

1. 创建 GitHub Token:
   - 访问 https://github.com/settings/tokens
   - 生成新的 Token（选择 `repo` 权限）

2. 设置环境变量:
   ```bash
   export GITHUB_TOKEN=your_github_token
   ```

3. 修改 `nodes/Node_106_GitHubFlow/main.py`:
   ```python
   self.use_mock = False
   ```

4. 重启 Node_106

---

## 故障排查

### 问题 1: 节点无法启动

**症状**: 运行 `python main.py` 后报错

**原因**: 依赖未安装

**解决**:
```bash
pip install fastapi uvicorn httpx pydantic
```

### 问题 2: 无法连接到节点

**症状**: `curl http://localhost:8105/health` 失败

**原因**: 节点未启动或端口被占用

**解决**:
```bash
# 检查端口占用
netstat -ano | findstr 8105  # Windows
lsof -i :8105                # Linux/macOS

# 杀死占用端口的进程或更换端口
```

### 问题 3: 集成测试失败

**症状**: `test_knowledge_github_integration.py` 部分测试失败

**原因**: 节点未启动

**解决**:
```bash
# 启动节点
start_knowledge_github_nodes.bat  # Windows

# 或手动启动
cd nodes/Node_105_UnifiedKnowledgeBase && python main.py &
cd nodes/Node_106_GitHubFlow && python main.py &
```

### 问题 4: GitHub API 请求失败

**症状**: Node_106 创建 Issue 失败

**原因**: GitHub Token 无效或权限不足

**解决**:
```bash
# 检查 Token
echo $GITHUB_TOKEN

# 重新生成 Token（确保权限正确）
```

---

## 性能优化

### Node_105 优化

1. **使用真实的向量数据库**: ChromaDB、Faiss、Pinecone
2. **使用更好的 Embedding 模型**: OpenAI、Sentence-Transformers
3. **启用缓存**: 缓存搜索结果
4. **批量处理**: 批量添加知识

### Node_106 优化

1. **使用更好的 LLM**: GPT-4、DeepSeek
2. **启用并发**: 并发处理多个 Issue
3. **缓存代码模板**: 缓存常用的代码模板
4. **集成 CI/CD**: 自动触发测试和部署

---

## 安全注意事项

1. **GitHub Token**: 不要将 Token 提交到代码仓库
2. **API 密钥**: 使用环境变量存储 API 密钥
3. **访问控制**: 限制节点的访问权限
4. **数据加密**: 加密敏感数据

---

## 未来增强

### Node_105

1. 支持更多 Embedding 模型
2. 支持更多向量数据库
3. 支持更多文档格式
4. 支持增量更新
5. 支持权限管理

### Node_106

1. 支持更多 Git 操作
2. 支持更多代码审查规则
3. 支持更多编程语言
4. 支持 CI/CD 集成
5. 支持团队协作

---

## 总结

通过 **Node_105** 和 **Node_106** 的集成，您可以实现：

1. **强大的知识管理**: 统一管理文档、代码、网页、笔记
2. **自动化工作流**: 从任务到代码的自动化流程
3. **代码知识库**: 将代码作为知识库进行管理
4. **智能问答**: 基于知识库的 RAG 问答

这两个节点是 UFO³ Galaxy 系统的重要组成部分，为您提供了强大的知识管理和开发自动化能力。

---

**Node_105 + Node_106** | Knowledge & GitHub Integration | 2026-01-22
