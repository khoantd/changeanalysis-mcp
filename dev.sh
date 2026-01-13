#!/bin/bash

# Development environment script for Change Analysis MCP
# This script sets up and runs the development server

set -e  # Exit on error

echo "🚀 Setting up Change Analysis MCP development environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $PYTHON_VERSION detected. Python 3.8 or higher is required."
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -e ".[dev]" --quiet

# Check if fastmcp is available
if ! command -v fastmcp &> /dev/null; then
    echo "❌ fastmcp command not found. Please ensure fastmcp is installed."
    exit 1
fi

echo "✅ Dependencies installed"

# Run the server
echo ""
echo "🌟 Starting MCP server..."
echo "   Server will be available at http://localhost:8000/mcp"
echo "   Press Ctrl+C to stop"
echo ""

fastmcp run server.py:mcp --transport http --port 8000
