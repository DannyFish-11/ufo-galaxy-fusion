import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import asyncio

# 导入 Qwen3-VL API 客户端
from qwen_vl_api import analyze_image_with_qwen_vl

# 导入 NLU 相关的结构，用于 Task 封装
from enhanced_nlu_v2 import Task, IntentType

@dataclass
class VLMNodeResult:
    """VLM 节点执行结果"""
    success: bool
    result_text: str
    processing_time: float
    image_url: Optional[str] = None
    error_message: Optional[str] = None

class VLMNode:
    """
    Node_106_VLM: 视觉语言模型（VLM）节点
    
    功能：
    1. 接收图像路径和文本提示。
    2. 调用 Qwen3-VL API 进行多模态分析。
    3. 返回分析结果。
    """
    
    NODE_ID = "Node_106_VLM"
    NODE_NAME = "Qwen3-VL 视觉理解"
    
    def __init__(self):
        print(f"VLMNode initialized: {self.NODE_NAME} ({self.NODE_ID})")
        
    async def execute(self, task: Task) -> VLMNodeResult:
        """
        执行 VLM 任务
        
        Args:
            task: 包含图像路径和提示的 Task 对象。
                  预期参数:
                  - image_path: 图像的本地路径 (str)
                  - prompt: 用户的文本提示 (str)
                  
        Returns:
            VLMNodeResult: 包含执行结果、时间等信息的对象。
        """
        start_time = time.time()
        
        # 1. 参数校验
        image_path = task.parameters.get("image_path")
        prompt = task.parameters.get("prompt")
        
        if not image_path or not prompt:
            end_time = time.time()
            return VLMNodeResult(
                success=False,
                result_text="VLM 节点执行失败：缺少 'image_path' 或 'prompt' 参数。",
                processing_time=end_time - start_time,
                error_message="Missing required parameters."
            )
            
        # 2. 调用 Qwen3-VL API
        try:
            # analyze_image_with_qwen_vl 是同步函数，但我们将其包装在 asyncio.to_thread 中以避免阻塞
            result_text = await asyncio.to_thread(analyze_image_with_qwen_vl, image_path, prompt)
            
            end_time = time.time()
            
            if result_text and not result_text.startswith("Error:"):
                return VLMNodeResult(
                    success=True,
                    result_text=result_text,
                    processing_time=end_time - start_time,
                    image_url=None # 图像 URL 在 API 内部处理，这里不返回
                )
            else:
                return VLMNodeResult(
                    success=False,
                    result_text=f"VLM 节点执行失败：API 返回错误。{result_text}",
                    processing_time=end_time - start_time,
                    error_message=result_text
                )
                
        except Exception as e:
            end_time = time.time()
            error_msg = f"VLM 节点执行异常: {e}"
            print(error_msg)
            return VLMNodeResult(
                success=False,
                result_text=error_msg,
                processing_time=end_time - start_time,
                error_message=str(e)
            )

# 示例用法（在 TaskRouter 中使用）
# async def main():
#     # 假设我们有一个 Task 对象
#     sample_task = Task(
#         task_id="vlm_test_001",
#         device_id="pc", # 假设在 PC 上执行
#         intent_type=IntentType.INFORMATION_QUERY,
#         action="vlm_analyze",
#         target="image",
#         parameters={
#             "image_path": "/home/ubuntu/Downloads/screenshot.png", # 假设这是截图路径
#             "prompt": "这张截图显示了什么？请用 JSON 格式总结出关键信息。"
#         },
#         depends_on=[],
#         confidence=1.0,
#         estimated_duration=5.0
#     )
#     
#     vlm_node = VLMNode()
#     result = await vlm_node.execute(sample_task)
#     print(asdict(result))
# 
# if __name__ == '__main__':
#     import time
#     asyncio.run(main())
