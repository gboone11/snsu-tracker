import os
import tempfile
import unittest
from database.connection import Database
from database.checklist_template_repository import ChecklistTemplateRepository


class TestChecklistTemplateRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.repo = ChecklistTemplateRepository(self.db)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_checklist_template(self):
        template_id = self.repo.create("Sanitation", "Line Cleaning", 0)
        self.assertIsNotNone(template_id)
        self.assertGreater(template_id, 0)

    def test_get_all_templates(self):
        self.repo.create("Sanitation", "Line Cleaning", 0)
        self.repo.create("Operations", "Startup", 0)
        templates = self.repo.get_all()
        self.assertEqual(len(templates), 2)

    def test_get_by_id(self):
        template_id = self.repo.create("Sanitation", "Line Cleaning", 0)
        template = self.repo.get_by_id(template_id)
        self.assertIsNotNone(template)
        self.assertEqual(template["task_name"], "Line Cleaning")

    def test_update_template(self):
        template_id = self.repo.create("Sanitation", "Line Cleaning", 0)
        success = self.repo.update(template_id, {"task_name": "Deep Cleaning"})
        self.assertTrue(success)
        template = self.repo.get_by_id(template_id)
        self.assertEqual(template["task_name"], "Deep Cleaning")

    def test_delete_template(self):
        template_id = self.repo.create("Sanitation", "Line Cleaning", 0)
        success = self.repo.delete(template_id)
        self.assertTrue(success)
        template = self.repo.get_by_id(template_id)
        self.assertIsNone(template)


if __name__ == '__main__':
    unittest.main()
