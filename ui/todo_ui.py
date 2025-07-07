from kivymd.app import MDApp
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.toolbar import MDTopAppBar 
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import (
    MDButton,
    MDButtonIcon,
    MDButtonText,
    MDIconButton,
)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers.datepicker import MDDatePicker


class TodoScreen(MDScreen):
    def __init__(self, db_manager, **kwargs):
        super().__init__(**kwargs)
        self.db = db_manager
        self.selected_date = None

        main_layout = MDBoxLayout(orientation='vertical')
        top_bar = MDTopAppBar(
            title="To-Do List",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=10
        )
        main_layout.add_widget(top_bar)

        # Buton selectat dată
        self.date_btn = MDButton(
            text="Choose Day",
            size_hint=(None, None),
            style="elevated",
            size=(150, 40),
            pos_hint={"center_x": 0.5},
            on_release=self.show_date_picker
        )
        main_layout.add_widget(self.date_btn)


        self.scroll = MDScrollView()
        self.task_list = MDList()
        self.scroll.add_widget(self.task_list)
        main_layout.add_widget(self.scroll)

        self.add_btn = MDButton(
            MDButtonIcon(icon="plus"),
            MDButtonText(text="Add Task"),
            style="elevated",
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

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()


    def on_date_selected(self, instance, value, date_range):
        self.selected_date = str(value)
        self.date_btn.text = f"Ziua: {self.selected_date}"
        self.refresh_tasks()

    
    def add_task(self, title, description, priority, popup):
        if title.strip():
            self.db.add_task(title = title.strip(), description = description.strip(), priority = priority)
            self.refresh_tasks()
            popup.dismiss()


    def refresh_tasks(self):
        self.task_list.clear_widgets()
        if not self.selected_date:
            return
        tasks = self.db.get_tasks_by_date(self.selected_date)
        for task in tasks:
            self.task_list.add_widget(
                OneLineListItem(text=f"{task.title} [{task.priority}]")
            )

        
    def show_add_task_dialog(self, *args):
        if not self.selected_date:
            self.date_btn.text = "Alege mai întâi o zi!"
            return
        
        self.dialog = MDDialog(
            title="Adaugă task",
            type="custom",
            content_cls=MDBoxLayout(
                MDTextField(hint_text="Titlu task", id="title"),
                MDTextField(hint_text="Descriere", id="desc"),
                MDTextField(hint_text="Prioritate (ex: low, medium, high)", id="priority"),
                orientation="vertical",
                spacing=10,
                size_hint_y=None,
                height="150dp",
            ),
            buttons=[
                MDButton(text="Anulează", on_release=lambda x: self.dialog.dismiss()),
                MDButton(text="Adaugă", on_release=self.add_task)
            ]
        )
        self.dialog.open()

    def add_task(self, *args):
        title = self.dialog.content_cls.ids.title.text
        description = self.dialog.content_cls.ids.desc.text
        priority = self.dialog.content_cls.ids.priority.text or "medium"
        
        if not title.strip():
            return  
        
        self.db.add_task(title=title.strip(), description=description.strip(), deadline=self.selected_date, priority=priority)
        self.dialog.dismiss()
        self.refresh_tasks()


    def mark_task_done(self, task_id, popup):
        self.db.mark_task_done(task_id)
        popup.dismiss()
        self.refresh_tasks()


    def go_back(self):
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"



