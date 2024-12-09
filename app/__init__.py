import urllib

from fastapi import FastAPI, Request

from .models import FieldTypeDetector
from .database.utils import parse_sample_data


app = FastAPI()

data = parse_sample_data()


@app.post("/get_form")
async def get_form(request: Request):
    content_type = request.headers.get("Content-Type", "application/x-www-form-urlencoded").lower()

    if "application/json" in content_type:
        body = await request.json()
    elif "application/x-www-form-urlencoded" in content_type:
        raw_data = await request.body()
        raw_str = raw_data.decode('utf-8')

        # Replace spaces to restore them.
        raw_str = raw_str.replace(' ', '%20')
        # Replace pluses to restore them.
        raw_str = raw_str.replace('+', '%2B')

        # Parse string.
        parsed_data = urllib.parse.parse_qsl(raw_str)
        body = dict(parsed_data)
    else:
        return {"error": "Unsupported Content-Type"}

    detector = FieldTypeDetector(fields=body)
    form_fields = detector.fields

    for item in data:
        item_fields = {key: value for key, value in item.items() if key != "name"}

        if len(form_fields) != len(item_fields):
            continue

        for key, field_type in form_fields.items():
            if key not in item_fields:
                break
            if item_fields[key] != field_type:
                break
        else:
            return item.get("name", "Unknown Name")

    return form_fields

