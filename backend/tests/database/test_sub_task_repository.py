import os
import tempfile
import unittest
from database.connection import Database
from database.line_repository import LineRepository
from database.run_repository import RunRepository
from database.process_step_repository import ProcessStepRepository
from database.step_execution_repository import StepExecutionRepository
from database.sub_task_repository import SubTaskRepository


class TestSubTaskRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.line_repo = LineRepository(self.db)
        self.run_repo = RunRepository(self.db)
        self.step_repo = ProcessStepRepository(self.db)
        self.exec_repo = StepExecutionRepository(self.db)
        self.repo = SubTaskRepository(self.db)

        self.line_id = self.line_repo.create(1)
        self.run_id = self.run_repo.create(
            self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active"
        )
        self.step_id = self.step_repo.create(1, "Sanitation", "Clean", 30)
        self.execution_id = self.exec_repo.create(
            self.run_id, self.step_id, "in_progress"
        )

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create(self):
        sub_task_id = self.repo.create(self.execution_id, "Rinse tanks", 1)
        self.assertIsNotNone(sub_task_id)
        self.assertGreater(sub_task_id, 0)

    def test_get_by_execution(self):
        self.repo.create(self.execution_id, "Rinse tanks", 1)
        self.repo.create(self.execution_id, "Sanitize lines", 2)
        sub_tasks = self.repo.get_by_execution(self.execution_id)
        self.assertEqual(len(sub_tasks), 2)
        self.assertEqual(sub_tasks[0]["sub_task_name"], "Rinse tanks")
        self.assertEqual(sub_tasks[1]["sub_task_name"], "Sanitize lines")

    def test_get_by_execution_ordering(self):
        self.repo.create(self.execution_id, "Second", 2)
        self.repo.create(self.execution_id, "First", 1)
        sub_tasks = self.repo.get_by_execution(self.execution_id)
        self.assertEqual(sub_tasks[0]["sub_task_name"], "First")
        self.assertEqual(sub_tasks[1]["sub_task_name"], "Second")

    def test_get_by_execution_empty(self):
        sub_tasks = self.repo.get_by_execution(self.execution_id)
        self.assertEqual(sub_tasks, [])

    def test_get_by_execution_isolation(self):
        step_id_2 = self.step_repo.create(2, "Ops", "Startup", 20)
        exec_id_2 = self.exec_repo.create(self.run_id, step_id_2, "in_progress")
        self.repo.create(self.execution_id, "Task A", 1)
        self.repo.create(exec_id_2, "Task B", 1)
        self.assertEqual(len(self.repo.get_by_execution(self.execution_id)), 1)
        self.assertEqual(len(self.repo.get_by_execution(exec_id_2)), 1)

    def test_update_name(self):
        sub_task_id = self.repo.create(self.execution_id, "Old name", 1)
        success = self.repo.update(sub_task_id, {"sub_task_name": "New name"})
        self.assertTrue(success)
        sub_tasks = self.repo.get_by_execution(self.execution_id)
        self.assertEqual(sub_tasks[0]["sub_task_name"], "New name")

    def test_update_completed(self):
        sub_task_id = self.repo.create(self.execution_id, "Check valves", 1)
        success = self.repo.update(
            sub_task_id,
            {
                "is_completed": 1,
                "completed_by": "JD",
                "completed_at": "2024-01-01T20:00:00",
            },
        )
        self.assertTrue(success)
        sub_tasks = self.repo.get_by_execution(self.execution_id)
        self.assertEqual(sub_tasks[0]["is_completed"], 1)
        self.assertEqual(sub_tasks[0]["completed_by"], "JD")

    def test_update_empty_returns_false(self):
        sub_task_id = self.repo.create(self.execution_id, "Task", 1)
        self.assertFalse(self.repo.update(sub_task_id, {}))

    def test_update_nonexistent_returns_false(self):
        self.assertFalse(self.repo.update(9999, {"sub_task_name": "X"}))

    def test_delete(self):
        sub_task_id = self.repo.create(self.execution_id, "Remove me", 1)
        success = self.repo.delete(sub_task_id)
        self.assertTrue(success)
        self.assertEqual(self.repo.get_by_execution(self.execution_id), [])

    def test_delete_nonexistent_returns_false(self):
        self.assertFalse(self.repo.delete(9999))


if __name__ == "__main__":
    unittest.main()
