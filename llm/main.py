from sqlalchemy import *
from sqlalchemy.schema import *
import os
from langchain.sql_database import SQLDatabase
from langchain_community.document_loaders import BigQueryLoader
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool


service_account_file = "/home/ahalenke/.gcp_keys/le-wagon-de-bootcamp.json" # Change to where your service account key file is located
project = "modern-water-402010"
dataset = "neobank_Silver_Tier"
sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'

os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

#query = """
#   SELECT *
#   FROM `modern-water-402010.neobank_Silver_Tier.transactions_facts`
#   LIMIT 10
#"""
#loader = BigQueryLoader(query)
#data = loader.load()

#Database information
db = SQLDatabase.from_uri(sqlalchemy_url)

#Convert questions to a SQL query
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many unique users?. Give me an integer"})

print(f'This is the SQL Query:\n{response}')

print(db.run(response))


execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
chain = write_query | execute_query
chain.invoke({"question": "How many unique users?. Give me an integer"})
