from sqlalchemy import *
from sqlalchemy.schema import *
import os
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent



service_account_file = "/home/ahalenke/.gcp_keys/le-wagon-de-bootcamp.json" # Change to where your service account key file is located
project = "modern-water-402010"
dataset = "neobank_Silver_Tier"
sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

#Database information
db = SQLDatabase.from_uri(sqlalchemy_url)

#Convert questions to a SQL query
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
agent_executor.invoke({"How many unique transactions happened in december 2018?"})
