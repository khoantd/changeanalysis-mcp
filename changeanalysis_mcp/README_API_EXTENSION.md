# Adding New APIs

This document explains how to add new API endpoints using the established design pattern.

## Architecture Overview

The codebase uses a layered architecture:

1. **Config Layer** (`config.py`): Configuration for API endpoints
2. **Client Layer** (`client.py`): Base HTTP client for making requests
3. **Service Layer** (`services.py`): Domain-specific service classes
4. **Server Layer** (`server.py`): MCP tools that use services

## Steps to Add a New API

### Example: Adding a "Users" API

#### Step 1: Create a Service Class

Add a new service class in `services.py`:

```python
class UsersService:
    """Service for interacting with users API."""
    
    def __init__(self, client: BaseAPIClient):
        self.client = client
    
    async def list_users(self, role: Optional[str] = None) -> List[Dict[str, Any]]:
        """List users, optionally filtered by role."""
        params = {"role": role} if role else None
        data = await self.client.get("/users", params=params)
        return data if isinstance(data, list) else [data]
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a specific user by ID."""
        return await self.client.get(f"/users/{user_id}")
```

#### Step 2: Add Service Property to Factory

In `services.py`, add a property to `APIServiceFactory`:

```python
@property
def users(self) -> UsersService:
    """Get the users service."""
    if not self._client:
        raise RuntimeError("Factory must be used as async context manager")
    return UsersService(self._client)
```

#### Step 3: Export the Service (Optional)

In `__init__.py`, add the new service to exports:

```python
from .services import APIServiceFactory, ChangeRequestsService, UsersService

__all__ = [
    # ... existing exports ...
    "UsersService",
]
```

#### Step 4: Create MCP Tools

In `server.py`, add new tools that use the service:

```python
@mcp.tool()
async def get_user(user_id: str) -> str:
    """Get user information by ID."""
    try:
        async with APIServiceFactory() as api_factory:
            user = await api_factory.users.get_user(user_id)
            return f"User information: {user}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error getting user: {str(e)}"
```

## Benefits of This Pattern

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Reusability**: Base client can be used by any service
3. **Testability**: Services can be easily mocked for testing
4. **Maintainability**: Changes to API structure are isolated to service classes
5. **Extensibility**: Adding new APIs follows a consistent pattern

## Configuration

To use a different API base URL or timeout, create a custom config:

```python
from changeanalysis_mcp.config import APIConfig

custom_config = APIConfig(
    base_url="http://custom-api.example.com",
    timeout=60.0
)

async with APIServiceFactory(config=custom_config) as api_factory:
    # Use services...
```
