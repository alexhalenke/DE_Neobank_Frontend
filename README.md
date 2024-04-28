# Transactions ELT Pipeline for a Neobank
(This is the frontend of our project. For accessing the backend (https://github.com/alexhalenke/DE_Neobank_Backend))


## Project Goal

A neobank gathered data of 2.7 million transactions. In this project we create a ELT pipeline for the data to enable the use of data analytics and visualization. 
The engineering challenges are the following: 
  - Extracting the data from the different data sources (csv files)
  - Storing the data in a datalake and a data warehouse
  - Data modelling according to business requirements: This has been done with dbt through the creation of different layers (Bronze, Silver & Gold)
  - Orchestrate the transformations with Airflow
  - Connecting to an interactive Dashboard 
  - Connecting a LLM to the datawarehouse
  - Making the process scalable and auto scheduled


## Set Up and Installation

Steps to set up and install the project:
  Backend
  - git clone the project
  - "poetry install"
  - create a .env file with: LAKE_BUCKET, POSTGRES_PASSWORD, DATASET, GCP_LOCATION, GCP_PROJECT_ID
  - create a datalake bucket to store data
  - "python de_neobank_backend/datalake/main_datalake.py" for uploading data into bucket
  - "python de_neobank_backend/pipeline/create_tables.py" for creating a dataset
  - "python de_neobank_backend/pipeline/upload_data.py" for uploading into the dataset
  - go into dbt folder and run "dbt run --target prod
  - "docker compose up --build" for airflow
  Frontend
  - git clone the project
  - "poetry install"
  - Set up .gcp_keys and .streamlit keys
  - "docker compose up --build" for accessing streamlit
  - Open the port 8501 and try out dashboard
  - With own OPENAI_API_KEY you can ask questions to the data
    

## Features

![Neo Bank](https://github.com/alexhalenke/DE_Neobank_Backend/assets/109359407/e7967894-8103-4b58-a960-b8af83acca6e)
Technologies used: 
  - GCP, BigQuery, dbt, Airflow, Docker, Streamllit, OpenAI


## Usage

How to use your project:
The deliverable of this project is a dashboard on streamlit. There are different filters that can be used. Here a screenshot of the dashboard:
![Screenshot 2024-04-27 213852](https://github.com/alexhalenke/DE_Neobank_Backend/assets/109359407/763f50f1-41f0-4d85-8bc5-0e5ae693d7aa)
In the dashboard there are 3 different parts. The marketing team, finance team and a space to ask questions to an LLM.
In the following image you can see the LLM part: 
![Screenshot 2024-04-27 220225](https://github.com/alexhalenke/DE_Neobank_Backend/assets/109359407/b105bf0f-009f-417e-838b-e98facfd1c88)


## Future improvements 
In the next weeks we are going to iteratively improve the project, implementing the following features:
  - inject .env with docker compose (https://docs.docker.com/compose/environment-variables/set-environment-variables/)
  - Own usage of OpenAI key
  - Terraform
  - CloudSQL
  - Orchestration of extract and load process
  - CI/CD pipeline
  - Build an API with different endpoints that trigger different dbt commands (https://medium.com/@ivan_toriya/step-by-step-guide-to-run-dbt-in-production-with-google-cloud-platform-fb1f035f3c7b)
    

## Credits  
Following persons have contributed to this project:
  - Enrico Dainelli
  - Ikechi Ochulo
  - Luiggi Navilys
  - Marlin Akhter
  - Alexander Halenke
