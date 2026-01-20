"""
Node 44: NFC - 近场通信
"""
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 44 - NFC", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

nfc = None
try:
    import nfc as _nfc
    nfc = _nfc
except ImportError:
    pass

class WriteRequest(BaseModel):
    data: str
    timeout: float = 5.0

@app.get("/health")
async def health():
    return {"status": "healthy" if nfc else "degraded", "node_id": "44", "name": "NFC", "nfc_available": nfc is not None, "timestamp": datetime.now().isoformat()}

@app.get("/read")
async def read_tag(timeout: float = 5.0):
    if not nfc:
        raise HTTPException(status_code=503, detail="nfcpy not installed")
    try:
        clf = nfc.ContactlessFrontend("usb")
        tag = clf.connect(rdwr={"on-connect": lambda tag: False}, terminate=lambda: False)
        if tag:
            data = tag.ndef.message if tag.ndef else None
            clf.close()
            return {"success": True, "tag_type": str(type(tag).__name__), "data": str(data) if data else None}
        clf.close()
        return {"success": False, "message": "No tag found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/write")
async def write_tag(request: WriteRequest):
    if not nfc:
        raise HTTPException(status_code=503, detail="nfcpy not installed")
    try:
        clf = nfc.ContactlessFrontend("usb")
        tag = clf.connect(rdwr={"on-connect": lambda tag: False})
        if tag and tag.ndef:
            import ndef
            tag.ndef.records = [ndef.TextRecord(request.data)]
            clf.close()
            return {"success": True, "data": request.data}
        clf.close()
        return {"success": False, "message": "No writable tag found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "read": return await read_tag(params.get("timeout", 5.0))
    elif tool == "write": return await write_tag(WriteRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8044)
