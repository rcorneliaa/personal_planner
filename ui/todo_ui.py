"""
To-Do List screen of the Personal Planner application.

This module defines the UI and logic for managing daily to-do tasks,
including date selection, task creation, status updates, and navigation.
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


#Clasa pentru To Do listuri

class TodoScreen(MDScreen):
    """
    Screen for managing to-do tasks.

    Allows users to select a date, view tasks for that day,
    add new tasks, and mark tasks as completed or in progress.
    """

    def __init__(self, db_manager, **kwargs):
        """Initializes the To-Do screen and its UI components."""
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


    
    def show_date_picker(self, *args):
        """
        Opens a date picker dialog.

        Allows the user to select the day for which tasks will be displayed.
        """
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()


    def on_date_selected(self, instance, value, date_range):
        """
        Handles the selected date from the date picker.

        :param instance: Date picker instance
        :param value: Selected date
        :param date_range: Optional date range (unused)
        """
        self.selected_date = str(value)
        self.date_btn.text = f"Ziua: {self.selected_date}"
        self.refresh_tasks()


    
    def add_task(self, title, popup):
        if title.strip():
            self.db.add_task(title = title.strip())
            self.refresh_tasks()
            popup.dismiss()

    
    def refresh_tasks(self):
        """
        Refreshes the task list for the selected date.

        Fetches tasks from the database and updates the UI accordingly.
        """
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
        """
        Displays a dialog for adding a new task.

        Requires a date to be selected before allowing task creation.
        """
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
        """
        Adds a new task for the selected date.

        Retrieves the task title from the dialog,
        saves it to the database, and refreshes the UI.
        """
        title = self.dialog.content_cls.ids.title.text
        
        if not title.strip():
            return  
        
        self.db.add_task(title=title.strip(), deadline=self.selected_date)
        self.dialog.dismiss()
        self.refresh_tasks()


    def mark_task_done(self, task_id, value):
        """
        Updates the status of a task.

        :param task_id: ID of the task
        :param value: Checkbox state (True if completed)
        """
        if value:
            self.db.mark_task_done(task_id) 
        else:
            self.db.mark_task_in_progress(task_id)  
        self.refresh_tasks()


    def go_back(self):
        """
        Navigates back to the start screen.
        """
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"



