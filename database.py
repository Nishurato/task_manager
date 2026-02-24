import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("tasks.db")
        self.create_table()

    def create_table(self):
        self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
        """
        )
        self.conn.commit()

    def add_task(self, title):
        self.conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    # Update one task status immediately.
    def toggle_task(self, task_id, done):
        self.conn.execute("UPDATE tasks SET done=? WHERE id=?", (done, task_id))
        self.conn.commit()

    # Batch-update task statuses with a single commit to reduce UI lag.
    def toggle_tasks_batch(self, updates):
        self.conn.executemany(
            "UPDATE tasks SET done=? WHERE id=?",
            [(done, task_id) for task_id, done in updates],
        )
        self.conn.commit()

    def get_tasks(self):
        return self.conn.execute("SELECT * FROM tasks").fetchall()
