"""test_managers.py — manager feature tests"""
import pytest
import store, simulation


def test_manager_is_assigned_to_team():
    store.add_team("Test FC")
    tid = store.team_ids()[0]
    store.add_manager(tid, "Alex Ferguson")
    mgr = store.get_manager(tid)
    assert mgr is not None
    assert mgr["name"] == "Alex Ferguson"
    assert mgr["team_id"] == tid


def test_get_all_managers_returns_one_per_team():
    for name in ("Club A", "Club B", "Club C"):
        store.add_team(name)
    for tid in store.team_ids():
        store.add_manager(tid, simulation.random_manager_name())
    assert len(store.get_all_managers()) == 3


def test_manager_initial_stats_are_zero():
    store.add_team("Fresh FC")
    tid = store.team_ids()[0]
    store.add_manager(tid, "New Boss")
    mgr = store.get_manager(tid)
    assert mgr["wins"] == 0
    assert mgr["draws"] == 0
    assert mgr["losses"] == 0
    assert mgr["points"] == 0
