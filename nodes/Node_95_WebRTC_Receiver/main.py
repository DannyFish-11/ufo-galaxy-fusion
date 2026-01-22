"""
Node_95: WebRTC 接收器

功能：
1. 接收来自安卓端的 WebRTC 视频流
2. 解码 H.264 视频流
3. 提供 HTTP API 供 Node_90 (VLM) 调用
4. 支持实时截图和视频录制

作者: Manus AI
版本: 1.0
日期: 2026-01-22
"""

import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import uvicorn
from typing import Optional, Dict
import json
import base64
from datetime import datetime
import io
from PIL import Image

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Node_95: WebRTC Receiver", version="1.0")

# 全局状态
class WebRTCState:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.latest_frame: Optional[bytes] = None
        self.frame_timestamp: Optional[datetime] = None
        self.is_receiving = False
    
    def update_frame(self, frame_data: bytes):
        """更新最新帧"""
        self.latest_frame = frame_data
        self.frame_timestamp = datetime.now()
        self.is_receiving = True

state = WebRTCState()

# API 模型
class SignalingMessage(BaseModel):
    type: str  # "offer", "answer", "ice_candidate"
    sdp: Optional[str] = None
    candidate: Optional[str] = None
    device_id: str

class FrameRequest(BaseModel):
    device_id: str
    format: str = "jpeg"  # "jpeg", "png", "raw"

# ============================================
# WebSocket 信令端点
# ============================================

@app.websocket("/signaling/{device_id}")
async def websocket_signaling(websocket: WebSocket, device_id: str):
    """
    WebRTC 信令 WebSocket 端点
    处理 Offer/Answer/ICE Candidate 交换
    """
    await websocket.accept()
    state.connections[device_id] = websocket
    logger.info(f"Device {device_id} connected for signaling")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 处理信令消息
            await handle_signaling_message(device_id, message)
            
    except WebSocketDisconnect:
        logger.info(f"Device {device_id} disconnected")
        state.connections.pop(device_id, None)
    except Exception as e:
        logger.error(f"Error in signaling for {device_id}: {e}")
        state.connections.pop(device_id, None)

async def handle_signaling_message(device_id: str, message: dict):
    """处理信令消息"""
    msg_type = message.get("type")
    logger.info(f"Received signaling message from {device_id}: {msg_type}")
    
    if msg_type == "offer":
        # TODO: 创建 Answer 并发送回设备
        answer = await create_answer(message.get("sdp"))
        await send_signaling_message(device_id, {
            "type": "answer",
            "sdp": answer
        })
    elif msg_type == "ice_candidate":
        # TODO: 添加 ICE Candidate
        await add_ice_candidate(device_id, message.get("candidate"))

async def send_signaling_message(device_id: str, message: dict):
    """发送信令消息到设备"""
    websocket = state.connections.get(device_id)
    if websocket:
        await websocket.send_text(json.dumps(message))

async def create_answer(offer_sdp: str) -> str:
    """创建 Answer SDP"""
    # TODO: 使用 aiortc 创建 Answer
    logger.info("Creating answer...")
    return "answer_sdp_placeholder"

async def add_ice_candidate(device_id: str, candidate: str):
    """添加 ICE Candidate"""
    # TODO: 使用 aiortc 添加 ICE Candidate
    logger.info(f"Adding ICE candidate for {device_id}")

# ============================================
# WebSocket 视频流端点
# ============================================

@app.websocket("/stream/{device_id}")
async def websocket_stream(websocket: WebSocket, device_id: str):
    """
    WebSocket 视频流端点
    接收来自安卓端的编码后的视频帧
    """
    await websocket.accept()
    logger.info(f"Device {device_id} connected for streaming")
    
    try:
        while True:
            # 接收二进制数据 (H.264 编码的视频帧)
            data = await websocket.receive_bytes()
            
            # 更新最新帧
            state.update_frame(data)
            logger.debug(f"Received frame from {device_id}: {len(data)} bytes")
            
    except WebSocketDisconnect:
        logger.info(f"Device {device_id} stream disconnected")
        state.is_receiving = False
    except Exception as e:
        logger.error(f"Error in stream for {device_id}: {e}")
        state.is_receiving = False

# ============================================
# HTTP API 端点
# ============================================

@app.get("/")
async def root():
    """根端点"""
    return {
        "service": "Node_95: WebRTC Receiver",
        "version": "1.0",
        "status": "running",
        "is_receiving": state.is_receiving,
        "last_frame_time": state.frame_timestamp.isoformat() if state.frame_timestamp else None
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "is_receiving": state.is_receiving,
        "connected_devices": len(state.connections)
    }

@app.post("/get_latest_frame")
async def get_latest_frame(request: FrameRequest):
    """
    获取最新的视频帧
    供 Node_90 (VLM) 调用
    """
    if not state.latest_frame:
        return JSONResponse(
            status_code=404,
            content={"error": "No frame available"}
        )
    
    # TODO: 解码 H.264 帧为 JPEG/PNG
    # 当前版本返回原始数据
    frame_base64 = base64.b64encode(state.latest_frame).decode('utf-8')
    
    return {
        "success": True,
        "device_id": request.device_id,
        "timestamp": state.frame_timestamp.isoformat(),
        "format": request.format,
        "frame_data": frame_base64
    }

@app.get("/stream_mjpeg/{device_id}")
async def stream_mjpeg(device_id: str):
    """
    MJPEG 流端点
    供浏览器或其他客户端实时查看
    """
    async def generate():
        while True:
            if state.latest_frame:
                # TODO: 将 H.264 帧转换为 JPEG
                # 当前版本返回占位符
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + state.latest_frame + b'\r\n')
            await asyncio.sleep(0.033)  # ~30 FPS
    
    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    logger.info("Starting Node_95: WebRTC Receiver on port 8095")
    uvicorn.run(app, host="0.0.0.0", port=8095, log_level="info")
