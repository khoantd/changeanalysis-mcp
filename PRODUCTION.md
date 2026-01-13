# Production Deployment Guide

This guide covers best practices for deploying the Change Analysis MCP server to production.

## Pre-Deployment Checklist

- [ ] All environment variables are configured
- [ ] API credentials are secured (not hardcoded)
- [ ] Logging is configured appropriately
- [ ] Health check endpoint is accessible
- [ ] Dependencies are pinned/versioned
- [ ] Security best practices are followed

## Environment Configuration

### Required Variables

Set these environment variables before starting the server:

```bash
export CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com
export CHANGE_ANALYSIS_API_KEY=your_secure_api_key_here
```

### Recommended Production Settings

```bash
# API Configuration
export CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com
export CHANGE_ANALYSIS_API_KEY=your_secure_api_key_here
export CHANGE_ANALYSIS_API_TIMEOUT=30.0
export CHANGE_ANALYSIS_AUTH_METHOD=x-api-key

# Logging
export LOG_LEVEL=INFO  # Use WARNING or ERROR in high-traffic environments
```

## Security Best Practices

### 1. Credential Management

**Never:**
- Commit API keys or credentials to version control
- Hardcode credentials in source code
- Share credentials via insecure channels

**Always:**
- Use environment variables or secure secret management systems
- Rotate API keys regularly
- Use least-privilege API keys
- Monitor API key usage

### 2. Network Security

- Use HTTPS for API connections in production
- Implement network-level security (firewalls, VPNs)
- Restrict server access to authorized clients only
- Use TLS/SSL certificates for encrypted communication

### 3. Logging and Monitoring

- Set appropriate log levels (INFO or WARNING for production)
- Monitor logs for security events
- Set up alerting for errors and failures
- Use log aggregation tools (e.g., ELK, Splunk, CloudWatch)

### 4. Error Handling

- Avoid exposing sensitive information in error messages
- Log detailed errors internally, return user-friendly messages externally
- Implement rate limiting if needed
- Monitor for unusual patterns or attacks

## Deployment Options

### Option 1: Direct Deployment

```bash
# Install the package
pip install changeanalysis-mcp

# Set environment variables
export CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com
export CHANGE_ANALYSIS_API_KEY=your_api_key

# Run the server
fastmcp run server.py:mcp --transport http --port 8000
```

### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .

ENV CHANGE_ANALYSIS_API_BASE_URL=""
ENV CHANGE_ANALYSIS_API_KEY=""
ENV LOG_LEVEL=INFO

EXPOSE 8000

CMD ["fastmcp", "run", "server.py:mcp", "--transport", "http", "--port", "8000"]
```

Build and run:

```bash
docker build -t changeanalysis-mcp .
docker run -d \
  -p 8000:8000 \
  -e CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com \
  -e CHANGE_ANALYSIS_API_KEY=your_api_key \
  changeanalysis-mcp
```

### Option 3: Systemd Service

Create `/etc/systemd/system/changeanalysis-mcp.service`:

```ini
[Unit]
Description=Change Analysis MCP Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/changeanalysis-mcp
Environment="CHANGE_ANALYSIS_API_BASE_URL=https://your-api-server.com"
Environment="CHANGE_ANALYSIS_API_KEY=your_api_key"
Environment="LOG_LEVEL=INFO"
ExecStart=/usr/bin/fastmcp run server.py:mcp --transport http --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable changeanalysis-mcp
sudo systemctl start changeanalysis-mcp
sudo systemctl status changeanalysis-mcp
```

## Monitoring and Health Checks

### Health Check Endpoint

The server provides a `health_check` tool that verifies:
- Server is operational
- API connection is working
- Basic connectivity tests

Use this tool regularly for monitoring:

```bash
# Via MCP client
health_check
```

### Log Monitoring

Monitor logs for:
- Connection errors
- Authentication failures
- High error rates
- Unusual request patterns

### Metrics to Track

- Request count and rate
- Error rates
- Response times
- API connection health
- Server uptime

## Troubleshooting Production Issues

### Connection Issues

1. Verify `CHANGE_ANALYSIS_API_BASE_URL` is correct
2. Check network connectivity
3. Verify firewall rules
4. Test API connectivity manually

### Authentication Failures

1. Verify `CHANGE_ANALYSIS_API_KEY` is set correctly
2. Check API key hasn't expired
3. Verify `CHANGE_ANALYSIS_AUTH_METHOD` matches API requirements
4. Check API key permissions

### Performance Issues

1. Monitor request timeouts
2. Adjust `CHANGE_ANALYSIS_API_TIMEOUT` if needed
3. Check API server performance
4. Monitor resource usage (CPU, memory)

### High Error Rates

1. Check API server status
2. Review error logs for patterns
3. Verify API rate limits aren't exceeded
4. Check for network issues

## Backup and Recovery

- Keep configuration backups (without secrets)
- Document deployment procedures
- Maintain rollback procedures
- Test recovery procedures regularly

## Updates and Maintenance

1. **Before updating:**
   - Review changelog
   - Test in staging environment
   - Backup current configuration

2. **During update:**
   - Deploy during low-traffic periods
   - Monitor logs closely
   - Have rollback plan ready

3. **After update:**
   - Verify health checks pass
   - Monitor for errors
   - Confirm functionality

## Support

For production issues:
1. Check logs first
2. Review this guide
3. Test health check endpoint
4. Contact support team with:
   - Error messages
   - Log excerpts
   - Configuration (without secrets)
   - Steps to reproduce
