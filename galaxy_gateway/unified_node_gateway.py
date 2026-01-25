#!/usr/bin/env python3
"""
UFO Galaxy Fusion - Unified Node Gateway

统一节点网关

核心职责:
1. 动态加载 102 个节点的业务逻辑 (nodes/ 目录)
2. 提供统一的 HTTP API 路由 (/api/nodes/{node_id}/execute)
3. 隔离节点执行环境，提供统一的错误处理
4. 消除管理 102 个独立进程的复杂度

作者: Manus AI
日期: 2026-01-26
版本: 1.0.0
"""

import os
import sys
import importlib
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UnifiedGateway")

app = FastAPI(title="UFO Galaxy Unified Node Gateway")

# 节点实例缓存
node_instances: Dict[str, Any] = {}

class ExecuteRequest(BaseModel):
    command: str
    params: Dict[str, Any] = {}

def load_nodes():
    """动态扫描并加载 nodes/ 目录下的所有节点"""
    nodes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nodes")
    if not os.path.exists(nodes_dir):
        logger.error(f"❌ Nodes directory not found: {nodes_dir}")
        return

    sys.path.append(nodes_dir)
    
    # 扫描 Node_XX 格式的目录
    for item in os.listdir(nodes_dir):
        if item.startswith("Node_") and os.path.isdir(os.path.join(nodes_dir, item)):
            node_id = item.split('_')[0] + "_" + item.split('_')[1] # 提取 Node_XX
            try:
                # 尝试导入 main.py
                module_path = f"{item}.main"
                module = importlib.import_lib(module_path)
                
                # 寻找节点类或初始化函数
                # 假设每个 main.py 都有一个与目录名相关的类，或者一个统一的 get_instance()
                instance = None
                if hasattr(module, "get_instance"):
                    instance = module.get_instance()
                elif hasattr(module, "Node"):
                    instance = module.Node()
                
                if instance:
                    node_instances[node_id] = instance
                    logger.info(f"✅ Loaded node: {node_id} from {item}")
                else:
                    logger.warning(f"⚠️  Node {node_id} loaded but no instance found (missing get_instance or Node class)")
            except Exception as e:
                logger.error(f"❌ Failed to load node {node_id}: {e}")

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Unified Node Gateway...")
    load_nodes()
    logger.info(f"✨ Total nodes loaded: {len(node_instances)}")

@app.get("/health")
async def global_health():
    return {"status": "healthy", "loaded_nodes": len(node_instances)}

@app.get("/api/nodes/{node_id}/health")
async def node_health(node_id: str):
    if node_id not in node_instances:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    return {"status": "healthy", "node_id": node_id}

@app.post("/api/nodes/{node_id}/execute")
async def execute_on_node(node_id: str, request: ExecuteRequest):
    if node_id not in node_instances:
        raise HTTPException(status_code=404, detail=f"Node {node_id} not found")
    
    instance = node_instances[node_id]
    
    try:
        # 统一调用接口：假设所有节点都有 process 或 execute 方法
        method = None
        for m in ["process", "execute", "run"]:
            if hasattr(instance, m):
                method = getattr(instance, m)
                break
        
        if not method:
            raise HTTPException(status_code=500, detail=f"Node {node_id} has no executable method")
            
        # 执行逻辑
        if asyncio.iscoroutinefunction(method):
            result = await method(request.command, **request.params)
        else:
            result = method(request.command, **request.params)
            
        return {"success": True, "node_id": node_id, "data": result}
        
    except Exception as e:
        logger.error(f"❌ Error executing on {node_id}: {e}")
        return {"success": False, "node_id": node_id, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    # 统一运行在 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)
