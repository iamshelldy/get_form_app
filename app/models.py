from pydantic import BaseModel, field_validator, validate_email
import re
from datetime import datetime


class FieldTypeDetector(BaseModel):
    """
    Class for detecting types of the fields passed in forms.

    Attributes:
        fields (dict[str, str]): Dictionary of field names and their values.
    """
    fields: dict[str, str]

    @field_validator("fields", mode="before")
    def detect_field_type(cls, value):
        """
        Method to detect type of each field in a dictionary.
        Checks every field in a dictionary to match one of the following types:
        - email
        - phone
        - date
        - text

        :param value: A dictionary with form fields, where keys
                      are field names and values are their data.
        :return: A dictionary with field names as keys and their types as values.
        """
        result = {}
        for field_name, field_value in value.items():
            if cls.is_email(field_value):
                result[field_name] = "email"
            elif cls.is_phone(field_value):
                result[field_name] = "phone"
            elif cls.is_date(field_value):
                result[field_name] = "date"
            else:
                result[field_name] = "text"
        return result

    @staticmethod
    def is_email(value: str) -> bool:
        """
        Checks if the value is a valid email address.

        :param value: Value to be checked.
        :return: True if the value is a valid email address and False otherwise.
        """
        try:
            validate_email(value)  # Using Pydantic email validation.
            return True
        except ValueError:
            return False

    @staticmethod
    def is_phone(value: str) -> bool:
        """
        Checks if the value is a valid phone number.

        :param value: Value to be checked.
        :return: True if the value is a valid number and False otherwise.
        """
        phone_pattern = r"^\+\d{1,3}\s\d{3}\s\d{3}\s\d{2}\s\d{2}$"
        return bool(re.match(phone_pattern, value))

    @staticmethod
    def is_date(value: str) -> bool:
        """
        Checks if the value is a valid date.
        Supported formats: DD.MM.YYYY and YYYY-MM-DD.

        :param value: Value to be checked.
        :return: True if the value is a valid date and False otherwise.
        """
        for date_format in ("%d.%m.%Y", "%Y-%m-%d"):
            try:
                datetime.strptime(value, date_format)
                return True
            except ValueError:
                continue
        return False

