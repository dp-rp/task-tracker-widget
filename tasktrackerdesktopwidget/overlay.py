# note: initial tkinter skeleton (incrementing counter) generated with the assistance of Qwen2.5-coder-32B-Instruct
# ... because it's better at writing good tkinter code faster than me. Cheers Qwen!

import tkinter as tk
import customtkinter as ctk
from .generic.workitems import get_generic_work_items
from .cob import get_time_until_cob_msg

# TODO: make window resizable?
# TODO: make window go invisible for a couple seconds when moused over? just like how I have ElevenClock configured

# TODO: display a metric for [HOURS LOGGED SO FAR] vs [HOURS LOGGED GOAL]. [HOURS LOGGED GOAL] will be
# ... `[DAILY_HOUR_LOG_GOAL] * [NUMBER_OF_DAYS_INTO_CURRENT_ITERATION]` (current iteration = current sprint)

# TODO: make this configurable and maybe less frequent by default (60000 milliseconds is a web request every minute) (also make sure request respect any retry-after headers in responses)
POLL_INTERVAL_MS = 60000  # milliseconds
WINDOW_ALPHA_WITH_HOVER = 0.3
WINDOW_ALPHA_WITHOUT_HOVER = 1.0


class MovableOverlay:
    def __init__(self, root):
        self.root = root

        # constants
        self._max_text_width = int(self.root.winfo_screenwidth() / 6)

        # initial states
        self.set_is_being_dragged(False)

        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep the window on top
        self.root.attributes(
            "-toolwindow", True
        )  # Makes window not appear in task bar and Alt+Tab (which we don't want, because it just adds noise to both)
        self.root.geometry(
            f"+{root.winfo_screenwidth() - self._max_text_width - 5}+{(root.winfo_screenheight()*0.75) - (root.winfo_height()/2) - 5}"
        )  # Position in bottom right corner

        self.work_items_text = "loading..."

        self.label = ctk.CTkLabel(
            root,
            text=str(self.work_items_text),
            font=("Helvetica", 12),
            fg_color="#333333",
            text_color="white",
            justify=ctk.LEFT,
            wraplength=self._max_text_width,
        )
        self.label.pack(padx=3, pady=3)

        self.start_counter()

        # Make the window draggable
        self.root.bind("<ButtonPress-1>", self.on_drag_start)
        self.root.bind("<ButtonRelease-1>", self.on_drag_end)
        self.root.bind("<B1-Motion>", self.on_drag_motion)

        # Create a context menu
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Exit", command=self.close_window)
        self.root.bind("<Button-3>", self.show_context_menu)

        # When cursor hovering
        self.root.bind("<Enter>", self.on_hover_start)

        # When cursor stops hovering
        self.root.bind("<Leave>", self.on_hover_end)

        self.root.configure(
            # Show the "movable" cursor when hovering over the window
            cursor="fleur",
            # Update the window's background colour
            fg_color="#242424",
        )

    def on_hover_start(self, e):
        # If the window is currently being dragged, ignore the position of the cursor
        if self._is_being_dragged == True:
            return

        self.root.attributes("-alpha", WINDOW_ALPHA_WITH_HOVER)

    def on_hover_end(self, e):
        self.root.attributes("-alpha", WINDOW_ALPHA_WITHOUT_HOVER)

    def on_drag_start(self, event):
        self.set_is_being_dragged(True)
        # We don't want any hover-based behavior to occur while dragging
        self.on_hover_end(None)
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag_end(self, event):
        self.set_is_being_dragged(False)
        # If we just finished dragging the window, the cursor is likely over it
        self.on_hover_start(None)

    def set_is_being_dragged(self, is_being_dragged):
        self._is_being_dragged = is_being_dragged

    def on_drag_motion(self, event):
        x = self.root.winfo_x() + event.x - self.drag_start_x
        y = self.root.winfo_y() + event.y - self.drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def start_counter(self):
        self.refresh_work_item_list()

        self.root.after(
            POLL_INTERVAL_MS, self.start_counter
        )  # Schedule the function to be called after 10 seconds

    def refresh_work_item_list(self):
        # TODO: display some text when info is getting re-polled
        # self.work_items_text = "polling..."
        # self.label.configure(text=str(self.work_items_text))
        # self.root.update()

        # Generate a string of in-progress work items
        try:
            work_items = get_generic_work_items()
            work_items_str = "\n----\n".join(
                [
                    f"{work_item['uid']}: {work_item['title']}   [ ⧗{work_item['hours_elapsed']} ]"
                    # TODO: temp - the assigned person isn't really necessary to display when I'm only showing work items assigned to me anyway - that
                    # ... being said, I still wanna keep that code there as an example for the moment because it would be google to provide some clarity
                    # ... on how to display who an item is assigned to if I do something like display all the work items under a given PBI in future.
                    # ... Honestly I probably don't really need it.
                    # + f" ({work_item['assigned_to']['unique_name'] if 'assigned_to' in work_item else 'no-one'})"
                    for work_item in work_items
                ]
            )

            # Set the label's text
            # TODO: allow the COB countdown to subtract from the "hours left" any meetings/events that have already been blocked out in calendar that have
            # ... a "show as:" value set to anything other than "free" - also make a not for the number of hours subtracted from the COB time remaining if
            # ... any time has been subtracted (e.g. 15min stand-ups + lunch each day mean that even best-case scenario a day is 6.8h long, not 8h long)
            self.work_items_text = get_time_until_cob_msg() + "\n" + work_items_str
            self.label.configure(text=str(self.work_items_text))
        except Exception as err:
            print(err)
            self.label.configure(text=f"Failed to refresh status of work items!: {err}")

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
