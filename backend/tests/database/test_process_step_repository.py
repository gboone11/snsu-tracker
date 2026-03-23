import os
import tempfile
import unittest
from database.connection import Database
from database.process_step_repository import ProcessStepRepository


class TestProcessStepRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.repo = ProcessStepRepository(self.db)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_process_step(self):
        step_id = self.repo.create(1, "Sanitation", "Clean line", 30)
        self.assertIsNotNone(step_id)
        self.assertGreater(step_id, 0)

    def test_get_all(self):
        self.repo.create(1, "Sanitation", "Clean line", 30)
        self.repo.create(2, "Operations", "Start line", 15)
        steps = self.repo.get_all()
        self.assertEqual(len(steps), 2)

    def test_get_by_id(self):
        step_id = self.repo.create(1, "Sanitation", "Clean line", 30)
        step = self.repo.get_by_id(step_id)
        assert step is not None
        self.assertEqual(step["task_name"], "Clean line")

    def test_update_process_step(self):
        step_id = self.repo.create(1, "Sanitation", "Clean line", 30)
        success = self.repo.update(step_id, {"avg_duration_minutes": 45})
        self.assertTrue(success)
        step = self.repo.get_by_id(step_id)
        assert step is not None
        self.assertEqual(step["avg_duration_minutes"], 45)

    def test_delete_process_step(self):
        step_id = self.repo.create(1, "Sanitation", "Clean line", 30)
        success = self.repo.delete(step_id)
        self.assertTrue(success)
        step = self.repo.get_by_id(step_id)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
