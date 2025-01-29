"""Browser interaction tool."""

import asyncio
import webbrowser
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field
from utils.ai_models import get_llm
from utils.common import logger


class WebUrl(BaseModel):
    """Web URL response."""

    url: str = Field(
        ...,
        description="The URL to open in the browser",
    )


open_browser_def = {
    "name": "open_browser",
    "description": "Opens a browser tab with the best-fitting URL based on the user's prompt.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The user's prompt to determine which URL to open.",
            },
        },
        "required": ["prompt"],
    },
}


async def open_browser_handler(prompt: str):
    """Open a browser tab with the best-fitting URL based on the user's prompt."""
    try:
        logger.info(f"📖 open_browser() Prompt: {prompt}")

        browser_urls = [
            "https://www.chatgpt.com",
            "https://www.tesla.com",
            "https://www.spacex.com",
            "https://www.goodreads.com",
        ]
        browser_urls_str = "\n".join(browser_urls)
        browser = "chrome"

        prompt_structure = f"""
        Select a browser URL from the list of browser URLs based on the user's prompt.

        # Steps:
        1. Infer the browser URL that the user wants to open from the user-prompt and the list of browser URLs.
        2. If the user-prompt is not related to the browser URLs, return an empty string.

        # Browser URLs:
        {browser_urls_str}

        # Prompt:
        {prompt}
        """

        llm = get_llm()
        structured_llm = llm.with_structured_output(WebUrl)
        response = structured_llm.invoke(prompt_structure)

        logger.info(f"📖 open_browser() Response: {response}")

        # Open the URL if it's not empty
        if response.url:
            logger.info(f"📖 open_browser() Opening URL: {response.url}")
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                await loop.run_in_executor(pool, webbrowser.get(browser).open, response.url)
            return f"URL opened successfully in the browser: {response.url}"
        else:
            error_message = f"Error retrieving URL from the prompt: {prompt}"
            logger.error(f"❌ {error_message}")
            return error_message

    except Exception as e:
        logger.error(f"❌ Error opening browser: {str(e)}")
        return {"status": "Error", "message": str(e)}


open_browser = (open_browser_def, open_browser_handler)
