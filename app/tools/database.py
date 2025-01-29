"""Database query tool with natural language to SQL conversion."""

import os

import chainlit as cl
import yaml
from config.database import db_config, db_connection, dialect_info
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from utils.ai_models import get_llm
from utils.common import logger


def load_schema_description():
    """Loads and formats the schema description from YAML file."""
    schema_path = os.path.join(os.path.dirname(__file__), "../config/schema.yaml")
    with open(schema_path, "r") as f:
        schema_data = yaml.safe_load(f)

    # Format the schema description
    description = "Available tables and their structures:\n\n"

    # Add tables and their columns
    for table_name, table_info in schema_data["schema"]["tables"].items():
        description += f"{table_name}\n"
        for column in table_info["columns"]:
            constraints = f", {column['constraints']}" if "constraints" in column else ""
            description += f"- {column['name']} ({column['type']}{constraints})\n"
        description += "\n"

    # Add example queries
    description += "Example queries:\n"
    for example in schema_data["schema"]["example_queries"]:
        description += f"Q: {example['question']}\n"
        description += f"A: {example['sql']}\n\n"

    return description


# Load schema description when module is imported
SCHEMA_DESCRIPTION = load_schema_description()


class SQLQuery(BaseModel):
    """SQL query generated from natural language."""

    query: str = Field(
        ...,
        description="The SQL query to execute",
    )
    explanation: str = Field(
        ...,
        description="Explanation of what the SQL query does",
    )


execute_sql_def = {
    "name": "execute_sql",
    "description": "Converts natural language to SQL and executes the query on the database.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "Natural language question about the data (e.g., 'Show me all users who joined last month')",
            },
        },
        "required": ["question"],
    },
}


async def execute_sql_handler(question: str):
    """Converts natural language to SQL, executes the query, and returns results."""
    try:
        logger.info(f"🤔 Processing natural language query: '{question}'")

        llm = get_llm("sql_generation")
        structured_llm = llm.with_structured_output(SQLQuery)

        dialect = db_config.dialect.lower()
        dialect_help = dialect_info.get(dialect, {"notes": "", "examples": ""})

        system_template = f"""
        You are an expert SQL query generator for {dialect.upper()} databases. Convert the given natural language question into a {dialect.upper()}-compatible SQL query.
        Ensure the query is efficient and follows {dialect.upper()} syntax and best practices.

        # Important Notes for {dialect.upper()}
        {dialect_help["notes"]}

        # Database Schema
        {SCHEMA_DESCRIPTION}

        # Example Queries for {dialect.upper()}
        {dialect_help["examples"]}
        
        # Question
        {{question}}

        # Task
        1. Analyze the question and the schema
        2. Generate a {dialect.upper()}-compatible SQL query
        3. Provide a brief explanation of what the query does
        4. Return both the query and explanation
        """

        prompt_template = PromptTemplate(
            input_variables=["question"],
            template=system_template,
        )

        chain = prompt_template | structured_llm
        sql_response = chain.invoke({"question": question})

        # Log the generated SQL
        logger.info(f"💡 Generated SQL query: {sql_response.query}")
        logger.info(f"💡 Generated SQL explanation: {sql_response.explanation}")

        # Group SQL query and explanation in one message with elements
        formatted_sql = (
            sql_response.query.replace(" FROM ", "\nFROM ")
            .replace(" JOIN ", "\nJOIN ")
            .replace(" WHERE ", "\nWHERE ")
            .replace(" GROUP BY ", "\nGROUP BY ")
            .replace(" ORDER BY ", "\nORDER BY ")
        )

        await cl.Message(content=formatted_sql, language="sql").send()
        await cl.Message(content=f"**Explanation:** {sql_response.explanation}").send()

        # Execute the generated SQL query
        result = db_connection.execute_query(sql_response.query)

        if "error" in result:
            await cl.Message(content=f"❌ Error executing query: {result['error']}", type="error").send()
            return result

        if "rows" in result:
            # Format SELECT query results
            columns = result["columns"]
            rows = result["rows"]

            if not rows:
                await cl.Message(content="Query executed successfully. No results found.").send()
                return {"message": "No results"}

            # Create a markdown table for better formatting
            header = "| " + " | ".join(f"**{str(col)}**" for col in columns) + " |"
            separator = "|" + "|".join("---" for _ in columns) + "|"
            rows_formatted = ["| " + " | ".join(str(value) for value in row.values()) + " |" for row in rows]

            table = "\n".join([header, separator] + rows_formatted)
            await cl.Message(content=f"**Query Results:**\n\n{table}").send()
            return {"rows": rows}
        else:
            # Format INSERT/UPDATE/DELETE results
            message = f"✅ Query executed successfully. Affected rows: {result['affected_rows']}"
            await cl.Message(content=message).send()
            return result

    except Exception as e:
        error_message = f"Error processing query: {str(e)}"
        logger.error(f"❌ {error_message}")
        await cl.Message(content=error_message, type="error").send()
        return {"error": error_message}


execute_sql = (execute_sql_def, execute_sql_handler)
