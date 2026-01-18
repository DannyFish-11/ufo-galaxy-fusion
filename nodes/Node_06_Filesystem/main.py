"""Node 06: Filesystem Tool - Safe file operations"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

NODE_ID = os.getenv("NODE_ID", "06")
app = FastAPI(title=f"UFO Galaxy Node {NODE_ID}: Filesystem")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health(): return {"status": "healthy", "node_id": NODE_ID, "layer": "L2_TOOLS"}

@app.get("/")
async def root(): return {"node_id": NODE_ID, "name": "Filesystem", "layer": "L2_TOOLS"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8006)
