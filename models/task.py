class Task:
    def __init__(self, id, title, description = None, deadline = None, priority = "medium", status ="in progres"):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

    
    def is_dne(self):
        return self.status == "done"
    

    def __str__(self):
        return f"[{self.priority.upper()}] {self.title} - {self.status.upper()}"
        