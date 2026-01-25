from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from ui.todo_ui import TodoScreen
from db.db_manager import DatabaseManager
from ui.main_window import StartScreen
from ui.vacations.vacation_ui import VacationsScreen
from ui.vacations.vacation_details_ui import VacationDetailScreen


class PersonalPlannerApp(MDApp):
    """
    Main application class for the Personal Planner app.

    Responsible for:
    - Initializing the database
    - Configuring the application theme
    - Setting up screen navigation
    """
    def build(self):
        """
        Builds and returns the root widget of the application.

        Initializes:
        - App theme
        - Database connection
        - ScreenManager and all screens
        """
        self.theme_cls.theme_style = "Light"  # sau "Dark"
        self.theme_cls.primary_palette = "DeepPurple"

        self.db = DatabaseManager()
        self.db.initialize_database()

        self.sm = ScreenManager()

        self.sm.add_widget(StartScreen(name="start"))
        self.sm.add_widget(TodoScreen(self.db, name="todo"))
        self.sm.add_widget(VacationsScreen(self.db, name = "vacations"))
        self.sm.add_widget(VacationDetailScreen(self.db, name ="vacation_details"))
    
       

        return self.sm

if __name__ == "__main__":
    PersonalPlannerApp().run()
