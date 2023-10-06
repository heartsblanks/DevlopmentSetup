import tkinter as tk

def is_row_empty(frame, row):
    # Check if all four columns in the given row are empty
    for col in range(frame.columns - 4, frame.columns):
        widget = frame.grid_slaves(row=row, column=col)
        if widget:
            return False
    return True

def insert_label(frame, row):
    # Insert a label with text in the last four columns of the given row
    label = tk.Label(frame, text="Empty Row")
    label.grid(row=row, column=frame.columns - 4, columnspan=4)

root = tk.Tk()
root.title("Check and Insert Labels")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

frame.rows = 10  # Number of rows
frame.columns = 10  # Number of columns

# Insert widgets or data in the frame as needed

# Check rows in the last four columns and insert labels when appropriate
for row in range(frame.rows):
    if is_row_empty(frame, row):
        insert_label(frame, row)

root.mainloop()