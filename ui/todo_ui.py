from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class TodoScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = 'vertical', **kwargs)

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

    
    def show_add_task_popup(self, instance):
        content = BoxLayout(orientation = 'vertical')
        input_title = TextInput(hint_text = "Task Title")
        btn_add = Button(text = "Add")
        btn_cancel = Button(text = "Cancel")

        btn_layout = BoxLayout(size_hint_y = None, height = 20)
        btn_layout.add_widget(btn_add)
        btn_layout.add_widget(btn_cancel)

        content.add_widget(input_title)
        content.add_widget(btn_layout)

        popup = Popup(title = "Add task", content = content, size_hint = (0.8, 0.4))

        btn_add.bind(on_release = lambda x: self.add_task(input_title.text, popup))
        btn_cancel.bind(on_release = popup.dismiss)

        popup.open()

    
    def add_task(self, title, popup):
        if title.strip():
            print("Task adăugat:", title)
            popup.dismiss()



