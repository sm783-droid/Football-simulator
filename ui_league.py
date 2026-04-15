"""ui_league.py — League Table tab"""
from tkinter import ttk
import store
from styles import PANEL, ACCENT, ACCENT2

_COLS   = ("pos","team","p","w","d","l","gf","ga","gd","pts")
_HEADS  = ("#","Team","P","W","D","L","GF","GA","GD","Pts")
_WIDTHS = (40, 200, 45, 45, 45, 45, 45, 45, 50, 55)

class LeagueTab:
    def __init__(self, parent):
        self._build(parent)

    def _build(self, f):
        ttk.Label(f, text="League Table", style="Header.TLabel").pack(pady=(18, 8))

        tf = ttk.Frame(f); tf.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        vsb = ttk.Scrollbar(tf, orient="vertical")
        self._tree = ttk.Treeview(tf, columns=_COLS, show="headings",
                                  yscrollcommand=vsb.set, selectmode="none")
        vsb.config(command=self._tree.yview)

        for col, head, width in zip(_COLS, _HEADS, _WIDTHS):
            anchor = "w" if col == "team" else "center"
            self._tree.heading(col, text=head, anchor=anchor)
            self._tree.column(col, width=width, anchor=anchor, stretch=(col == "team"))

        self._tree.tag_configure("top3", background="#1c3a2a")
        self._tree.tag_configure("odd",  background=PANEL)
        self._tree.tag_configure("even", background="#2c3245")
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(f, text="Refresh Table", command=self.refresh).pack(pady=(0, 14))

    def refresh(self):
        self._tree.delete(*self._tree.get_children())
        for pos, t in enumerate(store.get_teams(), 1):
            gd = t["goals_for"] - t["goals_against"]
            tag = "top3" if pos <= 3 else ("odd" if pos % 2 else "even")
            self._tree.insert("", "end", tags=(tag,), values=(
                pos, t["name"], t["played"], t["won"], t["drawn"], t["lost"],
                t["goals_for"], t["goals_against"],
                f"+{gd}" if gd > 0 else str(gd), t["points"]
            ))
