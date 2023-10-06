import tkinter as tk

def is_row_empty(frame, row):
    # Check if all columns in the given row are empty
    for col in range(frame.columns):
        widget = frame.grid_slaves(row=row, column=col)
        if widget:
            return False
    return True

def insert_label(frame, row):
    # Insert a label with text in all columns of the given row
    label = tk.Label(frame, text="Empty Row")
    label.grid(row=row, column=0, columnspan=frame.columns)

def get_existing_rows(frame):
    # Determine the number of rows with labels
    existing_rows = 0
    for row in range(frame.rows):
        if not is_row_empty(frame, row):
            existing_rows += 1
    return existing_rows

def add_row():
    existing_rows = get_existing_rows(frame)
    new_row = existing_rows
    frame.rows += 1

    # Check if the new row should have a label
    if is_row_empty(frame, new_row):
        insert_label(frame, new_row)

root = tk.Tk()
root.title("Dynamic Rows")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

frame.columns = 10  # Number of columns
frame.rows = 0  # Initialize the number of rows

# Create and insert some initial labels (for demonstration)
insert_label(frame, frame.rows)
frame.rows += 1

# Create a button to add a new row
add_button = tk.Button(root, text="Add Row", command=add_row)
add_button.grid(row=1, column=0, pady=10)

root.mainloop()