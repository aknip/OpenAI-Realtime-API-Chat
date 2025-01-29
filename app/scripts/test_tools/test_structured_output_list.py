"""Test for structured output list generation using LLM."""

import os
from typing import List
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.output_parsers import CommaSeparatedListOutputParser
from utils.ai_models import get_llm


class CommercialScenes(BaseModel):
    """A structured output for commercial scenes."""

    scene_descriptions: List[str] = Field(
        ...,
        description="A list of scene descriptions for a commercial",
    )


# Get LLM instance with creative temperature for scene descriptions
llm = get_llm("creative_content")
structured_llm = llm.with_structured_output(CommercialScenes)

system_template = """
Create a list of {{number_of_scenes}} scene descriptions for a {{topic}} commercial in the location {{location}}. Each scene should be a short paragraph that describes the scene in detail.
"""

prompt_template = PromptTemplate(
    input_variables=["number_of_scenes", "topic", "location"],
    template=system_template,
)

# Define an output parser
output_parser = CommaSeparatedListOutputParser()

if __name__ == "__main__":
    chain = prompt_template | llm | output_parser
    scene_list = chain.invoke({"number_of_scenes": 5, "topic": "range rover", "location": "Lanzarote"})
    print(scene_list)
