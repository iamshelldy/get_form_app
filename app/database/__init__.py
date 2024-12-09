import os

from motor.motor_asyncio import AsyncIOMotorClient

from .utils import parse_sample_data

MONGO_URI = os.getenv("MONGO_URI", "localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["form_templates"]
collection = db["templates"]


async def check_db_is_empty() -> bool:
    return not await collection.find_one()


async def init_db(data) -> None:
    await collection.drop()
    await collection.create_index("name")

    await collection.insert_many(data)


async def search_template(form_fields: dict[str, str]) -> list[str]:
    """
    Function to find a form template in a MongoDB database.
    We search for a document that has all the fields passed and
    their types, and return only the template names.
    """
    query = {}

    for field, field_type in form_fields.items():
        query[field] = field_type  # E.g. {"email": "email"}

    # Search for templates that match the request. Also remove id from results.
    result = await collection.find(query, {"_id": 0}).to_list()

    filtered_result = [
        item.get("name", "Unknown Name")
        for item in result
        if len(item) == len(form_fields) + 1  # +1 because name was excluded.
    ]

    return filtered_result
