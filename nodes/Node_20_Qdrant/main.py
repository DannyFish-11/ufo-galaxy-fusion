"""Node 20: Qdrant - 向量数据库"""
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 20 - Qdrant", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

qdrant_client = None
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_client = QdrantClient(url=QDRANT_URL)
except ImportError:
    pass

class SearchRequest(BaseModel):
    collection: str
    vector: List[float]
    limit: int = 10

class UpsertRequest(BaseModel):
    collection: str
    id: int
    vector: List[float]
    payload: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health():
    return {"status": "healthy" if qdrant_client else "degraded", "node_id": "20", "name": "Qdrant", "qdrant_available": qdrant_client is not None, "timestamp": datetime.now().isoformat()}

@app.post("/search")
async def search(request: SearchRequest):
    if not qdrant_client:
        raise HTTPException(status_code=503, detail="qdrant-client not installed. Run: pip install qdrant-client")
    try:
        results = qdrant_client.search(collection_name=request.collection, query_vector=request.vector, limit=request.limit)
        return {"success": True, "results": [{"id": r.id, "score": r.score, "payload": r.payload} for r in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upsert")
async def upsert(request: UpsertRequest):
    if not qdrant_client:
        raise HTTPException(status_code=503, detail="qdrant-client not installed")
    try:
        qdrant_client.upsert(collection_name=request.collection, points=[PointStruct(id=request.id, vector=request.vector, payload=request.payload or {})])
        return {"success": True, "id": request.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "search": return await search(SearchRequest(**params))
    elif tool == "upsert": return await upsert(UpsertRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)
