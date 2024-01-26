from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout

class SidebarButton(MDLabel):
    pass

class SidebarTextButton(MDLabel):
    pass

class MyApp(MDApp):
    def build(self):
        main_layout = BoxLayout(orientation="horizontal")  # Changed to BoxLayout

        # Sidebar
        self.sidebar = MDBoxLayout(orientation="vertical", size_hint=(0.2, 1), padding="8dp", spacing="8dp")
        self.sidebar.md_bg_color = (0.2, 0.2, 0.2, 1)

        # Add radio buttons to the sidebar
        self.sidebar.add_widget(self.create_radio_buttons())

        main_layout.add_widget(self.sidebar)

        # Main content area
        self.content_area = MDBoxLayout(orientation="vertical", size_hint=(0.8, 1), padding="8dp", spacing="8dp")
        self.content_area.add_widget(MDLabel(text="This is the main content area"))
        main_layout.add_widget(self.content_area)

        # Show the content area by default
        self.content_area.opacity = 1

        return main_layout

    def create_radio_buttons(self):
        box = BoxLayout(orientation='vertical')

        for page_name in ["Home", "Agents"]:
            rb = ToggleButton(group='pages', size_hint=(1, None), height=30)
            rb.text = page_name
            rb.bind(on_press=self.change_page)
            box.add_widget(rb)

        return box

    def change_page(self, instance):
        page_name = instance.text
        self.content_area.clear_widgets()

        if page_name == "Home":
            self.content_area.add_widget(MDLabel(text="Home content"))
        elif page_name == "Agents":
            self.content_area.add_widget(MDLabel(text="Agents content"))
if __name__ == "__main__":
    MyApp().run()
