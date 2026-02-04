from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog


class ActivityCard(MDCard):
    """
    Custom UI card used to display a vacation activity.

    Provides:
    - Activity details (time, name, location, notes)
    - Delete functionality with confirmation dialog
    """

    def __init__(self, activity_data, on_delete = None, on_edit = None, **kwargs):
        """
        Initializes an activity card.

        :param activity_data: Activity data object
        :param db: Database manager instance
        :param screen: Parent screen reference
        """
        super().__init__(**kwargs)
        self.activity_data = activity_data
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.orientation = "vertical"
        self.size_hint = (0.9, None)
        self.height = dp(140)
        self.padding = 40
        self.spacing = dp(6)
        self.radius = [10]
        self.pos_hint = {"center_x": 0.5}

        main_layout = MDBoxLayout(orientation="vertical", spacing=dp(6))

        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(24))

        header.add_widget(
            MDLabel(
                text=f"[b]{activity_data.start_time}[/b] - [b]{activity_data.end_time}[/b]",
                markup=True,
                theme_text_color= "Primary",
            )
        )

        
        header.add_widget(
            MDIconButton(
                icon="delete",
                # theme_text_color="Custom",
                # text_color=(0.6, 0, 0, 1),
                pos_hint={"center_y": 0.5},
                on_release=self.confirm_delete,
            )
        )

        header.add_widget(
            MDIconButton(
                icon="pencil",
                # theme_text_color="Custom",
                # text_color=(0.6, 0, 0, 1),
                pos_hint={"center_y": 0.5},
                on_release=self.edit_activity,
            )
        )

        main_layout.add_widget(header)

        main_layout.add_widget(
            MDLabel(
                text=f"[b]Activity[/b]: {activity_data.activity or 'No activity name'}",
                markup=True,
                halign="left",
                theme_text_color="Secondary",
            )
        )
        if activity_data.location:
            main_layout.add_widget(
                MDLabel(
                    text=f"Location: {activity_data.location}",
                    halign="left",
                    theme_text_color="Hint",
                )
            )

        if activity_data.notest:
            main_layout.add_widget(
                MDLabel(
                    text=f"Details: {activity_data.notest}",
                    halign="left",
                    theme_text_color="Hint",
                )
            )

        self.add_widget(main_layout)

    def confirm_delete(self, *args):
        """
        Opens a confirmation dialog before deleting the activity.
        """
        self.confirm_dialog = MDDialog(
        title="Confirmare",
        text=f"Ștergi activitatea „{self.activity_data.activity}”?",
        buttons=[
            MDRaisedButton(text="Anulează", on_release=lambda x: self.confirm_dialog.dismiss()),
            MDRaisedButton(text="Șterge", on_release=lambda x: self.delete_activity())
        ],
    )
        self.confirm_dialog.open()


    def delete_activity(self, *args):
        """
        Deletes the activity from the database and removes the card with animation.
        """
        self.confirm_dialog.dismiss()
        if self.on_delete:
            self.on_delete(self.activity_data.id, self)
        
        


    def edit_activity(self, *args):
    
        if self.on_edit:
            self.on_edit(self.activity_data)