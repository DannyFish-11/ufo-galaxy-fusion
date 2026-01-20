"""Node 42: CANbus - CAN 总线"""
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 42 - CANbus", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class CANbusTools:
    def __init__(self):
        self.initialized = True
    def get_tools(self):
        return [{"name": "send", "description": "发送数据", "parameters": {'can_id': 'ID', 'data': '数据'}}]
    async def call_tool(self, tool: str, params: dict):
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)
    async def _tool_send(self, params):
        return {"success": True, "message": "功能实现中 (演示模式)"}

tools = CANbusTools()

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "42", "name": "CANbus", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8042)
