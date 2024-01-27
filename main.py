from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
import os
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup



class SidebarButton(MDIconButton):
    pass

class HamburgerButton(MDIconButton):
    pass

class SidebarTextButton(MDBoxLayout):
    def __init__(self, parent, **kwargs):
        super(SidebarTextButton, self).__init__(**kwargs)
        self.button = HamburgerButton(icon="menu", on_release=parent.toggle_sidebar)
        self.add_widget(self.button)

class ChainManagement(MDLabel):
    pass

class PromptManagement(MDLabel):
    pass

class AgentInteractionsPage(Screen):
    def __init__(self, **kwargs):
        super(AgentInteractionsPage, self).__init__(name='Agent Interactions', **kwargs)

        self.agent_name = "OpenAI"
        self.conversation = "default_conversation"
        self.mode = "Chat"

        layout = MDBoxLayout(orientation='vertical', padding="8dp", spacing="8dp")
        layout.add_widget(MDLabel(text="Agent Interactions"))

        show_injection_var_docs = CheckBox()
        show_injection_var_docs.bind(active=self.on_show_docs_checkbox_change)
        layout.add_widget(show_injection_var_docs)

        layout.add_widget(MDLabel(text="Select Agent Interaction Mode"))
        mode_spinner = Spinner(values=["Chat", "Chains", "Prompt", "Instruct"], text=self.mode)
        mode_spinner.bind(text=self.on_mode_spinner_change)
        layout.add_widget(mode_spinner)

        layout.add_widget(MDLabel(text="Agent Name"))
        agent_name_spinner = Spinner(values=["Agent1", "Agent2", "Agent3"], text=self.agent_name)
        agent_name_spinner.bind(text=self.on_agent_spinner_change)
        layout.add_widget(agent_name_spinner)

        layout.add_widget(MDLabel(text="User Input"))
        self.user_input_text = TextInput(multiline=True)
        layout.add_widget(self.user_input_text)

        send_button = Button(text="Send")
        send_button.bind(on_press=self.on_send_button_press)
        layout.add_widget(send_button)

        self.add_widget(layout)

    def on_show_docs_checkbox_change(self, checkbox, value):
        pass

    def on_mode_spinner_change(self, spinner, text):
        self.mode = text

    def on_agent_spinner_change(self, spinner, text):
        self.agent_name = text

    def on_send_button_press(self, button):
        pass

class ChainManagementPage(Screen):
    def __init__(self, **kwargs):
        super(ChainManagementPage, self).__init__(name='Chain Management', **kwargs)
        self.add_widget(MDLabel(text="Chain Management content"))

class PromptManagementPage(Screen):
    def __init__(self, **kwargs):
        super(PromptManagementPage, self).__init__(name='Prompt Management', **kwargs)
        self.add_widget(MDLabel(text="Prompt Management content"))


class MemoryManagementPage(Screen):
    def __init__(self, **kwargs):
        super(MemoryManagementPage, self).__init__(name='Memory Management', **kwargs)
        self.add_widget(MDLabel(text="Memory Management content"))


class AgentManagementPage(Screen):
    def __init__(self, **kwargs):
        super(AgentManagementPage, self).__init__(name='Agent Management', **kwargs)
        self.agent_name = ""
        self.provider_name = ""
        self.agent_settings = {}
        self.extension_settings = {}
        self.available_commands = {}
        self.extension_setting_keys = []

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.header_label = Label(text="Agent Management", font_size=24)
        self.layout.add_widget(self.header_label)

        self.agent_selection_spinner = Spinner(text="Select Agent")
        self.agent_selection_spinner.values = ["Agent1", "Agent2", "Agent3"]  # Replace with your actual agent names
        self.agent_selection_spinner.bind(text=self.on_agent_spinner_change)
        self.layout.add_widget(self.agent_selection_spinner)

        self.agent_actions_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.import_agent_button = Button(text="Import Agent", on_press=self.import_agent)
        self.add_agent_button = Button(text="Add Agent", on_press=self.add_agent)
        self.agent_actions_layout.add_widget(self.import_agent_button)
        self.agent_actions_layout.add_widget(self.add_agent_button)
        self.layout.add_widget(self.agent_actions_layout)

        self.provider_selection_spinner = Spinner(text="Select Provider")
        self.provider_selection_spinner.values = ["Provider1", "Provider2", "Provider3"]  # Replace with your actual providers
        self.provider_selection_spinner.bind(text=self.on_provider_spinner_change)
        self.layout.add_widget(self.provider_selection_spinner)

        self.agent_settings_scrollview = ScrollView()
        self.agent_settings_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        self.agent_settings_scrollview.add_widget(self.agent_settings_layout)
        self.layout.add_widget(self.agent_settings_scrollview)

        self.update_settings_button = Button(text="Update Agent Settings", on_press=self.update_agent_settings)
        self.wipe_memories_button = Button(text="Wipe Agent Memories", on_press=self.wipe_agent_memories)
        self.delete_agent_button = Button(text="Delete Agent", on_press=self.delete_agent)
        self.layout.add_widget(self.update_settings_button)
        self.layout.add_widget(self.wipe_memories_button)
        self.layout.add_widget(self.delete_agent_button)

        self.add_widget(self.layout)

    def on_agent_spinner_change(self, spinner, text):
        self.agent_name = text
        # Load agent configuration and update UI
        self.load_agent_configuration()

    def import_agent(self, instance):
        # Implement import agent functionality
        pass

    def add_agent(self, instance):
        # Implement add agent functionality
        pass

    def on_provider_spinner_change(self, spinner, text):
        self.provider_name = text
        # Update provider settings in UI
        self.update_provider_settings()

    def update_provider_settings(self):
        # Implement updating provider settings in the UI
        pass

    def update_agent_settings(self, instance):
        # Implement updating agent settings
        pass

    def wipe_agent_memories(self, instance):
        # Implement wiping agent memories
        pass

    def delete_agent(self, instance):
        # Implement deleting agent
        pass

    def load_agent_configuration(self):
        # Implement loading agent configuration and updating UI
        pass


class AgentTrainingPage(Screen):
    def __init__(self, **kwargs):
        super(AgentTrainingPage, self).__init__(name='Agent Training', **kwargs)

        self.agent_name = "OpenAI"
        self.collection_number = 0

        layout = BoxLayout(orientation='vertical', spacing=8, padding=8)

        layout.add_widget(Label(text="Agent Training", font_size=20, color=(1,1,1,1)))

        mode_spinner = Spinner(text="Website", size_hint_y=None, height=40)
        mode_spinner.values = ["Website", "File", "Text", "GitHub Repository", "arXiv"]
        mode_spinner.bind(text=self.on_mode_spinner_change)
        layout.add_widget(mode_spinner)

        advanced_options_checkbox = CheckBox(size_hint_y=None, height=40)
        advanced_options_checkbox.bind(active=self.on_advanced_options_checkbox_change)
        layout.add_widget(advanced_options_checkbox)

        self.collection_number_input = TextInput(multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.collection_number_input)

        self.learn_input = TextInput(multiline=True, size_hint_y=None, height=100)
        layout.add_widget(self.learn_input)

        train_button = Button(text="Train", size_hint_y=None, height=40)
        train_button.bind(on_press=self.on_train_button_press)
        layout.add_widget(train_button)

        self.add_widget(layout)

    def on_mode_spinner_change(self, spinner, text):
        self.mode = text

    def on_advanced_options_checkbox_change(self, checkbox, value):
        self.show_advanced_options = value

    def on_train_button_press(self, button):
        if self.mode == "Website":
            # Handle training from websites
            pass
        elif self.mode == "File":
            # Handle training from files
            pass
        elif self.mode == "Text":
            # Handle training from text
            pass
        elif self.mode == "GitHub Repository":
            # Handle training from GitHub repository
            pass
        elif self.mode == "arXiv":
            # Handle training from arXiv
            pass


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(name='Home', **kwargs)
        self.add_widget(MDLabel(text="Home content"))

class MyApp(MDApp):
    sm = ScreenManager()

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
        self.content_area = MDBoxLayout(orientation="vertical", size_hint=(0.8, 1), pos_hint={"right": 1}, padding="8dp", spacing="8dp")
        main_layout.add_widget(self.content_area)

        # Show the content area by default
        self.content_area.opacity = 1

        # Create screens and add them to ScreenManager
        sm = MyApp.sm

        chain_management_screen = ChainManagementPage()
        sm.add_widget(chain_management_screen)

        prompt_management_screen = PromptManagementPage()
        sm.add_widget(prompt_management_screen)

        agent_interactions_screen = AgentInteractionsPage()
        sm.add_widget(agent_interactions_screen)

        memory_management_screen = MemoryManagementPage()
        sm.add_widget(memory_management_screen)

        agent_management_screen = AgentManagementPage()
        sm.add_widget(agent_management_screen)

        agent_training_screen = AgentTrainingPage()
        sm.add_widget(agent_training_screen)

        home_screen = HomeScreen()
        sm.add_widget(home_screen)

        # Set the default screen to Home
        self.change_page(ToggleButton(text="Home"))

        return main_layout

    def create_radio_buttons(self):
        box = BoxLayout(orientation='vertical')

        for page_name in ["Home", "Agent Interactions", "Agent Training", "Agent Management", "Memory Management", "Prompt Management", "Chain Management"]:
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

        # Find the corresponding screen in the ScreenManager
        screen = None
        for s in MyApp.sm.screens:
            if s.name == page_name:
                screen = s
                break

        # If the screen is found, add it to the content area
        if screen:
            self.content_area.add_widget(screen)

    def show_user(self, *args):
        self.change_page(ToggleButton(text="User"))

    def show_settings(self, *args):
        self.change_page(ToggleButton(text="Settings"))

    def show_help(self, *args):
        self.change_page(ToggleButton(text="Help"))

if __name__ == "__main__":
    MyApp().run()
