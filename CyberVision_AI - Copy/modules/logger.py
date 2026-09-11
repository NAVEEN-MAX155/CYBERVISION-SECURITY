import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "events.log")


def log_event(event):

    os.makedirs(LOG_DIR, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {event}\n")

    print(f"[LOG] {event}")