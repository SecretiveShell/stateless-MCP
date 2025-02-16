from mcp.types import CallToolResult

class StatelessCallToolResult(CallToolResult):
    list_resource_changed: bool = False