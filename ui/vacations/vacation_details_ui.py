from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem
from kivymd.uix.label import MDLabel
from datetime import date, timedelta
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.pickers.timepicker import MDTimePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from kivy.clock import Clock

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

        self.main_layout = MDBoxLayout(orientation = "vertical")
    
        # Bara de sus
        top_bar = MDTopAppBar(
            title="Itinerary",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=10,
            pos_hint={"top": 1},
            type_height="small",
        )
        self.main_layout.add_widget(top_bar)

        self.content_layout = MDBoxLayout(orientation = "horizontal")
        self.main_layout.add_widget(self.content_layout)

        self.add_widget(self.main_layout)


    def set_vacation(self, vacation):
        self.vacation = vacation
        if hasattr(self, 'rail'):
            self.content_layout.remove_widget(self.rail)

        if hasattr(self, 'detail_container'):
            self.content_layout.remove_widget(self.detail_container)
          
        self.rail =MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon="menu",
                ),
                size_hint_x=None,
                anchor = "bottom",
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
       
        for i in range(1, number_of_days + 1):
            item = MDNavigationRailItem(
                icon="calendar",
                text=f"Day{i}",
                
                on_release=lambda instance, day=i: self.show_day_details(day),
            )
            
            self.rail.add_widget(item)
        self.detail_container = MDBoxLayout(orientation = "vertical")
        

        self.content_layout.add_widget(self.rail)
        self.content_layout.add_widget(self.detail_container)
        self.show_day_details(1)

    def show_day_details(self, day):
        self.current_day = day
        self.detail_container.clear_widgets()

        self.add_activity_btn = MDRaisedButton(
            icon="plus",
            text = "Add Activity for the Day",
            pos_hint={"right": 0.97, "y": 0.02},
            size_hint=(None, None),
            height="48dp",
            padding=("12dp", "10dp", "12dp", "10dp"),
            on_release = self.show_details_dialog
         
        )
        # # Aici iei activitățile din DB pentru ziua curentă
        # activities = self.db.get_activities(self.vacation.id, day)

        
        self.detail_container.add_widget(MDLabel(text=f"Day {day} details", halign="center"))
        self.detail_container.add_widget(self.add_activity_btn)

    def show_details_dialog(self, *args):
        content = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=(20, 60, 20, 20),  
            size_hint_y=None,
            height=700,
            width = 900
            )

        self.start_time_btn = MDRectangleFlatButton(text = "Choose start time..")
        self.start_time_btn.bind(on_release = self.show_start_time_picker)
        content.add_widget(self.start_time_btn)

        self.end_time_btn = MDRectangleFlatButton(text = "Choose end time..")
        self.end_time_btn.bind(on_release = self.show_end_time_picker)
        content.add_widget(self.end_time_btn)

        self.activity = MDTextField(hint_text = "Activity", id = "activity")
        content.add_widget(self.activity)

        self.location = MDTextField(hint_text = "Location", id = "location")
        content.add_widget(self.location)

        self.notest = MDTextField(hint_text = "Details", id = "notest")
        content.add_widget(self.notest)


        self.activity_dialog = MDDialog(
            title = "Add activity",
            type = "custom",
            content_cls = content,
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: self.activity_dialog.dismiss()),
                MDRaisedButton(text="Add", on_release=self.add_activity)
            ]

        )
        self.activity_dialog.open()

    def show_start_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.set_start_time)
        time_dialog.open()

    def set_start_time(self, instance, value):
        self.start_time = value
        self.start_time_btn.text =f"Start time: {value.strftime("%H:%M")}" 

    def show_end_time_picker(self, instance):
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.set_end_time)
        time_dialog.open()

    def set_end_time(self, instance, value):
        self.end_time = value
        self.end_time_btn.text =f"End time: {value.strftime("%H:%M")}" 

    def add_activity(self, *args):
        activity = self.activity.text
        location = self.location.text
        notest  = self.notest.text
        vacation_id = self.vacation.id
        day_number = self.current_day
        day =  self.start_date + timedelta(days=day_number - 1)   

        self.db.add_activity(
        vacation_id=vacation_id,
        day_date=day.isoformat(),
        start_time=self.start_time.strftime("%H:%M"),
        end_time=self.end_time.strftime("%H:%M"),
        activity=activity,
        location=location,
        notest=notest,
               
    )   
        self.activity_dialog.dismiss()

    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction="right")
        app.sm.current = "vacations"

        