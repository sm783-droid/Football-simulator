"""test_simulation.py — pure algorithm tests (no DB)"""
from collections import Counter
import simulation


def test_random_names_returns_correct_count():
    assert len(simulation.random_names(10)) == 10


def test_random_names_are_unique():
    names = simulation.random_names(10)
    assert len(set(names)) == 10


def test_random_names_various_sizes():
    for n in (1, 5, 10):
        names = simulation.random_names(n)
        assert len(names) == n
        assert len(set(names)) == n


def test_make_fixtures_total_count():
    ids = list(range(1, 11))          # 10 teams
    assert len(simulation.make_fixtures(ids)) == 90


def test_make_fixtures_home_away_balance():
    ids = list(range(1, 11))
    fixtures = simulation.make_fixtures(ids)
    home_counts = Counter(h for _, h, _ in fixtures)
    away_counts = Counter(a for _, _, a in fixtures)
    for tid in ids:
        assert home_counts[tid] == 9, f"team {tid} home={home_counts[tid]}"
        assert away_counts[tid] == 9, f"team {tid} away={away_counts[tid]}"


def test_make_fixtures_five_per_week():
    ids = list(range(1, 11))
    by_week = Counter(w for w, _, _ in simulation.make_fixtures(ids))
    assert set(by_week.keys()) == set(range(1, 19)), "expected weeks 1-18"
    assert all(v == 5 for v in by_week.values()), f"uneven weeks: {by_week}"


def test_make_fixtures_no_team_plays_itself():
    ids = list(range(1, 11))
    for _, h, a in simulation.make_fixtures(ids):
        assert h != a


def test_make_fixtures_home_away_pairs_appear_once_each():
    """Each ordered pair (home, away) should appear exactly once."""
    ids = list(range(1, 11))
    pairs = [(h, a) for _, h, a in simulation.make_fixtures(ids)]
    pair_counts = Counter(pairs)
    assert all(v == 1 for v in pair_counts.values())


def test_random_score_types_and_range():
    for _ in range(200):
        h, a = simulation.random_score()
        assert isinstance(h, int) and isinstance(a, int)
        assert 0 <= h <= 5 and 0 <= a <= 5
