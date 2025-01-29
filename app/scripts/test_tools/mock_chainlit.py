"""Mock chainlit for testing."""

from contextlib import contextmanager
from unittest.mock import patch


class MockMessage:
    """Mock chainlit Message for testing."""

    def __init__(self, content: str, *args, **kwargs):
        self.content = content

    async def send(self):
        """Print message content instead of sending to chainlit."""
        print(f"\n=== Chainlit Message ===\n{self.content}\n=====================")


@contextmanager
def mock_chainlit():
    """Context manager to temporarily replace chainlit's Message class."""
    with patch("chainlit.Message", MockMessage):
        yield
