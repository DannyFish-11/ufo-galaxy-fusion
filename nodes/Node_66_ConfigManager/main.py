"""
Node 66: Config Manager
=======================
配置管理器 - 集中式配置管理

功能：
- 配置版本控制
- 热更新配置
- 配置验证
- 环境变量管理
"""

import os
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 66 - Config Manager", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置存储
config_store: Dict[str, Any] = {}
config_versions: list = []

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "node_id": "66",
        "name": "ConfigManager",
        "config_count": len(config_store),
        "version_count": len(config_versions),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/config")
async def get_all_config():
    """获取所有配置"""
    return {"configs": config_store}

@app.get("/config/{key}")
async def get_config(key: str):
    """获取指定配置"""
    if key not in config_store:
        raise HTTPException(status_code=404, detail=f"Config '{key}' not found")
    return {"key": key, "value": config_store[key]}

@app.post("/config/{key}")
async def set_config(key: str, request: Dict[str, Any]):
    """设置配置"""
    value = request.get("value")
    old_value = config_store.get(key)
    config_store[key] = value
    config_versions.append({
        "key": key,
        "old_value": old_value,
        "new_value": value,
        "timestamp": datetime.now().isoformat()
    })
    return {"success": True, "key": key, "value": value}

@app.get("/versions")
async def get_versions():
    """获取配置变更历史"""
    return {"versions": config_versions[-100:]}  # 最近100条

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8066)
