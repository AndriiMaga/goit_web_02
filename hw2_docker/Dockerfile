FROM python:3.11.9

WORKDIR /app


ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

COPY . .

CMD ["python", "main.py"]