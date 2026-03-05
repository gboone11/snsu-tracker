import os
import tempfile
import unittest
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api import app, db
from api_routers.user_api import user_repo


class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        db.db_path = self.temp_db.name
        user_repo.db.db_path = self.temp_db.name
        db._init_db()

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_and_get_users(self):
        self.client.post("/users", json={
            "username": "jdoe",
            "full_name": "John Doe",
            "initials": "JD",
            "team_name": "Operations"
        })
        
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)

    def test_get_user_by_id(self):
        create_response = self.client.post("/users", json={
            "username": "jdoe",
            "full_name": "John Doe",
            "initials": "JD",
            "team_name": "Operations"
        })
        user_id = create_response.json()["data"]["user_id"]
        
        response = self.client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["username"], "jdoe")

    def test_update_user(self):
        create_response = self.client.post("/users", json={
            "username": "jdoe",
            "full_name": "John Doe",
            "initials": "JD",
            "team_name": "Operations"
        })
        user_id = create_response.json()["data"]["user_id"]
        
        response = self.client.put(f"/users/{user_id}", json={
            "full_name": "Jane Doe",
            "initials": "JD2"
        })
        self.assertEqual(response.status_code, 200)
        
        get_response = self.client.get(f"/users/{user_id}")
        self.assertEqual(get_response.json()["data"]["full_name"], "Jane Doe")

    def test_delete_user(self):
        create_response = self.client.post("/users", json={
            "username": "jdoe",
            "full_name": "John Doe",
            "initials": "JD",
            "team_name": "Operations"
        })
        user_id = create_response.json()["data"]["user_id"]
        
        response = self.client.delete(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        
        get_response = self.client.get(f"/users/{user_id}")
        self.assertEqual(get_response.status_code, 404)

    def test_deactivate_user(self):
        create_response = self.client.post("/users", json={
            "username": "jdoe",
            "full_name": "John Doe",
            "initials": "JD",
            "team_name": "Operations"
        })

        user_id = create_response.json()["data"]["user_id"]
        
        response = self.client.post(f"/users/{user_id}/deactivate")
        self.assertEqual(response.status_code, 200)
        
        get_response = self.client.get(f"/users")
        self.assertEqual(len(get_response.json()["data"]), 0)


if __name__ == '__main__':
    unittest.main()
