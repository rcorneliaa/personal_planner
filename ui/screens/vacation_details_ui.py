"""
Vacation detail screen of the Personal Planner application.

This module defines the UI and logic for displaying and managing
daily itineraries within a selected vacation, including activities
per day and time-based scheduling.
"""
from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationrail import MDNavigationRail, MDNavigationRailItem
from kivymd.uix.label import MDLabel
from datetime import date, datetime, timedelta
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.pickers.timepicker import MDTimePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation
from kivy.clock import Clock
from ui.components.activity_card import ActivityCard
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import (
    MDNavigationRailItem,
    MDNavigationRail,
    MDNavigationRailMenuButton,
    MDNavigationRailFabButton,
   
)
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast


class VacationDetailScreen(MDScreen):
    """
    Screen displaying detailed vacation itinerary.

    Allows navigation between vacation days and management of
    daily activities, including time selection and notes.
    """

    def __init__(self, activities_services, **kwargs):
        super().__init__(**kwargs)
        self.activities_services = activities_services

        self.main_layout = MDBoxLayout(orientation = "vertical")
    
        # Bara de sus
        top_bar = MDTopAppBar(
            title="Itinerary",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            # elevation=10,
            pos_hint={"top": 1},
            type_height="small",
        )
        self.main_layout.add_widget(top_bar)

        self.content_layout = MDBoxLayout(orientation = "horizontal")
        self.main_layout.add_widget(self.content_layout)

        self.add_widget(self.main_layout)


    def set_vacation(self, vacation):
        """
        Sets the selected vacation and initializes day navigation.

        :param vacation: Vacation object containing start/end dates
        """
        self.vacation = vacation
        if hasattr(self, 'rail'):
            self.content_layout.remove_widget(self.rail)

        if hasattr(self, 'scroll'):
            self.content_layout.remove_widget(self.scroll)
          
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
        self.scroll = ScrollView(size_hint = (1,1))
        self.detail_container = MDBoxLayout(orientation = "vertical", size_hint = (1, None), spacing = 15, padding=(0, 56, 0, 0))
        self.detail_container.bind(minimum_height=self.detail_container.setter('height'))
        

        self.content_layout.add_widget(self.rail)
        self.scroll.add_widget(self.detail_container)
        self.content_layout.add_widget(self.scroll)
        self.show_day_details(1)

    def show_day_details(self, day):
        """
        Displays activities for a specific vacation day.

        :param day: Day number within the vacation
        """
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
        self.detail_container.add_widget(MDLabel(text=f"Day {day} details", halign="center"))
        day_date = self.start_date + timedelta(days=day - 1)
        activities = self.activities_services.get_activities(self.vacation.id, day_date.isoformat())

        for act in activities:
            card = ActivityCard(act, on_delete= self.handle_delete_activity, on_edit= self.handle_edit_activity)
            self.detail_container.add_widget(card)
            
        self.detail_container.add_widget(self.add_activity_btn)
        self.detail_container.bind(minimum_height=self.detail_container.setter('height'))

    def handle_delete_activity(self, activity_id, card):
        success, error = self.activities_services.delete_activity(activity_id)

        if not success:
            toast(error)
            return

        anim = Animation(opacity=0, duration=0.2)
        anim.bind(
            on_complete=lambda *a: self.detail_container.remove_widget(card)
        )
        anim.start(card)

    def handle_edit_activity(self, activity):
        self.show_details_dialog(edit_mode=True, activity=activity)


    def show_details_dialog(self, edit_mode = False, activity = None):
        """
        Opens a dialog for adding a new activity.
        """
        self.edit_mode = edit_mode
        self.edit_activity = activity

        content = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=(20, 60, 20, 20),
            size_hint_y=None,
            height=700
        )

        
        self.start_time = None
        self.end_time = None

        
        self.start_time_btn = MDRectangleFlatButton(text="Choose start time")
        self.start_time_btn.bind(on_release=self.show_start_time_picker)
        content.add_widget(self.start_time_btn)

       
        self.end_time_btn = MDRectangleFlatButton(text="Choose end time")
        self.end_time_btn.bind(on_release=self.show_end_time_picker)
        content.add_widget(self.end_time_btn)

      
        self.activity = MDTextField(hint_text="Activity")
        content.add_widget(self.activity)

        self.location = MDTextField(hint_text="Location")
        content.add_widget(self.location)

        self.notest = MDTextField(hint_text="Details")
        content.add_widget(self.notest)

       
        if edit_mode and activity:

            self.activity.text = activity.activity
            self.location.text = activity.location or ""
            self.notest.text = activity.notest or ""

            if isinstance(activity.start_time, str):
                self.start_time = datetime.strptime(activity.start_time, "%H:%M").time()
            else:
                self.start_time = activity.start_time

            if isinstance(activity.end_time, str):
                self.end_time = datetime.strptime(activity.end_time, "%H:%M").time()
            else:
                self.end_time = activity.end_time

            self.start_time_btn.text = f"Start time: {self.start_time.strftime('%H:%M')}"
            self.end_time_btn.text = f"End time: {self.end_time.strftime('%H:%M')}"
            title = "Edit activity"
            button_text = "Save"

        else:
            title = "Add activity"
            button_text = "Add"

        self.activity_dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text="Cancel",
                    on_release=lambda x: self.activity_dialog.dismiss()
                ),
                MDRaisedButton(
                    text=button_text,
                    on_release=self.save_activity
                )
            ]
        )

        self.activity_dialog.open()

    def show_start_time_picker(self, instance):
        """
        Opens a time picker for selecting activity start time.
        """
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.set_start_time)
        time_dialog.open()

    def set_start_time(self, instance, value):
        """
        Sets the selected start time.

        :param value: Selected time
        """
        self.start_time = value
        self.start_time_btn.text =f"Start time: {value.strftime("%H:%M")}" 

    def show_end_time_picker(self, instance):
        """
        Opens a time picker for selecting activity end time.
        """
        time_dialog = MDTimePicker()
        time_dialog.bind(time = self.set_end_time)
        time_dialog.open()

    def set_end_time(self, instance, value):
        """
        Sets the selected end time.

        :param value: Selected time
        """
        self.end_time = value
        self.end_time_btn.text =f"End time: {value.strftime("%H:%M")}" 

    def save_activity(self, *args):
        """
        Saves a new activity to the database
        and refreshes the current day view.
        """
        if not self.start_time or not self.end_time:
            toast("Select start and end time")
            return

        day = self.start_date + timedelta(days=self.current_day - 1)

        if self.edit_activity:
            success, error = self.activities_services.update_activity(
                activity_id=self.edit_activity.id,
                start_time=self.start_time.strftime("%H:%M"),
                end_time=self.end_time.strftime("%H:%M"),
                activity=self.activity.text,
                location=self.location.text,
                notest=self.notest.text,
            )

        else:
            success, error = self.activities_services.add_activity(
                vacation_id=self.vacation.id,
                day=day.isoformat(),
                start_time=self.start_time.strftime("%H:%M"),
                end_time=self.end_time.strftime("%H:%M"),
                activity=self.activity.text,
                location=self.location.text,
                notest=self.notest.text,
            )

        if not success:
            toast(error)
            return

        self.activity_dialog.dismiss()
        self.show_day_details(self.current_day)

    def go_back(self):
        """
        Navigates back to the vacations screen.
        """
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction="right")
        app.sm.current = "vacations"

        