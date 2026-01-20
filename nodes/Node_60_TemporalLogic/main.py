"""
Node 60: TemporalLogic - 时序逻辑
"""
import os, re
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 60 - TemporalLogic", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class TraceRequest(BaseModel):
    trace: List[Dict[str, bool]]
    formula: str

class LTLRequest(BaseModel):
    formula: str
    trace: List[str]

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "60", "name": "TemporalLogic", "timestamp": datetime.now().isoformat()}

def evaluate_ltl(formula: str, trace: List[Dict[str, bool]], pos: int = 0) -> bool:
    """评估 LTL 公式"""
    formula = formula.strip()
    
    if formula.startswith("G(") and formula.endswith(")"):
        inner = formula[2:-1]
        return all(evaluate_ltl(inner, trace, i) for i in range(pos, len(trace)))
    
    if formula.startswith("F(") and formula.endswith(")"):
        inner = formula[2:-1]
        return any(evaluate_ltl(inner, trace, i) for i in range(pos, len(trace)))
    
    if formula.startswith("X(") and formula.endswith(")"):
        inner = formula[2:-1]
        if pos + 1 < len(trace):
            return evaluate_ltl(inner, trace, pos + 1)
        return False
    
    if formula.startswith("!(") and formula.endswith(")"):
        inner = formula[2:-1]
        return not evaluate_ltl(inner, trace, pos)
    
    if " U " in formula:
        parts = formula.split(" U ", 1)
        phi, psi = parts[0].strip(), parts[1].strip()
        for i in range(pos, len(trace)):
            if evaluate_ltl(psi, trace, i):
                if all(evaluate_ltl(phi, trace, j) for j in range(pos, i)):
                    return True
        return False
    
    if " && " in formula:
        parts = formula.split(" && ")
        return all(evaluate_ltl(p.strip(), trace, pos) for p in parts)
    
    if " || " in formula:
        parts = formula.split(" || ")
        return any(evaluate_ltl(p.strip(), trace, pos) for p in parts)
    
    if pos < len(trace):
        return trace[pos].get(formula, False)
    return False

@app.post("/check")
async def check_formula(request: TraceRequest):
    """检查 LTL 公式是否在 trace 上成立"""
    result = evaluate_ltl(request.formula, request.trace)
    return {"success": True, "formula": request.formula, "satisfied": result, "trace_length": len(request.trace)}

@app.post("/always")
async def check_always(property: str, trace: List[Dict[str, bool]]):
    """G(property) - 总是成立"""
    result = all(state.get(property, False) for state in trace)
    return {"success": True, "formula": f"G({property})", "satisfied": result}

@app.post("/eventually")
async def check_eventually(property: str, trace: List[Dict[str, bool]]):
    """F(property) - 最终成立"""
    result = any(state.get(property, False) for state in trace)
    return {"success": True, "formula": f"F({property})", "satisfied": result}

@app.post("/until")
async def check_until(phi: str, psi: str, trace: List[Dict[str, bool]]):
    """phi U psi - phi 成立直到 psi 成立"""
    for i, state in enumerate(trace):
        if state.get(psi, False):
            if all(trace[j].get(phi, False) for j in range(i)):
                return {"success": True, "formula": f"{phi} U {psi}", "satisfied": True, "psi_at": i}
    return {"success": True, "formula": f"{phi} U {psi}", "satisfied": False}

@app.post("/next")
async def check_next(property: str, trace: List[Dict[str, bool]], position: int = 0):
    """X(property) - 下一状态成立"""
    if position + 1 < len(trace):
        result = trace[position + 1].get(property, False)
        return {"success": True, "formula": f"X({property})", "satisfied": result}
    return {"success": True, "formula": f"X({property})", "satisfied": False, "reason": "No next state"}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "check": return await check_formula(TraceRequest(**params))
    elif tool == "always": return await check_always(params.get("property", ""), params.get("trace", []))
    elif tool == "eventually": return await check_eventually(params.get("property", ""), params.get("trace", []))
    elif tool == "until": return await check_until(params.get("phi", ""), params.get("psi", ""), params.get("trace", []))
    elif tool == "next": return await check_next(params.get("property", ""), params.get("trace", []), params.get("position", 0))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8060)
