"""Node 17: EdgeTTS - 文字转语音"""
import os, asyncio
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
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
    output_path: str = "/tmp/tts_output.mp3"
    rate: str = "+0%"
    volume: str = "+0%"

@app.get("/health")
async def health():
    return {"status": "healthy" if edge_tts else "degraded", "node_id": "17", "name": "EdgeTTS", "edge_tts_available": edge_tts is not None, "timestamp": datetime.now().isoformat()}

@app.get("/voices")
async def list_voices():
    if not edge_tts:
        raise HTTPException(status_code=503, detail="edge-tts not installed. Run: pip install edge-tts")
    voices = await edge_tts.list_voices()
    return {"success": True, "voices": [{"name": v["Name"], "gender": v["Gender"], "locale": v["Locale"]} for v in voices]}

@app.post("/synthesize")
async def synthesize(request: TTSRequest):
    if not edge_tts:
        raise HTTPException(status_code=503, detail="edge-tts not installed. Run: pip install edge-tts")
    try:
        communicate = edge_tts.Communicate(request.text, request.voice, rate=request.rate, volume=request.volume)
        await communicate.save(request.output_path)
        return {"success": True, "output_path": request.output_path, "voice": request.voice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "synthesize": return await synthesize(TTSRequest(**params))
    elif tool == "voices": return await list_voices()
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8017)
