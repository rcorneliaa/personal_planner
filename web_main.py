import sys
import os
from datetime import date
from fastapi import Query


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from core.services.task_services import TaskServices
from core.db.db_manager import DatabaseManager
from pydantic import BaseModel

class Task(BaseModel):
    """Pydantic model representing a task."""
    title: str
    date: date

class Habit(BaseModel):
    """Pydantic model representing a habit."""
    title: str
    goal: int 

app = FastAPI()
db = DatabaseManager()
db.initialize_database()

task_services = TaskServices(db)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tasks")
def get_tasks(date):
    """
    Retrieve all tasks for a specific date.

    Args:
        date (datetime.date): The date for which tasks are requested.

    Returns:
        list[dict]: List of task objects for the given date.
    """
    tasks = task_services.get_tasks_by_date(date)
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    """
    Add a new task.

    Args:
        task (Task): Task data including title and date.

    Returns:
        dict: Success message if task was added.
    """
    succes = task_services.add_task(task.title, task.date)
    if succes:
        return {"message": "Task Added!"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id):
    """
    Delete a task by its ID.

    Args:
        task_id (int): ID of the task to delete.

    Returns:
        dict: Success message.
    """
    task_services.delete_task(task_id)
    return {"message": "Task Deleted!"}

@app.put("/tasks/{task_id}")
def mark_task_done(task_id):
    """
    Mark a task as done by its ID.

    Args:
        task_id (int): ID of the task to mark as completed.

    Returns:
        dict: Success message.
    """
    task_services.mark_task_done(task_id)
    return {"massage": "Done!"}


@app.get("/habits/")
def get_habits(week_start: date = Query(...)):
    """
    Retrieve all habits for a specific week.

    Args:
        week_start (datetime.date): Start date of the week.

    Returns:
        list[dict]: List of habits with weekly logs.
    """
    habits = task_services.get_habits(week_start)
    return habits

@app.post("/habits")
def add_habit(habit: Habit):
    """
    Add a new habit.

    Args:
        habit (Habit): Habit data including title and weekly goal.

    Returns:
        dict: Success message if habit was added.
    """
    success = task_services.add_habit(habit.title, habit.goal)
    if success:
        return {"message": "Habit Added"}
    
@app.delete("/habits/{habit_id}")
def delete_habit(habit_id):
    """
    Delete a habit by its ID.

    Args:
        habit_id (int): ID of the habit to delete.

    Returns:
        dict: Success message.
    """
    task_services.delete_habit(habit_id)
    return {"message": "Habit Deleted!"}

@app.put("/habits/{habit_id}")
def toggle_day(habit_id: int, day:date = Query(...)):
    """
    Toggle completion status for a habit on a specific day.

    Args:
        habit_id (int): ID of the habit.
        day (datetime.date): Day to toggle.

    Returns:
        dict: Success message.
    """
    task_services.toggle_day(habit_id, day)
    