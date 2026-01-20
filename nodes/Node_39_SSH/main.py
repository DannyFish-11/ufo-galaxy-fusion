"""Node 39: SSH - 远程执行"""
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 39 - SSH", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

paramiko = None
try:
    import paramiko as _paramiko
    paramiko = _paramiko
except ImportError:
    pass

class SSHRequest(BaseModel):
    host: str
    username: str
    password: Optional[str] = None
    key_path: Optional[str] = None
    command: str
    port: int = 22

@app.get("/health")
async def health():
    return {"status": "healthy" if paramiko else "degraded", "node_id": "39", "name": "SSH", "paramiko_available": paramiko is not None, "timestamp": datetime.now().isoformat()}

@app.post("/execute")
async def execute(request: SSHRequest):
    if not paramiko:
        raise HTTPException(status_code=503, detail="paramiko not installed. Run: pip install paramiko")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if request.key_path:
            key = paramiko.RSAKey.from_private_key_file(request.key_path)
            client.connect(request.host, port=request.port, username=request.username, pkey=key)
        else:
            client.connect(request.host, port=request.port, username=request.username, password=request.password)
        
        stdin, stdout, stderr = client.exec_command(request.command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        exit_code = stdout.channel.recv_exit_status()
        client.close()
        
        return {"success": True, "output": output, "error": error, "exit_code": exit_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "execute": return await execute(SSHRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8039)
