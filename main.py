import tkinter as tk
import logging
from gui import InstallOrchestrationGUI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    try:
        root = tk.Tk()
        app = InstallOrchestrationGUI(root)
        root.mainloop()
    except Exception as e:
        logging.exception("Unhandled exception occurred: %s", e)

if __name__ == "__main__":
    main()
