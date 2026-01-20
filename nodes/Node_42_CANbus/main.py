"""
Node 42: CANbus - CAN 总线通信
"""
import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 42 - CANbus", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

can = None
try:
    import can as _can
    can = _can
except ImportError:
    pass

class SendRequest(BaseModel):
    interface: str = "can0"
    arbitration_id: int
    data: List[int]
    is_extended_id: bool = False

class ReceiveRequest(BaseModel):
    interface: str = "can0"
    timeout: float = 1.0

buses = {}

def get_bus(interface: str):
    if not can:
        raise HTTPException(status_code=503, detail="python-can not installed")
    if interface not in buses:
        try:
            buses[interface] = can.interface.Bus(channel=interface, bustype="socketcan")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to open {interface}: {e}")
    return buses[interface]

@app.get("/health")
async def health():
    return {"status": "healthy" if can else "degraded", "node_id": "42", "name": "CANbus", "can_available": can is not None, "timestamp": datetime.now().isoformat()}

@app.post("/send")
async def send_message(request: SendRequest):
    bus = get_bus(request.interface)
    msg = can.Message(arbitration_id=request.arbitration_id, data=bytes(request.data), is_extended_id=request.is_extended_id)
    try:
        bus.send(msg)
        return {"success": True, "arbitration_id": hex(request.arbitration_id), "data": request.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/receive")
async def receive_message(request: ReceiveRequest):
    bus = get_bus(request.interface)
    msg = bus.recv(timeout=request.timeout)
    if msg:
        return {"success": True, "arbitration_id": hex(msg.arbitration_id), "data": list(msg.data), "timestamp": msg.timestamp}
    return {"success": False, "message": "No message received"}

@app.get("/interfaces")
async def list_interfaces():
    import subprocess
    result = subprocess.run(["ip", "link", "show", "type", "can"], capture_output=True, text=True)
    interfaces = [line.split(":")[1].strip() for line in result.stdout.split("\n") if ":" in line and "can" in line]
    return {"success": True, "interfaces": interfaces}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "send": return await send_message(SendRequest(**params))
    elif tool == "receive": return await receive_message(ReceiveRequest(**params))
    elif tool == "interfaces": return await list_interfaces()
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8042)
