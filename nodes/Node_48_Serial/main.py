"""
Node 48: Serial - 串口通信
"""
import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 48 - Serial", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

serial = None
try:
    import serial as _serial
    serial = _serial
except ImportError:
    pass

connections = {}

class ConnectRequest(BaseModel):
    port: str
    baudrate: int = 9600
    timeout: float = 1.0

class SendRequest(BaseModel):
    port: str
    data: str
    encoding: str = "utf-8"

class ReceiveRequest(BaseModel):
    port: str
    size: int = 1024

@app.get("/health")
async def health():
    return {"status": "healthy" if serial else "degraded", "node_id": "48", "name": "Serial", "pyserial_available": serial is not None, "timestamp": datetime.now().isoformat()}

@app.get("/ports")
async def list_ports():
    if not serial:
        raise HTTPException(status_code=503, detail="pyserial not installed")
    from serial.tools import list_ports
    ports = [{"device": p.device, "description": p.description, "hwid": p.hwid} for p in list_ports.comports()]
    return {"success": True, "ports": ports}

@app.post("/connect")
async def connect(request: ConnectRequest):
    if not serial:
        raise HTTPException(status_code=503, detail="pyserial not installed")
    try:
        ser = serial.Serial(request.port, request.baudrate, timeout=request.timeout)
        connections[request.port] = ser
        return {"success": True, "port": request.port, "baudrate": request.baudrate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/disconnect")
async def disconnect(port: str):
    if port in connections:
        connections[port].close()
        del connections[port]
        return {"success": True, "port": port}
    raise HTTPException(status_code=404, detail="Port not connected")

@app.post("/send")
async def send(request: SendRequest):
    if request.port not in connections:
        raise HTTPException(status_code=404, detail="Port not connected")
    ser = connections[request.port]
    ser.write(request.data.encode(request.encoding))
    return {"success": True, "sent": len(request.data)}

@app.post("/receive")
async def receive(request: ReceiveRequest):
    if request.port not in connections:
        raise HTTPException(status_code=404, detail="Port not connected")
    ser = connections[request.port]
    data = ser.read(request.size)
    return {"success": True, "data": data.decode("utf-8", errors="ignore"), "size": len(data)}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "ports": return await list_ports()
    elif tool == "connect": return await connect(ConnectRequest(**params))
    elif tool == "disconnect": return await disconnect(params.get("port"))
    elif tool == "send": return await send(SendRequest(**params))
    elif tool == "receive": return await receive(ReceiveRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8048)
