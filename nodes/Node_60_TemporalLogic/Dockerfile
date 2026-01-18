FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn httpx z3-solver

COPY main.py .

EXPOSE 8060

CMD ["python", "main.py"]
