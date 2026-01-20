"""
Node 09: Sandbox - 代码沙箱执行
"""
import os, subprocess, tempfile, shutil
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 09 - Sandbox", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ExecuteRequest(BaseModel):
    code: str
    language: str = "python"
    timeout: int = 30
    stdin: Optional[str] = None

LANGUAGE_CONFIG = {
    "python": {"ext": ".py", "cmd": ["python3"]},
    "javascript": {"ext": ".js", "cmd": ["node"]},
    "bash": {"ext": ".sh", "cmd": ["bash"]},
    "ruby": {"ext": ".rb", "cmd": ["ruby"]},
    "php": {"ext": ".php", "cmd": ["php"]},
}

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "09", "name": "Sandbox", "supported_languages": list(LANGUAGE_CONFIG.keys()), "timestamp": datetime.now().isoformat()}

@app.post("/execute")
async def execute_code(request: ExecuteRequest):
    lang = request.language.lower()
    if lang not in LANGUAGE_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {lang}")
    
    config = LANGUAGE_CONFIG[lang]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        code_file = os.path.join(tmpdir, f"code{config['ext']}")
        with open(code_file, "w") as f:
            f.write(request.code)
        
        cmd = config["cmd"] + [code_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=request.timeout, input=request.stdin, cwd=tmpdir)
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr, "return_code": result.returncode}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Execution timed out", "timeout": request.timeout}
        except Exception as e:
            return {"success": False, "error": str(e)}

@app.post("/eval")
async def eval_expression(expression: str, language: str = "python"):
    """快速求值表达式"""
    if language == "python":
        code = f"print({expression})"
    elif language == "javascript":
        code = f"console.log({expression})"
    else:
        raise HTTPException(status_code=400, detail=f"Eval not supported for {language}")
    
    return await execute_code(ExecuteRequest(code=code, language=language, timeout=5))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "execute": return await execute_code(ExecuteRequest(**params))
    elif tool == "eval": return await eval_expression(params.get("expression", ""), params.get("language", "python"))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
