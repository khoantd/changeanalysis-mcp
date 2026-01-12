# Change Analysis MCP

FastMCP project for change analysis.

## How to Run

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
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

### Running the Server

Start the MCP server:
```bash
fastmcp run server.py:mcp --transport http --port 8000
```

The server will start and be available at `http://localhost:8000/mcp`.

### Running the Client (Example)

To test the server with the example client:
```bash
python ../my_client.py
```

This will connect to the server and call the `analyze_change` tool with "Change-1" as the parameter.
