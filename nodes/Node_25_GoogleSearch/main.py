"""Node 25: GoogleSearch - Google 搜索"""
import os, requests
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 25 - GoogleSearch", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

class SearchRequest(BaseModel):
    query: str
    num: int = 10

@app.get("/health")
async def health():
    return {"status": "healthy" if (GOOGLE_API_KEY or SERPER_API_KEY) else "degraded", "node_id": "25", "name": "GoogleSearch", "google_configured": bool(GOOGLE_API_KEY), "serper_configured": bool(SERPER_API_KEY), "timestamp": datetime.now().isoformat()}

@app.post("/search")
async def search(request: SearchRequest):
    # 优先使用 Serper (更便宜)
    if SERPER_API_KEY:
        try:
            response = requests.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
                json={"q": request.query, "num": request.num},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            results = [{"title": r.get("title"), "url": r.get("link"), "snippet": r.get("snippet")} for r in data.get("organic", [])]
            return {"success": True, "query": request.query, "results": results, "engine": "serper"}
        except Exception as e:
            pass
    
    # 使用 Google Custom Search API
    if GOOGLE_API_KEY and GOOGLE_CSE_ID:
        try:
            response = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params={"key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID, "q": request.query, "num": min(request.num, 10)},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            results = [{"title": r.get("title"), "url": r.get("link"), "snippet": r.get("snippet")} for r in data.get("items", [])]
            return {"success": True, "query": request.query, "results": results, "engine": "google"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    raise HTTPException(status_code=503, detail="No search API configured. Set SERPER_API_KEY or GOOGLE_API_KEY+GOOGLE_CSE_ID")

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "search": return await search(SearchRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8025)
