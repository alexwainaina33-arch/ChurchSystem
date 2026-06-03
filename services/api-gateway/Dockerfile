FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python -c \"import asyncio; from app.database import engine; from app.models.church import Base; asyncio.run(engine.run_sync(Base.metadata.create_all)) \" 2>/dev/null; python seed.py; uvicorn app.main:app --host 0.0.0.0 --port 8000"]
