from contextlib import contextmanager

import pyodbc
from mcp.server.fastmcp import FastMCP

from config import settings

mcp = FastMCP("Microsoft SQL Server")


@contextmanager
def get_db():
    conn = pyodbc.connect(settings.mssql_connection_string)
    try:
        cursor = conn.cursor()
        yield cursor
    finally:
        cursor.close()
        if not conn.closed:
            conn.close()


@mcp.tool()
def execute_sql(sql: str) -> str:
    if not sql.strip().upper().startswith("SELECT"):
        return "Only SELECT queries are allowed."
    with get_db() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
    return str(data)
