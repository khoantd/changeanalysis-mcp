"""API service classes for different endpoints."""

from typing import List, Dict, Any, Optional
from .client import BaseAPIClient
from .config import APIConfig


class ChangeRequestsService:
    """Service for interacting with change-requests API."""
    
    def __init__(self, client: BaseAPIClient):
        """
        Initialize the service.
        
        Args:
            client: Base API client instance
        """
        self.client = client
    
    async def list_change_requests(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        department: Optional[str] = None,
        assignee_id: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List change requests with optional filtering and search.
        
        Args:
            status: Filter by status
            priority: Filter by priority
            department: Filter by department
            assignee_id: Filter by assignee ID
            search: Search by key, title, or description
            
        Returns:
            List of change request dictionaries
        """
        params = {}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if department:
            params["department"] = department
        if assignee_id:
            params["assignee_id"] = assignee_id
        if search:
            params["search"] = search
        
        data = await self.client.get("/change-requests", params=params if params else None)
        
        # Ensure we return a list
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "items" in data:
            return data["items"]
        else:
            return [data]
    
    async def get_change_request(self, change_id: str) -> Dict[str, Any]:
        """
        Get a specific change request by ID.
        
        Args:
            change_id: The ID of the change request
            
        Returns:
            Change request dictionary
        """
        return await self.client.get(f"/change-requests/{change_id}")
    
    async def create_change_request(self, change_request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new change request.
        
        Args:
            change_request_data: Dictionary containing change request data
            
        Returns:
            Created change request dictionary
        """
        return await self.client.post("/change-requests", json=change_request_data)
    
    async def update_change_request(
        self,
        change_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a change request.
        
        Args:
            change_id: The ID of the change request
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated change request dictionary
        """
        return await self.client.patch(f"/change-requests/{change_id}", json=update_data)
    
    async def delete_change_request(self, change_id: str) -> Dict[str, Any]:
        """
        Delete a change request.
        
        Args:
            change_id: The ID of the change request
            
        Returns:
            Empty dictionary (204 No Content response)
        """
        return await self.client.delete(f"/change-requests/{change_id}")
    
    async def add_comment(
        self,
        change_id: str,
        comment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Add a comment to a change request.
        
        Args:
            change_id: The ID of the change request
            comment_data: Dictionary containing comment data
            
        Returns:
            Created comment dictionary
        """
        return await self.client.post(
            f"/change-requests/{change_id}/comments",
            json=comment_data
        )
    
    async def approve_change_request(self, change_id: str) -> Dict[str, Any]:
        """
        Approve a change request.
        
        Args:
            change_id: The ID of the change request
            
        Returns:
            Updated change request dictionary
        """
        return await self.client.post(f"/change-requests/{change_id}/approve")
    
    async def reject_change_request(self, change_id: str) -> Dict[str, Any]:
        """
        Reject a change request.
        
        Args:
            change_id: The ID of the change request
            
        Returns:
            Updated change request dictionary
        """
        return await self.client.post(f"/change-requests/{change_id}/reject")


class APIServiceFactory:
    """Factory for creating API service instances."""
    
    def __init__(self, config: Optional[APIConfig] = None):
        """
        Initialize the factory.
        
        Args:
            config: API configuration. If None, uses DEFAULT_CONFIG.
        """
        self.config = config
        self._client: Optional[BaseAPIClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._client = BaseAPIClient(self.config)
        await self._client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)
    
    @property
    def change_requests(self) -> ChangeRequestsService:
        """Get the change requests service."""
        if not self._client:
            raise RuntimeError("Factory must be used as async context manager")
        return ChangeRequestsService(self._client)
    
    # Add more service properties here as you add new APIs
    # Example:
    # @property
    # def users(self) -> UsersService:
    #     """Get the users service."""
    #     if not self._client:
    #         raise RuntimeError("Factory must be used as async context manager")
    #     return UsersService(self._client)
