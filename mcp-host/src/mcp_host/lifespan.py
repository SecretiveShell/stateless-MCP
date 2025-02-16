from fastapi import FastAPI
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from contextlib import asynccontextmanager
from mcp_host.config import config

mcp_server = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    mcp_server_params = config.mcpServer
    async with stdio_client(mcp_server_params) as mcp_server:
        async with ClientSession(*mcp_server) as session:
            mcp_server = session
            yield
                
