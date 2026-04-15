"""db_games.py — fixture and score operations"""
from db import get_db


def has_fixtures():
    with get_db() as c:
        return c.execute("SELECT COUNT(*) FROM games").fetchone()[0] > 0


def add_fixture(week, home_id, away_id):
    with get_db() as c:
        c.execute("INSERT INTO games (game_week, home_team_id, away_team_id) VALUES (?,?,?)",
                  (week, home_id, away_id))


def get_week(week):
    with get_db() as c:
        return c.execute("""
            SELECT g.*, t1.name home_team, t2.name away_team
            FROM   games g
            JOIN   teams t1 ON g.home_team_id = t1.id
            JOIN   teams t2 ON g.away_team_id = t2.id
            WHERE  g.game_week = ? ORDER BY g.id
        """, (week,)).fetchall()


def max_week():
    with get_db() as c:
        return c.execute("SELECT MAX(game_week) FROM games").fetchone()[0] or 0


def current_week():
    with get_db() as c:
        r = c.execute(
            "SELECT MIN(game_week) FROM games WHERE played=0").fetchone()[0]
    return r if r is not None else max_week()


def save_score(game_id, hs, as_):
    with get_db() as c:
        game = c.execute("SELECT * FROM games WHERE id=?",
                         (game_id,)).fetchone()
        if game["played"]:
            _delta(c, game, -1)
        c.execute("UPDATE games SET home_score=?, away_score=?, played=1 WHERE id=?",
                  (hs, as_, game_id))
        _delta(c, game, +1, hs, as_)


def _delta(c, game, sign, hs=None, as_=None):
    """Add or subtract one game's stats from both teams (sign = +1 or -1)."""
    h, a = game["home_team_id"], game["away_team_id"]
    if hs is None:
        hs, as_ = game["home_score"], game["away_score"]

    c.execute("""UPDATE teams SET
        played        = played        + ?,
        goals_for     = goals_for     + ?,
        goals_against = goals_against + ?
        WHERE id = ?""", (sign, sign * hs, sign * as_, h))

    c.execute("""UPDATE teams SET
        played        = played        + ?,
        goals_for     = goals_for     + ?,
        goals_against = goals_against + ?
        WHERE id = ?""", (sign, sign * as_, sign * hs, a))

    if hs > as_:
        c.execute(
            "UPDATE teams SET won=won+?,  points=points+? WHERE id=?", (sign, sign*3, h))
        c.execute(
            "UPDATE teams SET lost=lost+?                  WHERE id=?", (sign, a))
    elif hs < as_:
        c.execute(
            "UPDATE teams SET lost=lost+?                  WHERE id=?", (sign, h))
        c.execute(
            "UPDATE teams SET won=won+?,  points=points+? WHERE id=?", (sign, sign*3, a))
    else:
        c.execute(
            "UPDATE teams SET drawn=drawn+?, points=points+? WHERE id=?", (sign, sign, h))
        c.execute(
            "UPDATE teams SET drawn=drawn+?, points=points+? WHERE id=?", (sign, sign, a))
