FROM postgres:13.3
RUN apt update && apt install python3 python3-pip postgresql-plpython3-${PG_MAJOR} -y
RUN echo 'CREATE EXTENSION IF NOT EXISTS plpython3u;' > /docker-entrypoint-initdb.d/py3.sql
FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
FROM python:3.11
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r /code/requirements.txt
COPY ./app /code/app
COPY ./.env /code/.env
COPY ./data_clean.json /code/data_clean.json
COPY ./data_fraud.json /code/data_fraud.json
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]