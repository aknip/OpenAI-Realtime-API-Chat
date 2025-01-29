"""Image generation tool."""

import base64
import os

import chainlit as cl
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from utils.ai_models import get_image_generation_config, get_llm
from utils.common import logger, scratch_pad_dir, together_client


class EnhancedPrompt(BaseModel):
    """Class for the text prompt"""

    content: str = Field(
        ...,
        description="The enhanced text prompt to generate an image",
    )


generate_image_def = {
    "name": "generate_image",
    "description": "Generates an image based on a given prompt.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "The prompt to generate an image (e.g., 'A beautiful sunset over the mountains')",
            },
        },
        "required": ["prompt"],
    },
}


async def generate_image_handler(prompt):
    """Generates an image based on a given prompt using the Together API."""
    try:
        logger.info(f"✨ Enhancing prompt: '{prompt}'")

        llm = get_llm("image_prompt")

        structured_llm = llm.with_structured_output(EnhancedPrompt)

        system_template = """
        Enhance the given prompt the best prompt engineering techniques such as providing context, specifying style, medium, lighting, and camera details if applicable. If the prompt requests a realistic style, the enhanced prompt should include the image extension .HEIC.

        # Original Prompt
        {prompt}

        # Objective
        **Enhance Prompt**: Add relevant details to the prompt, including context, description, specific visual elements, mood, and technical details. For realistic prompts, add '.HEIC' in the output specification.

        # Example
        "realistic photo of a person having a coffee" -> "photo of a person having a coffee in a cozy cafe, natural morning light, shot with a 50mm f/1.8 lens, 8425.HEIC"
        """

        prompt_template = PromptTemplate(
            input_variables=["prompt"],
            template=system_template,
        )

        chain = prompt_template | structured_llm
        enhanced_prompt = chain.invoke({"prompt": prompt}).content

        logger.info(f"🌄 Generating image based on prompt: '{enhanced_prompt}'")

        # Get image generation configuration
        img_config = get_image_generation_config()
        response = together_client.images.generate(
            prompt=prompt,
            model=img_config["name"],
            width=img_config["width"],
            height=img_config["height"],
            steps=img_config["steps"],
            n=img_config["n"],
            response_format=img_config["response_format"],
        )

        b64_image = response.data[0].b64_json
        image_data = base64.b64decode(b64_image)

        img_path = os.path.join(scratch_pad_dir, "generated_image.jpeg")
        with open(img_path, "wb") as f:
            f.write(image_data)

        logger.info(f"🖼️ Image generated and saved successfully at {img_path}")
        image = cl.Image(path=img_path, name="Generated Image", display="inline")
        await cl.Message(
            content=f"Image generated with the prompt '{enhanced_prompt}'",
            elements=[image],
        ).send()

        return "Image successfully generated"

    except Exception as e:
        logger.error(f"❌ Error generating image: {str(e)}")
        return {"error": str(e)}


generate_image = (generate_image_def, generate_image_handler)
