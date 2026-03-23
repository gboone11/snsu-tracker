import os
import tempfile
import unittest
from database.connection import Database
from database.line_repository import LineRepository
from database.run_repository import RunRepository
from database.communication_note_repository import CommunicationNoteRepository


class TestCommunicationNoteRepository(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)
        self.line_repo = LineRepository(self.db)
        self.run_repo = RunRepository(self.db)
        self.repo = CommunicationNoteRepository(self.db)
        
        self.line_id = self.line_repo.create("Line 1")
        self.run_id = self.run_repo.create(self.line_id, "2024-01-01 18:00", "2024-01-02 06:00", "active")

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_create_note(self):
        note_id = self.repo.create(self.line_id, "Line needs maintenance", "jdoe", self.run_id)
        self.assertIsNotNone(note_id)
        self.assertGreater(note_id, 0)

    def test_get_by_line(self):
        self.repo.create(self.line_id, "Note 1", "jdoe", self.run_id)
        self.repo.create(self.line_id, "Note 2", "asmith", None)
        notes = self.repo.get_by_line(self.line_id)
        self.assertEqual(len(notes), 2)

    def test_get_by_run(self):
        self.repo.create(self.line_id, "Note 1", "jdoe", self.run_id)
        self.repo.create(self.line_id, "Note 2", "asmith", None)
        notes = self.repo.get_by_run(self.run_id)
        self.assertEqual(len(notes), 1)

    def test_get_by_id(self):
        note_id = self.repo.create(self.line_id, "Line needs maintenance", "jdoe", self.run_id)
        note = self.repo.get_by_id(note_id)
        self.assertIsNotNone(note)
        self.assertEqual(note["note_text"], "Line needs maintenance")

    def test_update_note(self):
        note_id = self.repo.create(self.line_id, "Line needs maintenance", "jdoe", self.run_id)
        success = self.repo.update(note_id, {"note_text": "Line maintenance completed"})
        self.assertTrue(success)
        note = self.repo.get_by_id(note_id)
        self.assertEqual(note["note_text"], "Line maintenance completed")

    def test_delete_note(self):
        note_id = self.repo.create(self.line_id, "Line needs maintenance", "jdoe", self.run_id)
        success = self.repo.delete(note_id)
        self.assertTrue(success)
        note = self.repo.get_by_id(note_id)
        self.assertIsNone(note)


if __name__ == '__main__':
    unittest.main()
