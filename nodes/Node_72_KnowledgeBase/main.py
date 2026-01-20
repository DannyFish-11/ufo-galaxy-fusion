"""
Node 72: KnowledgeBase
====================
RAG 知识库
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 72 - KnowledgeBase", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class KnowledgeBaseTools:
    def __init__(self):
        
        # 使用内存存储 (生产环境应使用 ChromaDB/Qdrant)
        self.documents = []
        
    async def _tool_add_document(self, params):
        doc_id = len(self.documents)
        self.documents.append({"id": doc_id, "text": params.get("text", ""), "metadata": params.get("metadata", {})})
        return {"success": True, "doc_id": doc_id}
        
    async def _tool_search(self, params):
        query = params.get("query", "").lower()
        results = [doc for doc in self.documents if query in doc["text"].lower()][:params.get("top_k", 5)]
        return {"success": True, "results": results}
        
    async def _tool_delete(self, params):
        doc_id = params.get("doc_id")
        self.documents = [d for d in self.documents if d["id"] != doc_id]
        return {"success": True}

        self.initialized = True
        
    def get_tools(self):
        return [
            {"name": "add_document", "description": "添加文档", "parameters": {'text': '文档内容', 'metadata': '元数据'}},
            {"name": "search", "description": "搜索知识", "parameters": {'query': '查询文本', 'top_k': '返回数量'}},
            {"name": "delete", "description": "删除文档", "parameters": {'doc_id': '文档ID'}}
        ]
        
    async def call_tool(self, tool: str, params: dict):
        if not self.initialized:
            raise RuntimeError("KnowledgeBase not initialized")
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)

tools = KnowledgeBaseTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "72", "name": "KnowledgeBase", "timestamp": datetime.now().isoformat()}

@app.get("/tools")
async def list_tools():
    return {"tools": tools.get_tools()}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    try:
        return {"success": True, "result": await tools.call_tool(request.get("tool"), request.get("params", {}))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8072)
