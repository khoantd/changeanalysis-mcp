# Troubleshooting Guide

## Authentication Issues

### Error: "Authorization header present=False, X-API-Key present=False"

This error indicates that the API key is not being sent with requests. The server is making requests without authentication headers.

#### Root Cause

The `CHANGE_ANALYSIS_API_KEY` environment variable is not set or not accessible to the MCP server process.

#### Solution

1. **Set the environment variable** before starting the server:

   ```bash
   export CHANGE_ANALYSIS_API_KEY=your_api_key_here
   ```

2. **Verify the environment variable is set**:

   ```bash
   echo $CHANGE_ANALYSIS_API_KEY
   ```

3. **For remote deployments**, ensure the environment variable is set in:
   - Systemd service files (if using systemd)
   - Docker environment variables (if using Docker)
   - Process manager configuration (if using PM2, supervisor, etc.)
   - CI/CD pipeline secrets (if deployed via CI/CD)

#### Common Deployment Scenarios

##### Systemd Service

Edit `/etc/systemd/system/changeanalysis-mcp.service`:

```ini
[Service]
Environment="CHANGE_ANALYSIS_API_KEY=your_api_key_here"
Environment="CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com"
```

Then reload and restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart changeanalysis-mcp
```

##### Docker

```bash
docker run -d \
  -e CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com \
  -e CHANGE_ANALYSIS_API_KEY=your_api_key_here \
  changeanalysis-mcp
```

Or use a `.env` file:

```bash
docker run -d --env-file .env changeanalysis-mcp
```

##### Docker Compose

```yaml
services:
  changeanalysis-mcp:
    environment:
      - CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com
      - CHANGE_ANALYSIS_API_KEY=${CHANGE_ANALYSIS_API_KEY}
    # ... other config
```

##### Kubernetes

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: changeanalysis-mcp-secrets
type: Opaque
stringData:
  CHANGE_ANALYSIS_API_KEY: your_api_key_here
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: changeanalysis-mcp
spec:
  template:
    spec:
      containers:
      - name: changeanalysis-mcp
        env:
        - name: CHANGE_ANALYSIS_API_KEY
          valueFrom:
            secretKeyRef:
              name: changeanalysis-mcp-secrets
              key: CHANGE_ANALYSIS_API_KEY
```

#### Diagnostic Steps

1. **Check server logs** at startup - you should see:
   ```
   INFO: API key configured (from environment variables)
   ```
   If you see:
   ```
   WARNING: API key not configured...
   ```
   Then the environment variable is not set.

2. **Use the health_check tool** to verify configuration:
   ```bash
   # Via MCP client
   health_check
   ```
   This will show the current configuration status.

3. **Check environment variables** in the running process:
   ```bash
   # For systemd
   sudo systemctl show changeanalysis-mcp | grep Environment
   
   # For Docker
   docker exec <container_id> env | grep CHANGE_ANALYSIS
   ```

#### Additional Debugging

The server now logs warnings when API keys are missing. Check logs for:

```
WARNING: No API key configured. Set CHANGE_ANALYSIS_API_KEY environment variable.
```

If you see this, the environment variable is not accessible to the server process.

### Error: HTTP 401 Unauthorized

This means the API key is being sent but is invalid or expired.

**Solution:**
1. Verify the API key is correct
2. Check if the API key has expired
3. Verify the API key has the required permissions
4. Check if `CHANGE_ANALYSIS_AUTH_METHOD` matches your API's requirements

### Error: HTTP 403 Forbidden

The API key is valid but doesn't have permission for the requested operation.

**Solution:**
1. Check API key permissions
2. Verify the API key has access to the requested resources
3. Contact API administrator to verify permissions

## Connection Issues

### Error: Cannot connect to API

**Check:**
1. `CHANGE_ANALYSIS_API_BASE_URL` is set correctly
2. Network connectivity to the API server
3. Firewall rules allow outbound connections
4. API server is running and accessible

## Configuration Issues

### Error: "CHANGE_ANALYSIS_API_BASE_URL environment variable is required"

**Solution:**
Set the required environment variable:
```bash
export CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com
```

### Error: Invalid CHANGE_ANALYSIS_API_TIMEOUT value

**Solution:**
Ensure timeout is a valid number:
```bash
export CHANGE_ANALYSIS_API_TIMEOUT=30.0
```

### Error: Invalid CHANGE_ANALYSIS_AUTH_METHOD

**Solution:**
Use either `bearer` or `x-api-key`:
```bash
export CHANGE_ANALYSIS_AUTH_METHOD=x-api-key
```

## Getting Help

If issues persist:

1. Check server logs for detailed error messages
2. Run `health_check` tool to see configuration status
3. Verify all environment variables are set correctly
4. Test API connectivity manually (curl, etc.)
5. Review the PRODUCTION.md guide for deployment best practices
