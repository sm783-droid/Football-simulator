"""app.py — entry point; assembles tabs and wires refresh callbacks"""
import tkinter as tk
from tkinter import ttk
import db, db_games, styles
from ui_setup    import SetupTab
from ui_week     import WeekTab
from ui_league   import LeagueTab
from ui_managers import ManagersTab

class FootballApp:
    def __init__(self, root: tk.Tk):
        root.title("Football Tournament Simulator")
        root.geometry("960x660")
        root.configure(bg=styles.BG)

        db.init()
        styles.apply(root)

        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        tabs = [ttk.Frame(nb) for _ in range(4)]
        for frame, name in zip(tabs, ["  Setup  ", "  Game Week  ", "  League Table  ", "  Managers  "]):
            nb.add(frame, text=name)

        self.setup_tab    = SetupTab(tabs[0],  self.refresh_all)
        self.week_tab     = WeekTab(tabs[1],   self.refresh_league)
        self.league_tab   = LeagueTab(tabs[2])
        self.managers_tab = ManagersTab(tabs[3])
        self.refresh_all()

    def refresh_all(self):
        self.week_tab.current_week = db_games.current_week() or 1
        self.setup_tab.refresh()
        self.week_tab.refresh()
        self.league_tab.refresh()
        self.managers_tab.refresh()

    def refresh_league(self):
        self.league_tab.refresh()
        self.managers_tab.refresh()

if __name__ == "__main__":
    root = tk.Tk()
    FootballApp(root)
    root.mainloop()
