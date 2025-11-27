import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

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

if __name__ == "__main__":
    mcp.run()
