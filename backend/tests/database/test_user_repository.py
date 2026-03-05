import os
import tempfile
import unittest
from database.connection import Database
from database.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.repo = UserRepository(self.db)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_user(self):
        user_id = self.repo.create("jdoe", "John Doe", "JD", "Operations")
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0)

    def test_get_all_users(self):
        self.repo.create("jdoe", "John Doe", "JD", "Operations")
        self.repo.create("asmith", "Alice Smith", "AS", "Maintenance")
        users = self.repo.get_all()
        self.assertEqual(len(users), 2)

    def test_get_by_id(self):
        user_id = self.repo.create("jdoe", "John Doe", "JD", "Operations")
        user = self.repo.get_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "jdoe")

    def test_update_user(self):
        user_id = self.repo.create("jdoe", "John Doe", "JD", "Operations")
        success = self.repo.update(user_id, {"full_name": "Jane Doe"})
        self.assertTrue(success)
        user = self.repo.get_by_id(user_id)
        self.assertEqual(user["full_name"], "Jane Doe")

    def test_delete_user(self):
        user_id = self.repo.create("jdoe", "John Doe", "JD", "Operations")
        success = self.repo.delete(user_id)
        self.assertTrue(success)
        user = self.repo.get_by_id(user_id)
        self.assertIsNone(user)

    def test_deactivate_user(self):
        user_id = self.repo.create("jdoe", "John Doe", "JD", "Operations")
        success = self.repo.deactivate(user_id)
        self.assertTrue(success)
        users = self.repo.get_all()
        self.assertEqual(len(users), 0)


if __name__ == '__main__':
    unittest.main()
