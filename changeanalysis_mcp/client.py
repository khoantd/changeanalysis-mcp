"""Base API client for HTTP requests."""

import httpx
from typing import Optional, Dict, Any
from .config import APIConfig, DEFAULT_CONFIG


class BaseAPIClient:
    """Base client for making HTTP requests to APIs."""
    
    def __init__(self, config: Optional[APIConfig] = None):
        """
        Initialize the API client.
        
        Args:
            config: API configuration. If None, uses DEFAULT_CONFIG.
        """
        self.config = config or DEFAULT_CONFIG
        self._client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(timeout=self.config.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint path (e.g., '/change-requests')
            params: Query parameters
            headers: Request headers
            
        Returns:
            JSON response data
            
        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.RequestError: If there's a network error
        """
        if not self._client:
            raise RuntimeError("Client must be used as async context manager")
        
        url = f"{self.config.base_url}{endpoint}"
        response = await self._client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    
    async def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint path
            json: JSON payload
            headers: Request headers
            
        Returns:
            JSON response data
            
        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.RequestError: If there's a network error
        """
        if not self._client:
            raise RuntimeError("Client must be used as async context manager")
        
        url = f"{self.config.base_url}{endpoint}"
        response = await self._client.post(url, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
    
    async def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a PUT request.
        
        Args:
            endpoint: API endpoint path
            json: JSON payload
            headers: Request headers
            
        Returns:
            JSON response data
            
        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.RequestError: If there's a network error
        """
        if not self._client:
            raise RuntimeError("Client must be used as async context manager")
        
        url = f"{self.config.base_url}{endpoint}"
        response = await self._client.put(url, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
    
    async def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a DELETE request.
        
        Args:
            endpoint: API endpoint path
            headers: Request headers
            
        Returns:
            JSON response data
            
        Raises:
            httpx.HTTPStatusError: If the request fails
            httpx.RequestError: If there's a network error
        """
        if not self._client:
            raise RuntimeError("Client must be used as async context manager")
        
        url = f"{self.config.base_url}{endpoint}"
        response = await self._client.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
