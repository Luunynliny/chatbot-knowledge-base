## Requirements
- MacOS
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Instructions

### Install an LLM model using DMR

1. Setup [Docker](https://docs.docker.com/engine/install/)

2. Enable [Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#docker-desktop)

3. Pull `mistral:latest` model

4. Run the model

### Setup OpenWebUI

1. Pull OpenWebUI image

```bash
docker pull ghcr.io/open-webui/open-webui:main
```

1. Create a `docker-compose.yaml`

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    environment:
      - WEBUI_AUTH=False # Single User mode 
      - WEBUI_NAME=Chatbot Knowledge Base
      - OPENAI_API_BASE_URL=http://model-runner.docker.internal/engines/v1
    volumes:
      - open-webui:/app/backend/data
    depends_on:
    - docker-model-runner-mistral

  docker-model-runner-mistral:
    provider:
      type: model
      options:
        model: ai/mistral-4.0-nano

volumes:
  open-webui:
```

2. Build `docker compose up`

3. Access OpenWebUI at `localhost:3000`

4. Pull `smollm2:latest` model

5. Update the configuration

```yaml
services:
    open-webui:
        # ...
        depends_on:
            - docker-model-runner-mistral
            - docker-model-runner-smoll

    # ...
    docker-model-runner-smoll:
        provider:
        type: model
        options:
            model: ai/smollm2
    # ...
```

### MCP

1. Setup virtual environment

```bash
uv venv
source .venv/bin/activate
```

2. Install the [mcp](https://github.com/modelcontextprotocol/python-sdk) package

```bash
uv pip install mcp
```

3. Create a first MCP tool

```python
# servers/resources_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="resources-server")

@mcp.tool()
def get_asburd_poem() -> str:
    """
    Return content of the "Absurd Poem".
    """
    absurd_poem = """
The Moon Wore Socks Today

The moon wore socks today—
bright orange, with ducks that quack
whenever Jupiter sneezes.
A polite applause from passing meteors
echoed across the soup of night.
"""

    return absurd_poem

if __name__ == "__main__":
    mcp.run()
```

4. Configure [mcpo](https://github.com/open-webui/mcpo)

```dockerfile
# mcpo/dockerfile
FROM python:3.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir mcpo uv

WORKDIR /app

CMD ["mcpo", "--host", "0.0.0.0", "--port", "8000", "--config", "/app/config/config.json"]
```

```json
# mcpo/config.json
{
  "mcpServers": {
    "resources-server": {
      "command": "python",
      "args": ["/app/servers/resources_server.py"]
    }
  }
}
```

5. Create mcpo container

```yaml
services:
    # ...

    mcpo:
        build:
          context: ./mcpo
        container_name: mcpo
        ports:
          - "8000:8000"
        volumes:
          - ./mcpo/config.json:/app/config/config.json:ro
          - ./servers:/app/servers:ro
        restart: unless-stopped
```

6. Build docker and check the [MCP server health](http://localhost:8000/docs) 

7. Not all LLM model are compatible