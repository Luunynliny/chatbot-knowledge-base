## Requirements
- MacOS
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/)

## Instructions

### Install an LLM model using DMR

1. Setup [Docker](https://docs.docker.com/engine/install/)

2. Enable [Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#docker-desktop)

3. Pull `granite-4.0-nano:latest` model

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
    - docker-model-runner-granite

  docker-model-runner-granite:
    provider:
      type: model
      options:
        model: ai/granite-4.0-nano

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
            - docker-model-runner-granite
            - docker-model-runner-smoll

    # ...
    docker-model-runner-smoll:
        provider:
        type: model
        options:
            model: ai/smollm2
    # ...
```