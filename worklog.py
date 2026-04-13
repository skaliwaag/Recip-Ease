from datetime import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "worklog.txt")

def log_entry():
    print("\n🍴 Recip-Ease Work Log")
    print("─" * 30)
    
    name = input("Your name: ").strip()
    worked_on = input("What did you work on? ").strip()
    time_spent = input("How long (e.g. 1.5 hrs): ").strip()
    next_up = input("What's next for you? ").strip()
    blocked = input("Any blockers? (press Enter to skip): ").strip()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    entry = f"""
─────────────────────────────────────
{timestamp} | {name}
Worked on:  {worked_on}
Time spent: {time_spent}
Next up:    {next_up}
"""
    if blocked:
        entry += f"Blocked:    {blocked}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    print("\n✓ Logged. Thanks! Don't forget to post in #work-log on Discord too.")

if __name__ == "__main__":
    log_entry()