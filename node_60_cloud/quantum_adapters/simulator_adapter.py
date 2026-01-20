from typing import Dict, Any
import time
from .base_adapter import QuantumAdapterBase

class SimulatorAdapter(QuantumAdapterBase):
    """
    本地模拟器适配器（用于保底演示和测试）。
    """
    
    def __init__(self):
        self._connected = True
        self._name = "SIMULATOR_PROVIDER"

    @property
    def name(self) -> str:
        return self._name

    def connect(self) -> bool:
        """本地模拟器无需连接"""
        return True

    def run_optimization(self, circuit_data: Dict, backend: str = "local") -> Dict:
        """
        模拟运行量子优化任务。
        """
        print(f"[{self.name}] Running local simulation for optimization...")
        time.sleep(1) # 模拟快速计算
        
        job_id = f"sim_job_{int(time.time())}"
        
        # 模拟结果
        result = {
            "job_id": job_id,
            "status": "COMPLETED",
            "optimization_result": {
                "qubits": circuit_data.get("qubits", 4),
                "iterations": 5,
                "optimized_route": [1, 50, 60, 43, 2],
                "energy_cost": -0.75 # 模拟结果略差于真实量子机
            }
        }
        print(f"[{self.name}] Job {job_id} completed.")
        return result

    def get_status(self, job_id: str) -> str:
        """查询任务状态"""
        return "COMPLETED"
