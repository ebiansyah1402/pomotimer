import datetime
import time
import os
from playsound3 import playsound
import json
import threading

def countdown(duration_seconds, is_work_interval=True):
    """Displays a countdown timer and plays a looping notification until user input."""
    while duration_seconds > 0:
        minutes, seconds = divmod(duration_seconds, 60)
        timer = f"{minutes:02d}:{seconds:02d}"
        print(f"Time remaining: {timer}", end='\r')
        time.sleep(1)
        duration_seconds -= 1

    if is_work_interval:
        print("\nPomodoro finished!")
        notification_sound = 'break_start.wav'
        end_message = "Press Enter to start your break..."
    else:
        print("\nBreak over!")
        notification_sound = 'break_end.wav'
        end_message = "Press Enter to start your next Pomodoro..."

    try:
        def play_sound_loop(sound_file):
            while getattr(threading.current_thread(), "do_run", True):
                playsound(sound_file)
                time.sleep(0.5)
        
        sound_thread = threading.Thread(target=play_sound_loop, args=(notification_sound,))
        sound_thread.do_run = True
        sound_thread.start()

        print(f"\a{end_message}", end='\r')  # Audible bell character
        input()  # Wait for user to press Enter

        sound_thread.do_run = False  # Stop the sound loop
        sound_thread.join()  # Wait for the thread to finish

    except Exception as e:
        print(f"Error playing sound: {e}. Make sure '{notification_sound}' is in the same directory or provide the correct path.")
        input("Press Enter to continue...")

    if is_work_interval:
        return "break"
    else:
        return "work"

def log_activity():
    """Logs a user-provided activity with a timestamp to a daily text file."""
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d")
    time_string = now.strftime("%H:%M:%S")
    filename = f"{date_string}.txt"

    activity = input("What did you work on during this Pomodoro? ")

    try:
        with open(filename, "a") as file:
            file.write(f"[{time_string}] {activity}\n")
        print(f"Activity logged to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_time_target():
    """Asks the user for a time target and returns it as a datetime object, or None."""
    response = input("Do you have a specific time you need to finish by? (yes/no): ").lower()
    if response == 'yes':
        while True:
            target_time_str = input("Enter the target time in HH:MM format (e.g., 10:15): ")
            try:
                target_hour, target_minute = map(int, target_time_str.split(':'))
                now = datetime.datetime.now()
                target_datetime = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
                if target_datetime <= now:
                    print("Target time must be in the future. Please try again.")
                else:
                    return target_datetime
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
    return None

def display_google_data():
    """Reads and displays Google Tasks and Calendar data."""
    try:
        with open('google_tasks_and_calendar.json', 'r') as f:
            google_data = json.load(f)

        print("\n--- Your Upcoming Tasks ---")
        if google_data.get("tasks"):
            for task in google_data["tasks"]:
                print(f"- {task.get('title', 'No Title')} (Due: {task.get('due', 'No Due Date')})")
        else:
            print("No upcoming tasks found.")

        print("\n--- Your Upcoming Calendar Events (Primary) ---")
        if google_data.get("calendar_events"):
            for event in google_data["calendar_events"]:
                print(f"- {event.get('summary', 'No Summary')} (Start: {event.get('start', 'No Start Time')})")
        else:
            print("No upcoming events found in your primary calendar.")

        print("\n--- Your Upcoming Calendar Events (Holidays in Indonesia) ---")
        if google_data.get("holidays"):
            for event in google_data["holidays"]:
                print(f"- {event.get('summary', 'No Summary')} (Start: {event.get('start', 'No Start Time')})")
        else:
            print("No upcoming events found in the 'Holidays in Indonesia' calendar.")

    except FileNotFoundError:
        print("Error: google_data.json not found. Please run google_integration.py first.")
        return None
    except json.JSONDecodeError:
        print("Error: Could not decode google_data.json. The file might be corrupted.")
        return None
    return google_data

if __name__ == "__main__":
    now = datetime.datetime.now()
    print(f"Current time: {now.strftime('%H:%M')}")

    # Display Google Tasks and Calendar data
    google_data = display_google_data()

    if google_data is not None:
        work_duration_minutes = int(input("Enter the work duration in minutes (e.g., 25): "))
        break_duration_minutes = int(input("Enter the break duration in minutes (e.g., 5): "))

        time_target = get_time_target()

        if time_target:
            time_difference = time_target - now
            remaining_minutes = int(time_difference.total_seconds() / 60)
            num_work_intervals = remaining_minutes // (work_duration_minutes + break_duration_minutes)
            remaining_time_after_full_cycles = remaining_minutes % (work_duration_minutes + break_duration_minutes)

            print(f"\nTime until target ({time_target.strftime('%H:%M')}): {remaining_minutes} minutes.")
            if num_work_intervals > 0:
                print(f"You have time for {num_work_intervals} full work intervals and breaks ({work_duration_minutes} work, {break_duration_minutes} break).")
                input("Press Enter to start the Pomodoro cycles...")
                for i in range(num_work_intervals):
                    print(f"\n--- Pomodoro {i + 1} (Work) ---")
                    interval_end = countdown(work_duration_minutes * 60, is_work_interval=True)
                    log_activity()
                    if i < num_work_intervals - 1 and interval_end == "break":
                        print(f"\n--- Break ({break_duration_minutes} minutes) ---")
                        countdown(break_duration_minutes * 60, is_work_interval=False)
                        print("Break over. Next Pomodoro starting...\n")

                if remaining_time_after_full_cycles >= work_duration_minutes:
                    print("\n--- Final Work Interval ---")
                    countdown(work_duration_minutes * 60, is_work_interval=True)
                    log_activity()
                elif 0 < remaining_time_after_full_cycles < work_duration_minutes:
                    print(f"\n--- Short Work Interval ({remaining_time_after_full_cycles} minutes) ---")
                    countdown(remaining_time_after_full_cycles * 60, is_work_interval=True)
                    log_activity()

            elif remaining_time_after_full_cycles >= work_duration_minutes:
                print(f"You only have time for a {work_duration_minutes}-minute work interval.")
                input("Press Enter to start the work interval...")
                print("\n--- Work Interval ---")
                countdown(work_duration_minutes * 60, is_work_interval=True)
                log_activity()
            elif 0 < remaining_time_after_full_cycles < work_duration_minutes:
                print(f"You only have time for a shorter {remaining_time_after_full_cycles}-minute work interval.")
                input("Press Enter to start the work interval...")
                print(f"\n--- Short Work Interval ({remaining_time_after_full_cycles} minutes) ---")
                countdown(remaining_time_after_full_cycles * 60, is_work_interval=True)
                log_activity()
            else:
                print("Not enough time for even a short work interval. Consider adjusting your target or starting later.")

        else:
            try:
                num_pomodoros = int(input("Enter the number of Pomodoro intervals: "))
                print(f"\nStarting {num_pomodoros} Pomodoro intervals ({work_duration_minutes} work, {break_duration_minutes} break)...\n")

                for i in range(num_pomodoros):
                    print(f"\n--- Pomodoro {i + 1} (Work) ---")
                    interval_end = countdown(work_duration_minutes * 60, is_work_interval=True)
                    log_activity()
                    if i < num_pomodoros - 1 and interval_end == "break":
                        print(f"\n--- Break ({break_duration_minutes} minutes) ---")
                        countdown(break_duration_minutes * 60, is_work_interval=False)
                        print("Break over. Next Pomodoro starting...\n")

                print("\nAll Pomodoro intervals completed. Great job!")

            except ValueError:
                print("Invalid input. Please enter a whole number for the number of Pomodoro intervals.")
            except KeyboardInterrupt:
                print("\nTimer interrupted.")