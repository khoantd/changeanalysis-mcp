from fastmcp import FastMCP
import httpx
import json
import logging
from typing import Optional
from changeanalysis_mcp.services import APIServiceFactory
from changeanalysis_mcp.logging_config import setup_logging, get_logger

# Set up logging
setup_logging()
logger = get_logger()

# Log configuration status at startup
from changeanalysis_mcp.config import DEFAULT_CONFIG
if DEFAULT_CONFIG.api_key:
    logger.info("API key configured (from environment variables)")
else:
    logger.warning(
        "API key not configured. Set CHANGE_ANALYSIS_API_KEY environment variable. "
        "API requests will fail without authentication."
    )
logger.info(f"API base URL: {DEFAULT_CONFIG.base_url}")
logger.info(f"Auth method: {DEFAULT_CONFIG.auth_method}")

mcp = FastMCP("Change Analysis MCP Server")


@mcp.tool()
async def analyze_change(change: str) -> str:
    """Search for a change request using the change-requests API."""
    logger.info(f"Analyzing change request: {change}")
    try:
        # Basic input validation
        if not change or not change.strip():
            logger.warning("Empty change parameter provided")
            return "Error: Change parameter cannot be empty"
        
        async with APIServiceFactory() as api_factory:
            change_requests = await api_factory.change_requests.list_change_requests(search=change.strip())
            
            # Format the response
            if not change_requests:
                logger.info(f"No change requests found for '{change}'")
                return f"No change requests found for '{change}'"
            
            logger.info(f"Found {len(change_requests)} change request(s) for '{change}'")
            return f"Found {len(change_requests)} change request(s) for '{change}': {json.dumps(change_requests, indent=2)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error searching for change '{change}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error searching for change '{change}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error searching for change '{change}'")
        return f"Error searching for change '{change}': {str(e)}"


@mcp.tool()
async def list_change_requests(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    department: Optional[str] = None,
    assignee_id: Optional[str] = None,
    search: Optional[str] = None
) -> str:
    """List change requests with optional filtering by status, priority, department, assignee_id, or search term."""
    logger.info(f"Listing change requests with filters: status={status}, priority={priority}, "
                f"department={department}, assignee_id={assignee_id}, search={search}")
    try:
        async with APIServiceFactory() as api_factory:
            change_requests = await api_factory.change_requests.list_change_requests(
                status=status.strip() if status else None,
                priority=priority.strip() if priority else None,
                department=department.strip() if department else None,
                assignee_id=assignee_id.strip() if assignee_id else None,
                search=search.strip() if search else None
            )
            logger.info(f"Found {len(change_requests)} change request(s)")
            return f"Found {len(change_requests)} change request(s): {json.dumps(change_requests, indent=2)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error listing change requests: {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error listing change requests: {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception("Unexpected error listing change requests")
        return f"Error listing change requests: {str(e)}"


@mcp.tool()
async def get_change_request(change_request_id: str) -> str:
    """Get a specific change request by ID."""
    logger.info(f"Getting change request: {change_request_id}")
    try:
        if not change_request_id or not change_request_id.strip():
            logger.warning("Empty change_request_id provided")
            return "Error: Change request ID cannot be empty"
        
        async with APIServiceFactory() as api_factory:
            change_request = await api_factory.change_requests.get_change_request(change_request_id.strip())
            logger.info(f"Successfully retrieved change request: {change_request_id}")
            return json.dumps(change_request, indent=2)
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting change request '{change_request_id}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error getting change request '{change_request_id}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error getting change request '{change_request_id}'")
        return f"Error getting change request: {str(e)}"


@mcp.tool()
async def create_change_request(change_request_data: str) -> str:
    """Create a new change request. Provide change request data as JSON string."""
    logger.info("Creating new change request")
    try:
        if not change_request_data or not change_request_data.strip():
            logger.warning("Empty change_request_data provided")
            return "Error: Change request data cannot be empty"
        
        data = json.loads(change_request_data.strip())
        async with APIServiceFactory() as api_factory:
            change_request = await api_factory.change_requests.create_change_request(data)
            logger.info(f"Change request created successfully: {change_request.get('id', 'unknown')}")
            return f"Change request created successfully: {json.dumps(change_request, indent=2)}"
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in change_request_data: {str(e)}")
        return f"Invalid JSON format: {str(e)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error creating change request: {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error creating change request: {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception("Unexpected error creating change request")
        return f"Error creating change request: {str(e)}"


@mcp.tool()
async def update_change_request(change_request_id: str, update_data: str) -> str:
    """Update a change request. Provide update data as JSON string."""
    logger.info(f"Updating change request: {change_request_id}")
    try:
        if not change_request_id or not change_request_id.strip():
            logger.warning("Empty change_request_id provided")
            return "Error: Change request ID cannot be empty"
        if not update_data or not update_data.strip():
            logger.warning("Empty update_data provided")
            return "Error: Update data cannot be empty"
        
        data = json.loads(update_data.strip())
        async with APIServiceFactory() as api_factory:
            change_request = await api_factory.change_requests.update_change_request(
                change_request_id.strip(), data
            )
            logger.info(f"Change request updated successfully: {change_request_id}")
            return f"Change request updated successfully: {json.dumps(change_request, indent=2)}"
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in update_data: {str(e)}")
        return f"Invalid JSON format: {str(e)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error updating change request '{change_request_id}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error updating change request '{change_request_id}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error updating change request '{change_request_id}'")
        return f"Error updating change request: {str(e)}"


@mcp.tool()
async def delete_change_request(change_request_id: str) -> str:
    """Delete a change request by ID."""
    logger.info(f"Deleting change request: {change_request_id}")
    try:
        if not change_request_id or not change_request_id.strip():
            logger.warning("Empty change_request_id provided")
            return "Error: Change request ID cannot be empty"
        
        async with APIServiceFactory() as api_factory:
            await api_factory.change_requests.delete_change_request(change_request_id.strip())
            logger.info(f"Change request deleted successfully: {change_request_id}")
            return f"Change request {change_request_id} deleted successfully"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error deleting change request '{change_request_id}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error deleting change request '{change_request_id}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error deleting change request '{change_request_id}'")
        return f"Error deleting change request: {str(e)}"


@mcp.tool()
async def add_comment_to_change_request(change_request_id: str, comment_data: str) -> str:
    """Add a comment to a change request. Provide comment data as JSON string."""
    logger.info(f"Adding comment to change request: {change_request_id}")
    try:
        if not change_request_id or not change_request_id.strip():
            logger.warning("Empty change_request_id provided")
            return "Error: Change request ID cannot be empty"
        if not comment_data or not comment_data.strip():
            logger.warning("Empty comment_data provided")
            return "Error: Comment data cannot be empty"
        
        data = json.loads(comment_data.strip())
        async with APIServiceFactory() as api_factory:
            comment = await api_factory.change_requests.add_comment(change_request_id.strip(), data)
            logger.info(f"Comment added successfully to change request: {change_request_id}")
            return f"Comment added successfully: {json.dumps(comment, indent=2)}"
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in comment_data: {str(e)}")
        return f"Invalid JSON format: {str(e)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error adding comment to change request '{change_request_id}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error adding comment to change request '{change_request_id}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error adding comment to change request '{change_request_id}'")
        return f"Error adding comment: {str(e)}"


@mcp.tool()
async def approve_change_request(change_request_id: str) -> str:
    """Approve a change request by ID."""
    logger.info(f"Approving change request: {change_request_id}")
    try:
        if not change_request_id or not change_request_id.strip():
            logger.warning("Empty change_request_id provided")
            return "Error: Change request ID cannot be empty"
        
        async with APIServiceFactory() as api_factory:
            change_request = await api_factory.change_requests.approve_change_request(change_request_id.strip())
            logger.info(f"Change request approved successfully: {change_request_id}")
            return f"Change request approved successfully: {json.dumps(change_request, indent=2)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error approving change request '{change_request_id}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error approving change request '{change_request_id}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error approving change request '{change_request_id}'")
        return f"Error approving change request: {str(e)}"


@mcp.tool()
async def reject_change_request(change_request_id: str) -> str:
    """Reject a change request by ID."""
    logger.info(f"Rejecting change request: {change_request_id}")
    try:
        if not change_request_id or not change_request_id.strip():
            logger.warning("Empty change_request_id provided")
            return "Error: Change request ID cannot be empty"
        
        async with APIServiceFactory() as api_factory:
            change_request = await api_factory.change_requests.reject_change_request(change_request_id.strip())
            logger.info(f"Change request rejected successfully: {change_request_id}")
            return f"Change request rejected successfully: {json.dumps(change_request, indent=2)}"
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error rejecting change request '{change_request_id}': {e.response.status_code} - {e.response.text}")
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        logger.error(f"Request error rejecting change request '{change_request_id}': {str(e)}")
        return f"Request error occurred: {str(e)}"
    except Exception as e:
        logger.exception(f"Unexpected error rejecting change request '{change_request_id}'")
        return f"Error rejecting change request: {str(e)}"


@mcp.tool()
async def health_check() -> str:
    """Check the health status of the MCP server and API connection."""
    logger.info("Health check requested")
    
    # Check configuration first
    from changeanalysis_mcp.config import DEFAULT_CONFIG
    config_status = []
    config_status.append(f"API Base URL: {DEFAULT_CONFIG.base_url}")
    config_status.append(f"Auth Method: {DEFAULT_CONFIG.auth_method}")
    config_status.append(f"API Key Configured: {'Yes' if DEFAULT_CONFIG.api_key else 'No (WARNING: Requests will fail)'}")
    config_status.append(f"Timeout: {DEFAULT_CONFIG.timeout}s")
    
    if not DEFAULT_CONFIG.api_key:
        logger.warning("Health check: API key not configured")
        return (
            "Health check failed: API key not configured.\n\n"
            "Configuration Status:\n" + "\n".join(f"  - {s}" for s in config_status) + "\n\n"
            "Please set CHANGE_ANALYSIS_API_KEY environment variable."
        )
    
    try:
        async with APIServiceFactory() as api_factory:
            # Try a simple API call to verify connectivity
            await api_factory.change_requests.list_change_requests()
            logger.info("Health check passed")
            return (
                "Health check passed: Server is operational and API connection is working.\n\n"
                "Configuration Status:\n" + "\n".join(f"  - {s}" for s in config_status)
            )
    except httpx.HTTPStatusError as e:
        logger.warning(f"Health check failed - HTTP error: {e.response.status_code}")
        error_detail = ""
        if e.response.status_code == 401:
            error_detail = "\n\nAuthentication failed. Check that CHANGE_ANALYSIS_API_KEY is correct."
        elif e.response.status_code == 403:
            error_detail = "\n\nAccess forbidden. Check API key permissions."
        return (
            f"Health check warning: API returned HTTP {e.response.status_code}{error_detail}\n\n"
            "Configuration Status:\n" + "\n".join(f"  - {s}" for s in config_status)
        )
    except httpx.RequestError as e:
        logger.error(f"Health check failed - Request error: {str(e)}")
        return (
            f"Health check failed: Cannot connect to API - {str(e)}\n\n"
            "Configuration Status:\n" + "\n".join(f"  - {s}" for s in config_status)
        )
    except Exception as e:
        logger.exception("Health check failed - Unexpected error")
        return (
            f"Health check failed: {str(e)}\n\n"
            "Configuration Status:\n" + "\n".join(f"  - {s}" for s in config_status)
        )


if __name__ == "__main__":
    logger.info("Starting Change Analysis MCP Server")
    mcp.run()