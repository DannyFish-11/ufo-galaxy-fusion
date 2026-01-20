import os, json, base64, hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title='Node 03 - SecretVault', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

VAULT_FILE = os.getenv('VAULT_FILE', '/tmp/vault.enc')
VAULT_KEY = os.getenv('VAULT_KEY', 'default_key_change_me')
secrets: Dict[str, str] = {}

def encrypt(data: str) -> str:
    return base64.b64encode(data.encode()).decode()

def decrypt(data: str) -> str:
    return base64.b64decode(data.encode()).decode()

def load_vault():
    global secrets
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, 'r') as f:
            secrets = json.load(f)

def save_vault():
    with open(VAULT_FILE, 'w') as f:
        json.dump(secrets, f)

load_vault()

class SecretRequest(BaseModel):
    key: str
    value: Optional[str] = None

@app.get('/health')
async def health():
    return {'status': 'healthy', 'node_id': '03', 'name': 'SecretVault', 'secret_count': len(secrets)}

@app.post('/set')
async def set_secret(request: SecretRequest):
    if not request.value:
        raise HTTPException(status_code=400, detail='value required')
    secrets[request.key] = encrypt(request.value)
    save_vault()
    return {'success': True, 'key': request.key}

@app.get('/get/{key}')
async def get_secret(key: str):
    if key not in secrets:
        raise HTTPException(status_code=404, detail='Secret not found')
    return {'success': True, 'key': key, 'value': decrypt(secrets[key])}

@app.delete('/delete/{key}')
async def delete_secret(key: str):
    if key not in secrets:
        raise HTTPException(status_code=404, detail='Secret not found')
    del secrets[key]
    save_vault()
    return {'success': True, 'key': key}

@app.get('/list')
async def list_secrets():
    return {'success': True, 'keys': list(secrets.keys())}

@app.post('/mcp/call')
async def mcp_call(request: dict):
    tool = request.get('tool', '')
    params = request.get('params', {})
    if tool == 'set': return await set_secret(SecretRequest(**params))
    elif tool == 'get': return await get_secret(params.get('key'))
    elif tool == 'delete': return await delete_secret(params.get('key'))
    elif tool == 'list': return await list_secrets()
    raise HTTPException(status_code=400, detail=f'Unknown tool: {tool}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8003)
