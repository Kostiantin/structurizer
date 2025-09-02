# My Dockerfile for local testing
# Not used in Lambda to avoid ECS costs
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY api/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]