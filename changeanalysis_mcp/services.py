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
    ) -> List[Dict[str, Any]]:
        """
        List change requests with optional filtering and search.
        
        Args:
            status: Filter by status
            priority: Filter by priority
            department: Filter by department
            assignee_id: Filter by assignee ID
            
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


class SystemsService:
    """Service for interacting with systems API."""
    
    def __init__(self, client: BaseAPIClient):
        """
        Initialize the service.
        
        Args:
            client: Base API client instance
        """
        self.client = client
    
    async def list_systems(
        self,
        status: Optional[str] = None,
        criticality: Optional[str] = None,
        department: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List systems with optional filtering and search.
        
        Args:
            status: Filter by status
            criticality: Filter by criticality
            department: Filter by department
            owner_id: Filter by owner ID
            
        Returns:
            List of system dictionaries
        """
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        if criticality:
            params["criticality"] = criticality
        if department:
            params["department"] = department
        if owner_id:
            params["owner_id"] = owner_id
        
        data = await self.client.get("/get-systems", params=params if params else None)
        
        # Ensure we return a list
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "items" in data:
            return data["items"]
        else:
            return [data]
    
    async def get_system(self, system_id: str) -> Dict[str, Any]:
        """
        Get a specific system by ID.
        
        Args:
            system_id: The ID of the system
            
        Returns:
            System dictionary
        """
        return await self.client.get(f"/systems/{system_id}")
    
    async def create_system(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new system.
        
        Args:
            system_data: Dictionary containing system data
            
        Returns:
            Created system dictionary
        """
        return await self.client.post("/systems", json=system_data)
    
    async def update_system(
        self,
        system_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a system.
        
        Args:
            system_id: The ID of the system
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated system dictionary
        """
        return await self.client.patch(f"/systems/{system_id}", json=update_data)
    
    async def delete_system(self, system_id: str) -> Dict[str, Any]:
        """
        Delete a system.
        
        Args:
            system_id: The ID of the system
            
        Returns:
            Empty dictionary (204 No Content response)
        """
        return await self.client.delete(f"/systems/{system_id}")


class FeedbacksService:
    """Service for interacting with feedbacks API."""
    
    def __init__(self, client: BaseAPIClient):
        """
        Initialize the service.
        
        Args:
            client: Base API client instance
        """
        self.client = client
    
    async def list_feedbacks(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        source_system: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List feedbacks with optional filtering and search.
        
        Args:
            status: Filter by status
            category: Filter by category
            priority: Filter by priority
            source_system: Filter by source system identifier
            
        Returns:
            List of feedback dictionaries
        """
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        if category:
            params["category"] = category
        if priority:
            params["priority"] = priority
        if source_system:
            # FastAPI uses alias 'sourceSystem' but query param name is 'source_system'
            params["sourceSystem"] = source_system
        
        data = await self.client.get("/get-feedback", params=params if params else None)
        
        # Ensure we return a list
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "items" in data:
            return data["items"]
        else:
            return [data]
    
    async def get_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """
        Get a specific feedback by ID.
        
        Args:
            feedback_id: The ID of the feedback
            
        Returns:
            Feedback dictionary
        """
        return await self.client.get(f"/get-feedback/{feedback_id}")
    
    async def create_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new feedback.
        
        Args:
            feedback_data: Dictionary containing feedback data
            
        Returns:
            Created feedback dictionary
        """
        return await self.client.post("/get-feedback", json=feedback_data)
    
    async def update_feedback(
        self,
        feedback_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a feedback.
        
        Args:
            feedback_id: The ID of the feedback
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated feedback dictionary
        """
        return await self.client.patch(f"/get-feedback/{feedback_id}", json=update_data)
    
    async def delete_feedback(self, feedback_id: str) -> Dict[str, Any]:
        """
        Delete a feedback.
        
        Args:
            feedback_id: The ID of the feedback
            
        Returns:
            Empty dictionary (204 No Content response)
        """
        return await self.client.delete(f"/get-feedback/{feedback_id}")


class ProjectsService:
    """Service for interacting with projects API."""
    
    def __init__(self, client: BaseAPIClient):
        """
        Initialize the service.
        
        Args:
            client: Base API client instance
        """
        self.client = client
    
    async def list_projects(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        department: Optional[str] = None,
        project_manager_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        List projects with optional filtering and search.
        
        Args:
            status: Filter by status
            priority: Filter by priority
            department: Filter by department
            project_manager_id: Filter by project manager ID
            
        Returns:
            List of project dictionaries
        """
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        if department:
            params["department"] = department
        if project_manager_id:
            params["project_manager_id"] = project_manager_id
        
        data = await self.client.get("/get-projects", params=params if params else None)
        
        # Ensure we return a list
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "items" in data:
            return data["items"]
        else:
            return [data]
    
    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        Get a specific project by ID.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            Project dictionary
        """
        return await self.client.get(f"/get-projects/{project_id}")
    
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new project.
        
        Args:
            project_data: Dictionary containing project data
            
        Returns:
            Created project dictionary
        """
        return await self.client.post("/get-projects", json=project_data)
    
    async def update_project(
        self,
        project_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a project.
        
        Args:
            project_id: The ID of the project
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated project dictionary
        """
        return await self.client.patch(f"/get-projects/{project_id}", json=update_data)
    
    async def delete_project(self, project_id: str) -> Dict[str, Any]:
        """
        Delete a project.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            Empty dictionary (204 No Content response)
        """
        return await self.client.delete(f"/get-projects/{project_id}")


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
    
    @property
    def systems(self) -> SystemsService:
        """Get the systems service."""
        if not self._client:
            raise RuntimeError("Factory must be used as async context manager")
        return SystemsService(self._client)
    
    @property
    def feedbacks(self) -> FeedbacksService:
        """Get the feedbacks service."""
        if not self._client:
            raise RuntimeError("Factory must be used as async context manager")
        return FeedbacksService(self._client)
    
    @property
    def projects(self) -> ProjectsService:
        """Get the projects service."""
        if not self._client:
            raise RuntimeError("Factory must be used as async context manager")
        return ProjectsService(self._client)
