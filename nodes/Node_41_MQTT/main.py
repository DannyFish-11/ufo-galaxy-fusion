"""Node 41: MQTT - 消息队列"""
import os, json
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 41 - MQTT", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

paho_mqtt = None
try:
    import paho.mqtt.client as mqtt
    paho_mqtt = mqtt
except ImportError:
    pass

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASS = os.getenv("MQTT_PASS", "")

class PublishRequest(BaseModel):
    topic: str
    payload: Any
    qos: int = 0
    retain: bool = False

@app.get("/health")
async def health():
    return {"status": "healthy" if paho_mqtt else "degraded", "node_id": "41", "name": "MQTT", "paho_available": paho_mqtt is not None, "timestamp": datetime.now().isoformat()}

@app.post("/publish")
async def publish(request: PublishRequest):
    if not paho_mqtt:
        raise HTTPException(status_code=503, detail="paho-mqtt not installed. Run: pip install paho-mqtt")
    try:
        client = paho_mqtt.Client()
        if MQTT_USER:
            client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        payload = json.dumps(request.payload) if isinstance(request.payload, (dict, list)) else str(request.payload)
        result = client.publish(request.topic, payload, qos=request.qos, retain=request.retain)
        client.disconnect()
        return {"success": True, "topic": request.topic, "mid": result.mid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "publish": return await publish(PublishRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8041)
