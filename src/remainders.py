import schedule
import time
import threading
from src.tts import speak

# store active reminders so we can list them
active_reminders = []
_scheduler_started = False

def _run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    """Start the background scheduler thread — call once at startup."""
    global _scheduler_started
    if not _scheduler_started:
        t = threading.Thread(target=_run_scheduler, daemon=True)
        t.start()
        _scheduler_started = True
        print("Reminder scheduler started.")

def set_reminder(task, delay_minutes):
    """Set a one-time reminder after delay_minutes."""
    def remind():
        speak(f"Reminder: {task}")
        # remove it after firing — one-shot reminder
        return schedule.CancelJob

    job = schedule.every(delay_minutes).minutes.do(remind)
    active_reminders.append({"task": task, "minutes": delay_minutes})
    print(f"Reminder set: '{task}' in {delay_minutes} minutes.")
    return f"Reminder set for {task} in {delay_minutes} minutes."

def list_reminders():
    if not active_reminders:
        return "You have no active reminders."
    items = ", ".join([f"{r['task']} in {r['minutes']} minutes"
                       for r in active_reminders])
    return f"Your reminders: {items}"

def parse_reminder_command(command):
    """
    Extract task and time from voice command.
    Expected: 'remind me to call mom in 10 minutes'
    Returns: (task, minutes) or None
    """
    try:
        if "remind me to" in command:
            after = command.split("remind me to", 1)[1].strip()
        elif "set reminder" in command:
            after = command.split("set reminder", 1)[1].strip()
        else:
            return None

        # extract minutes
        if "in" in after or "minute" in after:
            parts = after.split("in", 1)
            task = parts[0].strip()
            time_part = parts[1].strip()
            # extract the number
            import re
            numbers = re.findall(r'\d+', time_part)
            if numbers:
                minutes = int(numbers[0])
                return task, minutes

        return None

    except Exception as e:
        print(f"Reminder parse error: {e}")
        return None