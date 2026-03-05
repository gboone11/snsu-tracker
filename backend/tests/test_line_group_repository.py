import os
import tempfile
import unittest
from database.connection import Database
from database.line_group_repository import LineGroupRepository


class TestLineGroupRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.repo = LineGroupRepository(self.db)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_line_group(self):
        group_id = self.repo.create("24/7", "24 hour 7 day operation", "06:00")
        self.assertIsNotNone(group_id)
        self.assertGreater(group_id, 0)

    def test_get_all_line_groups(self):
        self.repo.create("24/7", "24 hour 7 day operation", "06:00")
        self.repo.create("24/5", "24 hour 5 day operation", "06:00")
        groups = self.repo.get_all()
        self.assertEqual(len(groups), 2)

    def test_get_by_id(self):
        group_id = self.repo.create("24/7", "24 hour 7 day operation", "06:00")
        group = self.repo.get_by_id(group_id)
        self.assertIsNotNone(group)
        self.assertEqual(group["group_name"], "24/7")

    def test_update_line_group(self):
        group_id = self.repo.create("24/7", "24 hour 7 day operation", "06:00")
        success = self.repo.update(group_id, {"description": "Updated description"})
        self.assertTrue(success)
        group = self.repo.get_by_id(group_id)
        self.assertEqual(group["description"], "Updated description")

    def test_delete_line_group(self):
        group_id = self.repo.create("24/7", "24 hour 7 day operation", "06:00")
        success = self.repo.delete(group_id)
        self.assertTrue(success)
        group = self.repo.get_by_id(group_id)
        self.assertIsNone(group)


if __name__ == '__main__':
    unittest.main()
