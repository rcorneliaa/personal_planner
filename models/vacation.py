from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.animation import Animation

class Vacation:
    """
    Represents a vacation entity.

    Attributes:
        id (int): Unique identifier of the vacation
        destination (str): Vacation destination (country, city)
        start_date (str | date): Start date of the vacation
        end_date (str | date): End date of the vacation
    """

    def __init__(self, id,destination, start_date, end_date):
        self.id = id
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date


class Itinerary:
    """
    Represents an activity planned during a vacation day.
    """
    def __init__(self, id, vacation_id, day, start_time, end_time, activity, location, notest):
        self.id = id
        self.vacation_id = vacation_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity
        self.location = location
        self.notest = notest

class ActivityCard(MDCard):
    """
    Custom UI card used to display a vacation activity.

    Provides:
    - Activity details (time, name, location, notes)
    - Delete functionality with confirmation dialog
    """

    def __init__(self, activity_data, db = None, screen = None, **kwargs):
        """
        Initializes an activity card.

        :param activity_data: Activity data object
        :param db: Database manager instance
        :param screen: Parent screen reference
        """
        super().__init__(**kwargs)
        self.activity_data = activity_data
        self.db = db
        self.screen = screen
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
        if self.db:
            success = self.db.delete_activity(self.activity_data.id)
        else:
            success = True 

        if success:
            anim = Animation(opacity=0, duration=0.2)
            anim.bind(on_complete=lambda *a: self.remove_from_parent())
            anim.start(self)

    def remove_from_parent(self):
        """
        Removes the card from its parent layout.
        """
        if self.parent and self.screen:
            self.parent.remove_widget(self)

    # def edit_activity(self, *args):
    
    #     if not self.parent_screen:
    #         return

    #     self.parent_screen.show_details_dialog(
    #         edit_mode=True,
    #         existing_activity=self.activity,
    #         card=self
    #     )

        