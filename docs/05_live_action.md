# Live Action: Schedules & Games

These endpoints pull data that is often updating live during game days. They hit ESPN's presentation APIs, pulling pre-flattened JSON ready for display.

## 1. The Scoreboard (Daily Schedule & Live Scores)
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

    # For massive leagues like Men's College Basketball, ESPN only returns Top-25 matchups by default.
    # You can pass the optional `group` parameter to fetch EVERY game.
    # Group '50' = All NCAA Division 1 Basketball games.
    # Group '80' = All NCAA FBS Football games.
    div1_games = await espnpy.mens_college_basketball.scoreboard(date="20240224", group="50")
    print(f"Total Division 1 Games: {len(div1_games)}")
    
    # You can also filter by `season_type`! (1 = Preseason, 2 = Regular Season, 3 = Postseason)
    # If you omit the date but provide a season_type, it returns ALL upcoming games for that phase.
    playoffs = await espnpy.nfl.scoreboard(season_type="3")
    for game in playoffs:
        # The standardized dictionary also exposes the season year and slug for every game
        print(f"[{game['seasonYear']} {game['seasonSlug']}] {game['name']}")

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
    "seasonYear": 2023,
    "seasonType": 2,
    "seasonSlug": "regular-season",
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

## 2. A Specific Team's Schedule
If you don't want to query the entire league-wide scoreboard across 18 weeks just to find the games for a specific team, you can use `.schedule(team_id)`.

*(Note: The output dictionary schema is 100% identical to the `scoreboard()` output!)*

```python
# '1' is the Atlanta Falcons (NFL). We ask for their 2023 schedule.
# You can also pass season_type="1" to get their preseason schedule!
schedule = await espnpy.nfl.schedule("1", season="2023", season_type="2")

for game in schedule:
    print(f"[{game['date']}] {game['awayTeam']} at {game['homeTeam']}")
    print(f"Result: {game['awayScore']} - {game['homeScore']} ({game['status']})")
```

## 3. Game Summary (Boxscores, Play-by-Play, Odds)
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
         "gameId": "401547403",
         "id": "1",
         "name": "Atlanta Falcons",
         "abbreviation": "ATL",
         "logo": "https://a.espncdn.com/...",
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
         "position": "QB",
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

## 4. Advanced Odds (Multiple Sportsbooks)
While `game_summary` provides a single "consensus" betting line, you can fetch the opening, closing, and current betting lines from over a dozen individual sportsbooks (like DraftKings, FanDuel, and Caesars) directly using the `odds()` endpoint.

```python
import espnpy
import asyncio

async def test_odds():
    # Pass a Game ID
    nba_odds = await espnpy.nba.odds("401584703")
    
    # Let's find DraftKings specifically
    draftkings = next((o for o in nba_odds if o['provider'] == "DraftKings"), None)
    print(f"DraftKings Spread: {draftkings['spread']}")
    print(f"DraftKings Over/Under: {draftkings['overUnder']}")

asyncio.run(test_odds())
```

### Expected Output Structure:
```json
[
  {
    "provider": "DraftKings",
    "details": "MIL -6",
    "overUnder": 228.0,
    "spread": -6.0,
    "awayMoneyLine": 200,
    "homeMoneyLine": -245
  },
  {
    "provider": "Caesars Sportsbook",
    "details": "MIL -5.5",
    "overUnder": 229.5,
    "spread": -5.5,
    "awayMoneyLine": 195,
    "homeMoneyLine": -255
  }
]
```
