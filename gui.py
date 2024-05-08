import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import seaborn as sns

class NFLApp:
    def __init__(self, root, api):
        self.api = api
        self.root = root
        self.root.title("NFL Visual Analytics")

        self.team_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select Team:").grid(row=0, column=0, padx=10, pady=10)
        self.team_entry = ttk.Entry(self.root, textvariable=self.team_var)
        self.team_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ttk.Button(self.root, text="Search", command=self.search_team)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.plot_button = ttk.Button(self.root, text="Show Plot", command=self.show_plot)
        self.plot_button.grid(row=2, column=0, columnspan=3, pady=10)

    def search_team(self):
        team_name = self.team_var.get()
        team_stats = self.api.get_team_stats(team_name)

        self.result_text.delete(1.0, tk.END)
        if team_stats:
            result = f"Team: {team_stats['Team']}\nWins: {team_stats['Win']}\nLosses: {team_stats['Loss']}"
            self.result_text.insert(tk.END, result)
        else:
            messagebox.showerror("Error", "Team not found")

    def show_plot(self):
        data = self.api.data
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Team', y='Win', data=data)
        plt.title("Team Wins")
        plt.xlabel("Team")
        plt.ylabel("Wins")
        plt.show()