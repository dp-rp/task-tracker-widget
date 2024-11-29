# note: initial tkinter skeleton with an incrementing counter generated with the assistance of Qwen2.5-coder-32B-Instruct, because it's a better at writing good tkinter code faster than me. Cheers Qwen!

import tkinter as tk
from .generic.workitems import get_generic_work_items

# TODO: get the output (my in-progress work items) and make it display in a small movable, resizable window that's always-on-top that updates once every 5-10 minutes
# ... (and it should also go invisible for a couple seconds when moused over, just like how I have ElevenClock configured)

# TODO: make this configurable and also something a little less frequent (a web request every 10 seconds is a bit overkill)
POLL_INTERVAL_MS = 10000  # milliseconds

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
        work_items = get_generic_work_items()

        # TODO: display some text when info is getting re-polled
        # self.work_items_text = "polling..."
        # self.label.config(text=str(self.work_items_text))
        # sleep(0.2)

        self.work_items_text = "\n----\n".join([
            f"{work_item['uid']}: {work_item['title']} ({work_item['assigned_to']['unique_name'] if 'assigned_to' in work_item else 'no-one'})"
            for work_item
            in work_items
        ])
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
