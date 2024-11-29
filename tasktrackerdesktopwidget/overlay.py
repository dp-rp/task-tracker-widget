# note: initial tkinter skeleton (incrementing counter) generated with the assistance of Qwen2.5-coder-32B-Instruct
# ... because it's better at writing good tkinter code faster than me. Cheers Qwen!

import tkinter as tk
from .generic.workitems import get_generic_work_items
from datetime import datetime, time
import os

# TODO: get the output (my in-progress work items) and make it display in a small movable, resizable window that's
# ... always-on-top that updates once every 5-10 minutes (and it should also go invisible for a couple seconds when
# ... moused over, just like how I have ElevenClock configured)

# TODO: display a metric for [HOURS LOGGED SO FAR] vs [HOURS LOGGED GOAL]. [HOURS LOGGED GOAL] will be
# ... `[DAILY_HOUR_LOG_GOAL] * [NUMBER_OF_DAYS_INTO_CURRENT_ITERATION]` (current iteration = current sprint)

# TODO: pick a random message from a configurable JSON file that contains a big list of different messages to show
# ... next to the COB timer when it's past COB. e.g. "Go home!", "Do some yoga!", "Drink some water!", "Water your
# ... plants!", "Walk your dog!", "Pick up your kids!", "Go watch Netflix!", "Go nap!", "Go make some art!", "Go
# ... call a friend!"

# TODO: make this configurable and also something a little less frequent (a web request every 10 seconds is a bit overkill)
POLL_INTERVAL_MS = 10000  # milliseconds
PAST_COB_MESSAGE = "go home!"

def get_time_until_cob_msg():
    # TODO: HACK: would rather not read this from env var every time we call this func - good enough for now
    cob_hour = int(os.environ['COB_TIMER_COB_HOUR'])
    cob_minute = int(os.environ['COB_TIMER_COB_MINUTE'])

    # Calculate the difference in time
    five_pm = datetime.combine(datetime.now().date(), time(cob_hour, cob_minute))
    time_difference = five_pm - datetime.now()

    # If the current time is already past 5 PM, calculate for the next day
    # if time_difference.total_seconds() < 0:
    #     five_pm = five_pm + timedelta(days=1)
    #     time_difference = five_pm - now

    # Calculate the number of hours left
    seconds_left = time_difference.total_seconds()
    hours_left = f"{seconds_left / 3600:01.1f}"
    return f"There are {hours_left} hours left until close of business ({cob_hour:02}:{cob_minute:02}){' ---- ' + PAST_COB_MESSAGE if seconds_left < 0 else ''}\n"


class MovableOverlay:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.geometry('+{}+{}'.format(root.winfo_screenwidth() - 150, root.winfo_screenheight() - 100))  # Position in bottom right corner
        
        self.work_items_text = "loading..."
        self.label = tk.Label(root, text=str(self.work_items_text), font=('Helvetica', 8), bg='white', fg='black', justify=tk.LEFT)
        self.label.pack(padx=5, pady=5)
        
        self.start_counter()
        
        # Make the window draggable
        self.root.bind('<Button-1>', self.on_drag_start)
        self.root.bind('<B1-Motion>', self.on_drag_motion)
        
        # Create a context menu
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Exit", command=self.close_window)
        self.root.bind('<Button-3>', self.show_context_menu)

    def on_drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_motion(self, event):
        x = self.root.winfo_x() + event.x - self.drag_start_x
        y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")
    
    def start_counter(self):
        # TODO: display some text when info is getting re-polled
        # self.work_items_text = "polling..."
        # self.label.config(text=str(self.work_items_text))
        # self.root.update()

        # Generate a string of in-progress work items
        work_items = get_generic_work_items()
        work_items_str = "\n----\n".join([
            f"{work_item['uid']}: {work_item['title']} ({work_item['assigned_to']['unique_name'] if 'assigned_to' in work_item else 'no-one'})"
            for work_item
            in work_items
        ])

        # Set the label's text
        self.work_items_text = (
            get_time_until_cob_msg()
            + '\n'
            + work_items_str
        )
        self.label.config(text=str(self.work_items_text))

        self.root.after(POLL_INTERVAL_MS, self.start_counter)  # Schedule the function to be called after 10 seconds

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()
    
    def close_window(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MovableOverlay(root)
    root.mainloop()

if __name__ == "__main__":
    main()
