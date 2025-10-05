# ui/start_ui.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.image import Image

class StartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        title = MDLabel(
            text="Personal Planner",
            halign="center",
            theme_text_color="Primary",
            font_style="H4",
            pos_hint={"center_x": 0.5, "center_y": 0.9}
        )

        todo_button = MDRaisedButton(
            text="To-Do Lists",
            pos_hint={"center_x": 0.2, "center_y": 0.35},
            on_release=self.go_to_todo
        )
        
        vacation_planer_button = MDRaisedButton(
            text = "My Vacations",
            pos_hint = {"center_x": 0.8, "center_y": 0.35},
            on_release = self.go_vacations

        )

        self.image_display = Image(
            source=r"utils\logo.png", 
            size_hint=(0.6, 0.3),
            allow_stretch=True,
            keep_ratio=True,
            pos_hint={"center_x": 0.5, "center_y": 0.65}
        )

        
        layout.add_widget(self.image_display)
        layout.add_widget(title)
        layout.add_widget(todo_button)
        layout.add_widget(vacation_planer_button)
        self.add_widget(layout)

    def go_to_todo(self, instance):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='left')
        app.sm.current = "todo"

    def go_vacations(self, instance):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction = 'left')
        app.sm.current = "vacations"
