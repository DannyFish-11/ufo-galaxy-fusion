import os, subprocess
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title='Node 07 - Git', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

class GitRequest(BaseModel):
    repo_path: str
    command: Optional[str] = None
    url: Optional[str] = None
    message: Optional[str] = None
    branch: Optional[str] = None

def run_git(repo_path: str, args: list) -> dict:
    try:
        result = subprocess.run(['git'] + args, cwd=repo_path, capture_output=True, text=True, timeout=60)
        return {'success': result.returncode == 0, 'output': result.stdout, 'error': result.stderr}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.get('/health')
async def health():
    return {'status': 'healthy', 'node_id': '07', 'name': 'Git'}

@app.post('/clone')
async def clone(url: str, path: str):
    result = subprocess.run(['git', 'clone', url, path], capture_output=True, text=True, timeout=300)
    return {'success': result.returncode == 0, 'path': path, 'output': result.stdout, 'error': result.stderr}

@app.post('/status')
async def status(request: GitRequest):
    return run_git(request.repo_path, ['status'])

@app.post('/pull')
async def pull(request: GitRequest):
    return run_git(request.repo_path, ['pull'])

@app.post('/push')
async def push(request: GitRequest):
    return run_git(request.repo_path, ['push'])

@app.post('/commit')
async def commit(request: GitRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail='message required')
    run_git(request.repo_path, ['add', '-A'])
    return run_git(request.repo_path, ['commit', '-m', request.message])

@app.post('/mcp/call')
async def mcp_call(request: dict):
    tool = request.get('tool', '')
    params = request.get('params', {})
    if tool == 'clone': return await clone(params.get('url'), params.get('path'))
    elif tool == 'status': return await status(GitRequest(**params))
    elif tool == 'pull': return await pull(GitRequest(**params))
    elif tool == 'push': return await push(GitRequest(**params))
    elif tool == 'commit': return await commit(GitRequest(**params))
    raise HTTPException(status_code=400, detail=f'Unknown tool: {tool}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8007)
