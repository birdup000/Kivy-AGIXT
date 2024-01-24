from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import ObjectProperty


class SidebarButton(Label):
    icon = ObjectProperty(None)

    def __init__(self, text, icon_path, **kwargs):
        super(SidebarButton, self).__init__(text=text, **kwargs)
        self.icon = Image(source=icon_path, allow_stretch=True, keep_ratio=True)


class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="horizontal")

        # Sidebar
        sidebar = BoxLayout(orientation="vertical", size_hint=(0.2, 1))

        # Hamburger menu button
        menu_button = Button(text="E", font_size=32, bold=True)
        # Add your logic for opening/closing the menu here
        sidebar.add_widget(menu_button)

        # XT icon
        icon_label = BoxLayout(orientation="horizontal")
        icon = Image(source="path/to/xt_icon.png")
        icon_label.add_widget(icon)
        icon_label.add_widget(Label(text="XT", font_size=24, bold=True))
        sidebar.add_widget(icon_label)

        buttons = [
            SidebarButton(text="Home", icon_path="path/to/home_icon.png"),
            SidebarButton(text="Settings", icon_path="path/to/settings_icon.png"),
            SidebarButton(text="Help", icon_path="path/to/help_icon.png"),
        ]
        for button in buttons:
            button.icon.size_hint_y = 0.2
            sidebar.add_widget(button)

        # Main content area
        content_area = BoxLayout(orientation="vertical", size_hint=(0.8, 1))
        content_area.add_widget(Label(text="This is the main content area"))

        main_layout.add_widget(sidebar)
        main_layout.add_widget(content_area)

        return main_layout


if __name__ == "__main__":
    MyApp().run()
