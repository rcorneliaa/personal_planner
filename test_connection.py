# test_connection.py
from core.db.db_manager import DatabaseManager

# Testează conexiunea
db = DatabaseManager()

# Inițializează tabelele (dacă nu există deja)
db.initialize_database()

# Adaugă un task de test
task_id = db.add_task("Test cloud connection", "2026-02-17")
print(f"Task adăugat cu ID: {task_id}")

# Citește task-urile
tasks = db.get_tasks_by_date("2026-02-17")
print(f"Am găsit {len(tasks)} task-uri:")
for task in tasks:
    print(f"  • {task.title} - {task.status}")

# Curăță
db.delete_task(task_id)
print("Task șters")

db.close()