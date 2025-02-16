from fastapi import FastAPI
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession
from mcp.types import InitializeResult
from contextlib import asynccontextmanager
from mcp_host.config import config

mcp_server = None
initialise_result = None

def get_mcp_server() -> ClientSession:
    assert mcp_server is not None, "MCP server is not initialized"
    return mcp_server

def get_initialise_result() -> InitializeResult:
    assert initialise_result is not None, "Initialise result is not set"
    return initialise_result

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mcp_server, initialise_result

    mcp_server_params = config.mcpServer
    async with stdio_client(mcp_server_params) as transport:
        async with ClientSession(*transport) as session:
            initialise_result = await session.initialize() 
            mcp_server = session
            print(initialise_result)
            yield
                
