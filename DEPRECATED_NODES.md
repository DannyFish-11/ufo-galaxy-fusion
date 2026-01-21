# 废弃节点列表

**更新日期：** 2026-01-22  
**原因：** 系统架构优化，删除低价值和重复功能节点

---

## 已删除节点（6个）

### 1. Node_09_Search ❌

**删除日期：** 2026-01-22  
**原因：** 与 Node 22 (BraveSearch) 和 Node 25 (GoogleSearch) 功能重复  
**替代方案：** 使用 Node 22 (BraveSearch) 作为主要搜索接口  
**影响：** 无，功能已被其他节点覆盖

**注意：** Node_09_Sandbox 保留，不受影响

---

### 2. Node_26_Reserved ❌

**删除日期：** 2026-01-22  
**原因：** 预留节点，未实现任何功能  
**替代方案：** 无需替代  
**影响：** 无

---

### 3. Node_27_Reserved ❌

**删除日期：** 2026-01-22  
**原因：** 预留节点，未实现任何功能  
**替代方案：** 无需替代  
**影响：** 无

---

### 4. Node_55_Simulation ❌

**删除日期：** 2026-01-22  
**原因：** 功能模糊，使用场景不明确，使用率低  
**替代方案：** 可以使用 Node 09 (Sandbox) 或按需重新实现  
**影响：** 低，使用场景少

---

### 5. Node_60_TemporalLogic ❌

**删除日期：** 2026-01-22  
**原因：** 时间逻辑推理使用场景少  
**替代方案：** 功能可以通过 Node 53 (GraphLogic) 实现  
**影响：** 低，可以通过图逻辑实现类似功能

---

### 6. Node_63_GameTheory ❌

**删除日期：** 2026-01-22  
**原因：** 博弈论使用场景少  
**替代方案：** 功能可以通过 Node 62 (ProbabilisticProgramming) 实现  
**影响：** 低，可以通过概率编程实现类似功能

---

## 迁移指南

如果您的代码依赖了以上节点，请参考以下迁移方案：

### Node_09_Search → Node 22 (BraveSearch)

**原代码：**
```python
response = await httpx.post(
    "http://localhost:8009/search",
    json={"query": "UFO Galaxy"}
)
```

**新代码：**
```python
response = await httpx.post(
    "http://localhost:8022/search",
    json={"query": "UFO Galaxy"}
)
```

---

### Node_55_Simulation → Node 09 (Sandbox)

**原代码：**
```python
response = await httpx.post(
    "http://localhost:8055/simulate",
    json={"code": "print('hello')"}
)
```

**新代码：**
```python
response = await httpx.post(
    "http://localhost:8009/execute",
    json={
        "code": "print('hello')",
        "language": "python"
    }
)
```

---

### Node_60_TemporalLogic → Node 53 (GraphLogic)

**原代码：**
```python
response = await httpx.post(
    "http://localhost:8060/temporal",
    json={"formula": "G(p -> F(q))"}
)
```

**新代码：**
```python
# 使用图逻辑表示时间关系
response = await httpx.post(
    "http://localhost:8053/reason",
    json={
        "graph": {
            "nodes": ["p", "q"],
            "edges": [{"from": "p", "to": "q", "type": "eventually"}]
        }
    }
)
```

---

### Node_63_GameTheory → Node 62 (ProbabilisticProgramming)

**原代码：**
```python
response = await httpx.post(
    "http://localhost:8063/nash_equilibrium",
    json={"payoff_matrix": [[3,0],[5,1]]}
)
```

**新代码：**
```python
# 使用概率编程模拟博弈
response = await httpx.post(
    "http://localhost:8062/infer",
    json={
        "model": "game_theory",
        "data": {"payoff_matrix": [[3,0],[5,1]]}
    }
)
```

---

## 恢复方法

如果您需要恢复已删除的节点，可以从 Git 历史中恢复：

```bash
# 查看删除前的提交
git log --oneline --all -- nodes/Node_XX_*

# 恢复特定节点
git checkout <commit_hash> -- nodes/Node_XX_*

# 或者查看历史文件
git show <commit_hash>:nodes/Node_XX_*/main.py
```

---

## 反馈

如果您遇到任何问题或需要帮助，请：
1. 查看本文档的迁移指南
2. 检查替代节点的文档
3. 提交 Issue 到 GitHub

---

**维护人：** Manus AI Agent  
**最后更新：** 2026-01-22
