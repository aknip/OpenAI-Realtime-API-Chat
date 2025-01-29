"""AI model configuration and initialization."""

import os

import yaml
from langchain_groq import ChatGroq
from utils.common import logger


def load_model_config():
    """Loads the AI model configuration from YAML file."""
    config_path = os.path.join(os.path.dirname(__file__), "../config/ai_models.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["models"]


def get_llm(task: str = "default") -> ChatGroq:
    """Returns a configured LLM instance for the specified task."""
    try:
        config = load_model_config()
        default_config = config["default"]
        task_config = config.get(task, {})

        # Merge default config with task-specific config
        model_config = {**default_config, **task_config}

        return ChatGroq(
            model=model_config["name"],
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=model_config["temperature"],
            max_retries=model_config["max_retries"],
        )
    except Exception as e:
        logger.error(f"❌ Error initializing LLM for task '{task}': {str(e)}")
        # Fallback to default configuration
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0.1,
            max_retries=2,
        )


def get_image_generation_config(task: str = "image_generation") -> dict:
    """Returns configuration for image generation."""
    try:
        config = load_model_config()
        return config[task]
    except Exception as e:
        logger.error(f"❌ Error loading image generation config: {str(e)}")
        # Fallback to default configuration
        return {
            "provider": "together",
            "name": "black-forest-labs/FLUX.1.1-pro",
            "width": 1024,
            "height": 768,
            "steps": 4,
            "n": 1,
            "response_format": "b64_json",
        }
