"""
Node 19: Crypto
====================
加密工具
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 19 - Crypto", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class CryptoTools:
    def __init__(self):
        
        import hashlib
        from cryptography.fernet import Fernet
        
    async def _tool_hash(self, params):
        text = params.get("text", "").encode()
        algo = params.get("algorithm", "sha256")
        if algo == "md5":
            return {"success": True, "hash": hashlib.md5(text).hexdigest()}
        else:
            return {"success": True, "hash": hashlib.sha256(text).hexdigest()}
            
    async def _tool_encrypt(self, params):
        try:
            key = params.get("key", "").encode()
            f = Fernet(key)
            encrypted = f.encrypt(params.get("text", "").encode())
            return {"success": True, "ciphertext": encrypted.decode()}
        except Exception as e:
            return {"error": str(e)}

        self.initialized = True
        
    def get_tools(self):
        return [
            {"name": "encrypt", "description": "加密", "parameters": {'text': '明文', 'key': '密钥'}},
            {"name": "decrypt", "description": "解密", "parameters": {'ciphertext': '密文', 'key': '密钥'}},
            {"name": "hash", "description": "哈希", "parameters": {'text': '文本', 'algorithm': '算法 (md5/sha256)'}}
        ]
        
    async def call_tool(self, tool: str, params: dict):
        if not self.initialized:
            raise RuntimeError("Crypto not initialized")
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)

tools = CryptoTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "19", "name": "Crypto", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8019)
