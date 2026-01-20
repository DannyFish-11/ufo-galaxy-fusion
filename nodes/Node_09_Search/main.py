"""
Node 09: Search - 网络搜索聚合
"""
import os, requests
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 09 - Search", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")

class SearchRequest(BaseModel):
    query: str
    num_results: int = 10
    search_type: str = "web"

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "09", "name": "Search", "brave_configured": bool(BRAVE_API_KEY), "timestamp": datetime.now().isoformat()}

@app.post("/search")
async def search(request: SearchRequest):
    if BRAVE_API_KEY:
        try:
            response = requests.get("https://api.search.brave.com/res/v1/web/search", headers={"X-Subscription-Token": BRAVE_API_KEY, "Accept": "application/json"}, params={"q": request.query, "count": request.num_results}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = [{"title": r.get("title"), "url": r.get("url"), "description": r.get("description")} for r in data.get("web", {}).get("results", [])]
                return {"success": True, "results": results, "source": "brave"}
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
                snippet_el = r.select_one(".result__snippet")
                if title_el:
                    results.append({"title": title_el.get_text(strip=True), "url": "", "description": snippet_el.get_text(strip=True) if snippet_el else ""})
            return {"success": True, "results": results, "source": "duckduckgo"}
    except:
        pass
    
    return {"success": False, "error": "No search API available"}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "search": return await search(SearchRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
