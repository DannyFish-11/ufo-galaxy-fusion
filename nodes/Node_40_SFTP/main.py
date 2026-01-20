"""Node 40: SFTP - 文件传输"""
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 40 - SFTP", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

paramiko = None
try:
    import paramiko as _paramiko
    paramiko = _paramiko
except ImportError:
    pass

class SFTPRequest(BaseModel):
    host: str
    username: str
    password: Optional[str] = None
    key_path: Optional[str] = None
    port: int = 22

class TransferRequest(SFTPRequest):
    local_path: str
    remote_path: str

@app.get("/health")
async def health():
    return {"status": "healthy" if paramiko else "degraded", "node_id": "40", "name": "SFTP", "paramiko_available": paramiko is not None, "timestamp": datetime.now().isoformat()}

def get_sftp(request: SFTPRequest):
    if not paramiko:
        raise HTTPException(status_code=503, detail="paramiko not installed")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if request.key_path:
        key = paramiko.RSAKey.from_private_key_file(request.key_path)
        client.connect(request.host, port=request.port, username=request.username, pkey=key)
    else:
        client.connect(request.host, port=request.port, username=request.username, password=request.password)
    return client, client.open_sftp()

@app.post("/upload")
async def upload(request: TransferRequest):
    try:
        client, sftp = get_sftp(request)
        sftp.put(request.local_path, request.remote_path)
        sftp.close()
        client.close()
        return {"success": True, "action": "upload", "local": request.local_path, "remote": request.remote_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/download")
async def download(request: TransferRequest):
    try:
        client, sftp = get_sftp(request)
        sftp.get(request.remote_path, request.local_path)
        sftp.close()
        client.close()
        return {"success": True, "action": "download", "local": request.local_path, "remote": request.remote_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/list")
async def list_dir(request: SFTPRequest, path: str = "."):
    try:
        client, sftp = get_sftp(request)
        files = sftp.listdir_attr(path)
        result = [{"name": f.filename, "size": f.st_size, "is_dir": f.st_mode & 0o40000 != 0} for f in files]
        sftp.close()
        client.close()
        return {"success": True, "path": path, "files": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "upload": return await upload(TransferRequest(**params))
    elif tool == "download": return await download(TransferRequest(**params))
    elif tool == "list": return await list_dir(SFTPRequest(**{k: v for k, v in params.items() if k != "path"}), params.get("path", "."))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8040)
