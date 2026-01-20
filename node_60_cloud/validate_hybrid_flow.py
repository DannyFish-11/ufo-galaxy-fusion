import os
import json
import time
from hybrid_dispatcher import HybridDispatcher

class MockWebsocket:
    def send(self, message):
        data = json.loads(message)
        print(f"[MOCK WS] Sent to Node 50: {data['type']} - {data['payload'].get('details', '')}")

def run_test_scenario(name, env_vars, commands):
    print(f"\n--- Test Scenario: {name} ---")
    # 设置环境变量模拟不同环境
    for k, v in env_vars.items():
        os.environ[k] = v
    
    ws = MockWebsocket()
    dispatcher = HybridDispatcher(ws)
    
    for cmd in commands:
        dispatcher.dispatch(cmd)

if __name__ == "__main__":
    # 场景 1: 华为昇腾 ACL + 华为 HiQ 量子云
    run_test_scenario(
        "Huawei Ascend ACL + HiQ Quantum",
        {"ATLAS_MODE": "ACL", "QUANTUM_PROVIDER": "HUAWEI_HIQ"},
        [
            {
                "type": "command",
                "payload": {"command": "atlas_inference", "params": {"model": "resnet50"}}
            },
            {
                "type": "command",
                "payload": {"command": "quantum_optimize", "params": {"type": "vqe_routing"}}
            }
        ]
    )

    # 场景 2: 昇腾 MindSpore + 本地量子模拟器
    run_test_scenario(
        "MindSpore + Local Simulator",
        {"ATLAS_MODE": "MINDSPORE", "QUANTUM_PROVIDER": "SIMULATOR"},
        [
            {
                "type": "command",
                "payload": {"command": "atlas_inference", "params": {"model": "yolov8"}}
            },
            {
                "type": "command",
                "payload": {"command": "quantum_optimize", "params": {"type": "path_planning"}}
            }
        ]
    )

    # 场景 3: IBM Quantum 真实后端模拟
    run_test_scenario(
        "IBM Quantum Real Backend Simulation",
        {"ATLAS_MODE": "MOCK", "QUANTUM_PROVIDER": "IBM_QUANTUM", "IBM_QUANTUM_TOKEN": "MOCK_TOKEN"},
        [
            {
                "type": "command",
                "payload": {"command": "quantum_optimize", "params": {"type": "vqe_routing", "backend": "ibm_oslo"}}
            }
        ]
    )

    # 场景 4: 云端 REST API + 经典计算
    run_test_scenario(
        "Cloud REST + Classical Compute",
        {"ATLAS_MODE": "REST", "QUANTUM_PROVIDER": "SIMULATOR"},
        [
            {
                "type": "command",
                "payload": {"command": "atlas_inference", "params": {"model": "bert_nlp"}}
            },
            {
                "type": "command",
                "payload": {"command": "classical_compute", "params": {"task": "log_analysis"}}
            }
        ]
    )
