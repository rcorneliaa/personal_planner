from kivy.app import App
from ui.todo_ui import TodoScreen
from db.db_manager import DatabaseManager

class PersonalPlannerApp(App):
    def build(self):
        self.db = DatabaseManager()
        self.db.initialize_database()
        return TodoScreen(self.db)

if __name__ == "__main__":
    PersonalPlannerApp().run()
