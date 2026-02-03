from PIL import Image as PILImage
from kivymd.app import MDApp
from kivy.core.image import Image as CoreImage
from kivymd.uix.card import MDCard
from kivy.uix.screenmanager import SlideTransition

import io

class ClickCard(MDCard):
    """
    Custom clickable card used to open vacation details screen.

    When clicked, it navigates to the vacation details screen
    and passes the selected vacation object.
    """
    def __init__(self, vacation = None, **kwargs):
        """
        :param vacation: Vacation object associated with this card
        """
        super().__init__(**kwargs)
        self.vacation = vacation

    def on_touch_down(self, touch):
        """
        Handles touch down event to detect card click.
        """
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """
        Handles touch release and triggers navigation if clicked.
        """
        if touch.grab_current is self:
            touch.ungrab(self)
            self.go_to_detail()
            return True
        return super().on_touch_up(touch)
        
    def go_to_detail(self):
        """
        Navigates to the vacation details screen.
        """
        app = MDApp.get_running_app()
        app.root.get_screen("vacation_details").set_vacation(self.vacation)
        app.sm.transition = SlideTransition(direction="left")
        app.sm.current = "vacation_details" 


def load_resized_image(path, width, height):
    """
    Loads and resizes an image for use in Kivy UI.

    The image is resized using PIL and converted into
    a Kivy-compatible texture.

    :param path: Path to the image file
    :param width: Target width
    :param height: Target height
    :return: Kivy texture
    """
    pil_img = PILImage.open(path)
    pil_img.thumbnail((width, height), PILImage.Resampling.LANCZOS)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    return CoreImage(buf, ext="png").texture