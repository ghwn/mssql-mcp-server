# MSSQL MCP Server


## Prerequisites

- [uv](https://github.com/astral-sh/uv)
- [Claude Code](https://claude.com/product/claude-code)


## How To Set Up

1. Copy `.env.example` to `.env` and edit `.env`.
2. Move to your project.
   ```
   cd /path/to/project
   ```
3. Run the following command. You must replace `/path/to` with your actual path.
   ```
   claude mcp add --transport stdio mssql -- /path/to/uv --directory /path/to/mssql-mcp-server run mcp run /path/to/mssql-server/server.py
   ```
4. Verify the MCP server is successfully working.
   ```
   claude mcp list
   ```
