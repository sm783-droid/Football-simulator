"""styles.py — colour palette and ttk style configuration"""
from tkinter import ttk

BG, PANEL  = "#1b1f2a", "#252a38"
ACCENT     = "#27ae60"
ACCENT2    = "#2980b9"
TEXT, MUTED = "#ecf0f1", "#95a5a6"
WIN_CLR, DRAW_CLR, LOSS_CLR = "#27ae60", "#f39c12", "#e74c3c"
ENTRY_BG   = "#1b1f2a"

def apply(root):
    s = ttk.Style(root)
    s.theme_use("clam")

    s.configure(".",               background=BG,    foreground=TEXT, font=("Helvetica", 10))
    s.configure("TNotebook",       background=BG,    borderwidth=0)
    s.configure("TNotebook.Tab",   background=PANEL, foreground=MUTED,
                padding=[14, 6],   font=("Helvetica", 10, "bold"))
    s.map("TNotebook.Tab", background=[("selected", ACCENT)],
                           foreground=[("selected", TEXT)])

    s.configure("TFrame",          background=BG)
    s.configure("TLabel",          background=BG,    foreground=TEXT)
    s.configure("Header.TLabel",   background=BG,    foreground=TEXT,
                font=("Helvetica", 13, "bold"))
    s.configure("Muted.TLabel",    background=BG,    foreground=MUTED, font=("Helvetica", 9))
    s.configure("Week.TLabel",     background=BG,    foreground=ACCENT,
                font=("Helvetica", 14, "bold"))

    for name, bg, hover in [
        ("TButton",      PANEL,       ACCENT),
        ("Green.TButton", ACCENT,     "#1e8449"),
        ("Blue.TButton",  ACCENT2,    "#1a6fa0"),
        ("Danger.TButton","#922b21",  "#7b241c"),
    ]:
        s.configure(name, background=bg, foreground=TEXT,
                    font=("Helvetica", 10, "bold"), padding=[10, 5], relief="flat")
        s.map(name, background=[("active", hover)])

    s.configure("Treeview",         background=PANEL, foreground=TEXT,
                fieldbackground=PANEL, rowheight=26, borderwidth=0)
    s.configure("Treeview.Heading", background="#1a1e2a", foreground=ACCENT,
                font=("Helvetica", 10, "bold"), relief="flat")
    s.map("Treeview", background=[("selected", ACCENT2)])
    s.configure("TScrollbar",       background=PANEL, troughcolor=BG)
