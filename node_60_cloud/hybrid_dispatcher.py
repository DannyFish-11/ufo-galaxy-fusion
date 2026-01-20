import os
import asyncio
import websockets
import json
import time
from typing import Dict, Any, Optional

try:
    from .quantum_adapters.base_adapter import QuantumAdapterBase
    from .quantum_adapters.hiq_adapter import HuaweiHiQAdapter
    from .quantum_adapters.simulator_adapter import SimulatorAdapter
    from .quantum_adapters.qiskit_adapter import QiskitAdapter
except ImportError:
    from quantum_adapters.base_adapter import QuantumAdapterBase
    from quantum_adapters.hiq_adapter import HuaweiHiQAdapter
    from quantum_adapters.simulator_adapter import SimulatorAdapter
    from quantum_adapters.qiskit_adapter import QiskitAdapter

# --- Configuration ---
TAILSCALE_IP = os.environ.get("TAILSCALE_IP", "100.100.100.100") 
NODE_50_URL = os.environ.get("NODE_50_URL", f"ws://{TAILSCALE_IP}:8050")
DEVICE_ID = os.environ.get("DEVICE_ID", "Node_60_Hybrid_Agent")
WS_URL = f"{NODE_50_URL}/ws/ufo3/{DEVICE_ID}"

# --- AIP Communication Functions ---

def send_aip_message(websocket, message_type: str, payload: dict):
    """构造并发送 AIP 消息"""
    message = {
        "protocol": "AIP/1.0",
        "type": message_type,
        "source_node": DEVICE_ID,
        "target_node": "Node_50_Transformer",
        "timestamp": int(time.time()),
        "payload": payload
    }
    # 兼容同步和异步发送
    if hasattr(websocket, 'send'):
        if asyncio.iscoroutinefunction(websocket.send):
            # 异步环境由调用者处理
            pass
        else:
            websocket.send(json.dumps(message))
            print(f"-> Sent {message_type} message.")

async def async_send_aip_message(websocket, message_type: str, payload: dict):
    """异步构造并发送 AIP 消息"""
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

# --- Atlas Bridge ---

class AtlasBridge:
    """
    昇腾 Atlas 桥接器：负责将 AIP 任务转换为昇腾硬件可执行的计算任务。
    """
    def __init__(self):
        self.driver = self._load_driver()

    def _load_driver(self):
        """模拟根据环境加载不同的 Atlas 驱动"""
        mode = os.environ.get("ATLAS_MODE")
        if mode == "ACL":
            print("Atlas Bridge: Loaded ACL Driver (C++ binding).")
            return "ACL_DRIVER"
        elif mode == "MINDSPORE":
            print("Atlas Bridge: Loaded MindSpore Driver (Python).")
            return "MINDSPORE_DRIVER"
        elif mode == "REST":
            print("Atlas Bridge: Loaded REST API Driver (Cloud Service).")
            return "REST_DRIVER"
        else:
            print("Atlas Bridge: Loaded Mock Driver (Local Fallback).")
            return "MOCK_DRIVER"

    def run_inference(self, params: dict) -> Dict:
        """模拟运行推理任务"""
        model_name = params.get("model", "yolov8")
        print(f"Atlas Bridge: Running {model_name} inference using {self.driver}...")
        
        if self.driver == "REST_DRIVER":
            time.sleep(1)
            return {"model": model_name, "driver": self.driver, "result": "Inference complete via Cloud REST API."}
        else:
            time.sleep(2) 
            return {"model": model_name, "driver": self.driver, "result": "Inference complete via Local Accelerator."}

# --- Hybrid Dispatcher Core ---

class HybridDispatcher:
    """
    异构任务分发器：根据 AIP 命令类型，将任务路由到不同的计算模块。
    """
    def __init__(self, websocket):
        self.websocket = websocket
        self.atlas_bridge = AtlasBridge()
        self.quantum_adapter = self._load_quantum_adapter()

    def _load_quantum_adapter(self) -> QuantumAdapterBase:
        """根据环境变量动态加载量子云适配器"""
        provider_name = os.environ.get("QUANTUM_PROVIDER", "SIMULATOR")
        if provider_name == "HUAWEI_HIQ":
            adapter = HuaweiHiQAdapter()
        elif provider_name == "IBM_QUANTUM":
            adapter = QiskitAdapter()
        else:
            adapter = SimulatorAdapter()
        adapter.connect()
        return adapter

    def dispatch(self, data: dict):
        """主分发逻辑"""
        command = data["payload"].get("command")
        params = data["payload"].get("params", {})
        print(f"<- Received command: {command}")
        
        result_payload = {"command": command, "status": "failure", "details": "Not handled."}
        
        try:
            if command == "atlas_inference":
                result = self.atlas_bridge.run_inference(params)
                result_payload.update({"status": "success", "details": "Atlas inference complete.", "result": result})
            elif command == "quantum_optimize":
                result = self.quantum_adapter.run_optimization(params.get("circuit_data", {}), params.get("backend", "simulator"))
                result_payload.update({"status": "success", "details": "Quantum optimization complete.", "result": result})
            elif command == "classical_compute":
                time.sleep(1)
                result_payload.update({"status": "success", "details": "Classical compute complete.", "result": "Success"})
            else:
                result_payload["details"] = f"Unknown command: {command}"
        except Exception as e:
            result_payload["details"] = f"Execution error: {e}"
            
        # 发送结果
        if asyncio.iscoroutinefunction(self.websocket.send):
            # 异步环境需要特殊处理，这里在 dispatch 中我们假设是同步模拟或由外部 await
            pass
        else:
            send_aip_message(self.websocket, "command_result", result_payload)

    async def async_dispatch(self, data: dict):
        """异步分发逻辑"""
        command = data["payload"].get("command")
        params = data["payload"].get("params", {})
        print(f"<- Received command: {command}")
        
        result_payload = {"command": command, "status": "failure", "details": "Not handled."}
        
        try:
            if command == "atlas_inference":
                result = self.atlas_bridge.run_inference(params)
                result_payload.update({"status": "success", "details": "Atlas inference complete.", "result": result})
            elif command == "quantum_optimize":
                result = self.quantum_adapter.run_optimization(params.get("circuit_data", {}), params.get("backend", "simulator"))
                result_payload.update({"status": "success", "details": "Quantum optimization complete.", "result": result})
            elif command == "classical_compute":
                await asyncio.sleep(1)
                result_payload.update({"status": "success", "details": "Classical compute complete.", "result": "Success"})
            else:
                result_payload["details"] = f"Unknown command: {command}"
        except Exception as e:
            result_payload["details"] = f"Execution error: {e}"
            
        await async_send_aip_message(self.websocket, "command_result", result_payload)

# --- Main Client Loop ---

async def client_main():
    print(f"Node 60 Hybrid Agent connecting to {WS_URL}...")
    while True:
        try:
            async with websockets.connect(WS_URL) as websocket:
                print("Connection established.")
                await async_send_aip_message(websocket, "registration", {"device_type": "Hybrid_Compute_Agent"})
                dispatcher = HybridDispatcher(websocket)
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("type") == "command":
                        await dispatcher.async_dispatch(data)
                    elif data.get("type") == "status_request":
                        await async_send_aip_message(websocket, "status_update", {"quantum_provider": dispatcher.quantum_adapter.name})
        except Exception as e:
            print(f"Error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(client_main())
