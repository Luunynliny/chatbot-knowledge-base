## Requirements
- MacOS
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Instructions

### Install an LLM model using DMR

1. Setup [Docker](https://docs.docker.com/engine/install/)

2. Enable [Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#docker-desktop)

3. Pull `mistral:latest` model (Docker desktop)

4. Run the model (Docker desktop)

### Setup OpenWebUI

1. Create a `docker-compose.yaml`

```yaml
# docker-compose.yaml
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
        model: ai/mistral

volumes:
  open-webui:
```

2. Build `docker compose up`

3. Access OpenWebUI at http://localhost:3000/

4. Pull `smollm2:latest` model (Docker desktop)

5. Update the configuration

```yaml
# docker-compose.yaml
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

# ...
```

### MCP

#### First server

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

# ...
```

6. Build docker and check the [MCP server health](http://localhost:8000/docs)

7. In Open WebUI `Settings > External Tools > Manage Tool Servers`, add a connection to `http://localhost:8000/resources-server`

8. Test MCP with `mistral` and `smollm2`: not all LLM model are compatible

#### Connect to a MongoDB

1. Add a new server

```python
# servers/financial_server.py
from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mcp = FastMCP(name="financials-server")

MONGO_URL = f"mongodb://{os.environ['MONGODB_USER']}:{os.environ['MONGODB_PWD']}@mongodb:27017/?authSource=admin"

@mcp.tool()
def sum_expenses_for_a_category(
    category: str
) -> float | None:
    """
    Query the MongoDB 'financials.expenses' collection and return the total amount
    spent for the given expense category.

    Use this tool whenever the user asks things like:
    - "How much did I spend for Marketing in total?"
    - "What is the total I spent on Travel?"
    - "Sum of all Office expenses"

    Returns:
        The total sum of 'amount' for all expenses in the given category,
        or None if the category does not exist or no matching expenses are found.
    """

    client = MongoClient(MONGO_URL)
    db = client["financials"]

    pipeline = [
        { "$match": { "category": category } },
        {
            "$group": {
                "_id": None,
                "total": { "$sum": "$amount" }
            }
        }
    ]

    result = list(db["expenses"].aggregate(pipeline))

    if not result:
        return None

    return float(result[0]["total"])

if __name__ == "__main__":
    mcp.run()
```

2. Update `mcpo` dockerfile packages

```dockerfile
# mcpo/dockerfile
#...

RUN pip install --no-cache-dir mcpo uv pymongo dotenv mcp

# ...
```

3. Add database credentials

```yaml
# servers/.env
MONGODB_USER=user
MONGODB_PWD=root
```

4. Provide data

```javascript
// mongo-init.js
db = db.getSiblingDB('financials');
db.createCollection('expenses');

db.expenses.insertMany([
    { date: new Date("2024-01-01"), category: "Office", amount: 45.90 },
    { date: new Date("2024-01-02"), category: "Travel", amount: 120.00 },
    { date: new Date("2024-01-03"), category: "Meals", amount: 18.50 },
    { date: new Date("2024-01-04"), category: "Software", amount: 29.99 },
    { date: new Date("2024-01-05"), category: "Office", amount: 67.20 },
    { date: new Date("2024-01-06"), category: "Marketing", amount: 200.00 },
    { date: new Date("2024-01-07"), category: "Travel", amount: 89.00 },
    { date: new Date("2024-01-08"), category: "Meals", amount: 22.10 },
    { date: new Date("2024-01-09"), category: "Software", amount: 14.00 },
    { date: new Date("2024-01-10"), category: "Office", amount: 34.50 },
    { date: new Date("2024-01-11"), category: "Travel", amount: 155.40 },
    { date: new Date("2024-01-12"), category: "Meals", amount: 16.00 },
    { date: new Date("2024-01-13"), category: "Marketing", amount: 120.00 },
    { date: new Date("2024-01-14"), category: "Office", amount: 53.70 },
    { date: new Date("2024-01-15"), category: "Software", amount: 39.99 },
    { date: new Date("2024-01-16"), category: "Travel", amount: 210.00 },
    { date: new Date("2024-01-17"), category: "Meals", amount: 12.80 },
    { date: new Date("2024-01-18"), category: "Office", amount: 27.90 },
    { date: new Date("2024-01-19"), category: "Travel", amount: 98.00 },
    { date: new Date("2024-01-20"), category: "Marketing", amount: 300.00 }
]);

print("Dummy expenses inserted.");
```

5. Create the database container

```yaml
services:
    # ...

    mongodb:
        image: mongodb/mongodb-community-server:latest
        container_name: mongodb
        ports:
            - "27017:27017"
        volumes:
            - mongodb:/data/db
            - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
        environment:
            MONGO_INITDB_ROOT_USERNAME: ${MONGODB_USER}
            MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_PWD}

volumes:
  # ...
  mongodb:
```

6. Rebuild docker

7. In Open WebUI, add a connection to `http://localhost:8000/financials-server`

#### Connect to an API

1. Add API URL in `.env`

```yaml
# servers/.env
#...

TIME_API_URL=https://timeapi.io/api/time/current/zone?timeZone=Europe%2FParis
```

2. Add a new `get_current_datetime` tool to the `resources_server`

```python
# servers/resources_server.py
import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

# ...

@mcp.tool()
def get_current_datetime() -> str:
    """
    Returns the current datetime

    Use this tool whenever the user asks things like:
    - "What date is it today?"
    - "What day are we?"
    - "What is the current time?"

    Returns:
        The current datetime.
    """
    response = requests.get(os.getenv("TIME_API_URL"))

    if response.status_code == 200:
        data = json.loads(response.text)
        return json.dumps(data, indent=4)
    else:
        print("Failed to fetch data from the API")

# Must be included before the "main"
# ...
```

3. Update `mcpo` dockerfile packages

```dockerfile
# mcpo/dockerfile
#...

RUN pip install --no-cache-dir mcpo uv pymongo dotenv mcp requests

# ...
```

4. Rebuild docker