"""
test_managers.py — manager feature tests
"""
import pytest
import db, db_games, db_managers, simulation

def _setup_game(home_name="Home FC", away_name="Away FC"):
    """Register two teams with managers, add one fixture; return (home_id, away_id, game_id)."""
    db.add_team(home_name)
    db.add_team(away_name)
    home_id, away_id = db.team_ids()
    db_managers.add_manager(home_id, simulation.random_manager_name())
    db_managers.add_manager(away_id, simulation.random_manager_name())
    db_games.add_fixture(1, home_id, away_id)
    return home_id, away_id, db_games.get_week(1)[0]["id"]

def test_manager_is_assigned_to_team():
    db.add_team("Test FC")
    tid = db.team_ids()[0]
    db_managers.add_manager(tid, "Alex Ferguson")
    mgr = db_managers.get_manager(tid)
    assert mgr is not None
    assert mgr["name"] == "Alex Ferguson"
    assert mgr["team_id"] == tid


def test_get_all_managers_returns_one_per_team():
    for name in ["Club A", "Club B", "Club C"]:
        db.add_team(name)
    for tid in db.team_ids():
        db_managers.add_manager(tid, simulation.random_manager_name())
    assert len(db_managers.get_all_managers()) == 3


def test_manager_initial_stats_are_zero():
    db.add_team("Fresh FC")
    tid = db.team_ids()[0]
    db_managers.add_manager(tid, "New Boss")
    mgr = db_managers.get_manager(tid)
    assert mgr["wins"] == 0
    assert mgr["draws"] == 0
    assert mgr["losses"] == 0
    assert mgr["points"] == 0

