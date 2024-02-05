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
from kivy.uix.dropdown import DropDown
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.filechooser import FileChooserIconView
import json
from kivy.uix.gridlayout import GridLayout
from agixtsdk import AGiXTSDK
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
import Listen
import time


base_uri = "http://localhost:7437"
agixt_api_key = "your_agixt_api_key"
ApiClient = AGiXTSDK(base_uri=base_uri, api_key=agixt_api_key)


class SidebarButton(MDIconButton):
    pass

class HamburgerButton(MDIconButton):
    pass

class SidebarTextButton(MDBoxLayout):
    def __init__(self, parent, **kwargs):
        super(SidebarTextButton, self).__init__(**kwargs)
        self.button = HamburgerButton(icon="menu", on_release=parent.toggle_sidebar)
        self.add_widget(self.button)


class AgentInteractionsPage(Screen):
    def __init__(self, **kwargs):
        super(AgentInteractionsPage, self).__init__(name='Agent Interactions', **kwargs)
        agents = ApiClient.get_agents()
        agent_name = [agent['name'] for agent in agents]
        agent_config = ApiClient.get_agentconfig(agent_name=agent_name)

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

        self.agent_selection_spinner = Spinner(text="Select Agent")
        self.agent_selection_spinner.values = agent_name
        self.agent_selection_spinner.bind(text=self.on_agent_spinner_change)
        layout.add_widget(self.agent_selection_spinner)

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



class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(name='Home', **kwargs)
        
        # Provide the correct path to your image file
        image_source = "AGiXT-gradient-flat.png"

        self.add_widget(AsyncImage(source=image_source, size_hint_y=None, height=50))

        




def cached_get_extensions():
    return ApiClient.get_extensions()




class CommandSelectionPopup(Popup):
    def __init__(self, prompt, step_number, **kwargs):
        super(CommandSelectionPopup, self).__init__(**kwargs)
        self.prompt = prompt
        self.step_number = step_number
        self.title = "Select Command"
        self.size_hint = (None, None)
        self.size = (400, 400)

        agent_name = ApiClient.get_agents()
        if agent_name is None:
            agent_name = ""  # Set a default value if agent_name is None
        self.agent_name = agent_name  # Assign agent_name to instance variable
        self.available_commands = ApiClient.get_commands(agent_name=self.agent_name)  # Access instance variable
        self.agent_commands = self.available_commands

        self.command_name_dropdown = DropDown()

        if self.available_commands is not None:
            for command in [""] + list(self.available_commands):
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

        self.content = BoxLayout(orientation='vertical', spacing=10)
        self.content.add_widget(self.command_name_button)

    def on_command_name_selected(self, instance, selected_command):
        if selected_command:
            command_args = ApiClient.get_command_args(command_name=selected_command)
            if isinstance(command_args, str):
                command_args = [command_args]
            args = [list(command_args), {"prompt": self.prompt, "step_number": self.step_number}]
            new_prompt = {"command_name": selected_command, **args}
            self.result = [new_prompt]
            self.dismiss()




class ChainManagementPage(Screen):
    def __init__(self, **kwargs):
        super(ChainManagementPage, self).__init__(**kwargs)
        self.name = 'Chain Management'

        # Chain Name widgets
        chain_name_label = Label(text='Chain Name:', size_hint=(None, None), height=50, pos_hint={'center_x': 0.5, 'top': 1})
        self.chain_name = TextInput(multiline=False, size_hint=(None, None), size=(300, 40), pos_hint={'center_x': 0.5, 'top': 0.9})
        self.add_widget(chain_name_label)
        self.add_widget(self.chain_name)

        # Import Chain widgets
        chain_file_label = Label(text='Import Chain:', size_hint=(None, None), height=50, pos_hint={'center_x': 0.5, 'top': 0.8})
        self.chain_file = FileChooserListView(size_hint_y=None, height=50, pos_hint={'center_x': 0.5, 'top': 0.75})
        self.add_widget(chain_file_label)
        self.add_widget(self.chain_file)

        # Chain Action widgets
        chain_action_label = Label(text='Select Action:', size_hint=(None, None), height=50, pos_hint={'center_x': 0.5, 'top': 0.67})
        self.chain_action = DropDown()

        actions = ['Create Chain', 'Modify Chain', 'Delete Chain', 'Add Step']
        for action in actions:
            btn = Button(text=action, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.chain_action.select(btn.text))
            self.chain_action.add_widget(btn)

        main_button = Button(text='Select Action', size_hint=(None, None), height=44, pos_hint={'center_x': 0.5, 'top': 0.6})
        main_button.bind(on_release=self.chain_action.open)
        self.chain_action.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        self.add_widget(chain_action_label)
        self.add_widget(main_button)

        # Command Selection Button widget
        command_selection_button = Button(text='Select Command', size_hint_y=None, height=44, pos_hint={'center_x': 0.5, 'top': 0.5})
        command_selection_button.bind(on_release=self.show_command_selection_popup)
        self.add_widget(command_selection_button)

        # Action Button widget
        self.action_button = Button(text='Perform Action', size_hint_y=None, height=44, pos_hint={'center_x': 0.5, 'top': 0.4})
        self.action_button.bind(on_release=self.on_action_button_pressed)
        self.add_widget(self.action_button)

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
        selected_action = self.chain_action.text

        if selected_action == 'Create Chain':
            self.create_chain_action()
        elif selected_action == 'Modify Chain':
            self.modify_chain_action(chain_name)
        elif selected_action == 'Delete Chain':
            self.delete_chain_action(chain_name)
        elif selected_action == 'Add Step':
            self.add_step_action(chain_name)

    def create_chain_action(self):
        chain_name = self.chain_name.text

        # Import Chain
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
            agents = ApiClient.get_agents()
            self.modify_chain(chain_name=chain_name, agents=agents)
        else:
            print("Please select a chain to manage steps.")

    def delete_chain_action(self, chain_name):
        if chain_name:
            ApiClient.delete_chain(chain_name=chain_name)
            print(f"Chain '{chain_name}' deleted.")
        else:
            print("Chain name is required.")

    def add_step_action(self, chain_name):
        if chain_name:
            agents = ApiClient.get_agents()
            chain_steps = ApiClient.get_chain(chain_name=chain_name).get("steps", [])
            step_number = len(chain_steps) + 1
            self.add_new_step(chain_name=chain_name, step_number=step_number, agents=agents)
        else:
            print("Please select a chain to add a step.")

    def add_new_step(self, chain_name, step_number, agents):
        self.ids.output_label.text = f"Add Chain Step {step_number}\n"

        agent_name_dropdown = DropDown()
        for agent in [""] + [agent["name"] for agent in agents]:
            btn = Button(text=agent, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: agent_name_dropdown.select(btn.text))
            agent_name_dropdown.add_widget(btn)

        agent_name_button = Button(
            text="Select Agent",
            size_hint=(None, None),
            height=44,
        )
        agent_name_button.bind(on_release=agent_name_dropdown.open)
        agent_name_dropdown.bind(on_select=lambda instance, x: setattr(agent_name_button, 'text', x))

        prompt_categories_dropdown = DropDown()
        for prompt_type in [""] + ["Command", "Prompt", "Chain"]:
            btn = Button(text=prompt_type, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: prompt_categories_dropdown.select(btn.text))
            prompt_categories_dropdown.add_widget(btn)

        prompt_categories_button = Button(
            text="Select Step Type",
            size_hint=(None, None),
            height=44,
        )
        prompt_categories_button.bind(on_release=prompt_categories_dropdown.open)
        prompt_categories_dropdown.bind(on_select=lambda instance, x: setattr(prompt_categories_button, 'text', x))

        add_step_button = Button(
            text="Add New Step",
            size_hint=(None, None),
            height=44,
        )
        add_step_button.bind(on_release=lambda instance: self.perform_add_step(chain_name, step_number, agent_name_button.text, prompt_categories_button.text))

        self.ids.output_label.add_widget(agent_name_button)
        self.ids.output_label.add_widget(prompt_categories_button)
        self.ids.output_label.add_widget(add_step_button)

    def perform_add_step(self, chain_name, step_number, agent_name, prompt_type):
        if chain_name and step_number and agent_name and prompt_type:
            ApiClient.add_step(
                chain_name=chain_name,
                step_number=step_number,
                agent_name=agent_name,
                prompt_categories=ApiClient.get_prompt_categories(),
                prompt={},  # You may need to modify this part based on your actual implementation
            )
            self.ids.output_label.text = f"Step added to chain '{chain_name}'."
        else:
            self.ids.output_label.text = "All fields are required."








class PromptManagementPage(Screen):
    def __init__(self, **kwargs):
        super(PromptManagementPage, self).__init__(name='Prompt Management', **kwargs)

        self.title = "Prompt Management"
        
        layout = BoxLayout(orientation="vertical")
        
        # Display documentation
        layout.add_widget(Label(text="Prompt Management Documentation"))
        show_documentation = ToggleButton(text="Show Documentation", state="normal")
        layout.add_widget(show_documentation)
        documentation_label = Label(text="""
To create dynamic prompts that can have user inputs, you can use curly braces `{}` in your prompt content. 
Anything between the curly braces will be considered as an input field. For example:

"Hello, my name is {name} and I'm {age} years old."

In the above prompt, `name` and `age` will be the input arguments. These arguments can be used in chains.
""")
        layout.add_widget(documentation_label)
        show_documentation.bind(on_press=lambda x: self.toggle_widget_state(documentation_label))
        
        # Select action
        layout.add_widget(Label(text="Action"))
        action = ToggleButton(text="Create New Prompt", state="down")
        layout.add_widget(action)
        
        # New prompt category
        layout.add_widget(Label(text="New Prompt Category"))
        new_prompt_category = ToggleButton(text="New Prompt Category", state="normal")
        layout.add_widget(new_prompt_category)
        prompt_category_input = TextInput()
        layout.add_widget(prompt_category_input)
        create_category_button = Button(text="Create Prompt Category")
        layout.add_widget(create_category_button)
        create_category_button.bind(on_press=lambda x: self.create_prompt_category(prompt_category_input.text))
        
        # Select existing prompt category
        layout.add_widget(Label(text="Select Prompt Category"))
        prompt_categories = ["Default"]  # Replace with the actual prompt categories
        prompt_category_select = TextInput(text="Default")
        layout.add_widget(prompt_category_select)
        delete_category_button = Button(text="Delete Prompt Category")
        layout.add_widget(delete_category_button)
        delete_category_button.bind(on_press=lambda x: self.delete_prompt_category(prompt_category_select.text))
        
        # Prompt list
        layout.add_widget(Label(text="Existing Prompts"))
        prompt_list = ["Prompt 1", "Prompt 2"]  # Replace with the actual prompt list
        prompt_select = TextInput(text="")
        layout.add_widget(prompt_select)
        
        if action.state == "down":
            # Create new prompt
            import_prompt_button = FileChooserListView(filters=["*.txt"])
            layout.add_widget(import_prompt_button)
            create_prompt_button = Button(text="Create Prompt")
            layout.add_widget(create_prompt_button)
            create_prompt_button.bind(on_press=lambda x: self.create_prompt(prompt_select.text, import_prompt_button.selection))
        elif action.state == "normal":
            # Modify prompt
            prompt_content_input = TextInput(height=300)
            layout.add_widget(prompt_content_input)
            export_prompt_button = Button(text="Export Prompt")
            layout.add_widget(export_prompt_button)
            export_prompt_button.bind(on_press=lambda x: self.export_prompt(prompt_select.text, prompt_content_input.text))
        else:
            # Delete prompt
            delete_prompt_button = Button(text="Delete Prompt")
            layout.add_widget(delete_prompt_button)
            delete_prompt_button.bind(on_press=lambda x: self.delete_prompt(prompt_select.text))
        
        action.bind(on_press=lambda x: self.toggle_action_state(import_prompt_button, prompt_content_input, delete_prompt_button))
        
        # Perform Action button
        perform_action_button = Button(text="Perform Action")
        layout.add_widget(perform_action_button)
        perform_action_button.bind(on_press=self.perform_action)
        
        self.add_widget(layout)  # Add the layout to the screen

    def toggle_widget_state(self, widget):
        widget.disabled = not widget.disabled
        
    def toggle_action_state(self, import_prompt_button, prompt_content_input, delete_prompt_button):
        import_prompt_button.disabled = not import_prompt_button.disabled
        prompt_content_input.disabled = not prompt_content_input.disabled
        delete_prompt_button.disabled = not delete_prompt_button.disabled
        
    def create_prompt_category(self, category_name):
        # TODO: Implement the logic to create a new prompt category
        print(f"Created prompt category: {category_name}")
        
    def delete_prompt(self, prompt_name):
        # TODO: Implement the logic to delete a prompt
        print(f"Deleted prompt: {prompt_name}")

    def export_prompt(self, prompt_name, prompt_content):
        # TODO: Implement the logic to export a prompt
        print(f"Exported prompt: {prompt_name}, Content: {prompt_content}")

    def perform_action(self, instance):
        prompt_name = self.prompt_select.text
        prompt_content_input = self.prompt_content_input  # Access the prompt_content_input through the class instance
        prompt_content = prompt_content_input.text if prompt_content_input else None
        
        if prompt_name and (prompt_content or self.action.state == "normal"):  # Access the action through the class instance
            if self.action.state == "down":  # Access the action through the class instance
                self.create_prompt(prompt_name, self.import_prompt_button.selection)  # Access the import_prompt_button through the class instance
            elif self.action.state == "normal":  # Access the action through the class instance
                self.modify_prompt(prompt_name, prompt_content)
            else:
                self.delete_prompt(prompt_name)
        else:
            print("Prompt name and content are required.")

    def create_prompt(self, prompt_name, prompt_file):
        # TODO: Implement the logic to create a new prompt using the given prompt_name and prompt_file
        print(f"Created prompt: {prompt_name}, File: {prompt_file}")

    def modify_prompt(self, prompt_name, prompt_content):
        # TODO: Implement the logic to modify an existing prompt using the given prompt_name and prompt_content
        print(f"Modified prompt: {prompt_name}, Content: {prompt_content}")









class MemoryManagementPage(Screen):
    def __init__(self, **kwargs):
        super(MemoryManagementPage, self).__init__(name='Memory Management', **kwargs)

        # Create the main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add Kivy widgets to the layout
        layout.add_widget(Label(text="Memory Management"))
        layout.add_widget(Label(text="Enter Search Query:"))
        search_query = TextInput()
        layout.add_widget(search_query)

        # Add checkbox for Advanced Options
        advanced_options_checkbox = CheckBox(active=False)
        layout.add_widget(advanced_options_checkbox)

        # Create a Spinner for collection number
        collection_spinner = Spinner(
            text="Use collection number (Default is 0)",
            values=["0", "1", "2"],  # Update with your actual collection numbers
        )
        layout.add_widget(collection_spinner)

        # Create buttons for actions
        query_button = Button(text="Query Memory")
        delete_button = Button(text="Delete Memory")

        # Define button callbacks (implement functionality accordingly)
        def query_memory_callback(instance):
            # Indent the code block inside the function
            # Example:
            user_input = search_query.text
            print("Querying memory...")

        def delete_memory_callback(instance):
            # Implement deletion logic using ApiClient.delete_agent_memory
            # Update the UI accordingly
            pass

        # Bind buttons to their callbacks
        query_button.bind(on_press=query_memory_callback)
        delete_button.bind(on_press=delete_memory_callback)

        # Add buttons to the layout
        layout.add_widget(query_button)
        layout.add_widget(delete_button)

        self.add_widget(layout)





class AgentManagementPage(Screen):
    def __init__(self, **kwargs):
        super(AgentManagementPage, self).__init__(name='Agent Management', **kwargs)
        self.agent_name = ""
        self.provider_name = ""
        self.agent_settings = {}
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.add_widget(self.layout)

        self.load_agent_configuration()

    def load_agent_configuration(self):
        agents = ApiClient.get_agents()
        agent_names = [agent['name'] for agent in agents]
        agent_config = ApiClient.get_agentconfig(agent_name=agent_names[0])
        if agent_config is not None:
            if isinstance(agent_config, str):
                agent_config = json.loads(agent_config)
            self.extension_settings = {}
            commands = ApiClient.get_commands(agent_name=agent_names[0])
            if commands is not None:
                if isinstance(commands, str):
                    commands = json.loads(commands)
            else:
                commands = {}
        else:
            agent_config = {}
            commands = {}

        def get_providers():
            return ApiClient.get_providers()

        def provider_settings(provider_name: str):
            return ApiClient.get_provider_settings(provider_name=provider_name)

        def get_extension_settings():
            return ApiClient.get_extension_settings()

        self.extension_setting_keys = []

        agent_settings = agent_config.get("settings", {})
        self.embedder_name = agent_settings.get("embedder", "default")
        self.commands = agent_config.get("commands", {})

        self.header_label = Label(text="Agent Management", font_size=24)
        self.layout.add_widget(self.header_label)

        self.agent_selection_spinner = Spinner(text="Select Agent")
        self.agent_selection_spinner.values = agent_names if agent_names is not None else []
        self.agent_selection_spinner.bind(text=self.on_agent_spinner_change)
        self.layout.add_widget(self.agent_selection_spinner)

        self.agent_actions_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.import_agent_button = Button(text="Import Agent", on_press=self.import_agent)
        self.add_agent_button = Button(text="Add Agent", on_press=self.add_agent)
        self.agent_actions_layout.add_widget(self.import_agent_button)
        self.agent_actions_layout.add_widget(self.add_agent_button)
        self.layout.add_widget(self.agent_actions_layout)

        self.provider_selection_spinner = Spinner(text="Select Provider")
        providers = get_providers()  # Fix: Call the function without self.
        self.provider_selection_spinner.values = providers if providers is not None else []
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

    def on_agent_spinner_change(self, spinner, text):
        self.agent_name = text
        self.load_agent_configuration()

    def import_agent(self, instance):
        file_chooser = FileChooserListView(filters=["*.json"])
        file_chooser.bind(selection=self.on_file_selected)
        self.add_widget(file_chooser)

    def on_file_selected(self, file_chooser, selection):
        selected_file = selection and selection[0] or None
        if selected_file:
            with open(selected_file, "r") as agent_file:
                agent_settings = agent_file.read()
                try:
                    agent_config = json.loads(agent_settings)
                except json.JSONDecodeError:
                    print("Invalid JSON in selected file.")
                    return
            pass

    def add_agent(self, instance):
        agent_name = "test_agent"
        settings = {
            "provider": "gpt4free",
            "embedder": "default",
            "AI_MODEL": "gpt-3.5-turbo",
            "AI_TEMPERATURE": "0.7",
            "AI_TOP_P": "1",
            "MAX_TOKENS": "4096",
            "helper_agent_name": "OpenAI",
            "WEBSEARCH_TIMEOUT": 0,
            "WAIT_BETWEEN_REQUESTS": 1,
            "WAIT_AFTER_FAILURE": 3,
            "stream": False,
            "WORKING_DIRECTORY": "./WORKSPACE",
            "WORKING_DIRECTORY_RESTRICTED": True,
            "AUTONOMOUS_EXECUTION": False,
        }
        agent_name = "test_agent"
        add_agent_resp = ApiClient.add_agent(agent_name=agent_name, settings=settings)
        return add_agent_resp

    def on_provider_spinner_change(self, spinner, text):
        self.provider_name = text
        self.update_provider_settings()

    def update_agent_settings(self, instance):
        ApiClient.update_agent_settings(
            agent_name=self.agent_name, settings=self.agent_settings
        )
        pass

    def wipe_agent_memories(self, instance):
        if self.agent_name:
            ApiClient.wipe_agent_memories(agent_name=self.agent_name)
        else:
            print("No agent selected.")

    def delete_agent(self, instance):
        ApiClient.delete_agent(agent_name=self.agent_name)
        pass

    def add_agent_setting_checkbox(self, setting_name, setting_value):
        checkbox = CheckBox(size_hint_y=None, height=40, active=setting_value)
        checkbox.bind(active=self.on_agent_setting_checkbox_change)
        self.agent_settings_layout.add_widget(checkbox)

    def on_agent_setting_checkbox_change(self, checkbox, value):
        agent_config = ApiClient.get_agentconfig(agent_name=self.agent_name)
        if isinstance(agent_config, dict):
            agent_settings = agent_config.get("settings", {})
            agent_settings[checkbox.text] = value
        else:
            print("Invalid agent configuration")

    def add_command_checkbox(self, command_name, command_value):
        checkbox = CheckBox(size_hint_y=None, height=40, active=command_value)
        checkbox.bind(active=self.on_command_checkbox_change)
        self.agent_settings_layout.add_widget(checkbox)

    def on_command_checkbox_change(self, checkbox, value):
        self.commands[checkbox.text] = value

    def update_provider_settings(self):
        self.agent_settings["embedder"] = self.embedder_name
        if "WEBSEARCH_TIMEOUT" not in self.agent_settings:
            self.agent_settings["WEBSEARCH_TIMEOUT"] = 0
        websearch_timeout = TextInput(
            text=str(self.agent_settings["WEBSEARCH_TIMEOUT"])
        )

        for setting_name, setting_value in self.agent_settings.items():
            self.add_agent_setting_checkbox(setting_name, setting_value)

        for command_name, command_value in self.commands.items():
            self.add_command_checkbox(command_name, command_value)










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


class VoiceScreenPage(Screen):
    def __init__(self, **kwargs):
        super(VoiceScreenPage, self).__init__(name='Voice', **kwargs)
        self.add_widget(Label(text="Voice Screen"))
        



class MyApp(MDApp):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

        bogus_screen = Screen(name='Bogus')
        self.sm.add_widget(bogus_screen)
        self.sm.current = 'Bogus'

        prompt_management_screen = PromptManagementPage()
        self.sm.add_widget(prompt_management_screen)

        agent_interactions_screen = AgentInteractionsPage()
        self.sm.add_widget(agent_interactions_screen)

        memory_management_screen = MemoryManagementPage()
        self.sm.add_widget(memory_management_screen)

        agent_management_screen = AgentManagementPage()
        self.sm.add_widget(agent_management_screen)

        agent_training_screen = AgentTrainingPage()
        self.sm.add_widget(agent_training_screen)

        chain_management_screen = ChainManagementPage()
        self.sm.add_widget(chain_management_screen)

        voice_screen = VoiceScreenPage()
        self.sm.add_widget(voice_screen)

        home_screen = HomeScreen()
        self.sm.add_widget(home_screen)

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

        # Set the default screen to Home
        self.change_page(ToggleButton(text="Home"))

        return main_layout
    
        

    def create_radio_buttons(self):
        box = BoxLayout(orientation='vertical')

        for page_name in ["Home", "Agent Interactions", "Agent Training", "Agent Management", "Memory Management", "Prompt Management", "Chain Management", "Voice"]:
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
        for s in self.sm.screens:
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

MyApp().run()
