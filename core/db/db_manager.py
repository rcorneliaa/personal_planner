import sqlite3
from models.task import Task
from models.vacation import Vacation
from models.vacation import Itinerary

class DatabaseManager:
    """
    Handles all database operations for the application.

    Responsibilities:
    - Database initialization
    - CRUD operations for tasks, vacations and itineraries
    """

    def __init__(self, db_path = "personal_planner.db"):
        """
        Initializes the database connection.

        :param db_path: Path to SQLite database file
        """
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        self.conn.row_factory = sqlite3.Row
       

    def initialize_database(self):
        """
        Creates database tables if they do not already exist.
        """
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
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS itineraries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vacation_id INTEGER,
                day DATE,
                start_time TIME,
                end_time TIME,     
                activity TEXT,
                location TEXT,
                notest TEXT NULL,
                FOREIGN KEY (vacation_id) REFERENCES vacations(id)                                               
                 
                )
          """)
        self.conn.commit()

    # ============================= TASK MANAGEMENT =============================

    def add_task(self, title, deadline = None):
        """
        Adds a new task to the database.

        :param title: Task title
        :param deadline: Task date (YYYY-MM-DD)
        """
        self.conn.execute("""
            INSERT INTO tasks (title, date)
            VALUES(?, ?)
        """, (title, deadline))
        self.conn.commit()

    
    def get_tasks_by_date(self, date):
        """
        Retrieves tasks for a specific date.

        :param date: Date string (YYYY-MM-DD)
        :return: List of Task objects
        """
        cursor = self.conn.cursor()
        if date:
          cursor.execute("SELECT * FROM tasks WHERE date = ?", (date,))
        else:
          cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return [Task(**row) for row in rows]
    

    def mark_task_done(self, task_id):
        """
        Marks a task as completed.

        :param task_id: ID of the task
        """
        self.conn.execute(
            "UPDATE tasks SET status = 'done' WHERE id = ?",
            (task_id,)
        )
        self.conn.commit()

    def delete_task(self, task_id):
        self.conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        self.conn.commit()


     # ============================= VACATION MANAGEMENT =============================

    def add_vacation(self, destination, start_date, end_date):
        """
        Adds a new vacation to the database.
        """
        self.conn.execute("""
                INSERT INTO vacations(destination, start_date, end_date) VALUES (?, ?, ?)
                          """, (destination, start_date, end_date))
        self.conn.commit()

    def get_vacations(self):
        """
        Retrieves all vacations.

        :return: List of Vacation objects
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vacations")
        rows = cursor.fetchall()
        return [Vacation(**row) for row in rows]
    


    # ============================= ITINERARY MANAGEMENT =============================
    def add_activity(self, vacation_id, day, start_time, end_time, activity, location = None, notest = None):
        """
        Adds a new activity to a vacation itinerary.
        """
        self.conn.execute("""
                INSERT INTO itineraries(vacation_id, day, start_time, end_time, activity, location, notest) VALUES (?, ?, ?, ?, ?, ?, ?)
                          """, (vacation_id, day, start_time, end_time, activity, location, notest))
        self.conn.commit()


    def get_activities(self, vacation_id, day):
        """
        Retrieves activities for a specific vacation day.

        :return: List of Itinerary objects
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, vacation_id, day, start_time, end_time, activity, location, notest "
                       "FROM itineraries WHERE vacation_id=? AND day=?", (vacation_id, day))
        rows = cursor.fetchall()
        return [Itinerary(**row) for row in rows]
    
    def delete_activity(self, activity_id):
        """
        Deletes an activity from the database.

        :param activity_id: ID of the activity
        :return: True if deletion was successful
        """
        cursor = self.conn.cursor()
        cursor.execute("""DELETE FROM itineraries WHERE id=? """, (activity_id,))
        self.conn.commit()
        return True


    def update_activity(self, activity_id, start_time, end_time, activity, location, notest):
        self.conn.execute("""
            UPDATE itineraries
            SET start_time=?, end_time=?, activity=?, location=?, notest=?
            WHERE id=?
        """, (start_time, end_time, activity, location, notest, activity_id))
        self.conn.commit()

    
    