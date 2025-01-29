"""Stock price querying tool."""

import yfinance as yf
from utils.common import logger

query_stock_price_def = {
    "name": "query_stock_price",
    "description": "Queries the latest stock price information for a given stock symbol.",
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol to query (e.g., 'AAPL' for Apple Inc.)",
            },
            "period": {
                "type": "string",
                "description": "The time period for which to retrieve stock data (e.g., '1d' for one day, '1mo' for one month)",
            },
        },
        "required": ["symbol", "period"],
    },
}


async def query_stock_price_handler(symbol, period):
    """Queries the latest stock price information for a given stock symbol."""
    try:
        logger.info(f"📈 Fetching stock price for symbol: {symbol}, period: {period}")
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        if hist.empty:
            logger.warning(f"⚠️ No data found for symbol: {symbol}")
            return {"error": "No data found for the given symbol."}
        logger.info(f"💸 Stock data retrieved successfully for symbol: {symbol}")
        return hist.to_json()
    except Exception as e:
        logger.error(f"❌ Error querying stock price for symbol: {symbol} - {str(e)}")
        return {"error": str(e)}


query_stock_price = (query_stock_price_def, query_stock_price_handler)
