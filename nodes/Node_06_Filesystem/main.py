import os, shutil, glob
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title='Node 06 - Filesystem', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ALLOWED_PATHS = os.getenv('ALLOWED_PATHS', '/tmp,/home').split(',')

def is_allowed(path: str) -> bool:
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(p) for p in ALLOWED_PATHS)

class FileRequest(BaseModel):
    path: str
    content: Optional[str] = None
    dest: Optional[str] = None

@app.get('/health')
async def health():
    return {'status': 'healthy', 'node_id': '06', 'name': 'Filesystem', 'allowed_paths': ALLOWED_PATHS}

@app.post('/read')
async def read_file(request: FileRequest):
    if not is_allowed(request.path):
        raise HTTPException(status_code=403, detail='Path not allowed')
    if not os.path.exists(request.path):
        raise HTTPException(status_code=404, detail='File not found')
    with open(request.path, 'r') as f:
        return {'success': True, 'content': f.read()}

@app.post('/write')
async def write_file(request: FileRequest):
    if not is_allowed(request.path):
        raise HTTPException(status_code=403, detail='Path not allowed')
    os.makedirs(os.path.dirname(request.path) or '.', exist_ok=True)
    with open(request.path, 'w') as f:
        f.write(request.content or '')
    return {'success': True, 'path': request.path}

@app.post('/copy')
async def copy_file(request: FileRequest):
    if not is_allowed(request.path) or not is_allowed(request.dest):
        raise HTTPException(status_code=403, detail='Path not allowed')
    shutil.copy2(request.path, request.dest)
    return {'success': True, 'src': request.path, 'dest': request.dest}

@app.post('/move')
async def move_file(request: FileRequest):
    if not is_allowed(request.path) or not is_allowed(request.dest):
        raise HTTPException(status_code=403, detail='Path not allowed')
    shutil.move(request.path, request.dest)
    return {'success': True, 'src': request.path, 'dest': request.dest}

@app.get('/list')
async def list_dir(path: str, pattern: str = '*'):
    if not is_allowed(path):
        raise HTTPException(status_code=403, detail='Path not allowed')
    files = glob.glob(os.path.join(path, pattern))
    result = []
    for f in files:
        stat = os.stat(f)
        result.append({'name': os.path.basename(f), 'path': f, 'size': stat.st_size, 'is_dir': os.path.isdir(f)})
    return {'success': True, 'files': result}

@app.post('/mcp/call')
async def mcp_call(request: dict):
    tool = request.get('tool', '')
    params = request.get('params', {})
    if tool == 'read': return await read_file(FileRequest(**params))
    elif tool == 'write': return await write_file(FileRequest(**params))
    elif tool == 'copy': return await copy_file(FileRequest(**params))
    elif tool == 'move': return await move_file(FileRequest(**params))
    elif tool == 'list': return await list_dir(params.get('path'), params.get('pattern', '*'))
    raise HTTPException(status_code=400, detail=f'Unknown tool: {tool}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8006)
