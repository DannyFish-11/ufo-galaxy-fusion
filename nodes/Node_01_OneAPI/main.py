"""
Node 01: One-API Gateway
========================
流量总入口，统一管理所有 LLM API 调用。
封装现有 one-api 镜像，提供统一接口。

功能：
- 统一 API 入口 (OpenAI 兼容格式)
- 多模型负载均衡
- API Key 管理
- 请求限流与配额
- 调用统计与计费
"""

import os
import json
import time
import asyncio
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

import httpx
from fastapi import FastAPI, HTTPException, Header, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 01 - One-API Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Configuration
# =============================================================================

class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"
    ONEAPI = "oneapi"

@dataclass
class ProviderConfig:
    name: str
    base_url: str
    api_key: str
    models: List[str]
    priority: int = 0
    weight: int = 1
    enabled: bool = True
    rate_limit: int = 60  # requests per minute
    
@dataclass
class UsageStats:
    total_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    requests_by_model: Dict[str, int] = field(default_factory=dict)
    last_reset: datetime = field(default_factory=datetime.now)

# =============================================================================
# Gateway Core
# =============================================================================

class OneAPIGateway:
    """统一 API 网关"""
    
    def __init__(self):
        self.providers: Dict[str, ProviderConfig] = {}
        self.usage_stats: Dict[str, UsageStats] = {}  # by api_key
        self.rate_limits: Dict[str, List[float]] = {}  # api_key -> timestamps
        self._load_config()
        
    def _load_config(self):
        """加载配置"""
        # One-API 后端 (如果存在)
        oneapi_url = os.getenv("ONEAPI_URL", "http://oneapi:3000")
        oneapi_key = os.getenv("ONEAPI_API_KEY", "")
        
        if oneapi_key:
            self.providers["oneapi"] = ProviderConfig(
                name="One-API Backend",
                base_url=oneapi_url,
                api_key=oneapi_key,
                models=["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"],
                priority=1
            )
        
        # OpenAI 直连
        openai_key = os.getenv("OPENAI_API_KEY", "")
        if openai_key:
            self.providers["openai"] = ProviderConfig(
                name="OpenAI Direct",
                base_url="https://api.openai.com/v1",
                api_key=openai_key,
                models=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
                priority=2
            )
            
        # Anthropic 直连
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        if anthropic_key:
            self.providers["anthropic"] = ProviderConfig(
                name="Anthropic Direct",
                base_url="https://api.anthropic.com/v1",
                api_key=anthropic_key,
                models=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
                priority=2
            )
            
        # 本地 Ollama
        ollama_url = os.getenv("OLLAMA_URL", "http://host.containers.internal:11434")
        self.providers["local"] = ProviderConfig(
            name="Local Ollama",
            base_url=ollama_url,
            api_key="",
            models=["llama2", "mistral", "codellama", "qwen"],
            priority=10,  # 最低优先级作为 fallback
            rate_limit=1000
        )
        
    def _get_provider_for_model(self, model: str) -> Optional[ProviderConfig]:
        """根据模型选择提供商"""
        candidates = []
        for name, provider in self.providers.items():
            if not provider.enabled:
                continue
            # 检查模型是否匹配
            for supported in provider.models:
                if model.startswith(supported) or supported.startswith(model):
                    candidates.append((provider.priority, provider))
                    break
        
        if not candidates:
            # Fallback 到本地
            return self.providers.get("local")
            
        # 按优先级排序
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]
        
    def _check_rate_limit(self, api_key: str, provider: ProviderConfig) -> bool:
        """检查速率限制"""
        now = time.time()
        window = 60  # 1 minute window
        
        if api_key not in self.rate_limits:
            self.rate_limits[api_key] = []
            
        # 清理过期记录
        self.rate_limits[api_key] = [
            ts for ts in self.rate_limits[api_key] 
            if now - ts < window
        ]
        
        if len(self.rate_limits[api_key]) >= provider.rate_limit:
            return False
            
        self.rate_limits[api_key].append(now)
        return True
        
    def _record_usage(self, api_key: str, model: str, tokens: int, cost: float):
        """记录使用统计"""
        if api_key not in self.usage_stats:
            self.usage_stats[api_key] = UsageStats()
            
        stats = self.usage_stats[api_key]
        stats.total_requests += 1
        stats.total_tokens += tokens
        stats.total_cost += cost
        stats.requests_by_model[model] = stats.requests_by_model.get(model, 0) + 1
        
    async def chat_completion(
        self, 
        request: Dict[str, Any],
        api_key: str
    ) -> Dict[str, Any]:
        """处理 chat completion 请求"""
        model = request.get("model", "gpt-3.5-turbo")
        
        # 选择提供商
        provider = self._get_provider_for_model(model)
        if not provider:
            raise HTTPException(status_code=400, detail=f"No provider available for model: {model}")
            
        # 检查速率限制
        if not self._check_rate_limit(api_key, provider):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
        # 构建请求
        headers = {"Content-Type": "application/json"}
        if provider.api_key:
            headers["Authorization"] = f"Bearer {provider.api_key}"
            
        # 发送请求
        async with httpx.AsyncClient(timeout=120.0) as client:
            try:
                if "ollama" in provider.base_url.lower():
                    # Ollama 格式
                    response = await client.post(
                        f"{provider.base_url}/api/chat",
                        json={
                            "model": model,
                            "messages": request.get("messages", []),
                            "stream": False
                        }
                    )
                else:
                    # OpenAI 兼容格式
                    response = await client.post(
                        f"{provider.base_url}/chat/completions",
                        headers=headers,
                        json=request
                    )
                    
                response.raise_for_status()
                result = response.json()
                
                # 记录使用
                tokens = result.get("usage", {}).get("total_tokens", 0)
                cost = self._estimate_cost(model, tokens)
                self._record_usage(api_key, model, tokens, cost)
                
                return result
                
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Provider error: {str(e)}")
                
    def _estimate_cost(self, model: str, tokens: int) -> float:
        """估算成本"""
        # 简化的成本估算 (每1K tokens)
        costs = {
            "gpt-4": 0.03,
            "gpt-4-turbo": 0.01,
            "gpt-3.5-turbo": 0.001,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003,
            "claude-3-haiku": 0.00025,
        }
        
        for name, cost in costs.items():
            if model.startswith(name):
                return (tokens / 1000) * cost
                
        return 0.0  # 本地模型免费
        
    def get_stats(self, api_key: str) -> Dict[str, Any]:
        """获取使用统计"""
        stats = self.usage_stats.get(api_key, UsageStats())
        return {
            "total_requests": stats.total_requests,
            "total_tokens": stats.total_tokens,
            "total_cost": round(stats.total_cost, 4),
            "requests_by_model": stats.requests_by_model,
            "last_reset": stats.last_reset.isoformat()
        }
        
    def list_models(self) -> List[Dict[str, Any]]:
        """列出可用模型"""
        models = []
        for name, provider in self.providers.items():
            if provider.enabled:
                for model in provider.models:
                    models.append({
                        "id": model,
                        "provider": name,
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": provider.name
                    })
        return models

# =============================================================================
# Global Instance
# =============================================================================

gateway = OneAPIGateway()

# =============================================================================
# API Endpoints
# =============================================================================

class ChatRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[Dict[str, str]]
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False

@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "node_id": "01",
        "name": "One-API Gateway",
        "providers": len(gateway.providers),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/v1/models")
async def list_models():
    """列出可用模型 (OpenAI 兼容)"""
    return {
        "object": "list",
        "data": gateway.list_models()
    }

@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatRequest,
    authorization: str = Header(None)
):
    """Chat Completion (OpenAI 兼容)"""
    # 提取 API Key
    api_key = "default"
    if authorization and authorization.startswith("Bearer "):
        api_key = authorization[7:]
        
    result = await gateway.chat_completion(request.dict(), api_key)
    return result

@app.get("/v1/usage")
async def get_usage(authorization: str = Header(None)):
    """获取使用统计"""
    api_key = "default"
    if authorization and authorization.startswith("Bearer "):
        api_key = authorization[7:]
    return gateway.get_stats(api_key)

@app.get("/providers")
async def list_providers():
    """列出配置的提供商"""
    return {
        "providers": [
            {
                "name": p.name,
                "enabled": p.enabled,
                "models": p.models,
                "priority": p.priority
            }
            for p in gateway.providers.values()
        ]
    }

# =============================================================================
# MCP Tool Interface
# =============================================================================

@app.post("/mcp/call")
async def mcp_call(request: Dict[str, Any]):
    """MCP 工具调用接口"""
    tool = request.get("tool", "")
    params = request.get("params", {})
    
    if tool == "chat":
        return await gateway.chat_completion(params, "mcp")
    elif tool == "list_models":
        return {"models": gateway.list_models()}
    elif tool == "get_stats":
        return gateway.get_stats("mcp")
    else:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
