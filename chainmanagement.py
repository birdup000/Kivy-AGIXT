import json
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
import ApiClient
from kivy.uix.gridlayout import GridLayout

def cached_get_extensions():
    return [{"commands": [{"friendly_name": "Command 1"}, {"friendly_name": "Command 2"}]}]

class CommandSelectionPopup(Popup):
    def __init__(self, prompt, step_number, **kwargs):
        super(CommandSelectionPopup, self).__init__(**kwargs)
        self.prompt = prompt
        self.step_number = step_number
        self.title = "Select Command"
        self.size_hint = (None, None)
        self.size = (400, 400)

        self.agent_commands = cached_get_extensions()
        self.available_commands = [command["friendly_name"] for commands in self.agent_commands for command in commands["commands"]]

        self.command_name_dropdown = DropDown()

        for command in [""] + self.available_commands:
            btn = Button(text=command, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.command_name_dropdown.select(btn.text))
            self.command_name_dropdown.add_widget(btn)

        self.command_name_button = Button(
            text="Select Command",
            size_hint=(None, None),
            height=44,
        )
        self.command_name_button.bind(on_release=self.command_name_dropdown.open)
        self.command_name_dropdown.bind(on_select=self.on_command_name_selected)

        self.content = BoxLayout(orientation="vertical")
        self.content.add_widget(self.command_name_button)

    def on_command_name_selected(self, instance, selected_command):
        if selected_command:
            command_args = {"arg1": "value1"}
            args = command_args, self.prompt, self.step_number
            new_prompt = {"command_name": selected_command, **args}
            self.result = new_prompt
            self.dismiss()

class ChainManagementPage(Screen):
    def __init__(self, **kwargs):
        super(ChainManagementPage, self).__init__(**kwargs)

        # Use GridLayout with two columns
        self.layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=300)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

        # Chain-related widgets
        self.layout.add_widget(Label(text='Chain Management Page'))
        self.layout.add_widget(Label(text='Chain Name: '))
        self.chain_name = TextInput(multiline=False)
        self.layout.add_widget(self.chain_name)
        self.layout.add_widget(Label(text='Import Chain: '))
        self.layout.add_widget(FileChooserIconView())
        
        # Chain Action Dropdown
        self.chain_action = DropDown()
        for action in ['Create Chain', 'Modify Chain', 'Delete Chain']:
            btn = Button(text=action, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.chain_action.select(btn.text))
            self.chain_action.add_widget(btn)

        main_button = Button(text='Select Action', size_hint=(None, None), height=44)
        main_button.bind(on_release=self.chain_action.open)
        self.chain_action.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        self.layout.add_widget(main_button)

        # Command-related widgets
        command_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None), height=150)
        command_layout.bind(minimum_height=command_layout.setter('height'))

        command_selection_button = Button(text='Select Command', size_hint=(None, None), height=44)
        command_selection_button.bind(on_release=self.show_command_selection_popup)
        command_layout.add_widget(command_selection_button)

        self.action_button = Button(text='Perform Action', size_hint=(None, None), height=44)
        self.action_button.bind(on_release=self.on_action_button_pressed)
        command_layout.add_widget(self.action_button)

        self.layout.add_widget(command_layout)

    def show_command_selection_popup(self, instance):
        command_selection_popup = CommandSelectionPopup(prompt={}, step_number=0)
        command_selection_popup.bind(on_dismiss=self.on_command_selection_popup_dismiss)
        command_selection_popup.open()

    def on_command_selection_popup_dismiss(self, instance):
        new_prompt = instance.result
        if new_prompt:
            self.chain_name.text = new_prompt.get("command_name", "")

    def on_action_button_pressed(self, instance):
        chain_name = self.chain_name.text
        if self.chain_action.text == 'Create Chain':
            self.create_chain_action()
        elif self.chain_action.text == 'Modify Chain':
            self.modify_chain_action(chain_name)
        elif self.chain_action.text == 'Delete Chain':
            self.delete_chain_action(chain_name)

    def create_chain_action(self):
        chain_name = self.chain_name.text

        chain_file = self.chain_file.selection and self.chain_file.selection[0]
        if chain_file:
            chain_name = chain_file.split(".")[0]
            with open(chain_file, 'r') as file:
                chain_content = file.read()
                steps = json.loads(chain_content)
                ApiClient.import_chain(chain_name=chain_name, steps=steps)
                print(f"Chain '{chain_name}' added.")
            self.chain_file.selection.clear()

            if chain_name:
                ApiClient.add_chain(chain_name=chain_name)
                print(f"Chain '{chain_name}' created.")

    def modify_chain_action(self, chain_name):
        if chain_name:
            agents = []  # You need to populate this list with your data
            self.modify_chain(chain_name=chain_name, agents=agents)
        else:
            print("Please select a chain to manage steps.")

    def delete_chain_action(self, chain_name):
        if chain_name:
            ApiClient.delete_chain(chain_name=chain_name)
            print(f"Chain '{chain_name}' deleted.")
        else:
            print("Chain name is required.")

class CommandSelectionPage(Screen):
    def __init__(self, **kwargs):
        super(CommandSelectionPage, self).__init__(**kwargs)
        self.add_widget(Label(text='Command Selection Page'))

class ChainManagementApp(App):
    def build(self):
        # Create a ScreenManager
        sm = ScreenManager()

        # Create and add screens to the ScreenManager
        chain_management_page = ChainManagementPage(name='chain_management_page')
        command_selection_page = CommandSelectionPage(name='command_selection_page')

        sm.add_widget(chain_management_page)
        sm.add_widget(command_selection_page)

        return sm

    def show_chain_management_page(self):
        self.root.current = 'chain_management_page'

    def show_command_selection_page(self):
        self.root.current = 'command_selection_page'

if __name__ == "__main__":
    ChainManagementApp().run()
