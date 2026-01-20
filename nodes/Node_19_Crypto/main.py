"""Node 19: Crypto - 加密工具"""
import os, hashlib, base64, secrets
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 19 - Crypto", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# 尝试导入加密库
cryptography = None
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    cryptography = True
except ImportError:
    pass

class HashRequest(BaseModel):
    data: str
    algorithm: str = "sha256"

class EncryptRequest(BaseModel):
    data: str
    key: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "19", "name": "Crypto", "cryptography_available": cryptography is not None, "timestamp": datetime.now().isoformat()}

@app.post("/hash")
async def hash_data(request: HashRequest):
    try:
        if request.algorithm == "md5":
            h = hashlib.md5(request.data.encode()).hexdigest()
        elif request.algorithm == "sha1":
            h = hashlib.sha1(request.data.encode()).hexdigest()
        elif request.algorithm == "sha256":
            h = hashlib.sha256(request.data.encode()).hexdigest()
        elif request.algorithm == "sha512":
            h = hashlib.sha512(request.data.encode()).hexdigest()
        else:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {request.algorithm}")
        return {"success": True, "hash": h, "algorithm": request.algorithm}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/encrypt")
async def encrypt(request: EncryptRequest):
    if not cryptography:
        raise HTTPException(status_code=503, detail="cryptography not installed. Run: pip install cryptography")
    try:
        key = request.key.encode() if request.key else Fernet.generate_key()
        f = Fernet(key if len(key) == 44 else base64.urlsafe_b64encode(hashlib.sha256(key).digest()))
        encrypted = f.encrypt(request.data.encode())
        return {"success": True, "encrypted": encrypted.decode(), "key": key.decode() if isinstance(key, bytes) else key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decrypt")
async def decrypt(data: str, key: str):
    if not cryptography:
        raise HTTPException(status_code=503, detail="cryptography not installed")
    try:
        key_bytes = key.encode()
        f = Fernet(key_bytes if len(key_bytes) == 44 else base64.urlsafe_b64encode(hashlib.sha256(key_bytes).digest()))
        decrypted = f.decrypt(data.encode())
        return {"success": True, "decrypted": decrypted.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate_key")
async def generate_key():
    return {"success": True, "key": Fernet.generate_key().decode() if cryptography else secrets.token_urlsafe(32)}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "hash": return await hash_data(HashRequest(**params))
    elif tool == "encrypt": return await encrypt(EncryptRequest(**params))
    elif tool == "decrypt": return await decrypt(params.get("data"), params.get("key"))
    elif tool == "generate_key": return await generate_key()
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8019)
