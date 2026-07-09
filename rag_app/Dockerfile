FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create cache directory and grant full access permissions
ENV HF_HOME=/app/.cache
RUN mkdir -p /app/.cache && chmod -R 777 /app/.cache

# Download the model to the newly permissive directory
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

ENV PORT=7860
EXPOSE 7860
ENV PYTHONUNBUFFERED=1

# Fixed Module call (app instead of app.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
