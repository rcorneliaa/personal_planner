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
            text = "New Vacation",
            size_hint = (None, None),
            size = (150,40),
            pos_hint = {"center_x": 0.8},
            on_release = self.show_date_picker
         
        )
        main_layout.add_widget(self.add_vacation_btn)

        self.add_widget(main_layout)


    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"


    def show_date_picker(self, *args):
        date_dialog = MDDatePicker(
            title = "Choose start date"
        )
        date_dialog.open()

    
