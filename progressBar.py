import threading
import tkinter as tk
from tkinter import ttk

class ProgressBar:
    def __init__(self, master, max_value, message, size="400x75"):
        self.master = master
        self.max_value = max_value
        self.message = message

        self.top_level = tk.Toplevel(master)
        self.top_level.title("Installation Progress")
        self.top_level.geometry(size)
        self.top_level.protocol("WM_DELETE_WINDOW", self.disable_close_button)

        self.label = ttk.Label(self.top_level, text=self.message)
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self.top_level, orient="horizontal", length=350, mode="determinate", maximum=self.max_value)
        self.progress.pack()

        self.top_level.grab_set()

    def disable_close_button(self):
        pass

    def update(self, current_value):
        self.progress["value"] = current_value
        self.progress.update()

    def destroy(self):
        self.top_level.destroy()

def process_data(progress_bar):
    # Perform time-consuming tasks here
    for i in range(progress_bar.max_value):
        # Simulating a time-consuming task
        import time
        time.sleep(0.1)
        progress_bar.update(i + 1)

def start_processing():
    progress = ProgressBar(master, max_value=100, message="Processing Data")

    # Create a thread for the task
    thread = threading.Thread(target=process_data, args=(progress,))

    # Start the thread
    thread.start()

# Create the master window
master = tk.Tk()

# Button to start the processing
start_button = ttk.Button(master, text="Start Processing", command=start_processing)
start_button.pack()

# Run the Tkinter event loop
master.mainloop()