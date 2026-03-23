import os
import tempfile
import unittest
from database.connection import Database
from database.line_repository import LineRepository


class TestLineRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.repo = LineRepository(self.db)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_line(self):
        line_id = self.repo.create(1)
        self.assertIsNotNone(line_id)
        self.assertGreater(line_id, 0)

    def test_get_all_lines(self):
        self.repo.create(1)
        self.repo.create(2)
        lines = self.repo.get_all()
        self.assertEqual(len(lines), 2)

    def test_get_by_id(self):
        line_id = self.repo.create(1)
        line = self.repo.get_by_id(line_id)
        assert line is not None
        self.assertEqual(line["line_number"], 1)

    def test_update_line(self):
        line_id = self.repo.create(1)
        success = self.repo.update(line_id, {"line_number": 10})
        self.assertTrue(success)
        line = self.repo.get_by_id(line_id)
        assert line is not None
        self.assertEqual(line["line_number"], 10)

    def test_delete_line(self):
        line_id = self.repo.create(1)
        success = self.repo.delete(line_id)
        self.assertTrue(success)
        line = self.repo.get_by_id(line_id)
        self.assertIsNone(line)


if __name__ == "__main__":
    unittest.main()
