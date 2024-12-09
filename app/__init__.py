from fastapi import FastAPI, Request

from .models import FieldTypeDetector
from .database.utils import parse_sample_data


app = FastAPI()

data = parse_sample_data()


@app.post("/get_form")
async def get_form(request: Request):
    body = await request.json()

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

