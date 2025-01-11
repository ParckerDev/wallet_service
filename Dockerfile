FROM python:3.10-slim

RUN pip install --no-cache-dir poetry

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

CMD ["sh", "-c", "sleep 2 && ls && alembic revision --autogenerate -m 'pre initial migrations' && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
