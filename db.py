"""db.py — connection, schema, team operations"""
import sqlite3, os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "football.db")

@contextmanager
def get_db():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    try:
        yield c
        c.commit()
    finally:
        c.close()

def init():
    with get_db() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                played INTEGER DEFAULT 0, won INTEGER DEFAULT 0,
                drawn  INTEGER DEFAULT 0, lost INTEGER DEFAULT 0,
                goals_for INTEGER DEFAULT 0, goals_against INTEGER DEFAULT 0,
                points INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS managers (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER UNIQUE NOT NULL REFERENCES teams(id),
                name    TEXT    NOT NULL,
                wins    INTEGER DEFAULT 0,
                draws   INTEGER DEFAULT 0,
                losses  INTEGER DEFAULT 0,
                points  INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS games (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                game_week    INTEGER NOT NULL,
                home_team_id INTEGER NOT NULL REFERENCES teams(id),
                away_team_id INTEGER NOT NULL REFERENCES teams(id),
                home_score   INTEGER, away_score INTEGER,
                played       INTEGER DEFAULT 0
            );
        """)

def reset():
    with get_db() as c:
        c.executescript("DELETE FROM games; DELETE FROM managers; DELETE FROM teams;")

def add_team(name):
    with get_db() as c:
        c.execute("INSERT OR IGNORE INTO teams (name) VALUES (?)", (name,))

def get_teams():
    with get_db() as c:
        return c.execute("""
            SELECT * FROM teams
            ORDER BY points DESC,
                     (goals_for - goals_against) DESC,
                     goals_for DESC, name
        """).fetchall()

def team_count():
    with get_db() as c:
        return c.execute("SELECT COUNT(*) FROM teams").fetchone()[0]

def team_ids():
    with get_db() as c:
        return [r[0] for r in c.execute("SELECT id FROM teams ORDER BY id").fetchall()]
