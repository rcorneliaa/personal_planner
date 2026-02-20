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

        :param title: The title of the task
        :param date: The deadline for the task (YYYY-MM-DD)
        :return: True if the task was added successfully, False otherwise
        """
        if not title.strip():
            return  False, "You need to add a title for the task!"
        self.db.add_task(title=title.strip(), date=date)
        return True
        
    def mark_task_done(self, task_id):
        self.db.mark_task_done(task_id)

    def mark_task_in_progress(self, task_id):
        self.db.mark_task_in_progress(task_id)

    def get_tasks_by_date(self, date):
        return self.db.get_tasks_by_date(date)
    
    def delete_task(self, task_id):
        self.db.delete_task(task_id)

    def add_habit(self, title, goal):
        if not title.strip():
            return  False, "You need to add a title for the habit!"
        self.db.add_habit(title=title.strip(), goal=goal)
        return True
    
    def delete_habit(self, habit_id):
        self.db.delete_habit(habit_id)

    def get_habits(self, week_start):
        return self.db.get_weekly_habits(week_start)
    
    def toggle_day(self, habit_id, day):
        self.db.toggle_day(habit_id, day)