FROM python:3.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir mcpo uv pymongo dotenv mcp

WORKDIR /app

CMD ["mcpo", "--host", "0.0.0.0", "--port", "8000", "--config", "/app/config/config.json"]
