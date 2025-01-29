"""Test for Llama 3.2 vision model capabilities."""

import os
import base64
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path: str) -> str:
    """Encodes an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    # Path to your image
    image_path = "path/to/your/image.png"
    base64_image = encode_image(image_path)

    client = Groq()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You're an image caption expert specifically designed to write image captions that will be used in text-to-image models like Midjourney or FLUX. I'll give you an image and you directly need to answer with the caption that best describes the image. Every description must be complete, describing character, composition, lightning, style, artist, etc.",
                    },
                    {
                        "type": "text",
                        "text": "An example of a caption could be: 'A black-and-white portrait of a young woman laughing with her eyes closed, capturing a spontaneous and joyful expression. She has straight, shoulder-length hair and wears small hoop earrings. The high contrast lighting enhances her facial features and creates a striking shadow on her bare shoulders against the plain white background. The photograph's minimalist composition and raw emotion evoke a sense of authenticity and freedom, reminiscent of classic, candid portraiture in fashion and editorial photography.'",
                    },
                    {
                        "type": "text",
                        "text": "Please write a caption for the following image:",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )

    print(chat_completion.choices[0].message.content)
