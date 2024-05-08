import tkinter as tk
from api import NFLDataAPI
from gui import NFLApp
from gamefield import GameField

if __name__ == "__main__":
    #root = tk.Tk()
    api = NFLDataAPI()
    game_field = GameField()
    #app = NFLApp(root, api)
    #root.mainloop()