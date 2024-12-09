import json
import logging


logger = logging.getLogger("uvicorn")


def parse_sample_data(file: str = "app/database/sample_data.json") -> list[dict[str, str]]:
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File {file} not found. Please create it first.")
        exit(1)
    except (OSError, json.decoder.JSONDecodeError) as e:
        logger.error(f"Error parsing sample data: {e}")

        return []

