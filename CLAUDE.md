# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an MCP (Model Context Protocol) server that provides secure access to Microsoft SQL Server databases through Claude Desktop. The server implements read-only database operations with security restrictions.

## Architecture

- **server.py**: Main MCP server using FastMCP framework
  - Implements MCP resource for table data (`table://{table_name}`)
  - Provides `execute_sql` tool for SELECT queries only
  - Uses context manager for database connections
- **config.py**: Configuration management using Pydantic Settings
  - Loads environment variables from `.env` file
  - Constructs MSSQL connection string with security settings
- **Database Connection**: Uses pyodbc with ODBC Driver 18 for SQL Server

## Development Commands

### Running the Server
```bash
uv run mcp run server.py
```

### Installing Dependencies
```bash
uv sync
```

### Testing Server Integration
The server is designed to be used with Claude Desktop. Test by:
1. Setting up `.env` file with database credentials
2. Adding server configuration to `claude_desktop_config.json`
3. Restarting Claude Desktop
4. Verifying connection in Claude interface

## Configuration

The server requires a `.env` file with MSSQL connection details:
- Copy `.env.example` to `.env`
- Configure: `MSSQL_HOST`, `MSSQL_PORT`, `MSSQL_USER`, `MSSQL_PASSWORD`, `MSSQL_DB`

## Security Constraints

- Only SELECT queries are permitted through `execute_sql` tool
- Database connections use encrypted connections with TrustServerCertificate=yes
- Connection timeouts are enforced (default 30 seconds)
