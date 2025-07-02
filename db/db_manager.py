import sqlite3
from models.task import Task

class DatabaseManager:
    def __init__(self, db_path = "personal_planner.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row


    def initialize_database(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                priority TEXT,
                status TEXT DEFAULT 'in progress'
                 
                )
          """)
        self.conn.commit()


    def add_task(self, title, description, deadline = None, priority = 'medium'):
        self.conn.execute("""
            INSERT INTO tasks (title, description, deadline, priority)
            VALUES(?, ?, ?, ?)
        """, (title, description, deadline, priority))
        self.conn.commit()

    
    def get_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        
        rows = cursor.fetchall()
        print(f"TASKS IN DB: {len(rows)}") 
        return [Task(**row) for row in rows]
    

    def mark_task_done(self, task_id):
        self.conn.execute(
            "UPDATE tasks SET status = 'done' WHERE id = ?",
            (task_id,)
        )
        self.conn.commit()
        