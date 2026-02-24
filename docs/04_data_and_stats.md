# Data & Advanced Statistics

These endpoints pull mathematically intensive, advanced data like standings and player splits.

## 1. League Standings
Returns an ordered list (descending by Win Percentage) of every team in the league. It intelligently extracts and flattens ESPN's 10-layer-deep nested statistics into a clean dictionary.

```python
import espnpy
import asyncio

async def test_standings():
    nba = await espnpy.nba.standings()
    
    # The #1 overall team will always be at index 0 because of our built-in sorting algorithm
    best_team = nba[0]
    
    print(f"{best_team['team']} ({best_team['wins']}-{best_team['losses']})")
    print(f"Division Record: {best_team['divisionRecord']}")
    print(f"Point Differential: {best_team['differential']}")

asyncio.run(test_standings())
```

### Expected Output Structure:
```json
{
  "teamId": "25",
  "team": "Oklahoma City Thunder",
  "teamAbbreviation": "OKC",
  "logo": "https://a.espncdn.com/i/teamlogos/nba/500/okc.png",
  "group": "Western Conference",
  "wins": "44",
  "losses": "14",
  "ties": "0",
  "winPercent": ".759",
  "gamesBehind": "-",
  "streak": "W2",
  "pointsFor": "6929",
  "pointsAgainst": "6249",
  "differential": "+11.8",
  "homeRecord": "24-6",
  "awayRecord": "20-7",
  "divisionRecord": "8-3",
  "conferenceRecord": "29-11",
  "lastTenRecord": "8-2",
  "playoffSeed": "1"
}
```

## 2. Advanced Athlete Statistics (Splits)
Returns a dictionary grouping a player's career or season stats by "Splits" (e.g., How they play at Home vs Away, or when they Win vs Lose). The keys inside each split map directly to standard sports acronyms (e.g., `PTS` for Points, `YDS` for Yards).

```python
# '3139477' is Patrick Mahomes
mahomes_stats = await espnpy.nfl.athlete_stats("3139477")

wins = mahomes_stats.get("Wins/Ties", {})
print(f"Touchdowns in Wins: {wins.get('TD')}")
print(f"Passer Rating in Wins: {wins.get('RTG')}")

losses = mahomes_stats.get("Losses", {})
print(f"Touchdowns in Losses: {losses.get('TD')}")
print(f"Passer Rating in Losses: {losses.get('RTG')}")
```

### Expected Output Structure:
```json
{
  "All Splits": {
    "CMP": "315",
    "ATT": "502",
    "YDS": "3,587",
    "CMP%": "62.7",
    "AVG": "7.1",
    "TD": "5",
    "INT": "11",
    "LNG": "48",
    "SACK": "34",
    "RTG": "89.6",
    "CAR": "64"
  },
  "Home": {
    "CMP": "173",
    "ATT": "272",
    "YDS": "2,000",
    "CMP%": "63.6",
    "AVG": "7.4",
    ...
  },
  ...
}
```
