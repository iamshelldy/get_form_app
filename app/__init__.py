import logging
from urllib.parse import parse_qsl

from fastapi import FastAPI, Request

from .database import check_db_is_empty, init_db, search_template
from .database.utils import parse_sample_data
from .models import FieldTypeDetector


logger = logging.getLogger("uvicorn")

app = FastAPI()


@app.on_event("startup")
async def startup_db():
    logger.info("Starting the database check.")
    # If collection is empty, initialize database.
    if await check_db_is_empty():
        logger.info("Database is empty. Initializing database.")
        data = parse_sample_data()
        await init_db(data)
        logger.info("Database initialized.")
    else:
        logger.info("Database is already initialized.")


@app.post("/get_form")
async def get_form(request: Request):
    content_type = request.headers.get("Content-Type", "application/x-www-form-urlencoded").lower()

    if "application/json" in content_type:
        body = await request.json()
    elif "application/x-www-form-urlencoded" in content_type:
        raw_data = await request.body()
        raw_str = raw_data.decode("utf-8")

        # Replace spaces to restore them.
        raw_str = raw_str.replace(" ", "%20")
        # Replace pluses to restore them.
        raw_str = raw_str.replace("+", "%2B")

        # Parse string.
        parsed_data = parse_qsl(raw_str)
        body = dict(parsed_data)
    else:
        return {"error": "Unsupported Content-Type"}

    detector = FieldTypeDetector(fields=body)
    form_fields = detector.fields

    found_forms = await search_template(form_fields)
    # According to the task, need to find "имя наиболее подходящей
    # данному списку полей формы". The problem is that if there are
    # several templates with the same structure in the database, the
    # every template in list is matching. So return the first element.:)
    if found_forms:
        return found_forms[0]

    return form_fields

