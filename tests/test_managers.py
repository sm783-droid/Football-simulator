"""
test_managers.py — manager feature tests

3 tests below are INTENTIONALLY FAILING.
Managers exist and are linked to teams, but _delta() in db_games.py
does not yet update manager stats after results.

To fix: uncomment the TODO block at the bottom of _delta() in db_games.py.
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

# failing tests 
def test_manager_points_match_team_points_after_win():
    """After a home win, the manager's points should equal the team's points (3)."""
    home_id, _, game_id = _setup_game()
    db_games.save_score(game_id, 2, 0)          

    team = next(t for t in db.get_teams() if t["id"] == home_id)
    mgr  = db_managers.get_manager(home_id)

    assert mgr["points"] == team["points"]      


def test_manager_win_record_matches_team_after_multiple_games():
    """Manager's wins should track the team's wins across several game weeks."""
    db.add_team("Home FC"); db.add_team("Away FC")
    home_id, away_id = db.team_ids()
    db_managers.add_manager(home_id, simulation.random_manager_name())
    db_managers.add_manager(away_id, simulation.random_manager_name())

    for week in range(1, 4):                   
        db_games.add_fixture(week, home_id, away_id)
        db_games.save_score(db_games.get_week(week)[0]["id"], 1, 0)

    team = next(t for t in db.get_teams() if t["id"] == home_id)
    mgr  = db_managers.get_manager(home_id)

    assert mgr["wins"] == team["won"]           


def test_manager_stats_revert_correctly_on_score_override():
    """
    Override a result: manager stats should revert the old result
    and apply the new one, staying in sync with the team.
    """
    home_id, _, game_id = _setup_game()
    db_games.save_score(game_id, 3, 0)          
    db_games.save_score(game_id, 0, 0)          

    team = next(t for t in db.get_teams() if t["id"] == home_id)
    mgr  = db_managers.get_manager(home_id)

    assert mgr["points"] == team["points"]      
    assert mgr["draws"]  == team["drawn"]  