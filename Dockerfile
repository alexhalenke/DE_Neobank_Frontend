FROM python:3.8.14

# Do not use env as this would persist after the build and would impact your containers, children images
ARG DEBIAN_FRONTEND=noninteractive

# Force the stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED 1

# Setup workdir
WORKDIR /app

# Copy project files
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
COPY ./de_neobank_frontend ./neobank_gold

# Install Poetry
RUN pip3 install --no-cache-dir poetry

# Install dependencies using Poetry
RUN poetry install --no-root

# Expose port 8501 for Streamlit
EXPOSE 8501

# Set entrypoint to "poetry run" to execute commands within the Poetry environment
ENTRYPOINT ["poetry", "run"]
