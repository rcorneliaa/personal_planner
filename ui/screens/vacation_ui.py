"""
Vacations screen of the Personal Planner application.

This module defines the UI and logic for managing vacations,
including date selection, destination selection, and displaying
saved vacation plans.
"""

from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineAvatarIconListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar 
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers.datepicker import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from ui.components.vacation_card import load_resized_image
from ui.components.vacation_card import ClickCard
import json
from kivy.metrics import dp
from kivymd.toast import toast
import os

class VacationsScreen(MDScreen):
    """
    Screen for managing vacation plans.

    Allows users to add new vacations by selecting dates and destinations
    and displays existing vacations as cards with images and details.
    """


    def __init__(self, vacation_services, **kwargs):
        """Initializes the Vacations screen and loads destination data."""
        super().__init__(**kwargs)
        self.vacation_services = vacation_services

        with open(r"utils\destinations.json", "r", encoding= "utf-8") as file:
            self.destination_data = json.load(file)


      
        main_layout = MDBoxLayout(orientation = 'vertical')
        top_bar = MDTopAppBar(
            title = "My Vacations",
            left_action_items = [["arrow-left", lambda x: self.go_back()]],
            # elevation = 10,
            pos_hint = {"top": 1},
            type = "top"
            
        )
        main_layout.add_widget(top_bar)

        self.scroll = MDScrollView()
        self.vacation_list = GridLayout(
        cols=2,
        spacing=10,
        padding=[0, 20, 0, 0],
        size_hint_y=None
        )
        self.vacation_list.bind(minimum_height=self.vacation_list.setter('height'))
        self.scroll.add_widget(self.vacation_list)
        main_layout.add_widget(self.scroll)


        self.add_vacation_btn = MDRaisedButton(
            icon="plus",
            text = "New Vacation",
            pos_hint={"right": 0.97, "y": 0.02},
            size_hint=(None, None),
            height="48dp",
            padding=("12dp", "10dp", "12dp", "10dp"),
            on_release = self.show_details_dialog
         
        )
        main_layout.add_widget(self.add_vacation_btn)

        self.add_widget(main_layout)
        self.refresh_vacations()


    def go_back(self):
        """
        Navigates back to the start screen.
        """
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"

    
    def show_details_dialog(self, *args):
        """
        Opens a dialog for entering vacation details.

        The user can select start date, end date, and destination.
        """
        content = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=(20, 60, 20, 20),  
            size_hint_y=None,
            height=250
            )

        self.start_btn = MDRectangleFlatButton(text = "Choose start date...")
        self.start_btn.bind(on_release = self.show_start_date_picker)
        content.add_widget(self.start_btn)

        self.end_btn = MDRectangleFlatButton(text = "Choose end date...")
        self.end_btn.bind(on_release = self.show_end_date_picker)
        content.add_widget(self.end_btn)

        self.country_btn = MDRectangleFlatButton(text="Choose country/city...")
        self.country_btn.bind(on_release=self.open_country_menu)
        content.add_widget(self.country_btn)


        self.dialog = MDDialog(
            title = "Add your vacation details",
            type = "custom",
            content_cls = content,
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Save", on_release=self.add_vacation)
            ]

        )
        self.dialog.open()


    def show_start_date_picker(self, instance):
        """
        Opens a date picker for selecting the vacation start date.
        """
        date_dialog = MDDatePicker(
            title = "Start date"
        )
        date_dialog.bind(on_save = self.set_start_date)
        date_dialog.open()


    def set_start_date(self, instance, value, data_range):
        """
        Sets the selected start date.

        :param instance: Date picker instance
        :param value: Selected start date
        :param data_range: Optional date range (unused)
        """
        self.start_date = value
        self.start_btn.text = str(value)


    def show_end_date_picker(self, *args):
        """
        Opens a date picker for selecting the vacation end date.
        """
        date_dialog = MDDatePicker(
            title = "End date"
        )
        date_dialog.bind(on_save = self.set_end_date)
        date_dialog.open()


    def set_end_date(self, instance, value, data_range):
        """
        Sets the selected end date and validates it.

        Ensures that the end date is after the start date.
        """
        if value < self.start_date:
            toast("End date must be after start date!", [0.2, 0.2, 0.2, 0.5], 1)
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.show_end_date_picker(), 1)
        else:
            self.end_date = value
            self.end_btn.text = str(value)

    def open_country_menu(self, instance):
        """
        Opens a dropdown menu for selecting a country.
        """
        menu_items = [
            {"text": country,
             "viewclass": "OneLineListItem",
             "on_release": lambda x = country: self.select_country(x)
             } for country in self.destination_data.keys()  
        ]

        self.country_menu = MDDropdownMenu(
            caller = instance,
            items = menu_items,
            width_mult = 4
        )

        self.country_menu.open()

    def select_country(self, country):
        """
        Stores the selected country and opens the city menu.

        :param country: Selected country name
        """
        self.selected_country = country
        self.country_menu.dismiss()
        self.open_city_menu(country)

    def open_city_menu(self, country):
        """
        Opens a dropdown menu for selecting a city.

        :param country: Selected country
        """
        city_items = [
            {"text": city["city"],
             "viewclass": "OneLineListItem",
             "on_release": lambda x = city["city"]: self.select_city(x)
             }for city in self.destination_data[country]
        ]

        self.city_menu = MDDropdownMenu(
            caller = self.country_btn,
            items = city_items,
            width_mult = 4
        )

        self.city_menu.open()

    def select_city(self, city):
        """
        Stores the selected city and updates the UI.

        :param city: Selected city name
        """
        self.selected_city = city
        self.country_btn.text = f"{self.selected_country}, {city}"
        self.city_menu.dismiss()



    
    def add_vacation(self, *args):
        """
        Saves a new vacation to the database.

        Validates that all required details are selected
        before persisting the vacation.
        """
        if not hasattr(self, "start_date") or not hasattr(self, "end_date"):
            toast("Please select both start and end dates!", [0.2, 0.2, 0.2, 0.5], 1)
            return
        if not hasattr(self, "selected_country") or not hasattr(self, "selected_city"):
            toast("Please select a country and a city!", [0.2, 0.2, 0.2, 0.5], 1)
            return
    
        destination = f"{self.selected_country}, {self.selected_city}"
        start_date = str(self.start_date)
        end_date = str(self.end_date)
        succes = self.vacation_services.add_vacation(destination, start_date, end_date)
        if succes:
            self.dialog.dismiss()
            self.refresh_vacations()


    def refresh_vacations(self):
        """
        Refreshes the list of vacations displayed on screen.

        Retrieves vacations from the database and displays
        them as cards with images and destination labels.
        """

        self.vacation_list.clear_widgets()
        vacations = self.vacation_services.get_vacations()
        for vac in vacations:
            country, city = vac.destination.split(", ")
            picture_path = ""
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            if country in self.destination_data:
                for c in self.destination_data[country]:
                    if c["city"] == city:
                        picture = c.get("picture", "")
                        if picture:
                            picture_path = os.path.join(BASE_DIR, picture)
                            print("Calea imaginii:", picture_path)
                        break
            card = ClickCard(
                vacation= vac,
                orientation = "vertical",
                size_hint = (None, None),
                size=(dp(400), dp(300)),
                elevation = 1,
                padding = 20,
            
            )

            if picture_path and os.path.exists(picture_path):
                texture = load_resized_image(picture_path, 400, 300)
                img = Image(texture = texture, size_hint=(1, None), height=dp(240), allow_stretch = True, keep_ratio = True)
                card.add_widget(img)
            
            destination = vac.destination
            label = MDLabel(
                text=destination,
                halign="center",
                size_hint=(1, None),
                height=dp(40)
                
        
            )
            card.add_widget(label)
            self.vacation_list.add_widget(card)
    
   






    
