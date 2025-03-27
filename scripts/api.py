import redis.asyncio as redis
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from utils import run_mcp
from llama_index.tools.mcp import McpToolSpec, BasicMCPClient

@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url("redis://localhost:6379", encoding="utf8")
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()

app = FastAPI(lifespan=lifespan)

class McpInput(BaseModel):
    user_input: str

class McpOutput(BaseModel):
    response: str
    process: str

async def check_mcp_url(x_api_key: str = Header(None)):
    mcp_client = BasicMCPClient(x_api_key)
    tools = McpToolSpec(mcp_client)
    try:
        tool_list = await tools.to_tool_list_async()
        return x_api_key
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Zapier MCP URL")

@app.post("/mcp", dependencies=[Depends(RateLimiter(times=60, seconds=60))])
async def mcp(inpt: McpInput, x_api_key: str = Depends(check_mcp_url)) -> McpOutput:
    response, process = await run_mcp(x_api_key, inpt.user_input)
    return McpOutput(response=response, process=process)
