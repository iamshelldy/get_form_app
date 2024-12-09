from unittest import TestCase

import requests


class Test(TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/get_form"
        self.existing_form_query_json = {"email": "test@example.com", "phone": "+7 123 456 78 90"}
        self.existing_form_query_string = "email=test@example.com&phone=+7 123 456 78 90"
        self.existing_form_response = "Contacts Form"
        self.non_existing_form_query_json = {"email_field": "test@example.com", "phone": "+7 123 456 78 90"}
        self.non_existing_form_query_string = "email_field=test@example.com&phone=%2B7 123 456 78 90"
        self.non_existing_form_response = {"email_field": "email", "phone": "phone"}

    def test_get_existing_form_by_json(self):
        """Test for existing form sent in json format"""
        request = requests.post(self.base_url, json=self.existing_form_query_json)

        response = request.json()

        self.assertEqual(request.status_code, 200, "Expected status code 200")
        self.assertEqual(response, self.existing_form_response,
                         "The response should match the expected name of form.")

    def test_get_non_existing_form_by_json(self):
        """Test for non-existing form sent in json format"""
        request = requests.post(self.base_url, json=self.non_existing_form_query_json)

        response = request.json()

        self.assertEqual(request.status_code, 200, "Expected status code 200")
        self.assertEqual(response, self.non_existing_form_response,
                         "The response should match the expected types of fields.")

    def test_get_existing_form_by_string(self):
        """Test for existing form sent in query string format"""
        request = requests.post(
            self.base_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=self.existing_form_query_string
        )

        response = request.json()

        self.assertEqual(request.status_code, 200, "Expected status code 200")
        self.assertEqual(response, self.existing_form_response,
                         "The response should match the expected name of form.")

    def test_get_non_existing_form_by_string(self):
        """Test for non-existing form sent in query string format"""
        request = requests.post(
            self.base_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=self.non_existing_form_query_string
        )

        response = request.json()

        self.assertEqual(request.status_code, 200, "Expected status code 200")
        self.assertEqual(response, self.non_existing_form_response,
                         "The response should match the expected types of fields.")

