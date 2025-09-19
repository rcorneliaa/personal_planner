import sqlite3
from models.task import Task
from models.vacation import Vacation

class DatabaseManager:
    def __init__(self, db_path = "personal_planner.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
       

    def initialize_database(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'in progress'
                 
                )
          """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vacations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
                 
                )
          """)
        self.conn.commit()

    def add_task(self, title, deadline = None):
        self.conn.execute("""
            INSERT INTO tasks (title, date)
            VALUES(?, ?)
        """, (title, deadline))
        self.conn.commit()

    
    def get_tasks_by_date(self, date):
        cursor = self.conn.cursor()
        if date:
          cursor.execute("SELECT * FROM tasks WHERE date = ?", (date,))
        else:
          cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return [Task(**row) for row in rows]
    

    def mark_task_done(self, task_id):
        self.conn.execute(
            "UPDATE tasks SET status = 'done' WHERE id = ?",
            (task_id,)
        )
        self.conn.commit()

    def add_vacation(self, destination, start_date, end_date):
        self.conn.execute("""
                INSERT INTO vacations(destination, start_date, end_date) VALUES (?, ?, ?)
                          """, (destination, start_date, end_date))
        self.conn.commit()

    def get_vacations(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vacations")
        rows = cursor.fetchall()
        return [Vacation(**row) for row in rows]

    