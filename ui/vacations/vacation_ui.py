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


class VacationsScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager


        #Prima pagina
        main_layout = MDBoxLayout(orientation = 'vertical')
        top_bar = MDTopAppBar(
            title = "My Vacations",
            left_action_items = [["arrow-left", lambda x: self.go_back()]],
            elevation = 10,
            pos_hint = {"top": 1}
            
        )
        main_layout.add_widget(top_bar)

        #Adaugare vacanta noua
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


    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"

    
    def show_details_dialog(self, *args):
        content = MDBoxLayout(orientation="vertical",
    spacing=20,
    padding=(20, 60, 20, 20),  
    size_hint_y=None,
    height=250)

        self.start_btn = MDRectangleFlatButton(text = "Choose start date...")
        self.start_btn.bind(on_release = self.show_start_date_picker)
        content.add_widget(self.start_btn)

        self.end_btn = MDRectangleFlatButton(text = "Choose end date...")
        self.end_btn.bind(on_release = self.show_end_date_picker)
        content.add_widget(self.end_btn)

        # self.country_btn = MDRectangleFlatButton(text="Choose country/city...")
        # self.country_btn.bind(on_release=self.open_country_menu)
        # content.add_widget(self.country_btn)


        self.dialog = MDDialog(
            title = "Add your vacation details",
            type = "custom",
            content_cls = content,
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                #MDRaisedButton(text="Add", on_release=self.save_vacation)
            ]

        )
        self.dialog.open()


    def show_start_date_picker(self, instance):
        date_dialog = MDDatePicker(
            title = "Start date"
        )
        date_dialog.bind(on_save = self.set_start_date)
        date_dialog.open()


    def set_start_date(self, instance, value, data_range):
        self.start_date = value
        self.start_btn.text = str(value)


    def show_end_date_picker(self, instasnce):
        date_dialog = MDDatePicker(
            title = "End date"
        )
        date_dialog.bind(on_save = self.set_end_date)
        date_dialog.open()


    def set_end_date(self, instance, value, data_range):
        if value < self.start_date:
            from kivymd.toast import toast
            toast("End date must be after start date!", [0.2, 0.2, 0.2, 0.5], 1)
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.show_end_date_picker(), 1)
        else:
            self.end_date = value
            self.end_btn.text = str(value)



    
