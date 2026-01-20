import asyncio
import websockets
import json
import time
import os

# 假设 Node 50 运行在您的本地电脑上，并通过 Tailscale 获得了 IP
# 您需要将 TAILSCALE_IP 替换为您本地电脑的 Tailscale IP
# 或者使用 mDNS 域名 ufo-galaxy.local (如果已配置)
TAILSCALE_IP = os.environ.get("TAILSCALE_IP", "100.100.100.100") 
NODE_50_URL = os.environ.get("NODE_50_URL", f"ws://{TAILSCALE_IP}:8050")
DEVICE_ID = os.environ.get("DEVICE_ID", "Node_60_Cloud_Compute")
WS_URL = f"{NODE_50_URL}/ws/ufo3/{DEVICE_ID}"

async def send_aip_message(websocket, message_type: str, payload: dict):
    """构造并发送 AIP 消息"""
    message = {
        "protocol": "AIP/1.0",
        "type": message_type,
        "source_node": DEVICE_ID,
        "target_node": "Node_50_Transformer",
        "timestamp": int(time.time()),
        "payload": payload
    }
    await websocket.send(json.dumps(message))
    print(f"-> Sent {message_type} message.")

async def handle_aip_message(message: str, websocket):
    """处理接收到的 AIP 消息"""
    try:
        data = json.loads(message)
        msg_type = data.get("type")
        payload = data.get("payload", {})
        
        print(f"<- Received {msg_type} message.")
        
        if msg_type == "command":
            command = payload.get("command")
            params = payload.get("params", {})
            print(f"   Executing cloud command: {command} with params: {params}")
            
            # 模拟执行云端任务：日志分析、模型推理等
            if command == "analyze_logs":
                log_file = params.get("file_path", "/var/log/syslog")
                # 实际应用中，这里会运行一个复杂的分析脚本
                result = f"Log analysis complete for {log_file}. Found 12 critical errors."
                
            elif command == "backup_data":
                data_path = params.get("path", "/data/ufo_galaxy")
                # 实际应用中，这里会执行 S3 或其他云存储备份
                result = f"Data backup of {data_path} successful."
            
            else:
                result = f"Unknown command {command} received."

            # 模拟发送执行结果
            await send_aip_message(
                websocket, 
                "command_result", 
                {"command": command, "status": "success", "details": result}
            )
            
        elif msg_type == "status_request":
            # 模拟发送云服务器状态
            await send_aip_message(
                websocket, 
                "status_update", 
                {"os": "Ubuntu 22.04", "cpu_cores": 4, "memory_gb": 8, "tailscale_ip": TAILSCALE_IP, "is_active": True}
            )
            
        else:
            print(f"   Unhandled message type: {msg_type}")
            
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {message}")
    except Exception as e:
        print(f"Error handling message: {e}")

async def client_main():
    """Node 60 (Cloud Compute) 客户端主函数"""
    print(f"Connecting to UFO³ Galaxy Node 50 at {WS_URL}...")
    
    while True:
        try:
            async with websockets.connect(WS_URL) as websocket:
                print("Connection established. Sending registration message.")
                
                # 1. 发送注册消息
                await send_aip_message(
                    websocket, 
                    "registration", 
                    {"device_type": "Cloud_Compute", "capabilities": ["analyze_logs", "backup_data", "model_inference"]}
                )
                
                # 2. 持续监听消息
                while True:
                    message = await websocket.recv()
                    await handle_aip_message(message, websocket)
                    
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed gracefully. Reconnecting in 5 seconds...")
        except ConnectionRefusedError:
            print(f"Connection refused to {TAILSCALE_IP}. Node 50 might be down or Tailscale not running. Retrying in 5 seconds...")
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying in 5 seconds...")
            
        await asyncio.sleep(5)

if __name__ == "__main__":
    # 提示用户设置 TAILSCALE_IP 环境变量
    if "TAILSCALE_IP" not in os.environ:
        print("!!! WARNING: TAILSCALE_IP environment variable not set. Using default 100.100.100.100. !!!")
        print("Please set TAILSCALE_IP to your local computer's Tailscale IP for stable connection.")
        
    try:
        asyncio.run(client_main())
    except KeyboardInterrupt:
        print("\nClient stopped by user.")
