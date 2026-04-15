"""store.py — in-memory data store (replaces db.py, db_games.py, db_managers.py)

All state lives in module-level dicts/lists. No file I/O, no SQLite.
Data is lost when the process exits; that's fine for a simulator.
"""

# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
_teams    = {}   # team_id (int) -> dict
_managers = {}   # team_id (int) -> dict
_games    = []   # list of game dicts
_next_tid = 1
_next_gid = 1


# ---------------------------------------------------------------------------
# Init / Reset
# ---------------------------------------------------------------------------
def init():
    """No-op — state is initialised at import time."""
    pass


def reset():
    global _teams, _managers, _games, _next_tid, _next_gid
    _teams, _managers, _games = {}, {}, []
    _next_tid, _next_gid = 1, 1


# ---------------------------------------------------------------------------
# Teams
# ---------------------------------------------------------------------------
def add_team(name):
    global _next_tid
    if any(t["name"] == name for t in _teams.values()):
        return  # ignore duplicates
    _teams[_next_tid] = dict(id=_next_tid, name=name, played=0, won=0, drawn=0,
                              lost=0, goals_for=0, goals_against=0, points=0)
    _next_tid += 1


def get_teams():
    return sorted(
        _teams.values(),
        key=lambda t: (-t["points"],
                       -(t["goals_for"] - t["goals_against"]),
                       -t["goals_for"],
                       t["name"]),
    )


def team_count():
    return len(_teams)


def team_ids():
    return sorted(_teams.keys())


# ---------------------------------------------------------------------------
# Managers
# ---------------------------------------------------------------------------
def add_manager(team_id, name):
    _managers[team_id] = dict(team_id=team_id, name=name,
                               wins=0, draws=0, losses=0, points=0)


def get_manager(team_id):
    return _managers.get(team_id)


def get_all_managers():
    rows = []
    for m in sorted(_managers.values(), key=lambda m: -m["points"]):
        team = _teams.get(m["team_id"], {})
        rows.append({**m,
                     "team_name":   team.get("name", ""),
                     "team_points": team.get("points", 0)})
    return rows


# ---------------------------------------------------------------------------
# Fixtures / Games
# ---------------------------------------------------------------------------
def has_fixtures():
    return len(_games) > 0


def add_fixture(week, home_id, away_id):
    global _next_gid
    _games.append(dict(id=_next_gid, game_week=week,
                       home_team_id=home_id, away_team_id=away_id,
                       home_score=None, away_score=None, played=0))
    _next_gid += 1


def get_week(week):
    result = []
    for g in sorted(_games, key=lambda g: g["id"]):
        if g["game_week"] == week:
            row = dict(g)
            row["home_team"] = _teams[g["home_team_id"]]["name"]
            row["away_team"] = _teams[g["away_team_id"]]["name"]
            result.append(row)
    return result


def max_week():
    return max((g["game_week"] for g in _games), default=0)


def current_week():
    unplayed = [g["game_week"] for g in _games if not g["played"]]
    return min(unplayed) if unplayed else max_week()


def save_score(game_id, hs, as_):
    game = next((g for g in _games if g["id"] == game_id), None)
    if game is None:
        return
    if game["played"]:
        _delta(game, -1) 
    game["home_score"] = hs
    game["away_score"] = as_
    game["played"] = 1
    _delta(game, +1, hs, as_)


# ---------------------------------------------------------------------------
# Internal stat helpers
# ---------------------------------------------------------------------------
def _delta(game, sign, hs=None, as_=None):
    """Add or subtract one game's contribution from both teams."""
    h, a = game["home_team_id"], game["away_team_id"]
    if hs is None:
        hs, as_ = game["home_score"], game["away_score"]

    for tid, gf, ga in [(h, hs, as_), (a, as_, hs)]:
        t = _teams[tid]
        t["played"]        += sign
        t["goals_for"]     += sign * gf
        t["goals_against"] += sign * ga

    if hs > as_:
        _teams[h]["won"]    += sign;  _teams[h]["points"] += sign * 3
        _teams[a]["lost"]   += sign
    elif hs < as_:
        _teams[a]["won"]    += sign;  _teams[a]["points"] += sign * 3
        _teams[h]["lost"]   += sign
    else:
        _teams[h]["drawn"]  += sign;  _teams[h]["points"] += sign
        _teams[a]["drawn"]  += sign;  _teams[a]["points"] += sign
