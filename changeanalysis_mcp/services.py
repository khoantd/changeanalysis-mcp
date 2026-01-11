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
    
    async def list_change_requests(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List change requests, optionally filtered by search term.
        
        Args:
            search: Optional search term to filter change requests
            
        Returns:
            List of change request dictionaries
        """
        params = {"search": search} if search else None
        data = await self.client.get("/change-requests", params=params)
        
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
