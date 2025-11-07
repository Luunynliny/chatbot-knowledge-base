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

Meanwhile,
a toaster fell in love with a cloud,
and every morning it burnt the bread
just to see her rain again.

A philosopher pigeon
debated a lamppost about the meaning of “glow,”
while three confused violins
played jazz to the rhythm of an empty mailbox.

Somewhere,
a cactus bought a mirror
and started a self-help podcast.

And me?
I waved at the universe,
hoping it might wave back
with a handful of freshly laundered stars.
"""

    return absurd_poem.strip()

if __name__ == "__main__":
    mcp.run()