import sys
import os
from datetime import date
from fastapi import Query

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from core.services.task_services import TaskServices
from core.db.db_manager import DatabaseManager
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    date: date

class Habit(BaseModel):
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
    tasks = task_services.get_tasks_by_date(date)
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    succes = task_services.add_task(task.title, task.date)
    if succes:
        return {"message": "Task Added!"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id):
    task_services.delete_task(task_id)
    return {"message": "Task Deleted!"}

@app.put("/tasks/{task_id}")
def mark_task_done(task_id):
    task_services.mark_task_done(task_id)
    return {"massage": "Done!"}


@app.get("/habits/")
def get_habits(week_start: date = Query(...)):
    habits = task_services.get_habits(week_start)
    return habits

@app.post("/habits")
def add_habit(habit: Habit):
    success = task_services.add_habit(habit.title, habit.goal)
    if success:
        return {"message": "Habit Added"}
    
@app.delete("/habits/{habit_id}")
def delete_habit(habit_id):
    task_services.delete_habit(habit_id)
    return {"message": "Habit Deleted!"}

@app.put("/habits/{habit_id}")
def toggle_day(habit_id: int, day:date = Query(...)):
    task_services.toggle_day(habit_id, day)
    