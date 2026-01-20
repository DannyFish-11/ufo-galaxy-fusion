from abc import ABC, abstractmethod
from typing import Dict, Any

class QuantumAdapterBase(ABC):
    """
    量子计算适配器基类。
    所有具体的量子云实现（如 HiQ, OriginQ, IBM Qiskit）都应继承此类。
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """连接到量子云后端"""
        pass

    @abstractmethod
    def run_optimization(self, circuit_data: Dict, backend: str) -> Dict:
        """
        运行量子优化任务。
        :param circuit_data: 包含量子线路、参数等任务数据。
        :param backend: 目标后端名称（如 'simulator', 'real_device'）。
        :return: 包含优化结果的字典。
        """
        pass

    @abstractmethod
    def get_status(self, job_id: str) -> str:
        """查询任务状态"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """适配器名称"""
        pass
