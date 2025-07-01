from kivy.app import App
from ui.todo_ui import TodoScreen

class PersonalPlannerApp(App):
    def build(self):
        return TodoScreen()

if __name__ == "__main__":
    PersonalPlannerApp().run()
