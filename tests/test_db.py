"""test_db.py — team store operation tests"""
import pytest
import store


def test_add_team_persists():
    store.add_team("Test FC")
    names = [t["name"] for t in store.get_teams()]
    assert "Test FC" in names


def test_add_team_duplicate_is_ignored():
    store.add_team("Test FC")
    store.add_team("Test FC")
    assert store.team_count() == 1


def test_team_count_empty():
    assert store.team_count() == 0


def test_team_count_after_inserts():
    for name in ("Alpha FC", "Beta United", "Gamma City"):
        store.add_team(name)
    assert store.team_count() == 3


def test_team_ids_returns_list_of_ints():
    store.add_team("Alpha FC")
    ids = store.team_ids()
    assert isinstance(ids, list)
    assert all(isinstance(i, int) for i in ids)


def test_team_ids_count_matches_team_count():
    for n in ("A", "B", "C"):
        store.add_team(n)
    assert len(store.team_ids()) == store.team_count()


def test_get_teams_ordered_by_points():
    """Highest-points team should come first."""
    store.add_team("Top FC")
    store.add_team("Bottom FC")
    top_id, bot_id = store.team_ids()
    store.add_fixture(1, top_id, bot_id)
    store.save_score(store.get_week(1)[0]["id"], 3, 0)

    teams = store.get_teams()
    assert teams[0]["name"] == "Top FC"
    assert teams[0]["points"] == 3
    assert teams[1]["points"] == 0


def test_reset_removes_all_data():
    store.add_team("Gone FC")
    store.reset()
    assert store.team_count() == 0
    assert not store.has_fixtures()
