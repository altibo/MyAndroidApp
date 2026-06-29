from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

__version__ = "0.1.0"


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.10, 0.13, 0.20, 1)
            self.background = RoundedRectangle(radius=[dp(24)])
        self.bind(pos=self._update_background, size=self._update_background)

    def _update_background(self, *_):
        self.background.pos = self.pos
        self.background.size = self.size


class MyAndroidApp(App):
    count = 0

    def build(self):
        self.title = "MyAndroidApp"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(18),
        )

        root.add_widget(Widget(size_hint_y=0.2))

        card = Card(
            orientation="vertical",
            padding=dp(28),
            spacing=dp(18),
            size_hint_y=None,
            height=dp(380),
        )
        card.add_widget(
            Label(
                text="[b]Hallo Android![/b]",
                markup=True,
                font_size="32sp",
                color=(0.96, 0.97, 1, 1),
            )
        )
        card.add_widget(
            Label(
                text="Eine kleine Python-App,\ngebaut mit Kivy und Buildozer.",
                halign="center",
                font_size="18sp",
                color=(0.68, 0.72, 0.82, 1),
            )
        )

        self.counter_label = Label(
            text="Noch nicht gedrückt",
            font_size="17sp",
            color=(0.52, 0.84, 1, 1),
        )
        card.add_widget(self.counter_label)

        button = Button(
            text="Drück mich",
            size_hint_y=None,
            height=dp(58),
            background_normal="",
            background_color=(0.22, 0.54, 0.96, 1),
            font_size="18sp",
        )
        button.bind(on_release=self.increment)
        card.add_widget(button)

        root.add_widget(card)
        root.add_widget(
            Label(
                text=f"Version {__version__}",
                size_hint_y=0.2,
                color=(0.48, 0.52, 0.62, 1),
                font_size="14sp",
            )
        )
        return root

    def increment(self, *_):
        self.count += 1
        self.counter_label.text = f"{self.count} Mal gedrückt"


if __name__ == "__main__":
    MyAndroidApp().run()
