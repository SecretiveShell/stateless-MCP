from mcp.types import CallToolResult, ReadResourceResult

class StatelessCallToolResult(CallToolResult):
    list_resource_changed: bool = False

class StatelessReadResourcesResult(ReadResourceResult):
    list_resource_changed: bool = False