from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.utils import platform
from kivy_garden.mapview import MapMarker, MapSource, MapView
from plyer import gps

__version__ = "0.2.0"


class UserMarker(MapMarker):
    """A high-contrast position marker drawn without an image asset."""

    def __init__(self, **kwargs):
        kwargs.setdefault("source", "")
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("size", (dp(30), dp(30)))
        kwargs.setdefault("anchor_x", 0.5)
        kwargs.setdefault("anchor_y", 0.5)
        super().__init__(**kwargs)

        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.outer_circle = Ellipse()
            Color(0.04, 0.04, 0.04, 1)
            self.inner_circle = Ellipse()
        self.bind(pos=self._update_marker, size=self._update_marker)
        self._update_marker()

    def _update_marker(self, *_):
        self.outer_circle.pos = self.pos
        self.outer_circle.size = self.size
        inset = dp(7)
        self.inner_circle.pos = (self.x + inset, self.y + inset)
        self.inner_circle.size = (self.width - 2 * inset, self.height - 2 * inset)


class OverlayLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.04, 0.04, 0.04, 0.90)
            self.background = RoundedRectangle(radius=[dp(16)])
        self.bind(pos=self._update_background, size=self._update_background)

    def _update_background(self, *_):
        self.background.pos = self.pos
        self.background.size = self.size


class LocationButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0.04, 0.04, 0.04, 0.96)
            self.background = RoundedRectangle(radius=[dp(25)])
        self.bind(pos=self._update_background, size=self._update_background)

    def _update_background(self, *_):
        self.background.pos = self.pos
        self.background.size = self.size


class MyAndroidApp(App):
    user_location = None
    user_marker = None
    gps_running = False
    location_permission_granted = False
    centered_once = False

    def build(self):
        self.title = "MyAndroidApp"

        monochrome_osm = MapSource(
            url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
            cache_key="carto-light-osm",
            min_zoom=2,
            max_zoom=20,
            tile_size=256,
            image_ext="png",
            attribution="© OpenStreetMap contributors © CARTO",
            subdomains="abcd",
        )

        root = FloatLayout()
        self.map_view = MapView(
            lat=51.1657,
            lon=10.4515,
            zoom=6,
            map_source=monochrome_osm,
            double_tap_zoom=True,
        )
        root.add_widget(self.map_view)

        self.status_label = OverlayLabel(
            text="Standort wird vorbereitet …",
            color=(1, 1, 1, 1),
            font_size="14sp",
            size_hint=(None, None),
            size=(dp(230), dp(44)),
            pos_hint={"center_x": 0.5, "top": 0.97},
        )
        root.add_widget(self.status_label)

        attribution = Label(
            text="© OpenStreetMap · © CARTO",
            color=(0.1, 0.1, 0.1, 0.9),
            font_size="10sp",
            size_hint=(None, None),
            size=(dp(180), dp(28)),
            pos_hint={"x": 0.02, "y": 0.015},
        )
        root.add_widget(attribution)

        location_button = LocationButton(
            text="◎",
            color=(1, 1, 1, 1),
            font_size="29sp",
            size_hint=(None, None),
            size=(dp(54), dp(54)),
            pos_hint={"right": 0.95, "y": 0.055},
        )
        location_button.bind(on_release=self.center_on_user)
        root.add_widget(location_button)

        return root

    def on_start(self):
        if platform == "android":
            from android.permissions import Permission, request_permissions

            request_permissions(
                [
                    Permission.ACCESS_COARSE_LOCATION,
                    Permission.ACCESS_FINE_LOCATION,
                ],
                self._on_permission_result,
            )
        else:
            self._set_status("GPS ist auf Android verfügbar")

    def _on_permission_result(self, _permissions, grants):
        self.location_permission_granted = all(grants)
        if self.location_permission_granted:
            Clock.schedule_once(lambda _dt: self._start_gps())
        else:
            Clock.schedule_once(
                lambda _dt: self._set_status("Standortzugriff wurde abgelehnt")
            )

    def _start_gps(self):
        if self.gps_running:
            return
        try:
            gps.configure(
                on_location=self._on_location,
                on_status=self._on_gps_status,
            )
            gps.start(minTime=1000, minDistance=1)
            self.gps_running = True
            self._set_status("Standort wird gesucht …")
        except NotImplementedError:
            self._set_status("GPS wird auf diesem Gerät nicht unterstützt")
        except Exception as error:
            print(f"GPS konnte nicht gestartet werden: {error}")
            self._set_status("GPS konnte nicht gestartet werden")

    @mainthread
    def _on_location(self, **location):
        latitude = location.get("lat")
        longitude = location.get("lon")
        if latitude is None or longitude is None:
            return

        latitude = float(latitude)
        longitude = float(longitude)
        self.user_location = (latitude, longitude)

        if self.user_marker is None:
            self.user_marker = UserMarker(lat=latitude, lon=longitude)
            self.map_view.add_marker(self.user_marker)
        else:
            self.user_marker.lat = latitude
            self.user_marker.lon = longitude
            if self.user_marker._layer:
                self.user_marker._layer.reposition()

        accuracy = location.get("accuracy")
        if accuracy is not None:
            self._set_status(f"Standortgenauigkeit: ±{float(accuracy):.0f} m")
        else:
            self._set_status("Standort gefunden")

        if not self.centered_once:
            self.centered_once = True
            self.center_on_user()

    @mainthread
    def _on_gps_status(self, status_type, status_message):
        if status_type == "provider-disabled":
            self._set_status("Bitte GPS am Gerät einschalten")
        elif status_message:
            print(f"GPS-Status: {status_type}: {status_message}")

    def center_on_user(self, *_):
        if self.user_location is None:
            self._set_status("Standort wird noch gesucht …")
            return

        latitude, longitude = self.user_location
        if self.map_view.zoom < 16:
            self.map_view.zoom = 16
        self.map_view.center_on(latitude, longitude)

    def _set_status(self, message):
        self.status_label.text = message

    def _stop_gps(self):
        if not self.gps_running:
            return
        try:
            gps.stop()
        except Exception as error:
            print(f"GPS konnte nicht gestoppt werden: {error}")
        finally:
            self.gps_running = False

    def on_pause(self):
        self._stop_gps()
        return True

    def on_resume(self):
        if self.location_permission_granted:
            Clock.schedule_once(lambda _dt: self._start_gps())

    def on_stop(self):
        self._stop_gps()


if __name__ == "__main__":
    MyAndroidApp().run()
