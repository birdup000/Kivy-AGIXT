from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.behaviors import BackgroundColorBehavior
from kivy.animation import Animation


class SidebarButton(MDLabel, BackgroundColorBehavior):
    def __init__(self, text, **kwargs):
        super(SidebarButton, self).__init__(**kwargs)
        self.text = text
        self.bg_color = (0, 0, 0, 0) # Set the background color to transparent


class MyApp(MDApp):
    def build(self):
        main_layout = MDBoxLayout(orientation="horizontal")

        # Sidebar
        self.sidebar = MDBoxLayout(orientation="vertical", size_hint=(0.2, 1), padding="8dp", spacing="8dp")
        self.sidebar.bg_color = (0.2, 0.2, 0.2, 1) # Set the background color of the sidebar

        # Hamburger menu button
        self.menu_button = MDIconButton(icon="menu", pos_hint={"center_x": 0.1, "center_y": 0.90})
        self.menu_button.bind(on_release=self.toggle_sidebar) # Bind the button to the toggle_sidebar function
        main_layout.add_widget(self.menu_button)

        buttons = [
            SidebarButton(text="Agents"),
            SidebarButton(text="Settings"),
            SidebarButton(text="Help"),
        ]
        for button in buttons:
            self.sidebar.add_widget(button)

        # Main content area
        self.content_area = MDBoxLayout(orientation="vertical", size_hint=(0.8, 1), padding="8dp", spacing="8dp")
        self.content_area.add_widget(MDLabel(text="This is the main content area"))

        main_layout.add_widget(self.sidebar)
        main_layout.add_widget(self.content_area)

        # Show the content area by default
        self.content_area.opacity = 1

        return main_layout

    def toggle_sidebar(self, *args):
        if self.sidebar.x == 0:
            # Sidebar is currently open, so close it
            anim = Animation(x=-self.sidebar.width, duration=0.2)
            anim.start(self.sidebar)
            self.hide_button()
        else:
            # Sidebar is currently closed, so open it
            anim = Animation(x=0, duration=0.2)
            anim.start(self.sidebar)
            self.show_button()

    def show_button(self, *args):
        self.menu_button.pos_hint = {"center_x": 0.1, "center_y": 0.90}

    def hide_button(self):
        self.menu_button.pos_hint = {"center_x": 0.1, "center_y": 0.90}


if __name__ == "__main__":
    MyApp().run()
