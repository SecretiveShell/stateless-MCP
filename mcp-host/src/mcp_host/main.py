from typing import Any
from fastapi import FastAPI
from mcp_host import models
from mcp_host.lifespan import lifespan, get_mcp_server
from mcp.types import ListToolsResult, ListResourcesResult
from pydantic import AnyUrl
import urllib.parse

app = FastAPI(
    title="Stateless MCP Host",
    description="Stateless MCP Host",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/tools")
async def list_tools() -> ListToolsResult:
    server = get_mcp_server()
    return await server.list_tools()

@app.post("/tools/{tool}")
async def run_tool(tool: str, args: dict[str, Any]) -> models.StatelessCallToolResult:
    server = get_mcp_server()
    result = await server.call_tool(tool, args)
    
    data = result.model_dump() 
    data["list_resource_changed"] = False
    return models.StatelessCallToolResult.model_validate(data)

@app.get("/resources")
async def list_resources() -> ListResourcesResult:
    server = get_mcp_server()
    return await server.list_resources()

@app.post("/resources/{resource}")
async def run_resource(resource: str):
    server = get_mcp_server()
    resource = urllib.parse.unquote(resource)
    result = await server.read_resource(AnyUrl(resource))

    data = result.model_dump()
    data["list_resource_changed"] = False
    return models.StatelessReadResourcesResult.model_validate(data)
