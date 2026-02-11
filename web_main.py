import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from core.services.task_services import TaskServices
from core.db.db_manager import DatabaseManager
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    date: str

app = FastAPI()
db = DatabaseManager()
db.initialize_database()

task_services = TaskServices(db)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tasks")
def get_tasks(date: str):
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