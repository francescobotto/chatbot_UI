import os
import sqlite3

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def generate_sql_query(question: str) -> str:
    prompt = PromptTemplate.from_template(
        """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
        Generate a plain SQL query to answer this question: `{user_question}`
        {instructions}
        DDL statements:
        {create_table_statements}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    )

    model = prompt | llm

    response = model.invoke({"user_question": question,
                "instructions": "- if the question cannot be answered given the database schema, return 'I do not know' "
                                "- recall that the current date in YYYY-MM-DD format is 2024-09-29"
                                "- act as an expert in the field of computer science"
                                "- the main_market column is a list of the main markets for the machine, the prossible values are: 'BEVERAGE', 'FOOD', 'CHEMICAL', 'PHARMACEUTICAL', 'HOME CARE', 'BEER', 'SPIRITS', 'WINE&SPIRITS' and must queried with the LIKE operator"
                                "- An example response would be like: \nSELECT * FROM machines WHERE main_market LIKE '%BEER%' AND closure_head = 'SCREW CAP';"
                                "- You MUST return only a valid SQL query, without any additional text or character"
                                ,
                "create_table_statements": "CREATE TABLE machines (speed_production INTEGER, main_market TEXT, caps_applications TEXT, closure_heads TEXT);"})

    query = response.content
    
    if query == "I do not know":
        return query

    print(query)
    conn = sqlite3.connect('./db.db')
    c = conn.cursor()
    answer = ""
    for row in c.execute(query):
        versions = c.execute("SELECT * FROM versions WHERE machine_id = ?", (row[0],)).fetchall()
        options = c.execute("SELECT * FROM options WHERE machine_id = ?", (row[0],)).fetchall
        answer += str(row) + "\nVersions: " + str(versions) + "\nOptions: " + str(options) + "\n\n"

    conn.close()

    summary_prompt = PromptTemplate.from_template(
        """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
        Compare the different machines reported using few sentences and focusing on the specifications.
        Machines: {sql_result}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    )

    model = summary_prompt | llm

    response = model.invoke({"sql_result": answer})

    return response.content
 