"""ui_week.py — Game Week tab: view fixtures, simulate, save/override scores"""
import tkinter as tk
from tkinter import ttk, messagebox
import db_games, simulation
from styles import BG, PANEL, MUTED, TEXT, ENTRY_BG, WIN_CLR, DRAW_CLR, LOSS_CLR

class WeekTab:
    def __init__(self, parent, on_scores_change):
        self._on_change = on_scores_change
        self.current_week = 1
        self._game_ids = []
        self._rows = []
        self._build(parent)

    def _build(self, f):
        nav = ttk.Frame(f); nav.pack(fill="x", padx=20, pady=(16, 4))
        ttk.Button(nav, text="◀ Prev", command=self._prev).pack(side="left")
        self._week_lbl = ttk.Label(nav, text="Game Week —", style="Week.TLabel")
        self._week_lbl.pack(side="left", padx=20)
        ttk.Button(nav, text="Next ▶", command=self._next).pack(side="left")

        self._info = ttk.Label(f, text="", style="Muted.TLabel"); self._info.pack()
        self._fixture_frame = ttk.Frame(f); self._fixture_frame.pack(fill="x", padx=20, pady=8)
        for _ in range(5):
            self._rows.append(self._make_row(self._fixture_frame))

        btns = ttk.Frame(f); btns.pack(pady=10)
        ttk.Button(btns, text="Simulate Week", style="Green.TButton",
                   command=self._simulate).pack(side="left", padx=8)
        ttk.Button(btns, text="Save Scores",   style="Blue.TButton",
                   command=self._save).pack(side="left", padx=8)
        self._status = ttk.Label(f, text="", style="Muted.TLabel"); self._status.pack()

    def _make_row(self, parent):
        rf = tk.Frame(parent, bg=PANEL, padx=10, pady=8); rf.pack(fill="x", pady=3)
        def lbl(w=22, anchor="e"):
            l = tk.Label(rf, text="", bg=PANEL, fg=TEXT, font=("Helvetica", 11),
                         width=w, anchor=anchor); l.pack(side="left", padx=4); return l
        def entry():
            v = tk.StringVar()
            e = tk.Entry(rf, textvariable=v, width=3, bg=ENTRY_BG, fg=TEXT,
                         insertbackground=TEXT, font=("Helvetica", 12, "bold"),
                         justify="center", relief="flat", highlightthickness=1,
                         highlightbackground=PANEL)
            e.pack(side="left", padx=4); return v
        hl = lbl(); hv = entry()
        tk.Label(rf, text="–", bg=PANEL, fg=MUTED, font=("Helvetica", 13, "bold")).pack(side="left")
        av = entry(); al = lbl(anchor="w")
        badge = tk.Label(rf, text="", bg=PANEL, font=("Helvetica", 9, "bold"), width=8)
        badge.pack(side="right", padx=8)
        return dict(hl=hl, hv=hv, av=av, al=al, badge=badge)

    def refresh(self):
        mw = db_games.max_week()
        self._week_lbl.config(text=f"Game Week {self.current_week}" + (f" / {mw}" if mw else ""))
        games = db_games.get_week(self.current_week)
        if not games:
            self._info.config(text="No fixtures. Register teams and generate fixtures first.")
            for r in self._rows: r["hl"].config(text=""); r["al"].config(text="")
            self._game_ids = []; return
        self._info.config(text=f"{sum(g['played'] for g in games)} of {len(games)} played")
        self._game_ids = []
        for game, row in zip(games, self._rows):
            self._game_ids.append(game["id"])
            row["hl"].config(text=game["home_team"])
            row["al"].config(text=game["away_team"])
            if game["played"]:
                hs, as_ = game["home_score"], game["away_score"]
                row["hv"].set(str(hs)); row["av"].set(str(as_))
                result = ("HOME WIN", WIN_CLR) if hs > as_ else \
                         ("AWAY WIN", LOSS_CLR) if hs < as_ else ("DRAW", DRAW_CLR)
                row["badge"].config(text=result[0], fg=result[1])
            else:
                row["hv"].set(""); row["av"].set("")
                row["badge"].config(text="PENDING", fg=MUTED)

    def _simulate(self):
        if not db_games.has_fixtures():
            messagebox.showerror("No fixtures", "Generate fixtures first."); return
        for g in db_games.get_week(self.current_week):
            if not g["played"]:
                db_games.save_score(g["id"], *simulation.random_score())
        self.refresh(); self._on_change()
        self._status.config(text=f"✓  Week {self.current_week} simulated.")

    def _save(self):
        if not self._game_ids: messagebox.showerror("No fixtures", "Nothing to save."); return
        errors, parsed = [], []
        for idx, (gid, row) in enumerate(zip(self._game_ids, self._rows), 1):
            hs_raw, as_raw = row["hv"].get().strip(), row["av"].get().strip()
            if hs_raw == "" and as_raw == "": parsed.append(None); continue
            try:
                hs, as_ = int(hs_raw), int(as_raw)
                if hs < 0 or as_ < 0: raise ValueError
            except ValueError:
                errors.append(f"  Game {idx}: scores must be whole numbers ≥ 0.")
                parsed.append(None); continue
            parsed.append((hs, as_))
        if errors:
            messagebox.showerror("Invalid scores", "\n".join(errors)); return
        saved = sum(1 for gid, s in zip(self._game_ids, parsed)
                    if s and not db_games.save_score(gid, s[0], s[1]))
        self.refresh(); self._on_change()
        self._status.config(text=f"✓  {len([s for s in parsed if s])} score(s) saved.")

    def _prev(self):
        if self.current_week > 1: self.current_week -= 1; self.refresh()
    def _next(self):
        if self.current_week < db_games.max_week(): self.current_week += 1; self.refresh()
