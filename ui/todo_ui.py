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


#Clasa pentru To Do listuri

class TodoScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager
        self.selected_date = None


        #Prima pagina
        main_layout = MDBoxLayout(orientation='vertical')
        top_bar = MDTopAppBar(
            title="To-Do List",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=10
        )
        main_layout.add_widget(top_bar)

        #Selectare data        
        self.date_btn = MDRaisedButton(
            text="Choose Day",
            size_hint=(None, None),
            
            size=(150, 40),
            pos_hint={"center_x": 0.5},
            on_release=self.show_date_picker
        )
        main_layout.add_widget(self.date_btn)


        self.scroll = MDScrollView()
        self.task_list = MDList()
        self.scroll.add_widget(self.task_list)
        main_layout.add_widget(self.scroll)


        #Buton de Adauga Task
        self.add_btn = MDRaisedButton(
            icon="plus",
            text="Add Task",    
            pos_hint={"right": 0.97, "y": 0.02},
            size_hint=(None, None),
            height="48dp",
            padding=("12dp", "10dp", "12dp", "10dp"),
            on_release=self.show_add_task_dialog
        )
        self.add_btn.bind(on_release=self.show_add_task_dialog)
        main_layout.add_widget(self.add_btn)
        
        self.add_widget(main_layout)

        self.refresh_tasks()


    #De ales data
    def show_date_picker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()


    def on_date_selected(self, instance, value, date_range):
        self.selected_date = str(value)
        self.date_btn.text = f"Ziua: {self.selected_date}"
        self.refresh_tasks()


    #Functia sa adaug task
    def add_task(self, title, popup):
        if title.strip():
            self.db.add_task(title = title.strip())
            self.refresh_tasks()
            popup.dismiss()

    #REFRESHHHHHH PT TASK
    def refresh_tasks(self):
        self.task_list.clear_widgets()
        if not self.selected_date:
            return
        
        tasks = self.db.get_tasks_by_date(self.selected_date)
        for task in tasks:
            row = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height="40dp")

        
            checkbox = MDCheckbox(active=(task.status.lower() == "done"))
            checkbox.bind(active=lambda cb, value, task_id=task.id: self.mark_task_done(task_id, value))

            label = MDLabel(text=task.title)
          
            row.add_widget(checkbox)
            row.add_widget(label)

            self.task_list.add_widget(row)

        
    def show_add_task_dialog(self, *args):
        if not self.selected_date:
            self.date_btn.text = "Choose a day!"
            return
        
        self.dialog = MDDialog(
            title="Add Task",
            type="custom",
            content_cls=MDBoxLayout(
                MDTextField(hint_text="Title", id="title"),
                orientation="vertical",
                spacing=10,
                size_hint_y=None,
                height="150dp",
            ),
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Add", on_release=self.add_task)
            ]
        )
        self.dialog.open()


    def add_task(self, *args):
        title = self.dialog.content_cls.ids.title.text
        
        if not title.strip():
            return  
        
        self.db.add_task(title=title.strip(), deadline=self.selected_date)
        self.dialog.dismiss()
        self.refresh_tasks()


    def mark_task_done(self, task_id, value):
        if value:
            self.db.mark_task_done(task_id) 
        else:
            self.db.mark_task_in_progress(task_id)  
        self.refresh_tasks()


    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"



