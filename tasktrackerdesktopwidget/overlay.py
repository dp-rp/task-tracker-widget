# Note: initially tkinter skeleton generated with the assistance of Qwen2.5-coder-32B-Instruct, because it's at lot faster at writing tkinter code than me. Cheers Qwen!

import tkinter as tk

class MovableOverlay:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.geometry('+{}+{}'.format(root.winfo_screenwidth() - 150, root.winfo_screenheight() - 100))  # Position in bottom right corner
        
        self.counter = 0
        self.label = tk.Label(root, text=str(self.counter), font=('Helvetica', 18), bg='white', fg='black')
        self.label.pack(padx=10, pady=10)
        
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
        self.counter += 1
        self.label.config(text=str(self.counter))
        self.root.after(10000, self.start_counter)  # Schedule the function to be called after 10 seconds
    
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.context_menu.grab_release()
    
    def close_window(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovableOverlay(root)
    root.mainloop()
