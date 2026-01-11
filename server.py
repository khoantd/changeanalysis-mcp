from fastmcp import FastMCP
import httpx
from changeanalysis_mcp.services import APIServiceFactory


mcp = FastMCP("Change Analysis MCP Server")


@mcp.tool()
async def analyze_change(change: str) -> str:
    """Search for a change request using the change-requests API."""
    try:
        async with APIServiceFactory() as api_factory:
            change_requests = await api_factory.change_requests.list_change_requests(search=change)
            
            # Format the response
            if not change_requests:
                return f"No change requests found for '{change}'"
            return f"Found {len(change_requests)} change request(s) for '{change}': {change_requests}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        return f"Error searching for change '{change}': {str(e)}"


@mcp.tool()
def greet(change: str) -> str:
    return f"Hello {change}!"

if __name__ == "__main__":
    mcp.run()