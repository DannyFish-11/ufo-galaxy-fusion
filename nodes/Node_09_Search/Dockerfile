FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn httpx requests

COPY main.py .

EXPOSE 8009

CMD ["python", "main.py"]
