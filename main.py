from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.animation import Animation
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
class SidebarButton(MDIconButton):
    pass

class HamburgerButton(MDIconButton):
    pass

class SidebarTextButton(MDBoxLayout):
    def __init__(self, parent, **kwargs):
        super(SidebarTextButton, self).__init__(**kwargs)
        # Add the hamburger menu button
        self.button = HamburgerButton(icon="menu", on_release=parent.toggle_sidebar)
        self.add_widget(self.button)

class ChainManagement(MDLabel):
    pass

class PromptManagement(MDLabel):
    pass

class MyApp(MDApp):
    def build(self):
        main_layout = FloatLayout()

        # Sidebar
        self.sidebar = MDBoxLayout(orientation="vertical", size_hint=(0.2, 1), padding="8dp", spacing="8dp")
        self.sidebar.md_bg_color = (0.2, 0.2, 0.2, 1)

        # Hamburger menu button
        self.menu_button = HamburgerButton(icon="menu", pos_hint={"x": 0.05, "center_y": 0.90})
        self.menu_button.bind(on_release=self.toggle_sidebar)
        main_layout.add_widget(self.menu_button)

        # Close sidebar button
        close_button = SidebarTextButton(parent=self, pos_hint={"center_x": 0.5})
        self.sidebar.add_widget(close_button)

        # Add image icon and title to the top of the sidebar
        image_icon = AsyncImage(source="XT.png", size_hint_y=None, height=50)
        title_label = MDLabel(text="AGIXT", halign="center", theme_text_color="Custom", text_color=(1, 1, 1, 1), pos_hint={"center_x": 0.5, "center_y": 0.15})
        
        self.sidebar.add_widget(image_icon)
        self.sidebar.add_widget(title_label)

        # Add radio buttons to the sidebar
        self.sidebar.add_widget(self.create_radio_buttons())

        icon_buttons = [
            SidebarButton(icon="account", on_release=self.show_user),
            SidebarButton(icon="cog", on_release=self.show_settings),
            SidebarButton(icon="help", on_release=self.show_help),
        ]
        for button in icon_buttons:
            self.sidebar.add_widget(button)

        main_layout.add_widget(self.sidebar)

        # Main content area
        self.content_area = MDBoxLayout(orientation="vertical", size_hint=(0.8, 1), padding="8dp", spacing="8dp")
        main_layout.add_widget(self.content_area)

        # Show the content area by default
        self.content_area.opacity = 0

        # Create the Chain Management screen
        chain_management_screen = Screen(name='Chain Management')
        chain_management_screen.add_widget(ChainManagement(text="Chain Management content"))
        self.content_area.add_widget(chain_management_screen)

        # Create the Prompt Management screen
        prompt_management_screen = Screen(name='Prompt Management')
        prompt_management_screen.add_widget(PromptManagement(text="Prompt Management content"))
        self.content_area.add_widget(prompt_management_screen)

        # Create the Memory Management screen
        memory_management_screen = Screen(name='Memory Management')
        memory_management_screen.add_widget(MDLabel(text="Memory Management content"))
        self.content_area.add_widget(memory_management_screen)

        agent_management_screen = Screen(name='Agent Management')
        agent_management_screen.add_widget(MDLabel(text="Agent Management content"))
        self.content_area.add_widget(agent_management_screen)
        
        agent_training_screen = Screen(name='Agent Training')
        agent_training_screen.add_widget(MDLabel(text="Agent Training content"))
        self.content_area.add_widget(agent_training_screen)

        agent_interactions_screen = Screen(name='Agent Interactions')
        agent_interactions_screen.add_widget(MDLabel(text="Agent Interactions content"))
        self.content_area.add_widget(agent_interactions_screen)

        home_screen = Screen(name='Home')
        home_screen.add_widget(MDLabel(text="Home content"))
        self.content_area.add_widget(home_screen)

        return main_layout

    def create_radio_buttons(self):
        box = BoxLayout(orientation='vertical')

        for page_name in ["Home", "Agent Interactions", "Agent Training","Agent Management", "Memory Management", "Prompt Management", "Chain Management"]:
            rb = ToggleButton(group='pages', size_hint=(1, None), height=30)
            rb.text = page_name
            rb.bind(on_press=self.change_page)
            box.add_widget(rb)

        return box

    def toggle_sidebar(self, *args):
        if self.sidebar.x == 0:
            anim = Animation(x=-self.sidebar.width, duration=0.2)
            anim.start(self.sidebar)
            self.menu_button.opacity = 1 if self.menu_button.opacity == 0 else 1
        else:
            anim = Animation(x=0, duration=0.2)
            anim.start(self.sidebar)
            self.menu_button.opacity = 0

    def hide_sidebar(self, *args):
        self.menu_button.opacity = 1
        anim = Animation(x=-self.sidebar.width, duration=0.2)
        anim.start(self.sidebar)
        

    def change_page(self, instance):
        page_name = instance.text
        self.content_area.clear_widgets()
        sm = ScreenManager()
        chain_management_screen = Screen(name='Chain Management')  # Define the chain_management_screen variable
        prompt_management_screen = Screen(name='Prompt Management')  # Define the property_management_screen variable
        memory_management_screen = Screen(name='Memory Management')  # Define the memory_management_screen variable
        agent_management_screen = Screen(name='Agent Management')  # Define the agent_management_screen variable
        agent_training_screen = Screen(name='Agent Training')  # Define the agent_training_screen variable
        agent_interactions_screen = Screen(name='Agent Interactions')  # Define the agent_interactions_screen variable
        home_screen = Screen(name='Home')  # Define the home_screen variable
        if page_name == "Home":
            self.content_area.add_widget(home_screen)  # Add the home screen
        elif page_name == "Agent Interactions":
            self.content_area.add_widget(agent_interactions_screen)  # Add the Agent Interactions screen
        elif page_name == "Agent Training":
            self.content_area.add_widget(agent_training_screen)  # Add the Agent Training screen
        elif page_name == "Agent Management":
            self.content_area.add_widget(agent_management_screen)  # Add the Agent Management screen
        elif page_name == "Memory Management":
            self.content_area.add_widget(memory_management_screen)  # Add the Memory Management screen
        elif page_name == "Prompt Management":
            self.content_area.add_widget(prompt_management_screen)  # Add the Prompt Management screen
        elif page_name == "Chain Management":
            self.content_area.add_widget(chain_management_screen)  # Add the Chain Management screen
        return sm

    def show_user(self, *args):
        self.content_area.clear_widgets()
        self.content_area.add_widget(MDLabel(text="User content"))

    def show_settings(self, *args):
        self.content_area.clear_widgets()
        self.content_area.add_widget(MDLabel(text="Settings content"))

    def show_help(self, *args):
        self.content_area.clear_widgets()
        self.content_area.add_widget(MDLabel(text="Help content"))

if __name__ == "__main__":
    MyApp().run()
