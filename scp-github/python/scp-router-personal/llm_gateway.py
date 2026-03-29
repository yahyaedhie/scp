import httpx
import anthropic
from typing import Dict, Optional
import asyncio

class LLMGateway:
    def __init__(self, config):
        self.config = config
        self.deepseek_key = config.DEEPSEEK_API_KEY
        self.claude_key = config.CLAUDE_API_KEY
        self.default_model = config.DEFAULT_LLM
    
    async def call_deepseek(self, system_prompt: str, user_message: str) -> Dict:
        """Call DeepSeek API"""
        async with httpx.AsyncClient() as client:
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
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {response.status_code}")
            
            result = response.json()
            return {
                "response": result["choices"][0]["message"]["content"],
                "model": "deepseek",
                "usage": result.get("usage", {})
            }
    
    async def call_claude(self, system_prompt: str, user_message: str) -> Dict:
        """Call Claude API"""
        client = anthropic.Anthropic(api_key=self.claude_key)
        
        try:
            # Run in thread pool since anthropic client is synchronous
            response = await asyncio.to_thread(
                client.messages.create,
                model=self.config.CLAUDE_MODEL,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            return {
                "response": response.content[0].text,
                "model": "claude",
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    async def call(self, system_prompt: str, user_message: str, model: str = None) -> Dict:
        """Route to appropriate LLM"""
        model = model or self.default_model
        
        if model == "deepseek":
            return await self.call_deepseek(system_prompt, user_message)
        elif model == "claude":
            return await self.call_claude(system_prompt, user_message)
        else:
            raise ValueError(f"Unknown model: {model}")