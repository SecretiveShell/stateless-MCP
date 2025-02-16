from fastapi import FastAPI
from mcp_host.lifespan import lifespan

app = FastAPI(
    title="Stateless MCP Host",
    description="Stateless MCP Host",
    version="0.1.0",
    lifespan=lifespan,
)