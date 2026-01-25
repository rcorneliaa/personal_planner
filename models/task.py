class Task:
    """
    Represents a single task in the to-do list.

    Attributes:
        id (int): Unique identifier of the task
        title (str): Task title or description
        date (date | str): Due date of the task
        status (str): Current status of the task (default: "in progres")
    """
     
    def __init__(self, id, title, date, status ="in progres"):
        """
        Initializes a new task instance.

        :param id: Unique task identifier
        :param title: Task title
        :param date: Due date of the task
        :param status: Task status
        """
        self.id = id
        self.title = title
        self.date = date
        self.status = status

    
    def is_done(self):
        """
        Checks whether the task is completed.

        :return: True if task status is 'done', otherwise False
        """
        return self.status == "done"
    

    def __str__(self):
        return f"{self.title} - {self.status.upper()}"
        