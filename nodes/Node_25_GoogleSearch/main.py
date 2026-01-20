"""
Node 25: GoogleSearch - Google 搜索
"""
import os, requests
from datetime import datetime
from typing import Optional, List
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
    num_results: int = 10
    language: str = "en"

@app.get("/health")
async def health():
    configured = bool(GOOGLE_API_KEY and GOOGLE_CSE_ID) or bool(SERPER_API_KEY)
    return {"status": "healthy" if configured else "degraded", "node_id": "25", "name": "GoogleSearch", "google_configured": bool(GOOGLE_API_KEY), "serper_configured": bool(SERPER_API_KEY), "timestamp": datetime.now().isoformat()}

@app.post("/search")
async def search(request: SearchRequest):
    if SERPER_API_KEY:
        try:
            response = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}, json={"q": request.query, "num": request.num_results, "hl": request.language}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = [{"title": r.get("title"), "link": r.get("link"), "snippet": r.get("snippet")} for r in data.get("organic", [])]
                return {"success": True, "results": results, "source": "serper"}
        except Exception as e:
            pass
    
    if GOOGLE_API_KEY and GOOGLE_CSE_ID:
        try:
            response = requests.get("https://www.googleapis.com/customsearch/v1", params={"key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID, "q": request.query, "num": min(request.num_results, 10)}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = [{"title": r.get("title"), "link": r.get("link"), "snippet": r.get("snippet")} for r in data.get("items", [])]
                return {"success": True, "results": results, "source": "google"}
        except Exception as e:
            pass
    
    try:
        from urllib.parse import quote
        response = requests.get(f"https://html.duckduckgo.com/html/?q={quote(request.query)}", headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for r in soup.select(".result")[:request.num_results]:
                title_el = r.select_one(".result__title")
                link_el = r.select_one(".result__url")
                snippet_el = r.select_one(".result__snippet")
                if title_el:
                    results.append({"title": title_el.get_text(strip=True), "link": link_el.get_text(strip=True) if link_el else "", "snippet": snippet_el.get_text(strip=True) if snippet_el else ""})
            return {"success": True, "results": results, "source": "duckduckgo"}
    except:
        pass
    
    return {"success": False, "error": "No search API configured or available"}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "search": return await search(SearchRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8025)
