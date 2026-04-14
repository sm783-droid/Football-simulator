"""db_managers.py — manager CRUD

Manager stats (wins/draws/losses/points) exist in the schema but are never
updated by _delta() in db_games.py 
"""
from db import get_db


def add_manager(team_id: int, name: str):
    with get_db() as c:
        c.execute("INSERT OR REPLACE INTO managers (team_id, name) VALUES (?,?)",
                  (team_id, name))


def get_manager(team_id: int):
    """Return the manager row for a team, or None."""
    with get_db() as c:
        return c.execute(
            "SELECT * FROM managers WHERE team_id=?", (team_id,)
        ).fetchone()


def get_all_managers():
    """All managers joined with their team name, ordered by manager points."""
    with get_db() as c:
        return c.execute("""
            SELECT m.*, t.name AS team_name, t.points AS team_points
            FROM   managers m
            JOIN   teams    t ON m.team_id = t.id
            ORDER  BY m.points DESC
        """).fetchall()
