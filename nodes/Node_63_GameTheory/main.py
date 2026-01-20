"""
Node 63: GameTheory - 博弈论
"""
import os, random
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 63 - GameTheory", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class PayoffMatrix(BaseModel):
    player1_payoffs: List[List[float]]
    player2_payoffs: List[List[float]]
    player1_strategies: List[str] = None
    player2_strategies: List[str] = None

class AuctionRequest(BaseModel):
    bids: List[float]
    auction_type: str = "first_price"

class NegotiationRequest(BaseModel):
    player1_value: float
    player2_value: float
    rounds: int = 10

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "63", "name": "GameTheory", "timestamp": datetime.now().isoformat()}

@app.post("/nash_equilibrium")
async def find_nash_equilibrium(matrix: PayoffMatrix):
    """寻找纳什均衡 (纯策略)"""
    p1 = matrix.player1_payoffs
    p2 = matrix.player2_payoffs
    rows = len(p1)
    cols = len(p1[0]) if rows > 0 else 0
    
    equilibria = []
    
    for i in range(rows):
        for j in range(cols):
            is_best_for_p1 = all(p1[i][j] >= p1[k][j] for k in range(rows))
            is_best_for_p2 = all(p2[i][j] >= p2[i][k] for k in range(cols))
            
            if is_best_for_p1 and is_best_for_p2:
                s1 = matrix.player1_strategies[i] if matrix.player1_strategies else f"S{i+1}"
                s2 = matrix.player2_strategies[j] if matrix.player2_strategies else f"S{j+1}"
                equilibria.append({"player1": s1, "player2": s2, "payoffs": [p1[i][j], p2[i][j]]})
    
    return {"success": True, "nash_equilibria": equilibria, "count": len(equilibria)}

@app.post("/dominant_strategy")
async def find_dominant_strategy(matrix: PayoffMatrix):
    """寻找优势策略"""
    p1 = matrix.player1_payoffs
    p2 = matrix.player2_payoffs
    rows = len(p1)
    cols = len(p1[0]) if rows > 0 else 0
    
    p1_dominant = None
    for i in range(rows):
        is_dominant = True
        for k in range(rows):
            if k != i:
                if not all(p1[i][j] >= p1[k][j] for j in range(cols)):
                    is_dominant = False
                    break
        if is_dominant:
            p1_dominant = matrix.player1_strategies[i] if matrix.player1_strategies else f"S{i+1}"
            break
    
    p2_dominant = None
    for j in range(cols):
        is_dominant = True
        for k in range(cols):
            if k != j:
                if not all(p2[i][j] >= p2[i][k] for i in range(rows)):
                    is_dominant = False
                    break
        if is_dominant:
            p2_dominant = matrix.player2_strategies[j] if matrix.player2_strategies else f"S{j+1}"
            break
    
    return {"success": True, "player1_dominant": p1_dominant, "player2_dominant": p2_dominant}

@app.post("/prisoners_dilemma")
async def prisoners_dilemma(player1_cooperate: bool, player2_cooperate: bool):
    """囚徒困境"""
    payoffs = {
        (True, True): (-1, -1),
        (True, False): (-3, 0),
        (False, True): (0, -3),
        (False, False): (-2, -2)
    }
    
    p1_action = "Cooperate" if player1_cooperate else "Defect"
    p2_action = "Cooperate" if player2_cooperate else "Defect"
    result = payoffs[(player1_cooperate, player2_cooperate)]
    
    return {"success": True, "player1_action": p1_action, "player2_action": p2_action, "player1_payoff": result[0], "player2_payoff": result[1], "note": "Nash equilibrium is (Defect, Defect)"}

@app.post("/auction")
async def simulate_auction(request: AuctionRequest):
    """拍卖模拟"""
    bids = request.bids
    if not bids:
        raise HTTPException(status_code=400, detail="No bids provided")
    
    sorted_bids = sorted(enumerate(bids), key=lambda x: x[1], reverse=True)
    winner = sorted_bids[0][0]
    
    if request.auction_type == "first_price":
        price = sorted_bids[0][1]
    elif request.auction_type == "second_price":
        price = sorted_bids[1][1] if len(sorted_bids) > 1 else sorted_bids[0][1]
    else:
        raise HTTPException(status_code=400, detail=f"Unknown auction type: {request.auction_type}")
    
    return {"success": True, "auction_type": request.auction_type, "winner": winner, "winning_bid": sorted_bids[0][1], "price_paid": price}

@app.post("/negotiate")
async def alternating_offers(request: NegotiationRequest):
    """交替出价谈判"""
    history = []
    p1_value = request.player1_value
    p2_value = request.player2_value
    
    for round in range(request.rounds):
        if round % 2 == 0:
            offer = p1_value * (1 - 0.1 * round)
            proposer = "Player 1"
        else:
            offer = p2_value * (1 - 0.1 * round)
            proposer = "Player 2"
        
        history.append({"round": round + 1, "proposer": proposer, "offer": round(offer, 2)})
        
        if offer <= min(p1_value, p2_value) * 0.5:
            break
    
    final_offer = history[-1]["offer"]
    return {"success": True, "history": history, "final_offer": final_offer, "rounds": len(history)}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "nash_equilibrium": return await find_nash_equilibrium(PayoffMatrix(**params))
    elif tool == "dominant_strategy": return await find_dominant_strategy(PayoffMatrix(**params))
    elif tool == "prisoners_dilemma": return await prisoners_dilemma(params.get("player1_cooperate", True), params.get("player2_cooperate", True))
    elif tool == "auction": return await simulate_auction(AuctionRequest(**params))
    elif tool == "negotiate": return await alternating_offers(NegotiationRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8063)
