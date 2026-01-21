"""
UFO³ Galaxy - 统一 LLM 客户端
所有节点通过这个客户端调用 One-API 和本地 LLM
"""

import httpx
import os
from typing import List, Dict, Optional, AsyncIterator
from enum import Enum


class TaskType(Enum):
    """任务类型枚举"""
    CODE = "code"  # 代码生成
    REAL_TIME = "real_time"  # 实时信息
    COMPLEX = "complex"  # 复杂推理
    CHINESE = "chinese"  # 中文对话
    GENERAL = "general"  # 通用任务


class UnifiedLLMClient:
    """
    统一 LLM 客户端
    提供统一的接口调用 One-API 和本地 LLM
    """
    
    def __init__(
        self,
        one_api_url: str = None,
        local_llm_url: str = None,
        timeout: float = 60.0
    ):
        """
        初始化客户端
        
        Args:
            one_api_url: One-API 地址（默认从环境变量读取）
            local_llm_url: 本地 LLM 地址（默认从环境变量读取）
            timeout: 超时时间（秒）
        """
        self.one_api_url = one_api_url or os.getenv(
            "ONE_API_URL", "http://localhost:8001"
        )
        self.local_llm_url = local_llm_url or os.getenv(
            "LOCAL_LLM_URL", "http://localhost:8079"
        )
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "auto",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False,
        use_one_api: bool = True
    ) -> Dict:
        """
        统一的聊天接口
        
        Args:
            messages: 对话历史
                格式: [{"role": "user", "content": "..."}]
            model: 模型选择
                - "auto": 自动选择（推荐）
                - "local/*": 本地模型
                - "groq/*": Groq 模型
                - "together/*": Together AI 模型
                - "perplexity/*": Perplexity 模型
                - "zhipu/*": 智谱 AI 模型
                - "claude/*": Claude 模型
            temperature: 温度 (0.0-2.0)
            max_tokens: 最大 tokens
            stream: 是否流式输出
            use_one_api: 是否使用 One-API（False 则直接调用本地 LLM）
        
        Returns:
            响应结果
        """
        url = f"{self.one_api_url}/v1/chat/completions" if use_one_api else f"{self.local_llm_url}/v1/chat/completions"
        
        try:
            response = await self.client.post(
                url,
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": stream
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "error": str(e),
                "message": "LLM 调用失败"
            }
    
    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        model: str = "auto",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        use_one_api: bool = True
    ) -> AsyncIterator[str]:
        """
        流式聊天接口
        
        Args:
            同 chat() 方法
        
        Yields:
            流式响应的文本片段
        """
        url = f"{self.one_api_url}/v1/chat/completions" if use_one_api else f"{self.local_llm_url}/v1/chat/completions"
        
        async with self.client.stream(
            "POST",
            url,
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
        ) as response:
            async for chunk in response.aiter_text():
                if chunk.strip():
                    yield chunk
    
    async def chat_with_task_type(
        self,
        messages: List[Dict[str, str]],
        task_type: TaskType = TaskType.GENERAL,
        **kwargs
    ) -> Dict:
        """
        根据任务类型自动选择模型
        
        Args:
            messages: 对话历史
            task_type: 任务类型（TaskType 枚举）
            **kwargs: 其他参数传递给 chat()
        
        Returns:
            响应结果
        """
        # 根据任务类型选择模型
        model_map = {
            TaskType.CODE: "local/deepseek-coder:6.7b-instruct-q4_K_M",
            TaskType.REAL_TIME: "perplexity/sonar-pro",
            TaskType.COMPLEX: "together/deepseek-ai/DeepSeek-V3",
            TaskType.CHINESE: "local/qwen2.5:7b-instruct-q4_K_M",
            TaskType.GENERAL: "auto"
        }
        
        model = model_map.get(task_type, "auto")
        return await self.chat(messages, model=model, **kwargs)
    
    async def simple_ask(
        self,
        question: str,
        model: str = "auto",
        system_prompt: Optional[str] = None
    ) -> str:
        """
        简单问答接口（单轮对话）
        
        Args:
            question: 用户问题
            model: 模型选择
            system_prompt: 系统提示词（可选）
        
        Returns:
            回答文本
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": question})
        
        response = await self.chat(messages, model=model)
        
        if "error" in response:
            return f"错误: {response['message']}"
        
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")
    
    async def code_generation(
        self,
        prompt: str,
        language: str = "python"
    ) -> str:
        """
        代码生成专用接口
        
        Args:
            prompt: 代码需求描述
            language: 编程语言
        
        Returns:
            生成的代码
        """
        system_prompt = f"You are an expert {language} programmer. Generate clean, efficient, and well-documented code."
        
        return await self.simple_ask(
            prompt,
            model="local/deepseek-coder:6.7b-instruct-q4_K_M",
            system_prompt=system_prompt
        )
    
    async def real_time_search(
        self,
        query: str
    ) -> str:
        """
        实时搜索专用接口
        
        Args:
            query: 搜索查询
        
        Returns:
            搜索结果（带来源）
        """
        return await self.simple_ask(
            query,
            model="perplexity/sonar-pro"
        )
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import asyncio
        asyncio.run(self.close())


# 全局单例
_llm_client: Optional[UnifiedLLMClient] = None


def get_llm_client() -> UnifiedLLMClient:
    """
    获取全局 LLM 客户端单例
    
    Returns:
        UnifiedLLMClient 实例
    """
    global _llm_client
    if _llm_client is None:
        _llm_client = UnifiedLLMClient()
    return _llm_client


# 便捷函数
async def ask(question: str, model: str = "auto") -> str:
    """
    快速问答（全局函数）
    
    Args:
        question: 问题
        model: 模型选择
    
    Returns:
        回答
    """
    client = get_llm_client()
    return await client.simple_ask(question, model)


async def generate_code(prompt: str, language: str = "python") -> str:
    """
    快速代码生成（全局函数）
    
    Args:
        prompt: 代码需求
        language: 编程语言
    
    Returns:
        生成的代码
    """
    client = get_llm_client()
    return await client.code_generation(prompt, language)


async def search_realtime(query: str) -> str:
    """
    快速实时搜索（全局函数）
    
    Args:
        query: 搜索查询
    
    Returns:
        搜索结果
    """
    client = get_llm_client()
    return await client.real_time_search(query)
