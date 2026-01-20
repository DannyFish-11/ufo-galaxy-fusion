"""
Node 12: Postgres
====================
PostgreSQL 数据库
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 12 - Postgres", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class PostgresTools:
    def __init__(self):
        
        # 需要 psycopg2 库
        import psycopg2
        self.conn_string = os.getenv("POSTGRES_CONN", "")
        
    async def _tool_query(self, params):
        try:
            conn = psycopg2.connect(self.conn_string)
            cur = conn.cursor()
            cur.execute(params.get("sql", ""))
            results = cur.fetchall()
            conn.close()
            return {"success": True, "results": results}
        except Exception as e:
            return {"error": str(e)}

        self.initialized = True
        
    def get_tools(self):
        return [
            {"name": "query", "description": "执行查询", "parameters": {'sql': 'SQL 语句'}},
            {"name": "execute", "description": "执行命令", "parameters": {'sql': 'SQL 语句'}}
        ]
        
    async def call_tool(self, tool: str, params: dict):
        if not self.initialized:
            raise RuntimeError("Postgres not initialized")
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)

tools = PostgresTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "12", "name": "Postgres", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8012)
