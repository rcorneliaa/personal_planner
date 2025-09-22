from PIL import Image as PILImage
from kivymd.app import MDApp
from kivy.core.image import Image as CoreImage
from kivymd.uix.card import MDCard

import io

class ClickCard(MDCard):
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.go_to_detail()
        return super().on_touch_up(touch)
    def go_to_detail(self):
        app = MDApp.get_running_app()
        app.sm.current = "vacation_details" 


def load_resized_image(path, width, height):
    pil_img = PILImage.open(path)
    pil_img.thumbnail((width, height), PILImage.Resampling.LANCZOS)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    buf.seek(0)
    return CoreImage(buf, ext="png").texture