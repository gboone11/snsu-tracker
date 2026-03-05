import os
import tempfile
import unittest
from database.connection import Database
from database.line_group_repository import LineGroupRepository
from database.line_repository import LineRepository


class TestLineRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.group_repo = LineGroupRepository(self.db)
        self.repo = LineRepository(self.db)
        self.group_id = self.group_repo.create("24/7", "Test group", "06:00")

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_line(self):
        line_id = self.repo.create("Line 1", self.group_id)
        self.assertIsNotNone(line_id)
        self.assertGreater(line_id, 0)

    def test_get_all_lines(self):
        self.repo.create("Line 1", self.group_id)
        self.repo.create("Line 2", self.group_id)
        lines = self.repo.get_all()
        self.assertEqual(len(lines), 2)

    def test_get_by_id(self):
        line_id = self.repo.create("Line 1", self.group_id)
        line = self.repo.get_by_id(line_id)
        self.assertIsNotNone(line)
        self.assertEqual(line["line_number"], "Line 1")

    def test_update_line(self):
        line_id = self.repo.create("Line 1", self.group_id)
        success = self.repo.update(line_id, {"line_number": "Line 1A"})
        self.assertTrue(success)
        line = self.repo.get_by_id(line_id)
        self.assertEqual(line["line_number"], "Line 1A")

    def test_delete_line(self):
        line_id = self.repo.create("Line 1", self.group_id)
        success = self.repo.delete(line_id)
        self.assertTrue(success)
        line = self.repo.get_by_id(line_id)
        self.assertIsNone(line)


if __name__ == '__main__':
    unittest.main()
