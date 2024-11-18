import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


def generate_sql_query(question: str) -> str:

    load_dotenv()

    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    llm = ChatGroq(model="llama3-groq-70b-8192-tool-use-preview", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
        Generate a SQL query to answer this question: `{user_question}`
        {instructions}
        DDL statements:
        {create_table_statements}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    )

    model = prompt | llm

    response = model.invoke({"user_question": question,
                "instructions": "- if the question cannot be answered given the database schema, return 'I do not know' "
                                "\n- recall that the current date in YYYY-MM-DD format is 2024-09-29"
                                "act as an expert in the field of computer science"
                                ""
                                ,
                "create_table_statements": "CREATE TABLE machines (production_speed TEXT, main_market TEXT, application TEXT, closure_head TEXT, versions TEXT, options TEXT);"})


    return response.content
 