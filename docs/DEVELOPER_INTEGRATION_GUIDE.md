# 🚀 UFO Galaxy Fusion - 开发者集成手册

本手册旨在指导后续开发团队如何将 102 个真实的功能节点接入 **UFO Galaxy Fusion** 融合系统。

---

## 1. 核心集成逻辑

融合系统通过 **HTTP/JSON API** 与各个节点通信。每个节点需要作为一个独立的微服务运行，并暴露标准的 API 端点。

### 节点 API 标准协议

每个节点必须实现以下两个核心端点：

#### 1.1 健康检查 (`GET /health`)
- **用途**: 编排引擎用于检测节点是否在线。
- **响应格式**:
  ```json
  {
    "status": "healthy",
    "node_id": "Node_XX",
    "timestamp": 1706265600.0
  }
  ```

#### 1.2 命令执行 (`POST /execute`)
- **用途**: 接收并执行编排引擎下发的指令。
- **请求格式**:
  ```json
  {
    "command": "process",
    "params": {
      "key": "value"
    },
    "timestamp": 1706265600.0
  }
  ```
- **响应格式**:
  ```json
  {
    "success": true,
    "data": {
      "result": "..."
    },
    "error": null
  }
  ```

---

## 2. 节点代码修改指南

以 `nodes/Node_00_StateMachine/main.py` 为例，你需要将其包装为 API 服务。

### 推荐做法：使用 FastAPI 包装

```python
# nodes/Node_00_StateMachine/api_server.py
from fastapi import FastAPI
from .main import StateMachine  # 导入你的原功能类

app = FastAPI()
node = StateMachine()

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "Node_00"}

@app.post("/execute")
async def execute(request: dict):
    command = request.get("command")
    params = request.get("params", {})
    
    # 调用你原有的功能逻辑
    try:
        result = await node.process(command, **params)
        return {"success": true, "data": result}
    except Exception as e:
        return {"success": false, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
```

---

## 3. 批量部署建议

由于有 102 个节点，建议采用以下部署策略：

### 3.1 端口分配规则
系统已预设端口范围为 **9000 - 9118**：
- `Node_00` -> `9000`
- `Node_01` -> `9001`
- ...
- `Node_102` -> `9102`

### 3.2 使用统一网关 (推荐)
如果不想启动 102 个进程，可以编写一个统一网关，动态加载所有节点模块并在一个进程中运行。

---

## 4. 融合系统配置更新

当你的真实节点上线后，请确保 `config/topology.json` 中的 `api_url` 指向正确的地址。

```json
{
  "id": "Node_00",
  "api_url": "http://<YOUR_IP>:9000",
  ...
}
```

---

## 5. 验收测试

运行融合系统的端到端演示来验证集成是否成功：

```bash
python3 fusion/demo_e2e.py
```

如果看到 `✅ Task completed` 且执行路径正确，说明集成成功！

---

**如有疑问，请参考 `fusion/` 目录下的核心源码。**
**祝集成顺利！** 🚀
