from datetime import date, datetime, timedelta
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
    Handles all database operations for the Personal Planner application.

    This includes management of tasks, habits, vacations, and itineraries.
    Provides CRUD operations and utility methods for database interactions.
    """

    def __init__(self, db_url=None):
        """
        Initializes the database connection.

        Args:
            db_url (str, optional): PostgreSQL database URL. If None, defaults
                to environment variable 'DATABASE_URL' or 'postgresql://localhost:6543/postgres'.
        """
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "postgresql://localhost:6543/postgres")
        
        self.conn = psycopg2.connect(db_url)
        

    def _execute_query(self, query, params=None, fetch_one=False, fetch_all=False, dict_cursor=False):
        """
        Executes a SQL query with optional fetch and error handling.

        Args:
            query (str): SQL query string.
            params (tuple, optional): Parameters for the query.
            fetch_one (bool, optional): If True, fetches a single row.
            fetch_all (bool, optional): If True, fetches all rows.
            dict_cursor (bool, optional): If True, uses RealDictCursor for dict results.

        Returns:
            list[dict] | dict | None: Query result based on fetch options.
        """
        cursor = None
        try:
            
            if dict_cursor:
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            else:
                cursor = self.conn.cursor()
            
           
            cursor.execute(query, params or ())
            
            result = None
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            
        
            self.conn.commit()
            
            return result
            
        except Exception as e:
            self.conn.rollback()
            print(f"Eroare SQL: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise e
            
        finally:
            if cursor:
                cursor.close()

    def initialize_database(self):
        """
        Creates all required database tables if they do not exist.

        Tables created:
            - tasks
            - habits
            - habit_logs
            - vacations
            - itineraries
        """
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS tasks(
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'in progress'
            )
        """)
        
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS habits(
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                goal INTEGER
            )
        """)
        
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS habit_logs(
                id SERIAL PRIMARY KEY,
                habit_id INTEGER REFERENCES habits(id) ON DELETE CASCADE,
                log_date DATE NOT NULL,
                status BOOLEAN DEFAULT false,
                UNIQUE (habit_id, log_date)
            )
        """)
        
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS vacations(
                id SERIAL PRIMARY KEY,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL
            )
        """)
        
        self._execute_query("""
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
    
        try:
            self._execute_query("""
                ALTER TABLE tasks
                ALTER COLUMN date TYPE DATE
                USING date::DATE
            """)
        except Exception:
            pass  

    # ============================= TASK MANAGEMENT =============================

    def add_task(self, title, date):
        """
        Adds a new task to the database.

        Args:
            title (str): Task title.
            date (str | datetime.date): Task date.
        """
        self._execute_query(
            "INSERT INTO tasks (title, date) VALUES(%s, %s)",
            (title, date)
        )

    def get_tasks_by_date(self, date):
        """
        Retrieves tasks for a specific date.

        Args:
            date (str | datetime.date): Date for which to retrieve tasks.

        Returns:
            list[Task]: List of Task objects for the specified date.
        """
        if date:
            rows = self._execute_query(
                "SELECT * FROM tasks WHERE date = %s",
                (date,),
                fetch_all=True,
                dict_cursor=True
            )
        else:
            rows = self._execute_query(
                "SELECT * FROM tasks",
                fetch_all=True,
                dict_cursor=True
            )
        
        return [Task(**row) for row in rows] if rows else []

    def mark_task_done(self, task_id):
        """
        Marks a task as completed.
        """
        self._execute_query(
            "UPDATE tasks SET status = 'done' WHERE id = %s",
            (task_id,)
        )

    def delete_task(self, task_id):
        """
        Deletes a task.
        """
        self._execute_query(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

    # ============================= HABITS MANAGEMENT =============================

    def add_habit(self, title, goal):
        """
        Adds a new habit.

        Args:
            title (str): Habit title.
            goal (int): Weekly goal (1-7).
        """
        self._execute_query(
            "INSERT INTO habits(title, goal) VALUES(%s, %s)",
            (title, goal)
        )

    def delete_habit(self, habit_id):
        """
        Marks a habit as inactive (soft delete).
        """
        self._execute_query(
            "UPDATE habits SET active = FALSE WHERE id = %s",
            (habit_id,)
        )

    def get_weekly_habits(self, week_start):
        """
        Retrieves all habits and their completion logs for a week.

        Args:
            week_start (datetime.date): Start date of the week (Monday).

        Returns:
            list[dict]: List of habits with structure:
                {
                    "id": int,
                    "title": str,
                    "weekly_goal": int,
                    "logs": dict[str, bool]
                }
        """
        week_end = week_start + timedelta(days=6)
        
        rows = self._execute_query("""
            SELECT h.id, h.title, h.goal as weekly_goal,
                hl.log_date, hl.status
            FROM habits h
            LEFT JOIN habit_logs hl 
                ON h.id = hl.habit_id
                AND hl.log_date BETWEEN %s AND %s
                AND hl.status = TRUE  
            WHERE h.active = TRUE 
            ORDER BY h.id, hl.log_date
        """, (week_start, week_end), fetch_all=True, dict_cursor=True)
        
        habits_dict = {}
        
        for row in rows:
            hid = row["id"]
            if hid not in habits_dict:
                habits_dict[hid] = {
                    "id": hid,
                    "title": row["title"],
                    "weekly_goal": row["weekly_goal"],
                    "logs": set()  
                }
            
            if row["log_date"]:  
                log_day = row["log_date"].isoformat()
                habits_dict[hid]["logs"].add(log_day)
        
        
        result = []
        for habit in habits_dict.values():
            habit["logs"] = {day: True for day in habit["logs"]}
            result.append(habit)
        
        return result

    def toggle_day(self, habit_id, day):
        """
        Toggles a habit log for a specific day.
        """
        
        result = self._execute_query(
            "SELECT id FROM habit_logs WHERE habit_id = %s AND log_date = %s",
            (habit_id, day),
            fetch_one=True
        )
        
        if result:
           
            self._execute_query(
                "DELETE FROM habit_logs WHERE id = %s",
                (result[0],)
            )
        else:
           
            self._execute_query(
                "INSERT INTO habit_logs(habit_id, log_date, status) VALUES(%s, %s, TRUE)",
                (habit_id, day)
            )

    # ============================= VACATION MANAGEMENT =============================

    def add_vacation(self, destination, start_date, end_date):
        """
        Adds a new vacation to the database.

        Args:
            destination (str): Vacation destination.
            start_date (str | datetime.date): Start date.
            end_date (str | datetime.date): End date.
        """
        self._execute_query(
            "INSERT INTO vacations(destination, start_date, end_date) VALUES (%s, %s, %s)",
            (destination, start_date, end_date)
        )

    def get_vacations(self):
        """
        Retrieves all vacations from the database.

        Returns:
            list[Vacation]: List of Vacation objects.
        """
        rows = self._execute_query(
            "SELECT * FROM vacations",
            fetch_all=True,
            dict_cursor=True
        )
        
        return [Vacation(**row) for row in rows] if rows else []

    # ============================= ITINERARY MANAGEMENT =============================

    def add_activity(self, vacation_id, day, start_time, end_time, activity, location=None, notest=None):
        """
        Adds an activity to a vacation itinerary.

        Args:
            vacation_id (int): Vacation ID.
            day (str | datetime.date): Day of the activity.
            start_time (str | datetime.time): Start time.
            end_time (str | datetime.time): End time.
            activity (str): Activity description.
            location (str, optional): Activity location.
            notest (str, optional): Notes for the activity.
        """
        self._execute_query("""
            INSERT INTO itineraries(vacation_id, day, start_time, end_time, activity, location, notest) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (vacation_id, day, start_time, end_time, activity, location, notest))

    def get_activities(self, vacation_id, day):
        """
        Retrieves activities for a specific vacation day.

        Args:
            vacation_id (int): Vacation ID.
            day (str | datetime.date): Day to retrieve activities for.

        Returns:
            list[Itinerary]: List of Itinerary objects.
        """
        rows = self._execute_query("""
            SELECT id, vacation_id, day, start_time, end_time, activity, location, notest 
            FROM itineraries 
            WHERE vacation_id = %s AND day = %s
        """, (vacation_id, day), fetch_all=True, dict_cursor=True)
        
        return [Itinerary(**row) for row in rows] if rows else []

    def delete_activity(self, activity_id):
        """
        Deletes an activity from the itinerary.
        """
        self._execute_query(
            "DELETE FROM itineraries WHERE id = %s",
            (activity_id,)
        )
        return True

    def update_activity(self, activity_id, start_time, end_time, activity, location, notest):
        """
        Updates an existing activity.
        """
        self._execute_query("""
            UPDATE itineraries
            SET start_time = %s, end_time = %s, activity = %s, location = %s, notest = %s
            WHERE id = %s
        """, (start_time, end_time, activity, location, notest, activity_id))

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

    