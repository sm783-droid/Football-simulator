"""test_db.py — schema and team operation tests"""
import sqlite3
import pytest
import db


def test_init_creates_tables():
    with db.get_db() as c:
        tables = {r[0] for r in
                  c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    assert {"teams", "games"} <= tables


def test_add_team_persists():
    db.add_team("Test FC")
    with db.get_db() as c:
        row = c.execute("SELECT name FROM teams WHERE name='Test FC'").fetchone()
    assert row is not None


def test_add_team_duplicate_is_ignored():
    db.add_team("Test FC")
    db.add_team("Test FC")       # second insert should silently fail
    assert db.team_count() == 1


def test_team_count_empty():
    assert db.team_count() == 0


def test_team_count_after_inserts():
    for name in ("Alpha FC", "Beta United", "Gamma City"):
        db.add_team(name)
    assert db.team_count() == 3


def test_team_ids_returns_list_of_ints():
    db.add_team("Alpha FC")
    ids = db.team_ids()
    assert isinstance(ids, list)
    assert all(isinstance(i, int) for i in ids)


def test_team_ids_count_matches_team_count():
    for n in ("A", "B", "C"):
        db.add_team(n)
    assert len(db.team_ids()) == db.team_count()


def test_get_teams_ordered_by_points():
    """Highest-points team should come first."""
    import db_games
    db.add_team("Top FC"); db.add_team("Bottom FC")
    with db.get_db() as c:
        top_id = c.execute("SELECT id FROM teams WHERE name='Top FC'").fetchone()[0]
        bot_id = c.execute("SELECT id FROM teams WHERE name='Bottom FC'").fetchone()[0]
    db_games.add_fixture(1, top_id, bot_id)
    db_games.save_score(db_games.get_week(1)[0]["id"], 3, 0)   # Top FC wins

    teams = db.get_teams()
    assert teams[0]["name"] == "Top FC"
    assert teams[0]["points"] == 3
    assert teams[1]["points"] == 0


def test_reset_removes_all_data():
    db.add_team("Gone FC")
    db.reset()
    assert db.team_count() == 0
    with db.get_db() as c:
        assert c.execute("SELECT COUNT(*) FROM games").fetchone()[0] == 0
