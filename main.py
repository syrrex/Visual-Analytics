import tkinter as tk
from api import NFLDataAPI
from gui import NFLApp

if __name__ == "__main__":
    root = tk.Tk()
    api = NFLDataAPI()
    app = NFLApp(root, api)
    root.mainloop()