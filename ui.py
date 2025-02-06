import sys
from command_manager import CommandManager

class ShellUI:
    def __init__(self):
        self.command_manager = CommandManager()

    def run(self):
        print("Welcome to SmallShell. Type 'exit' to quit.")
        while True:
            command = input("SmallShell> ").strip()
            if command.lower() == "exit":
                print("Goodbye!")
                sys.exit()
            elif command.lower() == "history":
                self.command_manager.show_history()
            else:
                result = self.command_manager.handle_command(command)
                print(result)
