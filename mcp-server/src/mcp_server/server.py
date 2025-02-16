import os
import re
import httpx
from mcp.server.lowlevel import Server
import mcp.types as types
from pydantic import AnyUrl
import urllib.parse

SERVER_NAME = "mcp-stateless-server"

HOST_URL: str = os.getenv("STATELESS_MCP_HOST_URL", "http://localhost:8000") # type: ignore
assert HOST_URL is not None, "STATELESS_MCP_HOST_URL is not set"


server = Server(name=SERVER_NAME)

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    async with httpx.AsyncClient() as client:
        response = await client.get(HOST_URL + "/resources")
    
    parsed_response = types.ListResourcesResult.model_validate_json(response.text)
    
    return parsed_response.resources


@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    async with httpx.AsyncClient() as client:
        formatted_uri = urllib.parse.quote(str(uri), safe='')
        url = httpx.URL(f"{HOST_URL}/resource?resource={formatted_uri}", )
        response = await client.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch {uri}")
    
    parsed_response = types.ReadResourceResult.model_validate_json(response.text)
    
    if hasattr(parsed_response.contents[0], "text"):
        assert isinstance(parsed_response.contents[0], types.TextResourceContents)
        return parsed_response.contents[0].text
    
    else:
        assert isinstance(parsed_response.contents[0], types.BlobResourceContents)
        return parsed_response.contents[0].blob
