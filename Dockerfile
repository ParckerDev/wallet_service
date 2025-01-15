FROM python:3.10-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

CMD ["sh", "-c", "sleep 2 && alembic revision --autogenerate -m 'initial migrations' && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
