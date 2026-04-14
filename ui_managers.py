"""ui_managers.py — Manager Stats tab

Displays manager records next to their team's actual points so the bug
(manager stats stuck at 0) is immediately visible.
"""
import tkinter as tk
from tkinter import ttk
import db_managers
from styles import PANEL, ACCENT, ACCENT2, WIN_CLR, LOSS_CLR, MUTED

_COLS   = ("pos", "manager", "team", "w", "d", "l", "mgr_pts", "team_pts", "drift")
_HEADS  = ("#", "Manager", "Team", "W", "D", "L", "Mgr Pts", "Team Pts", "Drift")
_WIDTHS = (40, 160, 160, 45, 45, 45, 75, 80, 70)


class ManagersTab:
    def __init__(self, parent):
        self._build(parent)

    def _build(self, f):
        ttk.Label(f, text="Manager Stats", style="Header.TLabel").pack(pady=(18, 4))
        ttk.Label(
            f,
            text='⚠  "Mgr Pts" should equal "Team Pts" — any drift indicates the bug',
            style="Muted.TLabel",
        ).pack(pady=(0, 8))

        tf = ttk.Frame(f)
        tf.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        vsb = ttk.Scrollbar(tf, orient="vertical")
        self._tree = ttk.Treeview(
            tf,
            columns=_COLS,
            show="headings",
            yscrollcommand=vsb.set,
            selectmode="none",
        )
        vsb.config(command=self._tree.yview)

        for col, head, width in zip(_COLS, _HEADS, _WIDTHS):
            anchor = "w" if col in ("manager", "team") else "center"
            self._tree.heading(col, text=head, anchor=anchor)
            self._tree.column(col, width=width, anchor=anchor, stretch=(col == "team"))

        self._tree.tag_configure("odd",  background=PANEL)
        self._tree.tag_configure("even", background="#2c3245")
        # Red highlight when mgr pts != team pts (the bug is present)
        self._tree.tag_configure("bugged", background="#3b1a1a", foreground=LOSS_CLR)
        # Green when in sync
        self._tree.tag_configure("ok", background="#1a3b1a", foreground=WIN_CLR)

        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Legend
        legend = ttk.Frame(f)
        legend.pack(pady=(0, 6))
        tk.Label(legend, text="  Bug (mgr pts ≠ team pts)  ",
                 bg=LOSS_CLR, fg="#fff", font=("Helvetica", 9)).pack(side="left", padx=4)
        tk.Label(legend, text="  In sync  ",
                 bg=WIN_CLR, fg="#fff", font=("Helvetica", 9)).pack(side="left", padx=4)

        ttk.Button(f, text="Refresh Managers", command=self.refresh).pack(pady=(0, 14))

    def refresh(self):
        self._tree.delete(*self._tree.get_children())
        rows = db_managers.get_all_managers()

        if not rows:
            self._tree.insert("", "end", values=(
                "-", "(no managers registered)", "", "", "", "", "", "", ""
            ))
            return

        for pos, m in enumerate(rows, 1):
            mgr_pts  = m["points"]
            team_pts = m["team_points"]
            drift    = team_pts - mgr_pts

            if drift != 0:
                tag = "bugged"
                drift_str = f"−{drift}" if drift < 0 else f"+{drift}"
            else:
                tag = "ok"
                drift_str = "0"

            self._tree.insert("", "end", tags=(tag,), values=(
                pos,
                m["name"],
                m["team_name"],
                m["wins"],
                m["draws"],
                m["losses"],
                mgr_pts,
                team_pts,
                drift_str,
            ))
