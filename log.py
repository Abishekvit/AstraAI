from datetime import datetime

LOG_FILE = "astra_commands.log"

def log_command(command: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {command}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
