"""
Node 37: LinuxDBus - Linux D-Bus 通信
"""
import os, subprocess, platform
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 37 - LinuxDBus", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

IS_LINUX = platform.system() == "Linux"

def run_dbus(args: list, timeout: int = 10):
    if not IS_LINUX:
        return {"success": False, "error": "D-Bus only works on Linux"}
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return {"success": result.returncode == 0, "output": result.stdout.strip(), "error": result.stderr.strip() if result.returncode != 0 else None}
    except Exception as e:
        return {"success": False, "error": str(e)}

class NotificationRequest(BaseModel):
    title: str
    message: str
    timeout: int = 5000

class ServiceRequest(BaseModel):
    service: str
    action: str  # start, stop, restart, status

@app.get("/health")
async def health():
    return {"status": "healthy" if IS_LINUX else "unavailable", "node_id": "37", "name": "LinuxDBus", "is_linux": IS_LINUX, "timestamp": datetime.now().isoformat()}

@app.post("/notification")
async def send_notification(request: NotificationRequest):
    result = run_dbus(["notify-send", "-t", str(request.timeout), request.title, request.message])
    return {"success": result.get("success", False), "action": "notification"}

@app.post("/service")
async def manage_service(request: ServiceRequest):
    result = run_dbus(["systemctl", "--user", request.action, request.service])
    return result

@app.get("/services")
async def list_services():
    result = run_dbus(["systemctl", "--user", "list-units", "--type=service", "--no-pager"])
    return result

@app.get("/session_info")
async def get_session_info():
    result = run_dbus(["loginctl", "show-session", "self", "--no-pager"])
    return result

@app.post("/brightness")
async def set_brightness(level: int):
    level = max(0, min(100, level))
    result = run_dbus(["gdbus", "call", "--session", "--dest", "org.gnome.SettingsDaemon.Power", "--object-path", "/org/gnome/SettingsDaemon/Power", "--method", "org.freedesktop.DBus.Properties.Set", "org.gnome.SettingsDaemon.Power.Screen", "Brightness", f"<int32 {level}>"])
    return {"success": result.get("success", False), "level": level}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "notification": return await send_notification(NotificationRequest(**params))
    elif tool == "service": return await manage_service(ServiceRequest(**params))
    elif tool == "services": return await list_services()
    elif tool == "session_info": return await get_session_info()
    elif tool == "brightness": return await set_brightness(params.get("level", 50))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8037)
