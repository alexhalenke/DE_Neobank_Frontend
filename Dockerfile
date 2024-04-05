FROM python:3.8.19

# Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

#Setup workdir
WORKDIR /app

COPY ./pyproject.toml  ./pyproject.toml
COPY ./poetry.lock  ./poetry.lock
COPY ./de_neobank_frontend  ./neobank_gold
COPY ./llm ./llm
COPY ./.gcp_keys/ ./.gcp_keys

#Do not forget to add own OpenAI api key
ENV project=modern-water-402010
ENV dataset=neobank_Silver_Tier
ENV service_account_file=/app/.gcp_keys/le-wagon-de-bootcamp.json

RUN apt-get update \
    && apt-get -y upgrade \
    && pip3 install --no-cache-dir poetry \
    && poetry install --only main \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8501

ENTRYPOINT [ "poetry", "run" ]
