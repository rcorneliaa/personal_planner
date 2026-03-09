"""
To-Do List screen of the Personal Planner application.

This module defines the UI and logic for managing daily to-do tasks,
including date selection, task creation, status updates, and navigation.
"""

from datetime import timedelta
from kivymd.uix.gridlayout import GridLayout
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




class TodoScreen(MDScreen):
    """
    Screen for managing to-do tasks.

    Allows users to select a date, view tasks for that day,
    add new tasks, and mark tasks as completed or in progress.
    """

    def __init__(self, task_services, **kwargs):
        """Initializes the To-Do screen and its UI components."""
        super().__init__(**kwargs)
        self.task_services = task_services
        self.selected_date = None


        
   
        main_layout = MDBoxLayout(orientation='vertical', spacing=10, padding=10)

        top_bar = MDTopAppBar(
            title="To-Do List",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=10
        )
        main_layout.add_widget(top_bar)

        scroll = MDScrollView()
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        content.bind(minimum_height=content.setter('height')) 

        # ================= DATE SELECTION =================
        self.date_btn = MDRaisedButton(
            text="Choose Day",
            size_hint=(None, None),
            size=(150, 40),
            pos_hint={"center_x": 0.5},
            on_release=self.show_date_picker
        )
        content.add_widget(self.date_btn)

        # ================= TASKS =================
        self.task_list = MDBoxLayout(orientation='vertical', spacing=5, size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        content.add_widget(MDLabel(text="Tasks", halign="center", size_hint_y=None, height=40, theme_text_color="Custom", text_color=(0.5, 0, 0.5, 1)))
        content.add_widget(self.task_list)

        # Buton adaugare task
        self.add_task_btn = MDRaisedButton(text="Add Task", size_hint_y=None, pos_hint={"center_x": 0.5}, height=40)
        self.add_task_btn.bind(on_release=self.show_add_task_dialog)
        content.add_widget(self.add_task_btn)

        # ================= HABITS =================
        self.habits_title = MDLabel(
            text="Habits (Weekly)",
            halign="center",
            theme_text_color="Custom",
            text_color=(0.5, 0, 0.5, 1),
            size_hint_y=None,
            height="40dp"
        )
        content.add_widget(self.habits_title)

      
        self.habit_table = GridLayout(cols=9, size_hint_y=None, row_default_height=40, spacing=5)
        self.habit_table.bind(minimum_height=self.habit_table.setter('height'))
        content.add_widget(self.habit_table)

      
        self.add_habit_btn = MDRaisedButton(
            text="Add Habit",
            pos_hint={"center_x": 0.5},
            size_hint_y=None,
            height=40,
            on_release=self.show_add_habit_dialog
        )
        content.add_widget(self.add_habit_btn)

      
        scroll.add_widget(content)
        main_layout.add_widget(scroll)

     
        self.add_widget(main_layout)
        self.refresh_tasks()
        self.refresh_habits()


    
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
        self.selected_date = value
        self.date_btn.text = f"{self.selected_date}"
        self.refresh_tasks()
        self.refresh_habits()


    
    def refresh_tasks(self):
        """
        Refreshes the task list for the selected date.

        Fetches tasks from TaskService and updates the display.
        """
        self.task_list.clear_widgets()
        if not self.selected_date:
            return
        
        tasks = self.task_services.get_tasks_by_date(self.selected_date)
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
        Handles adding a new task from the dialog.

        Calls TaskService to add the task to the database,
        dismisses the dialog, and refreshes the task list in the UI.
        """
        title = self.dialog.content_cls.ids.title.text
        succes = self.task_services.add_task(title, self.selected_date)
        if succes:
            self.dialog.dismiss()
            self.refresh_tasks()


    def mark_task_done(self, task_id, value):
        """
        Updates task status via TaskService and refreshes UI.

        :param task_id: ID of the task
        :param value: True if task is completed
        """
        if value:
            self.task_services.mark_task_done(task_id) 
        else:
            self.task_services.mark_task_in_progress(task_id)  
        self.refresh_tasks()

    def show_add_habit_dialog(self, *args):
        """
        Displays a dialog for adding a new habit.

        Requires a date to be selected before allowing habit creation.
        """
        if not self.selected_date:
            self.date_btn.text = "Choose a day!"
            return
        
        content = MDBoxLayout(
            orientation = "vertical",
            spacing = 10,
            size_hint_y = None,
            height = "150dp"
        )

        self.habit_title_field = MDTextField(
            hint_text = "Title",
            size_hint_y = None,
            height = "400dp"
        )
        self.habit_goal_field = MDTextField(
        hint_text = "Weekly Goal (1-7)",
        size_hint_y = None,
        height = "40dp",
        input_filter = "int"
    )
        content.add_widget(self.habit_title_field)
        content.add_widget(self.habit_goal_field)

       
        
        self.dialog = MDDialog(
            title="Add Habit",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="Cancel", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Add", on_release=self.add_habit)
            ]
        )
        self.dialog.open()

    def add_habit(self, *args):
        """
        Handles adding a new habit from the dialog.

        Calls TaskService to add the habit to the database,
        dismisses the dialog, and refreshes the habit table in the UI.
        """
        title = self.habit_title_field.text
        try:
            goal = int(self.habit_goal_field.text)
        except ValueError:
            goal = 1
        goal = max(1, min(goal, 7))
        succes = self.task_services.add_habit(title, goal)
        if succes:
            self.dialog.dismiss()
            self.refresh_habit()

    def refresh_habits(self):
        """Refreshes the habits table for the selected week."""
        self.habit_table.clear_widgets()

        if not self.selected_date:
            return

        week_start = self.get_week_start(self.selected_date)
        habits = self.task_services.get_habits(week_start)

        grid = GridLayout(cols=11, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter("height"))

        # Header
        grid.add_widget(MDLabel(text="Habit", bold=True))
        for i in range(7):
            day = week_start + timedelta(days=i)
            grid.add_widget(MDLabel(text=day.strftime("%a")[0], bold=True))
        grid.add_widget(MDLabel(text="Goal", bold=True))
        grid.add_widget(MDLabel(text="Done", bold=True))
        grid.add_widget(MDLabel(text="Del", bold=True))

      
        for habit in habits:
            achieved = len([v for v in habit["logs"].values() if v])
            grid.add_widget(MDLabel(text=habit["title"]))

            for i in range(7):
                day = week_start + timedelta(days=i)
                day_str = day.strftime("%Y-%m-%d")

                def make_callback(habit_id, date_str, btn_color_ref):
                    return lambda x: self.toggle_day_ui(habit_id, date_str, btn_color_ref)

                btn = MDFlatButton(
                md_bg_color=self.get_habit_color(habit, day_str)
            )
                btn.bind(on_release=make_callback(habit["id"], day_str, btn))

                grid.add_widget(btn)

            grid.add_widget(MDLabel(text=str(habit["weekly_goal"])))
            grid.add_widget(MDLabel(text=str(achieved)))

            def make_del_callback(habit_id):
                return lambda x: self.delete_habit(habit_id)
            
            del_btn = MDIconButton(icon="delete", on_release=make_del_callback(habit["id"]))
            grid.add_widget(del_btn)

        self.habit_table.add_widget(grid)

    def get_week_start(self, date_obj):
        return date_obj - timedelta(days=date_obj.weekday())
    
    def get_habit_color(self, habit, day_str):
       
        return [0.6, 0, 0.8, 1] if habit["logs"].get(day_str) else [1, 1, 1, 1]

    
    def toggle_day_ui(self, habit_id, day_str, btn):
        """Toggle habit log in DB și schimbă culoarea imediat."""
        self.task_services.toggle_day(habit_id, day_str)
        week_start = self.get_week_start(self.selected_date)
        habits = self.task_services.get_habits(week_start)
        habit = next(h for h in habits if h["id"] == habit_id)
        
        # Folosește aceeași funcție pentru consistență
        btn.md_bg_color = self.get_habit_color(habit, day_str)


    def go_back(self):
        """
        Navigates back to the start screen.
        """
        app = MDApp.get_running_app()
        app.sm.transition = SlideTransition(direction='right')
        app.sm.current = "start"





    



