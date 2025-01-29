"""Test suite for tools."""

import asyncio

from dotenv import load_dotenv
from mock_chainlit import mock_chainlit
from tools.database import execute_sql_handler

load_dotenv()


async def test_database_tools():
    """Test database queries with mocked chainlit."""
    with mock_chainlit():
        await execute_sql_handler("Show me all active users")
        await execute_sql_handler("How many orders were placed last month?")
        await execute_sql_handler("Who are the top 5 users by order amount?")


if __name__ == "__main__":
    asyncio.run(test_database_tools())
