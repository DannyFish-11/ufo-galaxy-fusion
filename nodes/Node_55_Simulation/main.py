"""
Node 55: Simulation - 模拟仿真引擎
"""
import os, random, math
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 55 - Simulation", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class MonteCarloRequest(BaseModel):
    samples: int = 10000
    function: str = "pi"

class PhysicsRequest(BaseModel):
    initial_velocity: float
    angle: float
    gravity: float = 9.8
    time_step: float = 0.1
    max_time: float = 10.0

class PopulationRequest(BaseModel):
    initial_population: int
    birth_rate: float
    death_rate: float
    carrying_capacity: int
    time_steps: int

class QueueRequest(BaseModel):
    arrival_rate: float
    service_rate: float
    simulation_time: float = 100.0

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "55", "name": "Simulation", "timestamp": datetime.now().isoformat()}

@app.post("/monte_carlo")
async def monte_carlo(request: MonteCarloRequest):
    """蒙特卡洛模拟"""
    if request.function == "pi":
        inside = sum(1 for _ in range(request.samples) if random.random()**2 + random.random()**2 <= 1)
        pi_estimate = 4 * inside / request.samples
        return {"success": True, "function": "pi", "estimate": pi_estimate, "actual": math.pi, "error": abs(pi_estimate - math.pi)}
    elif request.function == "integral":
        total = sum(random.random()**2 for _ in range(request.samples))
        estimate = total / request.samples
        return {"success": True, "function": "x^2 from 0 to 1", "estimate": estimate, "actual": 1/3}
    return {"success": False, "error": "Unknown function"}

@app.post("/projectile")
async def projectile_motion(request: PhysicsRequest):
    """抛体运动模拟"""
    v0 = request.initial_velocity
    angle_rad = math.radians(request.angle)
    vx = v0 * math.cos(angle_rad)
    vy = v0 * math.sin(angle_rad)
    g = request.gravity
    dt = request.time_step
    
    trajectory = []
    x, y, t = 0, 0, 0
    while y >= 0 and t <= request.max_time:
        trajectory.append({"t": round(t, 2), "x": round(x, 2), "y": round(y, 2)})
        x += vx * dt
        y += vy * dt
        vy -= g * dt
        t += dt
    
    max_height = (v0 * math.sin(angle_rad))**2 / (2 * g)
    range_ = (v0**2 * math.sin(2 * angle_rad)) / g
    
    return {"success": True, "trajectory": trajectory, "max_height": round(max_height, 2), "range": round(range_, 2)}

@app.post("/population")
async def population_dynamics(request: PopulationRequest):
    """种群动态模拟 (Logistic Growth)"""
    population = request.initial_population
    history = [population]
    
    for _ in range(request.time_steps):
        growth = request.birth_rate * population * (1 - population / request.carrying_capacity)
        deaths = request.death_rate * population
        population = max(0, int(population + growth - deaths))
        history.append(population)
    
    return {"success": True, "history": history, "final_population": population, "carrying_capacity": request.carrying_capacity}

@app.post("/queue")
async def queue_simulation(request: QueueRequest):
    """M/M/1 队列模拟"""
    arrivals = []
    departures = []
    t = 0
    queue_length = 0
    total_wait = 0
    customers = 0
    
    while t < request.simulation_time:
        inter_arrival = random.expovariate(request.arrival_rate)
        t += inter_arrival
        if t >= request.simulation_time:
            break
        arrivals.append(t)
        queue_length += 1
        customers += 1
        
        service_time = random.expovariate(request.service_rate)
        departure = t + service_time + (queue_length - 1) * random.expovariate(request.service_rate)
        departures.append(departure)
        total_wait += departure - t
        queue_length = max(0, queue_length - 1)
    
    avg_wait = total_wait / customers if customers > 0 else 0
    utilization = request.arrival_rate / request.service_rate
    
    return {"success": True, "customers_served": customers, "average_wait": round(avg_wait, 2), "utilization": round(utilization, 2)}

@app.post("/random_walk")
async def random_walk(steps: int = 100, dimensions: int = 2):
    """随机游走模拟"""
    position = [0] * dimensions
    path = [position.copy()]
    
    for _ in range(steps):
        dim = random.randint(0, dimensions - 1)
        direction = random.choice([-1, 1])
        position[dim] += direction
        path.append(position.copy())
    
    distance = math.sqrt(sum(p**2 for p in position))
    return {"success": True, "final_position": position, "distance_from_origin": round(distance, 2), "steps": steps}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "monte_carlo": return await monte_carlo(MonteCarloRequest(**params))
    elif tool == "projectile": return await projectile_motion(PhysicsRequest(**params))
    elif tool == "population": return await population_dynamics(PopulationRequest(**params))
    elif tool == "queue": return await queue_simulation(QueueRequest(**params))
    elif tool == "random_walk": return await random_walk(params.get("steps", 100), params.get("dimensions", 2))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8055)
