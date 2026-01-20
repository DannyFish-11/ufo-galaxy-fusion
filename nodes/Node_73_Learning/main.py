"""
Node 73: Learning
====================
自主学习系统
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 73 - Learning", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class LearningTools:
    def __init__(self):
        
        self.feedback_log = []
        
    async def _tool_record_feedback(self, params):
        self.feedback_log.append(params)
        return {"success": True, "total_records": len(self.feedback_log)}
        
    async def _tool_get_stats(self, params):
        success_count = sum(1 for f in self.feedback_log if f.get("feedback") == "success")
        return {"success": True, "total": len(self.feedback_log), "success_rate": success_count / max(len(self.feedback_log), 1)}
        
    async def _tool_optimize(self, params):
        return {"success": True, "message": "参数优化完成 (演示模式)"}

        self.initialized = True
        
    def get_tools(self):
        return [
            {"name": "record_feedback", "description": "记录反馈", "parameters": {'task_id': '任务ID', 'feedback': '反馈 (success/failure)', 'details': '详情'}},
            {"name": "get_stats", "description": "获取统计", "parameters": {}},
            {"name": "optimize", "description": "优化参数", "parameters": {}}
        ]
        
    async def call_tool(self, tool: str, params: dict):
        if not self.initialized:
            raise RuntimeError("Learning not initialized")
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)

tools = LearningTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "73", "name": "Learning", "timestamp": datetime.now().isoformat()}

@app.get("/tools")
async def list_tools():
    return {"tools": tools.get_tools()}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    try:
        return {"success": True, "result": await tools.call_tool(request.get("tool"), request.get("params", {}))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8073)
