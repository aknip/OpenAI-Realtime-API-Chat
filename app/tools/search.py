"""Internet search tool using Tavily API."""

import chainlit as cl
from utils.common import logger, tavily_client

internet_search_def = {
    "name": "internet_search",
    "description": "Performs an internet search using the Tavily API.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to look up on the internet (e.g., 'What's the weather like in Madrid tomorrow?').",
            },
        },
        "required": ["query"],
    },
}


async def internet_search_handler(query):
    """Executes an internet search using the Tavily API and returns the result."""
    try:
        logger.info(f"🕵 Performing internet search for query: '{query}'")
        response = tavily_client.search(query)

        results = response.get("results", [])
        if not results:
            await cl.Message(content=f"No results found for '{query}'.").send()
            return None

        formatted_results = "\n".join(
            [
                f"{i+1}. [{result['title']}]({result['url']})\n{result['content'][:200]}..."
                for i, result in enumerate(results)
            ]
        )

        message_content = f"Search Results for '{query}':\n\n{formatted_results}"
        await cl.Message(content=message_content).send()

        logger.info(f"📏 Search results for '{query}' retrieved successfully.")
        return response["results"]
    except Exception as e:
        logger.error(f"❌ Error performing internet search: {str(e)}")
        await cl.Message(content=f"An error occurred while performing the search: {str(e)}").send()


internet_search = (internet_search_def, internet_search_handler)
