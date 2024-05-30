FROM python:3.10

WORKDIR /code

COPY ./Pipfile ./Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && pipenv install --system --deploy

COPY ./src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]