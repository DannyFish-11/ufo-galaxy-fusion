FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn httpx numpy

COPY main.py .

EXPOSE 8055

CMD ["python", "main.py"]
