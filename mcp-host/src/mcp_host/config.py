from pydantic import BaseModel
from mcp import StdioServerParameters
from os import getenv

class Config(BaseModel):
    mcpServer: StdioServerParameters


config_json = getenv("STATELESS_MCP_CONFIG")
assert config_json is not None, "STATELESS_MCP_CONFIG is not set"

config = Config.model_validate_json(config_json)