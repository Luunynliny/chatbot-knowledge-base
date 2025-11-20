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