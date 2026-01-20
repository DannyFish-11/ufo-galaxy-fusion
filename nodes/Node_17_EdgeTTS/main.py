"""
Node 17: EdgeTTS - 微软 Edge 文字转语音
"""
import os, tempfile, asyncio
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 17 - EdgeTTS", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

edge_tts = None
try:
    import edge_tts as _edge_tts
    edge_tts = _edge_tts
except ImportError:
    pass

class TTSRequest(BaseModel):
    text: str
    voice: str = "zh-CN-XiaoxiaoNeural"
    rate: str = "+0%"
    volume: str = "+0%"
    output_path: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "healthy" if edge_tts else "degraded", "node_id": "17", "name": "EdgeTTS", "edge_tts_available": edge_tts is not None, "timestamp": datetime.now().isoformat()}

@app.get("/voices")
async def list_voices(language: Optional[str] = None):
    if not edge_tts:
        raise HTTPException(status_code=503, detail="edge-tts not installed")
    
    voices = await edge_tts.list_voices()
    if language:
        voices = [v for v in voices if language.lower() in v["Locale"].lower()]
    
    return {"success": True, "voices": voices, "count": len(voices)}

@app.post("/synthesize")
async def synthesize(request: TTSRequest):
    if not edge_tts:
        raise HTTPException(status_code=503, detail="edge-tts not installed")
    
    output_path = request.output_path or tempfile.mktemp(suffix=".mp3")
    
    try:
        communicate = edge_tts.Communicate(request.text, request.voice, rate=request.rate, volume=request.volume)
        await communicate.save(output_path)
        
        return {"success": True, "path": output_path, "voice": request.voice, "text_length": len(request.text)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/stream")
async def stream_audio(request: TTSRequest):
    if not edge_tts:
        raise HTTPException(status_code=503, detail="edge-tts not installed")
    
    output_path = tempfile.mktemp(suffix=".mp3")
    
    try:
        communicate = edge_tts.Communicate(request.text, request.voice, rate=request.rate, volume=request.volume)
        await communicate.save(output_path)
        return FileResponse(output_path, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "voices": return await list_voices(params.get("language"))
    elif tool == "synthesize": return await synthesize(TTSRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8017)
