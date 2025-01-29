"""Common utilities and configurations."""

import os
import logging
from dotenv import load_dotenv
from together import Together
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Scratchpad directory
scratch_pad_dir = "../scratchpad"
os.makedirs(scratch_pad_dir, exist_ok=True)

# Initialize clients
together_client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
