class Task:
    def __init__(self, id, title, date, status ="in progres"):
        self.id = id
        self.title = title
        self.date = date
        self.status = status

    
    def is_done(self):
        return self.status == "done"
    

    def __str__(self):
        return f"{self.title} - {self.status.upper()}"
        