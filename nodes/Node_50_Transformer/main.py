"""Node 50: Transformer - 真正的 NLU"""
import os, requests
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 50 - Transformer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

ONEAPI_BASE_URL = os.getenv("ONEAPI_BASE_URL", "http://localhost:8001/v1")
ONEAPI_API_KEY = os.getenv("ONEAPI_API_KEY", "")

class NLUTools:
    def __init__(self):
        self.base_url = ONEAPI_BASE_URL
        self.api_key = ONEAPI_API_KEY
        self.initialized = bool(self.api_key)
    def get_tools(self):
        return [
            {"name": "understand", "description": "理解自然语言命令", "parameters": {"text": "用户输入"}},
            {"name": "extract_intent", "description": "提取意图", "parameters": {"text": "用户输入"}},
            {"name": "extract_entities", "description": "提取实体", "parameters": {"text": "用户输入"}}
        ]
    async def call_tool(self, tool: str, params: dict):
        text = params.get("text", "")
        if tool == "understand":
            prompt = f"理解以下命令并返回 JSON 格式的意图和参数：\n{text}\n\n返回格式：{{\"intent\": \"...\", \"params\": {{...}}}}"
        elif tool == "extract_intent":
            prompt = f"提取以下文本的意图：\n{text}"
        elif tool == "extract_entities":
            prompt = f"提取以下文本中的实体：\n{text}"
        else:
            return {"error": "Unknown tool"}
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}]},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return {"success": True, "result": data["choices"][0]["message"]["content"]}
        except Exception as e:
            return {"error": str(e)}

tools = NLUTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "50", "name": "Transformer", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8050)
