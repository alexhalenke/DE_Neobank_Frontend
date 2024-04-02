from sqlalchemy import *
from sqlalchemy.schema import *
import os
from langchain.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts.chat import HumanMessagePromptTemplate




service_account_file = "/home/ahalenke/.gcp_keys/le-wagon-de-bootcamp.json" # Change to where your service account key file is located
project = "modern-water-402010"
dataset = "neobank_Silver_Tier"
sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

#Database information
db = SQLDatabase.from_uri(sqlalchemy_url)

#Convert questions to a SQL query
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def retrieve_from_db(query: str) -> str:
    db_context = db_chain(query)
    db_context = db_context['result'].strip()
    return db_context

def generate(query: str) -> str:
    db_context = retrieve_from_db(query)

    system_message = """You are a professional consultant of the Neobank.
        You have to answer user's queries and provide relevant information to help the CEO understand how the business is going?.
        Example:

        Input:
        In which month, do the most transaction happen in our Neobank

        Context:
        The most amount of transactions happen in the following months:
        1. January
        2. February

        Output:
        TThe most amount of transactions happen in january and february
        """

    human_qry_template = HumanMessagePromptTemplate.from_template(
        """Input:
        {human_input}

        Context:
        {db_context}

        Output:
        """
    )
    messages = [
      SystemMessage(content=system_message),
      human_qry_template.format(human_input=query, db_context=db_context)
    ]
    response = llm(messages).content
    return response

if __name__ == "__main__":
    result = generate("How many transactions happened in December 2018 via an Apple device?")
    print(result)
