from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar 

class VacationDetailScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager

        main_layout = MDBoxLayout(orientation = 'vertical')

        top_bar = MDTopAppBar(
            title = "Itinerary",
            left_action_items = [["arrow-left", lambda x: self.go_back()]],
            elevation = 10,
            pos_hint = {"top": 1},
            type_height = "small",
            type = "top",
            
        )
        main_layout.add_widget(top_bar)
        self.add_widget(main_layout)

    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "vacations"