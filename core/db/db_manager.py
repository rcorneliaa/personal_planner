import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from models.task import Task
from models.vacation import Vacation
from models.vacation import Itinerary

load_dotenv() 

class DatabaseManager:
    """
    Handles all database operations for the application.

    Responsibilities:
    - Database initialization
    - CRUD operations for tasks, vacations and itineraries
    """

    def __init__(self, db_url = None):
        """
        Initializes the database connection.

        :param db_path: Path to SQLite database file
        """
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "postgresql://localhost:6543/postgres")
        
        self.conn = psycopg2.connect(db_url)
       
        self.conn.cursor_factory = RealDictCursor
       

    def initialize_database(self):
        """
        Creates database tables if they do not already exist.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'in progress'
                 
                )
          """)
        

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacations(
                id SERIAL PRIMARY KEY,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
                 
                )
          """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itineraries(
                id SERIAL PRIMARY KEY,
                vacation_id INTEGER REFERENCES vacations(id) ON DELETE CASCADE,
                day DATE,
                start_time TIME,
                end_time TIME,     
                activity TEXT,
                location TEXT,
                notest TEXT NULL
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
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (title, date)
            VALUES(%s, %s)
        """, (title, deadline))
        self.conn.commit()

       

    
    def get_tasks_by_date(self, date):
        """
        Retrieves tasks for a specific date.

        :param date: Date string (YYYY-MM-DD)
        :return: List of Task objects
        """
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        if date:
          cursor.execute("SELECT * FROM tasks WHERE date = %s", (date,))
        else:
          cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        return [Task(**row) for row in rows]
    

    def mark_task_done(self, task_id):
        """
        Marks a task as completed.

        :param task_id: ID of the task
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = 'done' WHERE id = %s",
            (task_id,)
        )
        self.conn.commit()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )
        self.conn.commit()


     # ============================= VACATION MANAGEMENT =============================

    def add_vacation(self, destination, start_date, end_date):
        """
        Adds a new vacation to the database.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
                INSERT INTO vacations(destination, start_date, end_date) VALUES (%s, %s, %s)
                          """, (destination, start_date, end_date))
        self.conn.commit()
       
    
    def get_vacations(self):
        """
        Retrieves all vacations.

        :return: List of Vacation objects
        """
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM vacations")
        rows = cursor.fetchall()
        return [Vacation(**row) for row in rows]
    


    # ============================= ITINERARY MANAGEMENT =============================
    def add_activity(self, vacation_id, day, start_time, end_time, activity, location=None, notest=None):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO itineraries(vacation_id, day, start_time, end_time, activity, location, notest) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (vacation_id, day, start_time, end_time, activity, location, notest))
        self.conn.commit()
        

    def get_activities(self, vacation_id, day):
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, vacation_id, day, start_time, end_time, activity, location, notest 
            FROM itineraries 
            WHERE vacation_id=%s AND day=%s
        """, (vacation_id, day))
        rows = cursor.fetchall()
        return [Itinerary(**row) for row in rows]

    def delete_activity(self, activity_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM itineraries WHERE id=%s", (activity_id,))
        self.conn.commit()
        return True

    def update_activity(self, activity_id, start_time, end_time, activity, location, notest):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE itineraries
            SET start_time=%s, end_time=%s, activity=%s, location=%s, notest=%s
            WHERE id=%s
        """, (start_time, end_time, activity, location, notest, activity_id))
        self.conn.commit()

    def close(self):
        """Închide conexiunea la baza de date"""
        if self.conn:
            self.conn.close()

    
    