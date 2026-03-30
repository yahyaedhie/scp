import httpx
import anthropic
from anthropic import AsyncAnthropic
from typing import Dict, Optional, Any
import asyncio
import time

class LLMGateway:
    def __init__(self, config):
        self.config = config
        self.deepseek_key = config.DEEPSEEK_API_KEY
        self.claude_key = config.CLAUDE_API_KEY
        self.default_model = config.DEFAULT_LLM
        
        # Initialize Async Anthropic client
        self.anthropic_client = AsyncAnthropic(api_key=self.claude_key)
    
    async def call_deepseek(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Call DeepSeek API using httpx"""
        start_time = time.time()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.config.DEEPSEEK_API_URL,
                    headers={
                        "Authorization": f"Bearer {self.deepseek_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.config.DEEPSEEK_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ]
                    },
                    timeout=45.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"DeepSeek API error: {response.status_code} - {response.text}")
                
                result = response.json()
                latency = time.time() - start_time
                
                return {
                    "response": result["choices"][0]["message"]["content"],
                    "model": "deepseek",
                    "latency_ms": int(latency * 1000),
                    "usage": result.get("usage", {})
                }
            except Exception as e:
                raise Exception(f"DeepSeek connection error: {str(e)}")
    
    async def call_claude(self, system_prompt: str, user_message: str) -> Dict[str, Any]:
        """Call Claude API using native AsyncAnthropic client"""
        start_time = time.time()
        try:
            response = await self.anthropic_client.messages.create(
                model=self.config.CLAUDE_MODEL,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            latency = time.time() - start_time
            return {
                "response": response.content[0].text,
                "model": "claude",
                "latency_ms": int(latency * 1000),
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    async def call(self, system_prompt: str, user_message: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Route to appropriate LLM and standardize output"""
        model = model or self.default_model
        
        if model == "deepseek":
            return await self.call_deepseek(system_prompt, user_message)
        elif model == "claude":
            return await self.call_claude(system_prompt, user_message)
        else:
            raise ValueError(f"Unknown model configured: {model}")