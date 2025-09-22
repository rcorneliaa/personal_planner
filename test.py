from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App

class MyApp(App):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # sau "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        layout = AnchorLayout()

        with layout.canvas:
            Color(*self.theme_cls.primary_color)
            self.rect = Rectangle(pos=layout.pos, size=layout.size)

        return layout

MyApp().run()