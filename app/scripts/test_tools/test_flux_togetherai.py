"""Test for image generation using Together AI's FLUX model."""

import os
import base64
from together import Together
from dotenv import load_dotenv
from ..utils.ai_models import get_image_generation_config

load_dotenv()

client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

if __name__ == "__main__":
    # Get image generation configuration
    img_config = get_image_generation_config()

    # Generate image using the Together API
    response = client.images.generate(
        prompt="A beautiful sunset over a mountain range",
        model=img_config["name"],
        width=img_config["width"],
        height=img_config["height"],
        steps=img_config["steps"],
        n=img_config["n"],
        response_format=img_config["response_format"],
    )

    # Get the base64-encoded image from the response
    b64_image = response.data[0].b64_json

    # Decode the base64 string to binary data
    image_data = base64.b64decode(b64_image)

    # Save the image to your local system as a .png file
    with open("generated_image.png", "wb") as f:
        f.write(image_data)

    print("Image saved as 'generated_image.png'")
