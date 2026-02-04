from unittest.mock import MagicMock, patch

import pytest

from server import execute_sql

REJECTED = "Only SELECT queries are allowed."


def _mock_db(columns, rows):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = rows
    mock_cursor.description = [(c,) for c in columns]
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return patch("server.pyodbc.connect", return_value=mock_conn)


# --- SELECT 허용 ---


def test_simple_select():
    # given
    sql = "SELECT 1 AS n"

    # when
    with _mock_db(["n"], [(1,)]):
        result = execute_sql(sql)

    # then
    assert "1" in result


def test_select_with_single_line_comment():
    # given
    sql = "-- 주석 내용\nSELECT * FROM items"

    # when
    with _mock_db(["id"], [(1,)]):
        result = execute_sql(sql)

    # then
    assert result != REJECTED


def test_select_with_block_comment():
    # given
    sql = "/* 블록 주석 */\nSELECT * FROM items"

    # when
    with _mock_db(["id"], [(1,)]):
        result = execute_sql(sql)

    # then
    assert result != REJECTED


def test_select_with_cte():
    # given
    sql = "WITH cte AS (SELECT 1 AS n) SELECT * FROM cte"

    # when
    with _mock_db(["n"], [(1,)]):
        result = execute_sql(sql)

    # then
    assert result != REJECTED


def test_select_with_leading_whitespace():
    # given
    sql = "   \n  SELECT 1 AS n"

    # when
    with _mock_db(["n"], [(1,)]):
        result = execute_sql(sql)

    # then
    assert result != REJECTED


# --- 비-SELECT 거부 ---


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO users (name) VALUES ('a')",
        "UPDATE users SET name = 'a'",
        "DELETE FROM users",
        "DROP TABLE users",
        "ALTER TABLE users ADD col INT",
        "CREATE TABLE t (id INT)",
        "",
        "   ",
    ],
)
def test_rejects_non_select(sql):
    # given: 위 parametrize sql

    # when
    result = execute_sql(sql)

    # then
    assert result == REJECTED
