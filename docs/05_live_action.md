# Live Action: Schedules & Games

These endpoints pull data that is often updating live during game days. They hit ESPN's presentation APIs, pulling pre-flattened JSON ready for display.

## 1. The Scoreboard (Schedule & Live Scores)
Returns a completely flattened, standardized list of every game played (or scheduled to be played) on a specific date. 

```python
import espnpy
import asyncio

async def test_scoreboard():
    # Date format must be "YYYYMMDD"
    # If no date is provided, it returns today's or the current week's schedule.
    games = await espnpy.nba.scoreboard(date="20231225")

    for game in games:
        print(f"{game['awayTeam']} at {game['homeTeam']}")
        print(f"Status: {game['status']} (Clock: {game['clock']})")
        print(f"Score: {game['awayScore']} - {game['homeScore']}")
        print(f"TV: {', '.join(game['broadcasts'])}")

asyncio.run(test_scoreboard())
```

*(Power-User Note: If you want ESPN's raw, unparsed, 10-layer-deep JSON dictionary for advanced data mining, pass `raw=True` to this method: `espnpy.nba.scoreboard(raw=True)`).*

### Expected Output Structure:
```json
[
  {
    "id": "401547403",
    "date": "2023-09-10T17:00Z",
    "name": "Carolina Panthers at Atlanta Falcons",
    "shortName": "CAR @ ATL",
    "status": "Final",
    "clock": "0:00",
    "period": 4,
    "venue": "Mercedes-Benz Stadium",
    "broadcasts": ["FOX"],
    "homeTeam": "Atlanta Falcons",
    "homeTeamId": "1",
    "homeScore": "24",
    "homeLogo": "https://a.espncdn.com/...",
    "awayTeam": "Carolina Panthers",
    "awayTeamId": "29",
    "awayScore": "10",
    "awayLogo": "https://a.espncdn.com/..."
  }
]
```

## 2. Game Summary (Boxscores, Play-by-Play, Odds)
Pass a specific Game ID (found via the `scoreboard` method) to get the final boxscore, the play-by-play log, and betting odds.

```python
summary = await espnpy.nfl.game_summary("401547403")

# 1. Betting Odds
print(f"Spread: {summary['odds'].get('spread')}")
print(f"Over/Under: {summary['odds'].get('overUnder')}")

# 2. Play-by-Play
for play in summary['plays'][-3:]: # Print the final 3 plays
    print(f"Q{play['period']} | {play['clock']} | {play['text']}")
    if play['scoringPlay']:
        print("^^^ THIS WAS A SCORING PLAY! ^^^")

# 3. Boxscore (Teams & Players)
for player in summary['boxscore']['players'][:2]:
    print(f"{player['name']}: {player['stats']}")
```

### Expected Output Structure:
```json
{
  "odds": {
    "provider": "consensus",
    "details": "ATL -3.5",
    "overUnder": 40.5,
    "spread": -3.5
  },
  "plays": [
    {
      "id": "401584689400",
      "text": "Cam Reddish makes free throw 2 of 2",
      "clock": "24.0",
      "period": 4,
      "scoringPlay": true,
      "scoreValue": 1
    }
  ],
  "boxscore": {
    "teams": [
       {
         "id": "1",
         "name": "Atlanta Falcons",
         "abbreviation": "ATL",
         "stats": {
           "1st Downs": "20",
           "Total Yards": "221"
         }
       }
    ],
    "players": [
       {
         "gameId": "401547403",
         "id": "4685720",
         "teamId": "29",
         "name": "Bryce Young",
         "shortName": null,
         "starter": false,
         "jersey": "9",
         "position": null,
         "headshot": "https://a.espncdn.com/...",
         "stats": {
            "passing": {
               "YDS": "146",
               "TD": "1"
            },
            "rushing": {
               "YDS": "17"
            }
         }
       }
    ]
  }
}
```
