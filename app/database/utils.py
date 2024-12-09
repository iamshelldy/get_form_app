import json


def parse_sample_data(file: str = "app/database/sample_data.json") -> list[dict[str, str]]:
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (OSError, json.decoder.JSONDecodeError):
        return []

