"""
Node 14: FFmpeg
====================
音视频处理
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 14 - FFmpeg", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class FFmpegTools:
    def __init__(self):
        
        import subprocess
        
    async def _tool_convert(self, params):
        try:
            subprocess.run(["ffmpeg", "-i", params.get("input"), params.get("output")], check=True)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

        self.initialized = True
        
    def get_tools(self):
        return [
            {"name": "convert", "description": "转换格式", "parameters": {'input': '输入文件', 'output': '输出文件'}},
            {"name": "extract_audio", "description": "提取音频", "parameters": {'input': '视频文件', 'output': '音频文件'}}
        ]
        
    async def call_tool(self, tool: str, params: dict):
        if not self.initialized:
            raise RuntimeError("FFmpeg not initialized")
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)

tools = FFmpegTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "14", "name": "FFmpeg", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8014)
