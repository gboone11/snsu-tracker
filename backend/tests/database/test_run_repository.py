import os
import tempfile
import unittest
from database.connection import Database
from database.line_group_repository import LineGroupRepository
from database.line_repository import LineRepository
from database.run_repository import RunRepository


class TestRunRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.group_repo = LineGroupRepository(self.db)
        self.line_repo = LineRepository(self.db)
        self.repo = RunRepository(self.db)
        group_id = self.group_repo.create("24/7", "Test group", "06:00")
        self.line_id = self.line_repo.create("Line 1", group_id)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_run(self):
        run_id = self.repo.create(self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")
        self.assertIsNotNone(run_id)
        self.assertGreater(run_id, 0)

    def test_get_active_runs(self):
        self.repo.create(self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")
        self.repo.create(self.line_id, "2024-01-02 18:00", "2024-01-03 06:00", "completed")
        runs = self.repo.get_active()
        self.assertEqual(len(runs), 1)

    def test_get_by_id(self):
        run_id = self.repo.create(self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")
        run = self.repo.get_by_id(run_id)
        self.assertIsNotNone(run)
        self.assertEqual(run["status"], "active")

    def test_update_run(self):
        run_id = self.repo.create(self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")
        success = self.repo.update(run_id, {"status": "completed"})
        self.assertTrue(success)
        run = self.repo.get_by_id(run_id)
        self.assertEqual(run["status"], "completed")

    def test_delete_run(self):
        run_id = self.repo.create(self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")
        success = self.repo.delete(run_id)
        self.assertTrue(success)
        run = self.repo.get_by_id(run_id)
        self.assertIsNone(run)


if __name__ == '__main__':
    unittest.main()
