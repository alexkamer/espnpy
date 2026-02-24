# The `LeagueProxy` Architecture

ESPN's undocumented API requires you to specify both the **Sport** (e.g., `football`) and the **League** (e.g., `nfl`) for every request. `espnpy` completely abstracts this away. 

It automatically maps over 384+ leagues to their respective sports.

### Perfect IDE Autocomplete
Every single one of the 384+ leagues is explicitly exposed in the root package module. This means you don't need to read documentation or memorize ESPN IDs to find the league you want.

When using VSCode, PyCharm, or any modern IDE, simply type `espnpy.` and a dropdown menu will instantly appear with every supported league.

```python
import espnpy
import asyncio

async def test_leagues():
    # Popular American Leagues
    nba_teams = await espnpy.nba.teams()
    nfl_scores = await espnpy.nfl.scoreboard()

    # English Premier League Soccer (ESPN ID: eng.1)
    # The dot in the ESPN ID is automatically converted to an underscore.
    epl_news = await espnpy.eng_1.news()

    # College Softball (ESPN ID: college-softball)
    # The hyphen in the ESPN ID is automatically converted to an underscore.
    softball_roster = await espnpy.college_softball.roster("12")

    # Obscure International Leagues
    mexico = await espnpy.mexican_winter_league.standings()

asyncio.run(test_leagues())
```
