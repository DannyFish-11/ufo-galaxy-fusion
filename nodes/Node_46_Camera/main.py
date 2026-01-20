"""
Node 46: Camera - 摄像头控制
"""
import os, tempfile
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 46 - Camera", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

cv2 = None
try:
    import cv2 as _cv2
    cv2 = _cv2
except ImportError:
    pass

class CaptureRequest(BaseModel):
    camera_id: int = 0
    output_path: Optional[str] = None

class RecordRequest(BaseModel):
    camera_id: int = 0
    output_path: str
    duration: int = 5
    fps: int = 30

@app.get("/health")
async def health():
    return {"status": "healthy" if cv2 else "degraded", "node_id": "46", "name": "Camera", "opencv_available": cv2 is not None, "timestamp": datetime.now().isoformat()}

@app.get("/list")
async def list_cameras():
    if not cv2:
        raise HTTPException(status_code=503, detail="opencv-python not installed")
    cameras = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append({"id": i, "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))})
            cap.release()
    return {"success": True, "cameras": cameras}

@app.post("/capture")
async def capture(request: CaptureRequest):
    if not cv2:
        raise HTTPException(status_code=503, detail="opencv-python not installed")
    output_path = request.output_path or tempfile.mktemp(suffix=".jpg")
    cap = cv2.VideoCapture(request.camera_id)
    if not cap.isOpened():
        raise HTTPException(status_code=404, detail=f"Camera {request.camera_id} not found")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise HTTPException(status_code=500, detail="Failed to capture")
    cv2.imwrite(output_path, frame)
    return {"success": True, "path": output_path}

@app.post("/record")
async def record(request: RecordRequest):
    if not cv2:
        raise HTTPException(status_code=503, detail="opencv-python not installed")
    cap = cv2.VideoCapture(request.camera_id)
    if not cap.isOpened():
        raise HTTPException(status_code=404, detail=f"Camera {request.camera_id} not found")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(request.output_path, fourcc, request.fps, (width, height))
    frames = request.duration * request.fps
    for _ in range(frames):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
    cap.release()
    out.release()
    return {"success": True, "path": request.output_path, "duration": request.duration}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "list": return await list_cameras()
    elif tool == "capture": return await capture(CaptureRequest(**params))
    elif tool == "record": return await record(RecordRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8046)
