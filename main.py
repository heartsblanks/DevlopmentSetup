import tkinter as tk
from gui import InstallOrchestrationGUI


def main():
    root = tk.Tk()
    app = InstallOrchestrationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
