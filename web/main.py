from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Personal Planner API"}
@app.post("/tasks")
def add_task(task: dict):
    return {"received": task}
