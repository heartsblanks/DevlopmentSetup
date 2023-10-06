import tkinter as tk
from tkinter import ttk
import threading
from tqdm import tqdm  # Import tqdm

class ProgressBar:
    def __init__(self, frame, message, row, column):
        self.frame = frame
        self.message = message
        self.row = row
        self.column = column

        self.label = ttk.Label(frame, text=self.message)
        self.label.grid(row=row, column=column, pady=10)

    def set_message(self, new_message):
        self.label.config(text=new_message)

def process_data(progress_bar):
    # Perform time-consuming tasks here
    total_iterations = 10

    # Create a tqdm progress bar
    for i in tqdm(range(total_iterations), desc="Processing", unit="step"):
        new_message = f"Processing Step {i + 1}"
        progress_bar.set_message(new_message)
        # Simulate a time-consuming task
        import time
        time.sleep(1)

def start_processing():
    frame = tk.Frame(master)
    frame.grid(row=1, column=0, padx=10, pady=10)  # Adjust row and column as needed

    progress = ProgressBar(frame, message="Processing Data", row=0, column=0)  # Specify row and column

    # Create a thread for the task
    thread = threading.Thread(target=process_data, args=(progress,))

    # Start the thread
    thread.start()

# Create the master window
master = tk.Tk()

# Button to start the processing
start_button = ttk.Button(master, text="Start Processing", command=start_processing)
start_button.grid(row=0, column=0, padx=10, pady=10)

# Run the Tkinter event loop
master.mainloop()