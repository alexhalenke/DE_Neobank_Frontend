from sqlalchemy import *
from sqlalchemy.schema import *
import os
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent


def query_database(question):
    # Set up environment variables
    service_account_file = os.environ.get("service_account_file")  # Change to where your service account key file is located
    project = os.environ.get("project")
    dataset = os.environ.get("dataset")
    sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

    # Connect to the database
    db = SQLDatabase.from_uri(sqlalchemy_url)

    # Convert questions to a SQL query
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
    response = agent_executor.invoke({"input": question})
    return response

if __name__ == "__main__":
    result = query_database("How many transations happened in 2018?")
    print(result)
