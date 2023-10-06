import tkinter as tk

root = tk.Tk()
root.title("Buttons in Frames")

# Create the left frame
left_frame = tk.Frame(root, width=200, height=300, bg="lightblue")
left_frame.grid(row=0, column=0, padx=10, pady=10)

# Create the right frame
right_frame = tk.Frame(root, width=200, height=300, bg="lightgreen")
right_frame.grid(row=0, column=1, padx=10, pady=10)

# Add buttons to the left frame in a grid
for i in range(3):
    for j in range(3):
        button = tk.Button(left_frame, text=f"Button {i*3+j+1}")
        button.grid(row=i, column=j, padx=5, pady=5)

# Add buttons to the right frame in a grid
for i in range(3):
    for j in range(3):
        button = tk.Button(right_frame, text=f"Button {i*3+j+4}")
        button.grid(row=i, column=j, padx=5, pady=5)

root.mainloop()