import sys
from command_manager import CommandManager
from nlp_engine import get_unix_command

class ShellUI:
    def __init__(self):
        self.command_manager = CommandManager()

    def run(self):
        print("Welcome to SmallShell. Type 'exit' to quit.")
        while True:
            ask = input("SmallShell> ").strip()
            if ask.lower() == "exit":
                print("Goodbye!")
                sys.exit()
            elif ask.lower() == "history":
                self.command_manager.show_history()
            else:
                command, reason = get_unix_command(ask) 
                result = self.command_manager.handle_command(command)
                print(result)
