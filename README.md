# Change Analysis MCP

FastMCP server for change analysis and change request management. This MCP server provides tools to interact with the Change Analysis API, allowing you to search, create, update, and manage change requests.

## Features

- Search and analyze change requests
- List change requests with filtering options
- Create, update, and delete change requests
- Add comments to change requests
- Approve or reject change requests
- Health check endpoint for monitoring

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Access to the Change Analysis API

## Installation

### Development Installation

1. Clone or navigate to the project directory:
```bash
cd changeanalysis-mcp
```

2. Install the package and its dependencies:
```bash
pip install -e .
```

Or install with development dependencies:
```bash
pip install -e ".[dev]"
```

### Production Installation

For production deployments, install from a built package or directly from source:

```bash
pip install changeanalysis-mcp
```

## Configuration

The server uses environment variables for configuration. **Never commit sensitive credentials to version control.**

### Required Environment Variables

- `CHANGE_ANALYSIS_API_BASE_URL` - Base URL for the Change Analysis API (required)

### Optional Environment Variables

- `CHANGE_ANALYSIS_API_KEY` - API key for authentication (optional, but recommended)
- `CHANGE_ANALYSIS_API_TIMEOUT` - Request timeout in seconds (default: 30.0)
- `CHANGE_ANALYSIS_AUTH_METHOD` - Authentication method: `bearer` or `x-api-key` (default: `x-api-key`)
- `LOG_LEVEL` - Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` (default: `INFO`)

### Configuration Example

Create a `.env` file in the project root (or set environment variables):

```bash
# Required
CHANGE_ANALYSIS_API_BASE_URL=http://your-api-server:8092

# Optional but recommended
CHANGE_ANALYSIS_API_KEY=your_api_key_here
CHANGE_ANALYSIS_API_TIMEOUT=30.0
CHANGE_ANALYSIS_AUTH_METHOD=x-api-key
LOG_LEVEL=INFO
```

**Note:** The `.env` file is gitignored. Never commit API keys or sensitive credentials.

## Running the Server

### Development Mode

#### Quick Start (Recommended)

Use the development script to automatically set up and run the server:
```bash
./dev.sh
```

This script will:
- Check Python version requirements
- Install/update dependencies (including dev dependencies)
- Start the MCP server on `http://localhost:8000/mcp`

#### Manual Start

Alternatively, start the MCP server manually:
```bash
fastmcp run server.py:mcp --transport http --port 8000
```

### Production Mode

For production, ensure all required environment variables are set, then run:

```bash
fastmcp run server.py:mcp --transport http --port 8000
```

Or use the entry point script:
```bash
changeanalysis-mcp
```

### Using Environment Variables

Set environment variables before running:

```bash
export CHANGE_ANALYSIS_API_BASE_URL=http://your-api-server:8092
export CHANGE_ANALYSIS_API_KEY=your_api_key_here
export LOG_LEVEL=INFO
fastmcp run server.py:mcp --transport http --port 8000
```

## Available Tools

The MCP server provides the following tools for agents and other clients. All tools
return human-readable strings, often with a pretty-printed JSON payload included
for structured consumption by agents. See `[AGENT_TOOLS.md](AGENT_TOOLS.md)` for a
complete, agent-focused reference.

- `analyze_change` - Search for change requests by keyword
- `list_change_requests` - List change requests with optional filters (status, priority, department, assignee_id, search)
- `get_change_request` - Get a specific change request by ID
- `create_change_request` - Create a new change request
- `update_change_request` - Update an existing change request
- `delete_change_request` - Delete a change request
- `add_comment_to_change_request` - Add a comment to a change request
- `approve_change_request` - Approve a change request
- `reject_change_request` - Reject a change request
- `health_check` - Check server and API connectivity health

Additional domains exposed via MCP tools:

- **Systems**
  - `list_systems` - List systems with optional filters (status, criticality, department, owner_id)
  - `get_system` - Get a specific system by ID
  - `create_system` - Create a new system
  - `update_system` - Update an existing system
  - `delete_system` - Delete a system by ID

- **Feedbacks**
  - `list_feedbacks` - List feedback entries with optional filters (status, category, priority, source_system)
  - `get_feedback` - Get a specific feedback entry by ID
  - `create_feedback` - Create a new feedback entry
  - `update_feedback` - Update an existing feedback entry
  - `delete_feedback` - Delete a feedback entry by ID

- **Projects**
  - `list_projects` - List projects with optional filters (status, priority, department, project_manager_id)
  - `get_project` - Get a specific project by ID
  - `create_project` - Create a new project
  - `update_project` - Update an existing project
  - `delete_project` - Delete a project by ID

## Logging

The server uses structured logging with configurable log levels. Logs are written to stderr (standard for MCP servers).

- Set `LOG_LEVEL=DEBUG` for detailed debugging information
- Set `LOG_LEVEL=INFO` for general operational information (default)
- Set `LOG_LEVEL=WARNING` for warnings and errors only
- Set `LOG_LEVEL=ERROR` for errors only

## Security Considerations

1. **Never commit API keys or credentials** to version control
2. **Use environment variables** for all sensitive configuration
3. **Use secure authentication** methods (API keys, bearer tokens)
4. **Monitor logs** for suspicious activity
5. **Keep dependencies updated** for security patches
6. **Use HTTPS** for API connections in production

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

Format code with black:
```bash
black .
```

### Linting

Lint code with ruff:
```bash
ruff check .
```

## Troubleshooting

### Connection Errors

If you encounter connection errors:
1. Verify `CHANGE_ANALYSIS_API_BASE_URL` is set correctly
2. Check network connectivity to the API server
3. Verify API key is valid (if using authentication)
4. Check firewall rules and network policies

### Authentication Errors

If authentication fails:
1. Verify `CHANGE_ANALYSIS_API_KEY` is set correctly
2. Check `CHANGE_ANALYSIS_AUTH_METHOD` matches your API's requirements
3. Ensure API key has proper permissions

### Health Check

Use the `health_check` tool to verify server and API connectivity:
```bash
# Via MCP client
health_check
```

## License

See LICENSE file for details.

## Support

For issues and questions, please refer to the project repository or contact the development team.
