FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn httpx nashpy

COPY main.py .

EXPOSE 8063

CMD ["python", "main.py"]
