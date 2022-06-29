import json
import types
import unittest
import sys
import os
from fastapi.testclient import TestClient


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app.api import app

class TestApi(unittest.TestCase):
    client = TestClient(app)

    def test_get_patients(self):
        data = {"username": "edipo3", "password": "123"}
        response = self.client.post("/token", data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

if __name__ == '__name__':
    unittest.main()