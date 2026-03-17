from datetime import datetime, timedelta

import pytest
import requests
from jsonschema import validate, ValidationError
 

URL = "http://127.0.0.1:8000"
date ="2026-03-17"
date_obj = datetime.strptime(date, "%Y-%m-%d").date()
monday = date_obj - timedelta(days=date_obj.weekday())

habit_schema = {
    "type": "array",
    "items":{
    "type":"object",
    "required": ["id", "title", "weekly_goal", "logs"],
    "properties": {
        "id":{
            "type":"number",
            "minimum": 1
        },
        "title":{
            "type": "string",
            "minLength": 1
        },
        "weekly_goal":{
            "type": "number",
            "minimum": 1,
            "maximum": 7
        },
        "logs":{
            "type": "object",
            "patternProperties": {
                "^\\d{4}-\\d{2}-\\d{2}$": { 
                    "type": "boolean"
                }

        }
    }
}
}
}

task_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["id", "title", "date", "status"],
            "properties": {
                "id": { "type": "number" },
                "title": { "type": "string" },
                "date": { "type": "string", "format": "date" },
                "status": { "type": "string", "enum": ["in progress", "done"] }
            }
        }
    };

class TestTask:
    def test_get_tasks_empty(self, log_extra):
        response = requests.get(f"{URL}/tasks?date={date}")
        
        assert response.status_code == 200

        body = response.json()
        assert isinstance(body, list)

        assert len(body) == 0

    def test_add_task(self, log_extra):
       payload = {"title": "Test API with pytest", 
                  "date": date
                  }
       response = requests.post(f"{URL}/tasks", json= payload)

       assert response.status_code == 200
       assert response.json()["message"] == "Task Added!"

    def test_get_tasks(self, log_extra):
        response = requests.get(f"{URL}/tasks?date={date}")
        data = response.json()
        assert any(task["title"] == "Test API with pytest" for task in data)

    def test_mark_task_done(self, log_extra):
        response = requests.get(f"{URL}/tasks?date={date}")
        task_id = response.json()[0]["id"]
        response = requests.put(f"{URL}/tasks/{task_id}")
        assert response.status_code == 200

        assert response.json()["massage"] == "Done!"

        response = requests.get(f"{URL}/tasks?date={date}")
        tasks = response.json()
        for task in tasks:
            if task["id"]== task_id:
                assert task["status"]== "done"
                break

    def test_delete_task(self, log_extra):
        response = requests.get(f"{URL}/tasks?date={date}")
        task_id = response.json()[0]["id"]
        response = requests.delete(f"{URL}/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["message"]=="Task Deleted!"

        response = requests.get(f"{URL}/tasks?date={date}")
        assert not response.json()


class TestHabits:
    def test_get_habits_empty(self):
        response = requests.get(f"{URL}/habits/?week_start={monday}")

        assert response.status_code == 200

        body = response.json()
        assert isinstance(body, list)

        assert len(body)==0

    def test_add_habit(self):
        payload = {"title": "Gym",
                   "goal": 4}
        response = requests.post(f"{URL}/habits", json = payload)

        assert response.status_code == 200

        assert response.json()["message"]== "Habit Added"


    

    def test_toggle_day(self):
        response = requests.get(f"{URL}/habits/?week_start={monday}")
        task_id = response.json()[0]["id"]

        response = requests.put(f"{URL}/habits/{task_id}?day={monday}")

        assert response.status_code == 200


    def test_get_habit(self):
            
            response = requests.get(f"{URL}/habits/?week_start={monday}")

            assert response.status_code == 200

            body = response.json()

            try:
                validate(body, habit_schema)
            except ValidationError as e:
                pytest.fail(f"Schema validation failed: {e}")


