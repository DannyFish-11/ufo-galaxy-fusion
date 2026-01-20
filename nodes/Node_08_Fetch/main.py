"""Node 08: Fetch - HTTP Client"""
import requests
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 08 - Fetch", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class FetchTools:
    def get_tools(self):
        return [
            {"name": "get", "description": "GET 请求", "parameters": {"url": "URL", "headers": "请求头 (可选)"}},
            {"name": "post", "description": "POST 请求", "parameters": {"url": "URL", "data": "数据", "headers": "请求头 (可选)"}},
            {"name": "download", "description": "下载文件", "parameters": {"url": "URL", "save_path": "保存路径"}}
        ]
    async def call_tool(self, tool: str, params: dict):
        url = params.get("url", "")
        headers = params.get("headers", {})
        if tool == "get":
            try:
                r = requests.get(url, headers=headers, timeout=30)
                r.raise_for_status()
                return {"success": True, "status_code": r.status_code, "content": r.text[:1000]}
            except Exception as e:
                return {"error": str(e)}
        elif tool == "post":
            try:
                data = params.get("data", {})
                r = requests.post(url, json=data, headers=headers, timeout=30)
                r.raise_for_status()
                return {"success": True, "status_code": r.status_code, "content": r.text[:1000]}
            except Exception as e:
                return {"error": str(e)}
        elif tool == "download":
            try:
                r = requests.get(url, stream=True, timeout=60)
                r.raise_for_status()
                save_path = params.get("save_path", "/tmp/download")
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return {"success": True, "path": save_path, "size": os.path.getsize(save_path)}
            except Exception as e:
                return {"error": str(e)}
        return {"error": "Unknown tool"}

tools = FetchTools()

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "08", "name": "Fetch", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8008)
