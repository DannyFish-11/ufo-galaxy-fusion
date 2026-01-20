"""
Node 47: Audio - 音频录制和播放
"""
import os, wave, tempfile
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 47 - Audio", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

pyaudio = None
try:
    import pyaudio as _pyaudio
    pyaudio = _pyaudio
except ImportError:
    pass

class RecordRequest(BaseModel):
    output_path: Optional[str] = None
    duration: int = 5
    sample_rate: int = 44100
    channels: int = 1

class PlayRequest(BaseModel):
    file_path: str

@app.get("/health")
async def health():
    return {"status": "healthy" if pyaudio else "degraded", "node_id": "47", "name": "Audio", "pyaudio_available": pyaudio is not None, "timestamp": datetime.now().isoformat()}

@app.get("/devices")
async def list_devices():
    if not pyaudio:
        raise HTTPException(status_code=503, detail="pyaudio not installed")
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        devices.append({"id": i, "name": info["name"], "input_channels": info["maxInputChannels"], "output_channels": info["maxOutputChannels"]})
    p.terminate()
    return {"success": True, "devices": devices}

@app.post("/record")
async def record(request: RecordRequest):
    if not pyaudio:
        raise HTTPException(status_code=503, detail="pyaudio not installed")
    output_path = request.output_path or tempfile.mktemp(suffix=".wav")
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=request.channels, rate=request.sample_rate, input=True, frames_per_buffer=1024)
    frames = []
    for _ in range(0, int(request.sample_rate / 1024 * request.duration)):
        data = stream.read(1024)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(output_path, "wb")
    wf.setnchannels(request.channels)
    wf.setsampwidth(2)
    wf.setframerate(request.sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    return {"success": True, "path": output_path, "duration": request.duration}

@app.post("/play")
async def play(request: PlayRequest):
    if not pyaudio:
        raise HTTPException(status_code=503, detail="pyaudio not installed")
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    wf = wave.open(request.file_path, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return {"success": True, "file": request.file_path}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "devices": return await list_devices()
    elif tool == "record": return await record(RecordRequest(**params))
    elif tool == "play": return await play(PlayRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8047)
