"""
Node 13: SQLite - SQLite 数据库操作
"""
import os, sqlite3, json
from datetime import datetime
from typing import Optional, List, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 13 - SQLite", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DB_PATH = os.getenv("SQLITE_DB_PATH", "/tmp/galaxy.db")
connections = {}

class QueryRequest(BaseModel):
    sql: str
    params: Optional[List[Any]] = None
    db_path: Optional[str] = None

class TableRequest(BaseModel):
    table_name: str
    columns: dict
    db_path: Optional[str] = None

def get_connection(db_path: str = None):
    path = db_path or DB_PATH
    if path not in connections:
        connections[path] = sqlite3.connect(path, check_same_thread=False)
        connections[path].row_factory = sqlite3.Row
    return connections[path]

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "13", "name": "SQLite", "default_db": DB_PATH, "timestamp": datetime.now().isoformat()}

@app.post("/query")
async def execute_query(request: QueryRequest):
    try:
        conn = get_connection(request.db_path)
        cursor = conn.cursor()
        
        if request.params:
            cursor.execute(request.sql, request.params)
        else:
            cursor.execute(request.sql)
        
        if request.sql.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            results = [dict(zip(columns, row)) for row in rows]
            return {"success": True, "results": results, "count": len(results)}
        else:
            conn.commit()
            return {"success": True, "rowcount": cursor.rowcount, "lastrowid": cursor.lastrowid}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/create_table")
async def create_table(request: TableRequest):
    columns_sql = ", ".join([f"{name} {dtype}" for name, dtype in request.columns.items()])
    sql = f"CREATE TABLE IF NOT EXISTS {request.table_name} ({columns_sql})"
    return await execute_query(QueryRequest(sql=sql, db_path=request.db_path))

@app.get("/tables")
async def list_tables(db_path: Optional[str] = None):
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    result = await execute_query(QueryRequest(sql=sql, db_path=db_path))
    if result["success"]:
        return {"success": True, "tables": [r["name"] for r in result["results"]]}
    return result

@app.get("/schema/{table_name}")
async def get_schema(table_name: str, db_path: Optional[str] = None):
    sql = f"PRAGMA table_info({table_name})"
    result = await execute_query(QueryRequest(sql=sql, db_path=db_path))
    if result["success"]:
        return {"success": True, "table": table_name, "columns": result["results"]}
    return result

@app.post("/insert")
async def insert_data(table_name: str, data: dict, db_path: Optional[str] = None):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    return await execute_query(QueryRequest(sql=sql, params=list(data.values()), db_path=db_path))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "query": return await execute_query(QueryRequest(**params))
    elif tool == "create_table": return await create_table(TableRequest(**params))
    elif tool == "tables": return await list_tables(params.get("db_path"))
    elif tool == "schema": return await get_schema(params.get("table_name", ""), params.get("db_path"))
    elif tool == "insert": return await insert_data(params.get("table_name", ""), params.get("data", {}), params.get("db_path"))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8013)
