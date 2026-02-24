# espnpy 🏀🏈⚾️🏒

[![PyPI version](https://badge.fury.io/py/espnpy.svg)](https://badge.fury.io/py/espnpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`espnpy` is a high-performance, fully asynchronous Python wrapper for ESPN's undocumented internal APIs. It completely abstracts away ESPN's complex, deeply-nested JSON and aggressive pagination, providing developers with clean, flattened dictionaries.

Built on `httpx` with `HTTP/2` and `asyncio.Semaphore` connection pooling, `espnpy` effortlessly handles fetching thousands of URLs concurrently without triggering timeouts or aggressive rate-limits.

## Features (v2.0.0)
- **Massive League Support:** Auto-discovers and supports 384+ leagues (NFL, NBA, MLB, NHL, College Sports, Soccer, and obscure international leagues).
- **Perfect IDE Autocomplete:** 384 explicit properties for instant querying (e.g. `espnpy.nba.teams()`).
- **Entity Resolution:** Fetches Lists of Sports, Leagues, Teams, and Athletes.
- **Rosters:** Fetches the current active roster for a specific team.
- **Advanced Stats:** Fetch full league `standings` or a specific player's `athlete_stats` (Home vs Away, Wins vs Losses).
- **Live Action:** Fetch daily `scoreboards` (schedules, live scores, and TV networks).
- **Game Summaries:** Fetch detailed `game_summary` including Boxscores, Play-by-Play logs, and Betting Odds.
- **News:** Fetch the latest headlines and articles for a league or filtered to a specific team.

## Installation

```bash
pip install espnpy
```

## Quickstart

Because `espnpy` is heavily optimized with connection pooling, it must be run asynchronously.

```python
import asyncio
import json
from espnpy import ESPNClient

async def main():
    # Use the client as an async context manager for automatic session cleanup
    async with ESPNClient() as client:
        
        # 1. Fetch the NFL Scoreboard for Week 1 (Sept 10, 2023)
        scoreboard = await client.nfl.scoreboard(date="20230910")
        for game in scoreboard[:2]:
            print(f"{game['awayTeam']} at {game['homeTeam']} ({game['status']})")
        
        # 2. Get the detailed Boxscore and Play-by-Play for a specific game
        summary = await client.nfl.game_summary(scoreboard[0]['id'])
        print(f"Betting Spread: {summary['odds'].get('spread')}")
        
        # 3. Fetch the current active roster for the Atlanta Hawks (Team ID 1)
        hawks_roster = await client.nba.roster(team_id="1")
        print(f"Hawks Roster Size: {len(hawks_roster)}")
        
        # 4. Fetch details for a specific athlete (Stephen Curry, ID: 3975)
        steph = await client.nba.athlete("3975")
        print(f"{steph['fullName']} plays for Team ID: {steph['teamId']}")
        
        # 5. Fetch the latest news for the English Premier League
        epl_news = await client.eng_1.news(limit=3)
        for article in epl_news:
            print(f"Headline: {article['headline']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## The `LeagueProxy` Magic
You don't need to know whether the NBA belongs to the "basketball" sport category on ESPN's backend. `espnpy` handles the translation automatically.

**Perfect IDE Autocomplete:**
Every single one of the 384+ leagues is explicitly exposed in the root package module. This means you don't need to read documentation or memorize ESPN IDs to find the league you want.

When using VSCode, PyCharm, or any modern IDE, simply type `espnpy.` and a dropdown menu will instantly appear with every supported league.

```python
# ESPN League: 'eng.1' (English Premier League)
# The dot in the ESPN ID is automatically converted to an underscore.
espnpy.eng_1.teams()

# ESPN League: 'college-softball'
# The hyphen in the ESPN ID is automatically converted to an underscore.
espnpy.college_softball.news()
```

## Available Methods
Once you have accessed a league via the proxy (e.g. `espnpy.nba`), you have access to the following standardized methods:

- `await espnpy.nba.teams()`: All teams in the league.
- `await espnpy.nba.roster(team_id)`: The active roster for a specific team.
- `await espnpy.nba.athletes(active=True)`: All athletes in the league.
- `await espnpy.nba.athlete(athlete_id)`: A specific athlete's details.
- `await espnpy.nba.athlete_stats(athlete_id)`: Advanced statistical splits (e.g., Home vs Away records).
- `await espnpy.nba.standings()`: The full league standings, ordered by win percentage.
- `await espnpy.nba.scoreboard(date="YYYYMMDD")`: The schedule/scores for a day (or current week if omitted).
- `await espnpy.nba.game_summary(event_id)`: Boxscore, play-by-play, and betting odds for a specific game.
- `await espnpy.nba.news(team_id=None, limit=50)`: The latest news headlines.

*(If you require the raw, unparsed JSON from ESPN for advanced data extraction, you can pass `raw=True` to methods like `scoreboard()`.)*
