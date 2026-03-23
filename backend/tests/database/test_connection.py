import os
import sqlite3
import tempfile
import unittest
from database.connection import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_init_db_creates_all_tables(self):
        expected_tables = [
            'lines', 'process_steps', 'runs', 'step_executions',
            'checklist_templates', 'checklist_items', 'checklist_completions',
            'communication_notes'
        ]
        
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = [row[0] for row in cursor.fetchall()]
        
        for table in expected_tables:
            self.assertIn(table, tables)

    def test_init_db_creates_indexes(self):
        expected_indexes = [
            'idx_steps_order', 'idx_runs_line',
            'idx_executions_run', 'idx_notes_line', 'idx_checklist_template'
        ]
        
        with self.db.get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'"
            )
            indexes = [row[0] for row in cursor.fetchall()]
        
        for index in expected_indexes:
            self.assertIn(index, indexes)

    def test_clear_data_removes_all_records(self):
        with self.db.get_connection() as conn:
            conn.execute("INSERT INTO lines (line_number) VALUES ('Line 1')")
        
        self.db.clear_data()
        
        with self.db.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM lines")
            self.assertEqual(cursor.fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
