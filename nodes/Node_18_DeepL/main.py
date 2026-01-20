"""
Node 18: DeepL - 翻译服务
"""
import os, requests
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 18 - DeepL", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com/v2"

class TranslateRequest(BaseModel):
    text: str
    target_lang: str
    source_lang: Optional[str] = None

class BatchTranslateRequest(BaseModel):
    texts: List[str]
    target_lang: str
    source_lang: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "healthy" if DEEPL_API_KEY else "degraded", "node_id": "18", "name": "DeepL", "api_configured": bool(DEEPL_API_KEY), "timestamp": datetime.now().isoformat()}

@app.post("/translate")
async def translate(request: TranslateRequest):
    if not DEEPL_API_KEY:
        # Fallback to free translation API
        try:
            response = requests.get(f"https://api.mymemory.translated.net/get", params={"q": request.text, "langpair": f"{request.source_lang or 'auto'}|{request.target_lang}"}, timeout=10)
            data = response.json()
            if data.get("responseStatus") == 200:
                return {"success": True, "translated_text": data["responseData"]["translatedText"], "source": "mymemory"}
        except:
            pass
        raise HTTPException(status_code=503, detail="DeepL API key not configured")
    
    try:
        response = requests.post(f"{DEEPL_API_URL}/translate", headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}, data={"text": request.text, "target_lang": request.target_lang, "source_lang": request.source_lang} if request.source_lang else {"text": request.text, "target_lang": request.target_lang}, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "translated_text": data["translations"][0]["text"], "detected_source_lang": data["translations"][0].get("detected_source_language")}
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/batch")
async def batch_translate(request: BatchTranslateRequest):
    results = []
    for text in request.texts:
        result = await translate(TranslateRequest(text=text, target_lang=request.target_lang, source_lang=request.source_lang))
        results.append(result)
    return {"success": True, "results": results}

@app.get("/languages")
async def list_languages():
    if not DEEPL_API_KEY:
        return {"success": True, "languages": [{"code": "EN", "name": "English"}, {"code": "ZH", "name": "Chinese"}, {"code": "JA", "name": "Japanese"}, {"code": "DE", "name": "German"}, {"code": "FR", "name": "French"}]}
    
    try:
        response = requests.get(f"{DEEPL_API_URL}/languages", headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"}, timeout=10)
        if response.status_code == 200:
            return {"success": True, "languages": response.json()}
    except:
        pass
    return {"success": False, "error": "Failed to fetch languages"}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "translate": return await translate(TranslateRequest(**params))
    elif tool == "batch": return await batch_translate(BatchTranslateRequest(**params))
    elif tool == "languages": return await list_languages()
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8018)
