"""Node 18: DeepL - 翻译"""
import os, requests
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 18 - DeepL", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")

class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "EN"
    source_lang: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "healthy" if DEEPL_API_KEY else "degraded", "node_id": "18", "name": "DeepL", "api_configured": bool(DEEPL_API_KEY), "timestamp": datetime.now().isoformat()}

@app.post("/translate")
async def translate(request: TranslateRequest):
    if not DEEPL_API_KEY:
        # 使用免费的 Google Translate 作为 fallback
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(request.text, dest=request.target_lang.lower())
            return {"success": True, "text": result.text, "source_lang": result.src, "target_lang": request.target_lang, "engine": "google"}
        except:
            raise HTTPException(status_code=503, detail="DeepL API not configured and Google Translate unavailable")
    
    try:
        response = requests.post(
            "https://api-free.deepl.com/v2/translate",
            headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"},
            data={"text": request.text, "target_lang": request.target_lang, "source_lang": request.source_lang} if request.source_lang else {"text": request.text, "target_lang": request.target_lang},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return {"success": True, "text": data["translations"][0]["text"], "source_lang": data["translations"][0]["detected_source_language"], "target_lang": request.target_lang, "engine": "deepl"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "translate": return await translate(TranslateRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8018)
