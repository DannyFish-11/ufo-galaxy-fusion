#!/usr/bin/env python3
"""
Node 50 - Transformer (NLU Brain)
UFO³ Galaxy 的核心 NLU 引擎，负责：
1. 接收来自各客户端的自然语言命令
2. 理解用户意图并解析任务
3. 智能分发任务到相应的节点
4. 协调多节点协同工作
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Node50")

# OneAPI 配置
ONEAPI_BASE_URL = os.getenv("ONEAPI_BASE_URL", "http://100.123.215.126:3000/v1")
ONEAPI_API_KEY = os.getenv("ONEAPI_API_KEY", "sk-your-oneapi-key")

# 节点能力注册表
NODE_CAPABILITIES = {
    "Node_42": ["camera", "vision", "surveillance", "detection", "拍照", "监控", "检测", "巡逻"],
    "Node_43": ["3d_print", "bambu", "printer", "打印", "制造", "3D打印"],
    "Node_48": ["video", "image", "media", "pixverse", "视频", "图片", "生成", "创作"],
    "Node_60": ["compute", "quantum", "ibm", "optimization", "计算", "量子", "优化", "路径"],
    "windows": ["desktop", "automation", "browser", "file", "桌面", "浏览器", "文件", "操作"],
    "android": ["mobile", "notification", "sensor", "移动", "通知", "传感器"]
}

# 任务模板
TASK_TEMPLATES = {
    "3d_print": {
        "target_node": "Node_43",
        "action": "start_print",
        "parameters": ["model_file", "material", "quality"]
    },
    "video_generation": {
        "target_node": "Node_48",
        "action": "generate_video",
        "parameters": ["prompt", "duration", "style"]
    },
    "quantum_compute": {
        "target_node": "Node_60",
        "action": "optimize_path",
        "parameters": ["problem_type", "constraints"]
    },
    "camera_capture": {
        "target_node": "Node_42",
        "action": "capture_image",
        "parameters": ["resolution", "mode"]
    },
    "desktop_automation": {
        "target_node": "windows",
        "action": "automate",
        "parameters": ["steps", "target_app"]
    }
}

class ConnectionManager:
    """WebSocket 连接管理器"""
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.node_info: Dict[str, Dict] = {}
    
    async def connect(self, device_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[device_id] = websocket
        self.node_info[device_id] = {
            "connected_at": datetime.now().isoformat(),
            "status": "online"
        }
        logger.info(f"Device {device_id} connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, device_id: str):
        if device_id in self.active_connections:
            del self.active_connections[device_id]
        if device_id in self.node_info:
            self.node_info[device_id]["status"] = "offline"
        logger.info(f"Device {device_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_to_device(self, device_id: str, message: dict):
        """发送消息到指定设备"""
        if device_id in self.active_connections:
            try:
                await self.active_connections[device_id].send_json(message)
                return True
            except Exception as e:
                logger.error(f"Failed to send message to {device_id}: {e}")
                return False
        else:
            logger.warning(f"Device {device_id} not connected")
            return False
    
    async def broadcast(self, message: dict, exclude: Optional[str] = None):
        """广播消息到所有连接的设备"""
        for device_id, websocket in self.active_connections.items():
            if device_id != exclude:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Failed to broadcast to {device_id}: {e}")

class NLUEngine:
    """自然语言理解引擎"""
    
    def __init__(self):
        self.oneapi_available = False
        self._check_oneapi()
    
    def _check_oneapi(self):
        """检查 OneAPI 是否可用"""
        try:
            import requests
            response = requests.get(f"{ONEAPI_BASE_URL}/models", timeout=5)
            self.oneapi_available = response.status_code == 200
            logger.info(f"OneAPI status: {'Available' if self.oneapi_available else 'Unavailable'}")
        except Exception as e:
            logger.warning(f"OneAPI not available: {e}")
            self.oneapi_available = False
    
    async def understand_command(self, command: str, context: dict = None) -> dict:
        """
        理解用户命令并生成任务计划
        
        Args:
            command: 用户输入的自然语言命令
            context: 上下文信息（如当前设备、历史任务等）
        
        Returns:
            任务计划字典，包含目标节点、动作和参数
        """
        logger.info(f"Understanding command: {command}")
        
        # 如果 OneAPI 可用，使用 AI 模型进行理解
        if self.oneapi_available:
            return await self._understand_with_ai(command, context)
        else:
            # 否则使用规则匹配
            return self._understand_with_rules(command)
    
    async def _understand_with_ai(self, command: str, context: dict = None) -> dict:
        """使用 AI 模型理解命令"""
        try:
            import requests
            
            system_prompt = """你是 UFO³ Galaxy 系统的 NLU 引擎。你的任务是理解用户的自然语言命令，并将其转换为结构化的任务计划。

可用的节点和能力：
- Node_42: 摄像头、视觉检测、监控、巡逻
- Node_43: 3D 打印、Bambu Lab 打印机控制
- Node_48: 视频生成、图片生成、媒体创作 (PixVerse)
- Node_60: 异构计算、量子计算、路径优化 (IBM Quantum)
- windows: 桌面自动化、浏览器控制、文件操作
- android: 移动设备控制、通知、传感器

请将用户命令转换为 JSON 格式的任务计划：
{
    "intent": "任务意图",
    "target_nodes": ["目标节点列表"],
    "tasks": [
        {
            "node": "节点名称",
            "action": "动作名称",
            "parameters": {"参数名": "参数值"}
        }
    ],
    "workflow": "sequential" 或 "parallel"
}"""

            user_prompt = f"用户命令：{command}"
            if context:
                user_prompt += f"\n上下文：{json.dumps(context, ensure_ascii=False)}"
            
            response = requests.post(
                f"{ONEAPI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {ONEAPI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                task_plan = json.loads(content)
                logger.info(f"AI understanding result: {task_plan}")
                return task_plan
            else:
                logger.error(f"AI API error: {response.status_code} - {response.text}")
                return self._understand_with_rules(command)
        
        except Exception as e:
            logger.error(f"AI understanding failed: {e}")
            return self._understand_with_rules(command)
    
    def _understand_with_rules(self, command: str) -> dict:
        """使用规则匹配理解命令（备用方案）"""
        command_lower = command.lower()
        
        # 3D 打印相关
        if any(kw in command_lower for kw in ["打印", "3d", "bambu", "print"]):
            return {
                "intent": "3d_print",
                "target_nodes": ["Node_43"],
                "tasks": [{
                    "node": "Node_43",
                    "action": "start_print",
                    "parameters": {
                        "command": command,
                        "model_file": "warning_sign.3mf" if "警告" in command else "default.3mf"
                    }
                }],
                "workflow": "sequential"
            }
        
        # 视频生成相关
        elif any(kw in command_lower for kw in ["视频", "生成", "video", "pixverse", "创作"]):
            return {
                "intent": "video_generation",
                "target_nodes": ["Node_48"],
                "tasks": [{
                    "node": "Node_48",
                    "action": "generate_video",
                    "parameters": {
                        "prompt": command,
                        "duration": 5,
                        "style": "realistic"
                    }
                }],
                "workflow": "sequential"
            }
        
        # 量子计算相关
        elif any(kw in command_lower for kw in ["优化", "路径", "计算", "quantum", "量子"]):
            return {
                "intent": "quantum_compute",
                "target_nodes": ["Node_60"],
                "tasks": [{
                    "node": "Node_60",
                    "action": "optimize_path",
                    "parameters": {
                        "problem_type": "tsp",
                        "description": command
                    }
                }],
                "workflow": "sequential"
            }
        
        # 摄像头相关
        elif any(kw in command_lower for kw in ["拍照", "监控", "巡逻", "camera", "检测"]):
            return {
                "intent": "camera_capture",
                "target_nodes": ["Node_42"],
                "tasks": [{
                    "node": "Node_42",
                    "action": "capture_image",
                    "parameters": {
                        "mode": "surveillance" if "巡逻" in command else "single",
                        "resolution": "1080p"
                    }
                }],
                "workflow": "sequential"
            }
        
        # 桌面自动化相关
        elif any(kw in command_lower for kw in ["浏览器", "打开", "搜索", "browser", "桌面"]):
            return {
                "intent": "desktop_automation",
                "target_nodes": ["windows"],
                "tasks": [{
                    "node": "windows",
                    "action": "automate",
                    "parameters": {
                        "command": command
                    }
                }],
                "workflow": "sequential"
            }
        
        # 复杂任务：巡逻 + 检测 + 打印
        elif "巡逻" in command and "异常" in command:
            return {
                "intent": "patrol_and_alert",
                "target_nodes": ["Node_42", "Node_43"],
                "tasks": [
                    {
                        "node": "Node_42",
                        "action": "start_surveillance",
                        "parameters": {"mode": "continuous", "alert_on_anomaly": True}
                    },
                    {
                        "node": "Node_43",
                        "action": "prepare_print",
                        "parameters": {"model_file": "warning_sign.3mf", "trigger": "on_alert"}
                    }
                ],
                "workflow": "parallel"
            }
        
        # 默认：未识别的命令
        else:
            return {
                "intent": "unknown",
                "target_nodes": [],
                "tasks": [],
                "workflow": "sequential",
                "error": "无法识别的命令"
            }

# 创建 FastAPI 应用
app = FastAPI(title="Node 50 - Transformer (NLU Brain)")
manager = ConnectionManager()
nlu_engine = NLUEngine()

@app.get("/")
async def root():
    return {
        "node": "Node_50_Transformer",
        "status": "running",
        "version": "1.0.0",
        "capabilities": ["nlu", "task_dispatch", "coordination"],
        "active_connections": len(manager.active_connections)
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "oneapi_available": nlu_engine.oneapi_available,
        "connected_devices": list(manager.active_connections.keys())
    }

@app.websocket("/ws/ufo3/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    """
    WebSocket 端点，处理客户端连接和消息
    
    AIP/1.0 协议格式：
    {
        "protocol": "AIP/1.0",
        "message_id": "unique_id",
        "timestamp": "ISO8601",
        "from": "device_id",
        "to": "target_device_id",
        "type": "command|response|event|heartbeat",
        "payload": {...}
    }
    """
    await manager.connect(device_id, websocket)
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()
            logger.info(f"Received from {device_id}: {data}")
            
            # 验证 AIP 协议
            if data.get("protocol") != "AIP/1.0":
                await websocket.send_json({
                    "protocol": "AIP/1.0",
                    "type": "error",
                    "payload": {"error": "Invalid protocol version"}
                })
                continue
            
            message_type = data.get("type")
            payload = data.get("payload", {})
            
            # 处理不同类型的消息
            if message_type == "command":
                # 用户命令
                command = payload.get("command", "")
                context = payload.get("context", {})
                
                # NLU 理解
                task_plan = await nlu_engine.understand_command(command, context)
                
                # 发送理解结果给发送者
                await manager.send_to_device(device_id, {
                    "protocol": "AIP/1.0",
                    "message_id": f"resp_{data.get('message_id')}",
                    "timestamp": datetime.now().isoformat(),
                    "from": "Node_50",
                    "to": device_id,
                    "type": "response",
                    "payload": {
                        "status": "understood",
                        "task_plan": task_plan
                    }
                })
                
                # 分发任务到目标节点
                for task in task_plan.get("tasks", []):
                    target_node = task.get("node")
                    if target_node in manager.active_connections:
                        await manager.send_to_device(target_node, {
                            "protocol": "AIP/1.0",
                            "message_id": f"task_{datetime.now().timestamp()}",
                            "timestamp": datetime.now().isoformat(),
                            "from": "Node_50",
                            "to": target_node,
                            "type": "command",
                            "payload": {
                                "action": task.get("action"),
                                "parameters": task.get("parameters"),
                                "source_device": device_id
                            }
                        })
                        logger.info(f"Task dispatched to {target_node}: {task}")
                    else:
                        logger.warning(f"Target node {target_node} not connected")
            
            elif message_type == "response":
                # 节点响应，转发给原始请求者
                source_device = payload.get("source_device")
                if source_device and source_device in manager.active_connections:
                    await manager.send_to_device(source_device, data)
            
            elif message_type == "event":
                # 事件通知，广播给所有设备
                await manager.broadcast(data, exclude=device_id)
            
            elif message_type == "heartbeat":
                # 心跳响应
                await websocket.send_json({
                    "protocol": "AIP/1.0",
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(device_id)
    except Exception as e:
        logger.error(f"WebSocket error for {device_id}: {e}")
        manager.disconnect(device_id)

if __name__ == "__main__":
    # 从环境变量读取端口
    port = int(os.getenv("NODE_50_PORT", "8050"))
    
    logger.info("=" * 60)
    logger.info("Node 50 - Transformer (NLU Brain) Starting...")
    logger.info(f"Listening on port: {port}")
    logger.info(f"OneAPI Base URL: {ONEAPI_BASE_URL}")
    logger.info("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
