# ui/start_ui.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.image import Image

class StartScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=40)

        title = MDLabel(
            text="Personal Planner",
            halign="center",
            theme_text_color="Primary",
            font_style="H4"
        )

        todo_button = MDRaisedButton(
            text="To-Do Lists",
            pos_hint={"center_x": 0.2},
            on_release=self.go_to_todo
        )
        
        vacation_planer_button = MDRaisedButton(
            text = "My Vacations",
            pos_hint = {"center_x": 0.5},
            on_release = self.go_vacations

        )

        self.image_display = Image(
            source=r"utils\logo.png", 
            size_hint=(1, 0.5),
            allow_stretch=True,
            keep_ratio=True
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
