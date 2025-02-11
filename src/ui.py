import sys
from command_manager import CommandManager
from nlp_engine import get_linux_command

SHELL_PROMPT = "SmallShell>"
class ShellUI:
    def __init__(self):
        self.command_manager = CommandManager()

    def run(self):
        print("Welcome to SmallShell. Type 'exit' to quit.")
        while True:
            ask = input(SHELL_PROMPT).strip()
            if ask.lower() == "exit":
                print("Goodbye!")
                sys.exit()
            elif ask.lower() == "clear":
                print("\033c")
            elif ask.lower() == "history":
                self.command_manager.show_history()
            elif ask == "\x1b[A":  # up key, show the previous command
                previous_command = self.command_manager.get_previous_command()
                if previous_command:
                    print(previous_command)
                    ask = previous_command
            elif ask == "\x1b[B":  # down key, show the next command
                next_command = self.command_manager.get_next_command()
                if next_command:
                    print(next_command)
                    ask = next_command
            else:
                command, reason, note = get_linux_command(ask) 
                result = self.command_manager.handle_command(ask, command)
                print(SHELL_PROMPT, command, "\n")
                print(result , "\n")
                print(note) 
