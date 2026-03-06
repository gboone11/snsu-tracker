import os
import tempfile
import unittest
from database.connection import Database
from database.checklist_template_repository import ChecklistTemplateRepository
from database.checklist_item_repository import ChecklistItemRepository


class TestChecklistItemRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.template_repo = ChecklistTemplateRepository(self.db)
        self.repo = ChecklistItemRepository(self.db)
        self.template_id = self.template_repo.create("Sanitation", "Line Cleaning", 0)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_checklist_item(self):
        item_id = self.repo.create(self.template_id, 1, "Remove all product")
        self.assertIsNotNone(item_id)
        self.assertGreater(item_id, 0)

    def test_get_by_template(self):
        self.repo.create(self.template_id, 1, "Remove all product")
        self.repo.create(self.template_id, 2, "Rinse with water")
        items = self.repo.get_by_template(self.template_id)
        self.assertEqual(len(items), 2)

    def test_get_by_id(self):
        item_id = self.repo.create(self.template_id, 1, "Remove all product")
        item = self.repo.get_by_id(item_id)
        self.assertIsNotNone(item)
        self.assertEqual(item["item_text"], "Remove all product")

    def test_update_item(self):
        item_id = self.repo.create(self.template_id, 1, "Remove all product")
        success = self.repo.update(item_id, {"item_text": "Remove all materials"})
        self.assertTrue(success)
        item = self.repo.get_by_id(item_id)
        self.assertEqual(item["item_text"], "Remove all materials")

    def test_delete_item(self):
        item_id = self.repo.create(self.template_id, 1, "Remove all product")
        success = self.repo.delete(item_id)
        self.assertTrue(success)
        item = self.repo.get_by_id(item_id)
        self.assertIsNone(item)


if __name__ == '__main__':
    unittest.main()
