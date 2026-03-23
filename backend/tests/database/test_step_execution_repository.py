import os
import tempfile
import unittest
from database.connection import Database
from database.line_repository import LineRepository
from database.run_repository import RunRepository
from database.process_step_repository import ProcessStepRepository
from database.step_execution_repository import StepExecutionRepository


class TestStepExecutionRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.line_repo = LineRepository(self.db)
        self.run_repo = RunRepository(self.db)
        self.step_repo = ProcessStepRepository(self.db)
        self.repo = StepExecutionRepository(self.db)

        self.line_id = self.line_repo.create(1)
        self.run_id = self.run_repo.create(
            self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active"
        )
        self.step_id = self.step_repo.create(1, "Sanitation", "Clean", 30)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_step_execution(self):
        execution_id = self.repo.create(self.run_id, self.step_id, "not-started")
        self.assertIsNotNone(execution_id)
        self.assertGreater(execution_id, 0)

    def test_get_by_run(self):
        self.repo.create(self.run_id, self.step_id, "not-started")
        executions = self.repo.get_by_run(self.run_id)
        self.assertEqual(len(executions), 1)

    def test_get_by_id(self):
        execution_id = self.repo.create(self.run_id, self.step_id, "not-started")
        execution = self.repo.get_by_id(execution_id)
        assert execution is not None
        self.assertEqual(execution["status"], "not-started")

    def test_update_step_execution(self):
        execution_id = self.repo.create(self.run_id, self.step_id, "not-started")
        success = self.repo.update(execution_id, {"status": "completed"})
        self.assertTrue(success)
        execution = self.repo.get_by_id(execution_id)
        assert execution is not None
        self.assertEqual(execution["status"], "completed")

    def test_delete_step_execution(self):
        execution_id = self.repo.create(self.run_id, self.step_id, "not-started")
        success = self.repo.delete(execution_id)
        self.assertTrue(success)
        execution = self.repo.get_by_id(execution_id)
        self.assertIsNone(execution)


if __name__ == "__main__":
    unittest.main()
