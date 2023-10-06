import tkinter as tk
from tkinter import ttk

def complete_progress():
    progress_bar.stop()  # Stop the progress bar
    progress_bar["value"] = 100  # Set progress to 100%
    progress_bar["style"] = "red.Horizontal.TProgressbar"  # Change the color to red

root = tk.Tk()
root.title("Determinate Progress Bar")

# Create a custom style with a red color for the progress bar
s = ttk.Style()
s.configure("red.Horizontal.TProgressbar", foreground="red", background="red")

# Create the determinate progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=100, style="red.Horizontal.TProgressbar")
progress_bar.pack(pady=20)

start_button = tk.Button(root, text="Start Progress", command=lambda: progress_bar.start(10))
start_button.pack()

complete_button = tk.Button(root, text="Complete Progress", command=complete_progress)
complete_button.pack()

root.mainloop()