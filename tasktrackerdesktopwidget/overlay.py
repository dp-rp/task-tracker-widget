# note: initial tkinter skeleton (incrementing counter) generated with the assistance of Qwen2.5-coder-32B-Instruct
# ... because it's better at writing good tkinter code faster than me. Cheers Qwen!

import tkinter as tk
import customtkinter as ctk
from .generic.workitems import get_generic_work_items
from .cob import get_time_until_cob_msg

# TODO: get the output (my in-progress work items) and make it display in a small movable, resizable window that's
# ... always-on-top that updates once every 5-10 minutes (and it should also go invisible for a couple seconds when
# ... moused over, just like how I have ElevenClock configured)

# TODO: display a metric for [HOURS LOGGED SO FAR] vs [HOURS LOGGED GOAL]. [HOURS LOGGED GOAL] will be
# ... `[DAILY_HOUR_LOG_GOAL] * [NUMBER_OF_DAYS_INTO_CURRENT_ITERATION]` (current iteration = current sprint)

# TODO: make this configurable and also something a little less frequent (a web request every 10 seconds is a bit overkill)
POLL_INTERVAL_MS = 10000  # milliseconds


class MovableOverlay:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.geometry('+{}+{}'.format(root.winfo_screenwidth() - 150, root.winfo_screenheight() - 100))  # Position in bottom right corner
        # TODO: set the max width of the window to 200px, but let the height be whatever it is by default
        # self.root.maxsize(200,None)
        
        self.work_items_text = "loading..."
        
        self.label = ctk.CTkLabel(root, text=str(self.work_items_text), font=('Helvetica', 12), fg_color='#333333', text_color='white', justify=ctk.LEFT)
        self.label.pack(padx=3, pady=3)
        
        self.start_counter()
        
        # Make the window draggable
        self.root.bind('<Button-1>', self.on_drag_start)
        self.root.bind('<B1-Motion>', self.on_drag_motion)
        
        # Create a context menu
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Exit", command=self.close_window)
        self.root.bind('<Button-3>', self.show_context_menu)

        self.root.configure(
            # Show the "movable" cursor when hovering over the window
            cursor="fleur",
            # Update the window's background colour
            background="#e6b905"
        )

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
        # self.label.configure(text=str(self.work_items_text))
        # self.root.update()

        # Generate a string of in-progress work items
        work_items = get_generic_work_items()
        work_items_str = "\n----\n".join([
            f"{work_item['uid']}: {work_item['title']}"
            # TODO: temp - the assigned person isn't really necessary to display when I'm only showing work items assigned to me anyway - that
            # ... being said, I still wanna keep that code there as an example for the moment because it would be google to provide some clarity
            # ... on how to display who an item is assigned to if I do something like display all the work items under a given PBI in future.
            # ... Honestly I probably don't really need it.
            # + f" ({work_item['assigned_to']['unique_name'] if 'assigned_to' in work_item else 'no-one'})"
            for work_item
            in work_items
        ])

        # Set the label's text
        # TODO: allow the COB countdown to subtract from the "hours left" any meetings/events that have already been blocked out in calendar that have
        # ... a "show as:" value set to anything other than "free" - also make a not for the number of hours subtracted from the COB time remaining if
        # ... any time has been subtracted (e.g. 15min stand-ups + lunch each day mean that even best-case scenario a day is 6.8h long, not 8h long)
        self.work_items_text = (
            get_time_until_cob_msg()
            + '\n'
            + work_items_str
        )
        self.label.configure(text=str(self.work_items_text))

        self.root.after(POLL_INTERVAL_MS, self.start_counter)  # Schedule the function to be called after 10 seconds

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()
    
    def close_window(self):
        self.root.destroy()

def main():
    root = ctk.CTk()
    app = MovableOverlay(root)
    root.mainloop()

if __name__ == "__main__":
    main()
