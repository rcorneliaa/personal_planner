from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner


class TodoScreen(BoxLayout):
    def __init__(self, db_manager, **kwargs):
        super().__init__(orientation = 'vertical', **kwargs)
        self.db = db_manager

        #TASK ZONE
        self.task_list = GridLayout(cols = 1, size_hint_y = None)
        self.task_list.bind(minimum_height = self.task_list.setter('height'))

        #SCROLLVIEW
        self.scroll  = ScrollView()
        self.scroll.add_widget(self.task_list)
        self.add_widget(self.scroll)

        #ADD BUTTON
        add_button = Button(text = "Add Task", size_hint_y = None, height = 40)
        self.add_widget(add_button)
        add_button.bind(on_release=self.show_add_task_popup)
        self.refresh_tasks()

    
    def show_add_task_popup(self, instance):
        content = BoxLayout(orientation = 'vertical', spacing=10, padding=10)
        
        input_title = TextInput(hint_text = "Task Title", multiline = False)
        input_desc = TextInput(hint_text="Descriere (opțional)", multiline=True, size_hint_y=None, height=80)
        priority_spinner = Spinner(
        text="medium",
        values=["low", "medium", "high"],
        size_hint_y=None,
        height=40
    )

        btn_add = Button(text = "Add")
        btn_cancel = Button(text = "Cancel")

        btn_layout = BoxLayout(size_hint_y = None, height = 20)
        btn_layout.add_widget(btn_add)
        btn_layout.add_widget(btn_cancel)

        content.add_widget(input_title)
        content.add_widget(input_desc)
        content.add_widget(priority_spinner)
        content.add_widget(btn_layout)

        popup = Popup(title = "Add task", content = content, size_hint = (0.8, 0.4))

        btn_add.bind(on_release=lambda x: self.add_task(
        input_title.text,
        input_desc.text,
        priority_spinner.text,
        popup
        ))
        btn_cancel.bind(on_release=popup.dismiss)

        popup.open()

    
    def add_task(self, title, description, priority, popup):
        if title.strip():
            self.db.add_task(title = title.strip(), description = description.strip(), priority = priority)
            self.refresh_tasks()
            popup.dismiss()


    def refresh_tasks(self):
        self.task_list.clear_widgets()

        tasks = self.db.get_tasks()
        for task in tasks:
            btn = Button(
            text=str(task),
            size_hint_y=None,
            height=40
        )
            btn.bind(on_release=lambda _, t=task: self.show_task_details(t))
            self.task_list.add_widget(btn)
        

    def show_task_details(self, task):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title_label = Label(text=f"Titlu: {task.title}", size_hint_y=None, height=30)
        desc_label = Label(text=f"Descriere: {task.description or '-'}", size_hint_y=None, height=30)
        status_label = Label(text=f"Status: {task.status}", size_hint_y=None, height=30)

        mark_done_btn = Button(text="Marchează ca finalizat", size_hint_y=None, height=40)
        close_btn = Button(text="Închide", size_hint_y=None, height=40)

        btns = BoxLayout(size_hint_y=None, height=40)
        btns.add_widget(mark_done_btn)
        btns.add_widget(close_btn)

        content.add_widget(title_label)
        content.add_widget(desc_label)
        content.add_widget(status_label)
        content.add_widget(btns)

        popup = Popup(title="Detalii Task", content=content, size_hint=(0.85, 0.5))

        mark_done_btn.bind(on_release=lambda x: self.mark_task_done(task.id, popup))
        close_btn.bind(on_release=popup.dismiss)

        popup.open()

    def mark_task_done(self, task_id, popup):
        self.db.mark_task_done(task_id)
        popup.dismiss()
        self.refresh_tasks()



