"""test_bugs.py — failing tests that expose the manager-stats bug.

These tests are EXPECTED TO FAIL on the current codebase.
Manager stats (wins/draws/losses/points) are never written by _delta(),
so they stay at 0 even after match results are saved.
"""
import pytest
import db, db_games, db_managers


@pytest.fixture
def two_teams_with_managers():
    """Two teams, each with a manager, and one unplayed fixture in week 1."""
    db.add_team("Home FC")
    db.add_team("Away FC")
    home_id, away_id = db.team_ids()
    db_managers.add_manager(home_id, "Alice")
    db_managers.add_manager(away_id, "Bob")
    db_games.add_fixture(1, home_id, away_id)
    game_id = db_games.get_week(1)[0]["id"]
    return home_id, away_id, game_id


def test_winning_manager_gets_3_points(two_teams_with_managers):
    """After a home win (2-0), the home manager should have 3 points and 1 win."""
    home_id, away_id, game_id = two_teams_with_managers

    db_games.save_score(game_id, 2, 0)

    home_mgr = db_managers.get_manager(home_id)
    assert home_mgr["points"] == 3, (
        f"Expected home manager to have 3 points after a win, got {home_mgr['points']}"
    )
    assert home_mgr["wins"] == 1, (
        f"Expected home manager to have 1 win, got {home_mgr['wins']}"
    )


def test_losing_manager_gets_0_points_and_1_loss(two_teams_with_managers):
    """After a home win (2-0), the away manager should have 0 points and 1 loss."""
    home_id, away_id, game_id = two_teams_with_managers

    db_games.save_score(game_id, 2, 0)

    away_mgr = db_managers.get_manager(away_id)
    assert away_mgr["losses"] == 1, (
        f"Expected away manager to have 1 loss, got {away_mgr['losses']}"
    )
    assert away_mgr["points"] == 0


def test_draw_gives_both_managers_1_point(two_teams_with_managers):
    """After a 1-1 draw, both managers should have 1 point and 1 draw."""
    home_id, away_id, game_id = two_teams_with_managers

    db_games.save_score(game_id, 1, 1)

    home_mgr = db_managers.get_manager(home_id)
    away_mgr = db_managers.get_manager(away_id)

    assert home_mgr["draws"] == 1 and home_mgr["points"] == 1, (
        f"Home manager: expected 1 draw / 1 pt, got {home_mgr['draws']} draws / {home_mgr['points']} pts"
    )
    assert away_mgr["draws"] == 1 and away_mgr["points"] == 1, (
        f"Away manager: expected 1 draw / 1 pt, got {away_mgr['draws']} draws / {away_mgr['points']} pts"
    )


def test_manager_points_match_team_points_after_win(two_teams_with_managers):
    """Manager points should always mirror their team's points."""
    home_id, away_id, game_id = two_teams_with_managers

    db_games.save_score(game_id, 3, 1)

    home_team = next(t for t in db.get_teams() if t["id"] == home_id)
    home_mgr  = db_managers.get_manager(home_id)

    assert home_mgr["points"] == home_team["points"], (
        f"Manager points ({home_mgr['points']}) out of sync with team points ({home_team['points']})"
    )


def test_score_override_keeps_manager_stats_in_sync(two_teams_with_managers):
    """Saving a new score over an existing result should update manager stats, not stack them."""
    home_id, away_id, game_id = two_teams_with_managers

    db_games.save_score(game_id, 2, 0)   # home wins
    db_games.save_score(game_id, 0, 2)   # override: away wins

    home_mgr = db_managers.get_manager(home_id)
    away_mgr = db_managers.get_manager(away_id)

    # After the override the home manager should have 0 points (lost), not 3
    assert home_mgr["points"] == 0, (
        f"Home manager should have 0 pts after override to a loss, got {home_mgr['points']}"
    )
    assert home_mgr["losses"] == 1 and home_mgr["wins"] == 0

    # Away manager should now have the win
    assert away_mgr["points"] == 3, (
        f"Away manager should have 3 pts after override to a win, got {away_mgr['points']}"
    )
    assert away_mgr["wins"] == 1 and away_mgr["losses"] == 0
