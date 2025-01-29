"""Test for Python file creation using LLM."""

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from utils.ai_models import get_llm

load_dotenv()


class PythonFile(BaseModel):
    """Python file content."""

    filename: str = Field(
        ...,
        description="The name of the Python file with the extension .py",
    )
    content: str = Field(
        ...,
        description="The Python code to be saved in the file",
    )


# Get LLM instance configured for Python code generation
llm = get_llm("python_code")
structured_llm = llm.with_structured_output(PythonFile)

system_template = """
Create a Python script for the given topic. The script should be well-commented, use best practices, and aim to be simple yet effective. 
Include informative docstrings and comments where necessary.

# Topic
{topic}

# Requirements
1. **Define Purpose**: Write a brief docstring explaining the purpose of the script.
2. **Implement Logic**: Implement the logic related to the topic, keeping the script easy to understand.
3. **Best Practices**: Follow Python best practices, such as using functions where appropriate and adding comments to clarify the code.
"""

prompt_template = PromptTemplate(
    input_variables=["topic"],
    template=system_template,
)

chain = prompt_template | structured_llm

if __name__ == "__main__":
    response = chain.invoke({"topic": "Print a random number from 500 to 1000."})
    print(response.filename)
    print(response.content)
