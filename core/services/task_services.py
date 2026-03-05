class TaskServices:
    """
    Handles all business logic for tasks.
    Interacts with the database but knows nothing about the UI.
    """

    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_task(self, title, date):
        """
        Adds a new task to the database.
        """
        if not title.strip():
            return  False, "You need to add a title for the task!"
        self.db.add_task(title=title.strip(), date=date)
        return True
        
    def mark_task_done(self, task_id):
        """
        Marks a task as completed.
        """
        self.db.mark_task_done(task_id)

    def mark_task_in_progress(self, task_id):
        """
        Marks a task as in progress.
        """
        self.db.mark_task_in_progress(task_id)

    def get_tasks_by_date(self, date):
        """
        Retrieves tasks for a specific date.
        """
        return self.db.get_tasks_by_date(date)
    
    def delete_task(self, task_id):
        """
        Deletes a task from the database.
        """
        self.db.delete_task(task_id)

    def add_habit(self, title, goal):
        """
        Adds a new habit to the database with validation.

        Returns:
            tuple[bool, str | None]: (Success flag, Error message if any)
        """
        if not title.strip():
            return  False, "You need to add a title for the habit!"
        self.db.add_habit(title=title.strip(), goal=goal)
        return True
    
    def delete_habit(self, habit_id):
        """
        Deletes (deactivates) a habit.
        """
        self.db.delete_habit(habit_id)

    def get_habits(self, week_start):
        """
        Retrieves all habits and their weekly logs.
        """
        return self.db.get_weekly_habits(week_start)
    
    def toggle_day(self, habit_id, day):
        """
        Toggles the completion status of a habit for a specific day.
        """
        self.db.toggle_day(habit_id, day)