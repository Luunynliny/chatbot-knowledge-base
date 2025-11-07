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