"""ui_setup.py — Setup tab: register teams, generate fixtures, reset"""
import tkinter as tk
from tkinter import ttk, messagebox
import store, simulation
from styles import PANEL, ACCENT2, TEXT


class SetupTab:
    def __init__(self, parent, on_change):
        self._on_change = on_change
        self._build(parent)

    def _build(self, f):
        ttk.Label(f, text="Season Setup",
                  style="Header.TLabel").pack(pady=(18, 4))
        ttk.Label(f, text="Register 10 teams randomly, then generate the full fixture list.",
                  style="Muted.TLabel").pack()

        row = ttk.Frame(f)
        row.pack(pady=14)
        ttk.Button(row, text="Register 10 Teams", style="Green.TButton",
                   command=self._register).pack(side="left", padx=6)
        ttk.Button(row, text="Generate Fixtures", style="Blue.TButton",
                   command=self._generate).pack(side="left", padx=6)
        ttk.Button(row, text="Reset Season",      style="Danger.TButton",
                   command=self._reset).pack(side="left", padx=6)

        lf = ttk.Frame(f)
        lf.pack(fill="both", expand=True, padx=30, pady=(0, 10))
        sb = ttk.Scrollbar(lf, orient="vertical")
        self._listbox = tk.Listbox(lf, bg=PANEL, fg=TEXT, selectbackground=ACCENT2,
                                   font=("Helvetica", 11), relief="flat", borderwidth=0,
                                   yscrollcommand=sb.set, activestyle="none")
        sb.config(command=self._listbox.yview)
        self._listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._status = ttk.Label(f, text="", style="Muted.TLabel")
        self._status.pack(pady=(0, 8))

    def refresh(self):
        self._listbox.delete(0, "end")
        for i, t in enumerate(store.get_teams(), 1):
            self._listbox.insert("end", f"  {i:>2}.  {t['name']}")

    def _register(self):
        if store.team_count() > 0:
            if not messagebox.askyesno("Teams exist", "Reset and re-register?"):
                return
            store.reset()
        for name in simulation.random_names(10):
            store.add_team(name)
        for team in store.get_teams():
            store.add_manager(team["id"], simulation.random_manager_name())
        self._on_change()
        self._status.config(text="✓  10 teams registered with managers.")

    def _generate(self):
        if store.team_count() < 10:
            messagebox.showerror("No teams", "Register 10 teams first.")
            return
        if store.has_fixtures():
            if not messagebox.askyesno("Fixtures exist", "Regenerate?"):
                return
            names = [self._listbox.get(i) for i in range(self._listbox.size())]
            store.reset()
            for n in names:
                store.add_team(n.strip())
        for (w, h, a) in simulation.make_fixtures(store.team_ids()):
            store.add_fixture(w, h, a)
        self._on_change()
        self._status.config(text=f"✓  90 fixtures over {store.max_week()} game weeks.")

    def _reset(self):
        if not messagebox.askyesno("Reset", "Delete all data? This cannot be undone."):
            return
        store.reset()
        self._on_change()
        self._status.config(text="Season reset.")
