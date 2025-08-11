# main.py

import tkinter as tk
from gui import UnifiedGUI

# ==============================================================================
# == 🚦 RUN APPLICATION
# ==============================================================================
if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    
    # Initialize the GUI application
    app = UnifiedGUI(root)
    
    # Start the Tkinter event loop
    root.mainloop()