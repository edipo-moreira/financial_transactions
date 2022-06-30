import json
import unittest
import sys
import os
from fastapi.testclient import TestClient


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.api import app


class TestApi(unittest.TestCase):
    client = TestClient(app)
    data = {"username": "teste", "password": "teste"}

    def test_post_token(self):
        response = self.client.post("/token", data=json.dumps(self.data))
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(body.keys()), ["access_token", "token_type", "expires_in_minutes"]
        )

    def test_post_token_non_existent_username_or_password(self):
        data = {"username": "teste_", "password": "teste_"}
        response = self.client.post("/token", data=json.dumps(data))
        body = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(body, {"detail": "Incorrect username or password"})

    def test_post_token_non_existent_body(self):
        response = self.client.post("/token")
        body = response.json()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            body,
            {
                "detail": [
                    {
                        "loc": ["body"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        )

    def test_invalid_token(self):
        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer"

        response = self.client.get("/patients", headers=headers)
        body = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(body, {"detail": "Could not validate credentials"})

    def test_non_existent_authorization(self):
        headers = dict()
        headers["Content-Type"] = "application/json"

        response = self.client.get("/patients", headers=headers)
        body = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(body, {"detail": "Not authenticated"})

    def test_get_patients(self):
        response_token = self.client.post("/token", data=json.dumps(self.data))
        body_token = response_token.json()
        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {body_token.get('access_token')}"

        response = self.client.get("/patients", headers=headers)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(body[0].keys()), ["uuid", "first_name", "last_name", "date_of_birth"]
        )

    def test_get_pharmacies(self):
        response_token = self.client.post("/token", data=json.dumps(self.data))
        body_token = response_token.json()
        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {body_token.get('access_token')}"

        response = self.client.get("/pharmacies", headers=headers)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(body[0].keys()), ["uuid", "name", "city"])

    def test_get_transactions(self):
        response_token = self.client.post("/token", data=json.dumps(self.data))
        body_token = response_token.json()
        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {body_token.get('access_token')}"

        response = self.client.get("/transactions", headers=headers)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(body[0].keys()), ["patient", "pharmacy", "uuid", "amount", "timestamp"]
        )


if __name__ == "__name__":
    unittest.main()
