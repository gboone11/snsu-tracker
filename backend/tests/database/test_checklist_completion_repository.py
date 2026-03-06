import os
import tempfile
import unittest
from database.connection import Database
from database.line_group_repository import LineGroupRepository
from database.line_repository import LineRepository
from database.run_repository import RunRepository
from database.process_step_repository import ProcessStepRepository
from database.step_execution_repository import StepExecutionRepository
from database.checklist_template_repository import ChecklistTemplateRepository
from database.checklist_item_repository import ChecklistItemRepository
from database.checklist_completion_repository import ChecklistCompletionRepository


class TestChecklistCompletionRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        
        group_repo = LineGroupRepository(self.db)
        line_repo = LineRepository(self.db)
        run_repo = RunRepository(self.db)
        step_repo = ProcessStepRepository(self.db)
        execution_repo = StepExecutionRepository(self.db)
        template_repo = ChecklistTemplateRepository(self.db)
        item_repo = ChecklistItemRepository(self.db)
        self.repo = ChecklistCompletionRepository(self.db)
        
        group_id = group_repo.create("24/7", "Test", "06:00")
        line_id = line_repo.create("Line 1", group_id)
        run_id = run_repo.create(line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")
        step_id = step_repo.create(group_id, 1, "Sanitation", "Clean", 30)
        self.execution_id = execution_repo.create(run_id, step_id, "not-started")
        template_id = template_repo.create("Sanitation", "Cleaning", 0)
        self.item_id = item_repo.create(template_id, 1, "Remove product")

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_completion(self):
        completion_id = self.repo.create(self.execution_id, self.item_id)
        self.assertIsNotNone(completion_id)
        self.assertGreater(completion_id, 0)

    def test_get_by_execution(self):
        self.repo.create(self.execution_id, self.item_id)
        completions = self.repo.get_by_execution(self.execution_id)
        self.assertEqual(len(completions), 1)

    def test_get_by_id(self):
        completion_id = self.repo.create(self.execution_id, self.item_id)
        completion = self.repo.get_by_id(completion_id)
        self.assertIsNotNone(completion)
        self.assertEqual(completion["is_completed"], 0)

    def test_update_completion(self):
        completion_id = self.repo.create(self.execution_id, self.item_id)
        success = self.repo.update(completion_id, {"is_completed": 1, "completed_by": "jdoe"})
        self.assertTrue(success)
        completion = self.repo.get_by_id(completion_id)
        self.assertEqual(completion["is_completed"], 1)

    def test_delete_completion(self):
        completion_id = self.repo.create(self.execution_id, self.item_id)
        success = self.repo.delete(completion_id)
        self.assertTrue(success)
        completion = self.repo.get_by_id(completion_id)
        self.assertIsNone(completion)


if __name__ == '__main__':
    unittest.main()
