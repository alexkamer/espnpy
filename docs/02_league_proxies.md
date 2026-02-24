# The `LeagueProxy` Architecture

ESPN's API requires you to specify both the **Sport** (e.g., `football`) and the **League** (e.g., `nfl`) for every request. `espnpy` abstracts this away by automatically mapping 384+ leagues to their respective sports.

### Explicit Shortcuts
The most common American sports leagues are defined explicitly so they instantly appear in your IDE's Autocomplete (VSCode, PyCharm).
- `espnpy.nfl`
- `espnpy.nba`
- `espnpy.mlb`
- `espnpy.nhl`
- `espnpy.wnba`
- `espnpy.college_football`
- `espnpy.mens_college_basketball`

### Dynamic Proxies (The "Hidden Magic")
If a league isn't explicitly defined above, you can still access it dynamically via Python dot-notation. The package will automatically convert underscores (`_`) into the hyphens (`-`) or dots (`.`) that ESPN requires.

**Examples:**
```python
import espnpy
import asyncio

async def test_leagues():
    # English Premier League Soccer (ESPN ID: eng.1)
    # The underscore is automatically converted to a dot.
    epl = await espnpy.eng_1.teams()

    # College Softball (ESPN ID: college-softball)
    # The underscore is automatically converted to a hyphen.
    softball = await espnpy.college_softball.news()

    # Mexican Winter League Baseball
    mexico = await espnpy.mexican_winter_league.standings()

asyncio.run(test_leagues())
```
