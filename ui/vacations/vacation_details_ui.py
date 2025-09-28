from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem
from kivymd.uix.label import MDLabel
from datetime import date

from kivy.clock import Clock
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import (
    MDNavigationRailItem,
    MDNavigationRail,
    MDNavigationRailMenuButton,
    MDNavigationRailFabButton,
   
)
from kivymd.uix.screen import MDScreen




class VacationDetailScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager

        self.layout = MDBoxLayout()
    
        # Bara de sus
        top_bar = MDTopAppBar(
            title="Itinerary",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=10,
            pos_hint={"top": 1},
            type_height="small",
        )
        self.layout.add_widget(top_bar)
        self.add_widget(self.layout)


    def set_vacation(self, vacation):
        print("executa functia")
        self.vacation = vacation
        if hasattr(self, 'rail'):
            self.layout.remove_widget(self.rail)
            print("a fost sters")

        self.rail =MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon="menu",
                ),
                size_hint_x=None,
                anchor = "center",
                pos_hint={"top": 1}
            )
       
        start_date = (
            date.fromisoformat(vacation.start_date)
            if isinstance(vacation.start_date, str)
            else vacation.start_date
        )
        end_date = (
            date.fromisoformat(vacation.end_date)
            if isinstance(vacation.end_date, str)
            else vacation.end_date
        )

        self.start_date = start_date
        self.end_date = end_date
     
        number_of_days = (end_date - start_date).days + 1
        print(number_of_days)
        print(f"destinatia este: {self.vacation.destination}")

       
        for i in range(1, number_of_days + 1):
            item = MDNavigationRailItem(
                icon="calendar",
                text=f"Day{i}",
                
                #on_release=lambda instance, day=i: self.select_day(day),
            )
            
            self.rail.add_widget(item)

        self.layout.add_widget(self.rail)


    def go_back(self):
        """Revenire la ecranul de vacanțe"""
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction="right")
        app.sm.current = "vacations"
