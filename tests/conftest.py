"""conftest.py — shared pytest fixtures for all test modules"""
import sys, os
import pytest

# Make source root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import db


@pytest.fixture(autouse=True)
def isolated_db(tmp_path):
    """Point db.DB_PATH at a fresh temp file for every test, then tear it down."""
    db.DB_PATH = str(tmp_path / "test_football.db")
    db.init()
    yield
    # tmp_path is cleaned up automatically by pytest


@pytest.fixture
def ten_teams():
    """Register 10 unique teams and return their IDs."""
    import simulation
    for name in simulation.random_names(10):
        db.add_team(name)
    return db.team_ids()


@pytest.fixture
def full_fixtures(ten_teams):
    """Build and persist all 90 fixtures; return the team ID list."""
    import db_games, simulation
    for w, h, a in simulation.make_fixtures(ten_teams):
        db_games.add_fixture(w, h, a)
    return ten_teams


@pytest.fixture
def two_teams():
    """Add two teams and one unplayed game; returns (home_id, away_id, game_id)."""
    import db_games
    db.add_team("Home FC")
    db.add_team("Away FC")
    ids = db.team_ids()
    db_games.add_fixture(1, ids[0], ids[1])
    game = db_games.get_week(1)[0]
    return ids[0], ids[1], game["id"]
