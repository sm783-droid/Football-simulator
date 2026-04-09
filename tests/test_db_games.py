"""test_db_games.py — fixture scheduling, scoring, and stat delta tests"""
import pytest
import db, db_games


def _team(name):
    db.add_team(name)
    return db.team_ids()[-1]

def _stats(team_id):
    t = next(t for t in db.get_teams() if t["id"] == team_id)
    return dict(t)


def test_no_fixtures_initially():
    assert not db_games.has_fixtures()


def test_add_and_retrieve_fixture(two_teams):
    home_id, away_id, _ = two_teams
    games = db_games.get_week(1)
    assert len(games) == 1
    assert games[0]["home_team_id"] == home_id
    assert games[0]["away_team_id"] == away_id
    assert games[0]["played"] == 0


def test_max_week(full_fixtures):
    assert db_games.max_week() == 18


def test_current_week_is_first_unplayed(full_fixtures):
    assert db_games.current_week() == 1
    # Play week 1
    for g in db_games.get_week(1):
        db_games.save_score(g["id"], 1, 0)
    assert db_games.current_week() == 2


def test_current_week_when_all_played(two_teams):
    _, _, gid = two_teams
    db_games.save_score(gid, 1, 1)
    assert db_games.current_week() == db_games.max_week()

def test_home_win_stats(two_teams):
    home_id, away_id, gid = two_teams
    db_games.save_score(gid, 2, 0)
    h, a = _stats(home_id), _stats(away_id)
    assert h["won"] == 1 and h["points"] == 3 and h["goals_for"] == 2
    assert a["lost"] == 1 and a["points"] == 0 and a["goals_against"] == 2


def test_away_win_stats(two_teams):
    home_id, away_id, gid = two_teams
    db_games.save_score(gid, 0, 3)
    h, a = _stats(home_id), _stats(away_id)
    assert h["lost"] == 1 and h["points"] == 0
    assert a["won"] == 1 and a["points"] == 3


def test_draw_stats(two_teams):
    home_id, away_id, gid = two_teams
    db_games.save_score(gid, 1, 1)
    for tid in (home_id, away_id):
        s = _stats(tid)
        assert s["drawn"] == 1 and s["points"] == 1


def test_score_override_reverts_old_stats(two_teams):
    home_id, away_id, gid = two_teams
    db_games.save_score(gid, 3, 0)          # home win → 3 pts
    db_games.save_score(gid, 1, 1)          # override → draw
    h, a = _stats(home_id), _stats(away_id)
    assert h["won"] == 0 and h["drawn"] == 1 and h["points"] == 1
    assert a["lost"] == 0 and a["drawn"] == 1 and a["points"] == 1


def test_played_flag_set_after_save(two_teams):
    _, _, gid = two_teams
    db_games.save_score(gid, 0, 0)
    assert db_games.get_week(1)[0]["played"] == 1


def test_gf_equals_ga_after_full_season(full_fixtures):
    import simulation
    for w in range(1, 19):
        for g in db_games.get_week(w):
            db_games.save_score(g["id"], *simulation.random_score())
    teams = db.get_teams()
    assert sum(t["goals_for"] for t in teams) == sum(t["goals_against"] for t in teams)


def test_total_points_consistent_after_full_season(full_fixtures):
    """Total pts = 3 × wins + draws (each draw adds 2 pts to the pool)."""
    import simulation
    for w in range(1, 19):
        for g in db_games.get_week(w):
            db_games.save_score(g["id"], *simulation.random_score())
    teams = db.get_teams()
    total_pts  = sum(t["points"] for t in teams)
    total_wins = sum(t["won"]    for t in teams)
    total_draws= sum(t["drawn"]  for t in teams)
    assert total_pts == total_wins * 3 + total_draws
