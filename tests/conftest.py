"""conftest.py — shared pytest fixtures for all test modules"""
import sys, os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import store


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the in-memory store before every test."""
    store.reset()
    yield


@pytest.fixture
def ten_teams():
    """Register 10 unique teams and return their IDs."""
    import simulation
    for name in simulation.random_names(10):
        store.add_team(name)
    return store.team_ids()


@pytest.fixture
def full_fixtures(ten_teams):
    """Build and persist all 90 fixtures; return the team ID list."""
    import simulation
    for w, h, a in simulation.make_fixtures(ten_teams):
        store.add_fixture(w, h, a)
    return ten_teams


@pytest.fixture
def two_teams():
    """Add two teams and one unplayed game; returns (home_id, away_id, game_id)."""
    store.add_team("Home FC")
    store.add_team("Away FC")
    ids = store.team_ids()
    store.add_fixture(1, ids[0], ids[1])
    game = store.get_week(1)[0]
    return ids[0], ids[1], game["id"]
