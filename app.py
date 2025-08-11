#streamlit app
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai


load_dotenv()

#configure the google generative ai api

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#function to load google model and provide sql query as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt[0], question])
    return response.text

# helper to clean LLM SQL output (remove ```sql fences, backticks, extra text)
def clean_sql_response(text: str) -> str:
    if not text:
        return ""
    s = text.strip()
    # remove triple backtick fences
    if s.startswith("```"):
        # drop leading ```... and take until next ```
        parts = s.split("```")
        # parts like: ['','sql\nSELECT ...',''] or ['','SELECT ...','']
        if len(parts) >= 2:
            s = parts[1]
    # remove an optional leading language tag like 'sql' on first line
    lines = s.splitlines()
    if lines and lines[0].strip().lower() in {"sql", "sqlite", "postgresql", "mysql"}:
        lines = lines[1:]
    s = "\n".join(lines).strip()
    # keep only the first statement up to ';' if multiple provided
    if ";" in s:
        s = s.split(";")[0] + ";"
    # normalize whitespace
    return s.strip()

#function to retrieve the sql query
def read_sql_query(sql, db):
    # allow only SELECT queries
    if not sql:
        raise ValueError("Empty SQL query.")
    sql_lower = sql.strip().lower()
    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")
    conn = sqlite3.connect(db)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()

#define Prompt so big
prompt=[
    """
     You are a helpful assistant that generates sql queries to answer questions about a database.
     The database schema is as follows:
     CREATE TABLE STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SELECTION VARCHAR(25), MARKS INT);
     The user will ask you questions about the database, and you will need to generate the appropriate sql query to answer the question.
     
     the sql database is name STUDENT and contains the following data:
     name varchar(25), class varchar(25), selection varchar(25), marks int;


     follow these guidelines when generating sql query
     1. ensure the output contains only the sql query-do not include explanations
     2. use proper sql syntax
     3.if query involves multiple tables, use proper join syntax
     4. if query involves aggregate functions, use proper aggregate functions

     for example
     -question: how many students are there in class 10th?
       -sql query: select count(*) from student where class = '10th';
    -question: how many students are there in class 10th and science?
      -sql query: select count(*) from student where class = '10th' and selection = 'science';
    -question: how many students are there in class 10th and science and marks greater than 90?
      -sql query: select count(*) from student where class = '10th' and selection = 'science' and marks > 90;

     """
]

#streamlit app
st.set_page_config(page_title="SQL QUERY GENERATOR | ALIDIAMOND", page_icon="📊", layout="centered", initial_sidebar_state="auto")

#display the Alidiamond logo and header
st.image("OIP.jpg", width=200)
st.markdown("# Alidiamond's Gemini App - Your AI-Powered SQL Query Generator")
st.markdown("## Ask a question about the database and get the appropriate sql query as a response")

#take user input
question = st.text_input("? Enter your query question in the plan English ", key = "input")

#generate the sql query
if st.button("Generate SQL Query"):
    raw_sql = get_gemini_response(question, prompt)
    cleaned_sql = clean_sql_response(raw_sql)
    st.subheader("Generated SQL")
    st.code(cleaned_sql, language="sql")
    try:
        rows = read_sql_query(cleaned_sql, "student.db")
        st.subheader("Results")
        if rows:
            for r in rows:
                st.write(r)
        else:
            st.info("Query executed successfully but returned no rows.")
    except Exception as e:
        st.error(f"Failed to execute SQL: {e}")
