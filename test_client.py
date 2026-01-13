import asyncio
import warnings
from fastmcp import Client
from fastmcp.client import StreamableHttpTransport

# Suppress deprecation warning - we're already using StreamableHttpTransport explicitly
# This warning appears to be internal to FastMCP and doesn't affect functionality
warnings.filterwarnings("ignore", category=DeprecationWarning, module="contextlib")

client = Client(StreamableHttpTransport("http://localhost:8000/mcp"))

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"change": name})
        print(result)

async def analyze_change(change: str):
    async with client:
        result = await client.call_tool("analyze_change", {"change": change})
        print(result)

async def list_available_tools():
    """List all available tools from the MCP server."""
    async with client:
        try:
            # Try to get tools list if available
            tools = await client.list_tools()
            print("Available tools:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description}")
        except AttributeError:
            # If list_tools doesn't exist, try to inspect the client
            print("Cannot list tools directly. Please ensure the server is running.")
            print("Make sure to restart the server after adding new tools.")

async def list_changes(
    status: str = None,
    priority: str = None,
    department: str = None,
    assignee_id: str = None,
    search: str = None
):
    """
    List change requests with optional filtering.
    
    Note: Make sure the MCP server is running and has been restarted
    after adding the list_change_requests tool.
    """
    async with client:
        # Build params dict, only including non-None values
        params = {}
        if status is not None:
            params["status"] = status
        if priority is not None:
            params["priority"] = priority
        if department is not None:
            params["department"] = department
        if assignee_id is not None:
            params["assignee_id"] = assignee_id
        if search is not None:
            params["search"] = search
        
        result = await client.call_tool("list_change_requests", params)
        print(result)

# asyncio.run(analyze_change("CHG-005"))
asyncio.run(list_changes(search="CHG"))