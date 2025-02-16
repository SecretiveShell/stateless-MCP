from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from .server import SERVER_NAME, server


async def run_stdio():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )

def main() -> None:
    import asyncio
    asyncio.run(run_stdio())

if __name__ == "__main__":
    main()