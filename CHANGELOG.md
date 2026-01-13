# Changelog

## [0.1.0] - Production Ready Release

### Added

#### Configuration Management
- **Environment Variable Support**: All configuration now uses environment variables
  - `CHANGE_ANALYSIS_API_BASE_URL` (required)
  - `CHANGE_ANALYSIS_API_KEY` (optional)
  - `CHANGE_ANALYSIS_API_TIMEOUT` (optional, default: 30.0)
  - `CHANGE_ANALYSIS_AUTH_METHOD` (optional, default: x-api-key)
  - `LOG_LEVEL` (optional, default: INFO)
- **`get_config_from_env()` function**: Properly validates and loads configuration from environment variables
- **Configuration validation**: Validates timeout values and auth methods

#### Logging
- **Structured logging**: Added comprehensive logging system with configurable levels
- **Logging configuration module**: `changeanalysis_mcp/logging_config.py`
- **Request/response logging**: All tools now log operations with appropriate levels
- **Error logging**: Detailed error logging with stack traces for debugging

#### Security Improvements
- **Removed hardcoded credentials**: API keys are no longer hardcoded in source
- **Input validation**: All tool parameters are validated and sanitized
- **Error message sanitization**: Error messages don't expose sensitive information

#### Monitoring & Observability
- **Health check tool**: New `health_check` tool for monitoring server and API connectivity
- **Comprehensive error handling**: Improved error messages and logging throughout

#### Documentation
- **Production deployment guide**: Added `PRODUCTION.md` with deployment best practices
- **Updated README**: Comprehensive documentation with environment variables, security considerations, and troubleshooting
- **Configuration examples**: Clear examples for setting up environment variables

#### Code Quality
- **Removed test code**: Removed `greet` function (test/debug code)
- **Improved error handling**: Better exception handling with proper logging
- **Type safety**: Improved type hints and validation

### Changed

#### Configuration
- **`DEFAULT_CONFIG`**: Now attempts to load from environment variables first, falls back to defaults only in development
- **Auth method normalization**: Auth methods are normalized to lowercase for consistency

#### Error Handling
- **Improved error messages**: More user-friendly error messages
- **Structured error logging**: Errors are logged with context before returning to user

#### Server Tools
- **Input validation**: All tools now validate and sanitize input parameters
- **Logging**: All tools log operations at appropriate levels
- **Error handling**: Consistent error handling pattern across all tools

### Security

- **No hardcoded credentials**: All credentials must be provided via environment variables
- **Input sanitization**: All user inputs are validated and sanitized
- **Secure defaults**: Sensible security defaults for production use

### Documentation

- **Production guide**: Comprehensive production deployment guide
- **Environment variables**: Documented all configuration options
- **Security best practices**: Added security considerations section
- **Troubleshooting**: Added troubleshooting guide

### Migration Guide

#### For Existing Deployments

1. **Set environment variables**:
   ```bash
   export CHANGE_ANALYSIS_API_BASE_URL=http://your-api-server:8092
   export CHANGE_ANALYSIS_API_KEY=your_api_key
   ```

2. **Update logging** (optional):
   ```bash
   export LOG_LEVEL=INFO
   ```

3. **Restart the server**: The server will automatically use environment variables

#### Breaking Changes

- **Hardcoded API key removed**: You must now provide `CHANGE_ANALYSIS_API_KEY` via environment variable
- **Configuration required**: `CHANGE_ANALYSIS_API_BASE_URL` is now required (no hardcoded fallback in production)

### Notes

- The server maintains backward compatibility for development use (fallback defaults)
- Production deployments should always use environment variables
- All sensitive data is now externalized to environment variables
- Logging is configured to write to stderr (standard for MCP servers)
