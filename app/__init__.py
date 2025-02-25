import pkgutil
import importlib
import inspect
from app.commands import Command
from app.commands import CommandHandler

class App:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.load_plugins()  # Load plugins dynamically

    
    def load_plugins(self):
        '''Dynamically load all plugins from the `app/plugins` directory.'''
        plugins_package = "app.plugins"
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace(".", "/")]):
            if not is_pkg:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}') 
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, Command) and item is not Command:
                            self.command_handler.Register_Command(item_name, item())
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore

    def start(self):
        """Start the REPL loop for user interaction."""
        print("Welcome to Calculator! Type 'menu' to see available commands, or 'exit' to quit.")
        self.command_handler.Execute_Command("Menu")  # Show available commands at startup

        while True:
            c = input("Enter the command: ").strip()
            if c.lower() == "exit":
                print("Exiting...")
                break
            else:
                self.command_handler.Execute_Command(*c.split())