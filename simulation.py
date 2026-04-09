"""simulation.py — pure algorithms (no DB calls)"""
import random

_CITIES   = ["Manchester","Liverpool","London","Birmingham","Leeds","Sheffield",
             "Bristol","Leicester","Nottingham","Newcastle","Portsmouth",
             "Brighton","Coventry","Derby","Ipswich","Sunderland","Burnley"]
_SUFFIXES = ["United","City","FC","Athletic","Wanderers","Rovers","Town",
             "Villa","Palace","Hotspur","Rangers","Albion","County","Forest"]

_MGR_FIRST = ["Alex","Chris","David","Gary","José","Jürgen","Marco","Pep",
               "Rafael","Roberto","Sean","Steve","Thomas","Tony","Walter"]
_MGR_LAST  = ["Anderson","Bennett","Clarke","Ferguson","Garcia","Hughes",
               "Klopp","Mourinho","Pearce","Rodgers","Silva","Smith","Taylor"]

def random_manager_name() -> str:
    return f"{random.choice(_MGR_FIRST)} {random.choice(_MGR_LAST)}"

def random_names(n=10):
    """Return n unique random team names."""
    names, attempts = set(), 0
    while len(names) < n and attempts < 500:
        names.add(f"{random.choice(_CITIES)} {random.choice(_SUFFIXES)}")
        attempts += 1
    return list(names)[:n]

def make_fixtures(team_ids):
    """
    Full home-and-away round-robin (Berger table).
    Returns [(game_week, home_id, away_id), ...]
    10 teams → 90 fixtures over 18 weeks, 5 per week.
    """
    teams = list(team_ids)
    if len(teams) % 2:
        teams.append(None)          # bye slot for odd counts
    n, half = len(teams), len(teams) // 2
    first_leg = []
    for rnd in range(n - 1):
        for i in range(half):
            h, a = teams[i], teams[n - 1 - i]
            if h and a:
                first_leg.append((rnd + 1, h, a))
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]   # rotate except first
    return_leg = [(w + (n - 1), a, h) for w, h, a in first_leg]
    return first_leg + return_leg

def random_score():
    """Weighted random score; home side has slight advantage."""
    home = random.choices(range(6), weights=[15, 30, 25, 15, 10, 5])[0]
    away = random.choices(range(6), weights=[20, 30, 25, 15,  7, 3])[0]
    return home, away
