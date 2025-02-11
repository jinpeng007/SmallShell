import subprocess
import sqlite3

class CommandManager:
    def __init__(self):
        self.history_db = "history.db"
        self.init_history_db()
        self.allowed_commands = ["ls", "pwd", "echo", "hostname", "date", "cal"] 

    def init_history_db(self):
        with sqlite3.connect(self.history_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS history (query TEXT, result TEXT)"
            )
    def handle_command(self, ask: str, command: str) -> str:
        #if command.split()[0] in self.allowed_commands:
        return self.execute_system_command(ask, command)
        #return f"Disallowed command: '{command}'"

    def execute_system_command(self, ask: str, cmd: str) -> str:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            self.save_to_history(ask, result.stdout.strip())
            return result.stdout.strip()
        except Exception as e:
            return f"Error executing command: {e}"

    def save_to_history(self, query: str, result: str):
        with sqlite3.connect(self.history_db) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO history (query, result) VALUES (?, ?)", (query, result))
            conn.commit()

    def show_history(self):
        with sqlite3.connect(self.history_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history")
            rows = cursor.fetchall()
            for query, result in rows:
                print(f"Query: {query}\nResult: {result}\n")
    def get_previous_command(self):
        with sqlite3.connect(self.history_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT query FROM history ORDER BY ROWID DESC LIMIT 1")
            return cursor.fetchone()[0]
    def get_next_command(self):
        with sqlite3.connect(self.history_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT query FROM history ORDER BY ROWID ASC LIMIT 1")
            return cursor.fetchone()[0]
