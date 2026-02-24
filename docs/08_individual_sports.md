# Individual Sports: Racing, Tennis, Golf & MMA

ESPN's internal databases were originally built for traditional team sports (like NFL and NBA). As a result, data for individual sports like Tennis (ATP/WTA), Racing (F1/NASCAR), Golf (PGA), and MMA (UFC) is structurally completely different behind the scenes.

`espnpy` automatically detects these individual sports and dynamically rewrites its API queries and parsers to ensure you still get the exact same standardized, flattened dictionaries you expect!

Here is how `espnpy` handles these sports and how you can query them.

---

## 1. Rankings (Replacing Standings)

In team sports, `.standings()` returns a list of teams sorted by Win Percentage. 
In individual sports, ESPN does not have "standings". They have **Rankings**.

`espnpy` intelligently intercepts calls to `.standings()` for Tennis, Golf, and MMA, routes them to ESPN's hidden `/rankings` endpoints, and perfectly standardizes the output.

```python
import espnpy
import asyncio

async def get_tennis_rankings():
    # 1. ATP Tennis Rankings
    atp_rankings = await espnpy.atp.standings()
    
    print(f"Total Ranked Players: {len(atp_rankings)}")
    
    # Carlos Alcaraz will be near the top!
    world_number_one = atp_rankings[0]
    print(f"Rank {world_number_one['rank']}: {world_number_one['name']} ({world_number_one['points']} Pts)")
    
    # 2. F1 Driver Standings
    # F1 technically uses standings, but ranks Drivers instead of Teams. 
    # espnpy automatically sorts them by Championship Points.
    f1 = await espnpy.f1.standings()
    print(f"F1 Leader: {f1[0]['name']}")

asyncio.run(get_tennis_rankings())
```

### Expected Output Structure:
```json
{
  "id": "3782",
  "name": "Carlos Alcaraz",
  "abbreviation": "C. Alcaraz",
  "logo": "https://a.espncdn.com/i/headshots/tennis/players/full/3782.png",
  "group": "ATP",
  "points": "13550.0",
  "rank": "1",
  "streak": "-",
  "wins": "0", 
  "losses": "0" 
}
```

---

## 2. The Scoreboard (Flattening Tournaments & Races)

In Tennis, the "Event" on ESPN's scoreboard isn't a match—it's an entire *Tournament* (like the US Open). The actual matches are buried three levels deep under obscure `groupings`. 

If you call `.scoreboard()` on a Tennis league, `espnpy` recursively unwraps the tournament groupings and instantly hands you back a clean, flattened list of every single 1v1 match happening that day!

```python
import espnpy
import asyncio

async def get_matches():
    # Fetch all ATP matches happening on a specific date during a tournament
    matches = await espnpy.atp.scoreboard(date="20240224")
    
    print(f"Total Matches Found: {len(matches)}")
    
    for match in matches[:3]:
        # 'tournamentName' holds the name of the overarching event!
        print(f"Tournament: {match['tournamentName']}")
        
        # 'homeTeam' and 'awayTeam' are automatically populated with the player names!
        print(f"{match['homeTeam']} vs {match['awayTeam']}")
        print(f"Status: {match['status']}")
        
        if match['homeScore']:
            print(f"Sets Won: {match['homeScore']} - {match['awayScore']}")
            print(f"Set-by-Set Linescores: {match['setScores']}") # e.g., "6-3, 6-4"

asyncio.run(get_matches())
```

### Racing Grids
For Racing (like Formula 1), `scoreboard()` will return the upcoming scheduled sessions (e.g., Free Practice 1, Qualifying, Race Day) rather than 1v1 matchups.

---

## 3. Supported vs. Unsupported Endpoints

Because ESPN's backend for Individual Sports is limited compared to massive leagues like the NFL, not every `espnpy` method is supported by ESPN.

| Method | Team Sports | Tennis / Golf / MMA | Racing |
| :--- | :--- | :--- | :--- |
| `.standings()` | ✅ Supported | ✅ Supported (Rankings) | ✅ Supported (Driver Pts)|
| `.scoreboard()` | ✅ Supported | ✅ Supported (Matches) | ✅ Supported (Sessions)|
| `.news()` | ✅ Supported | ✅ Supported | ✅ Supported |
| `.athlete(id)` | ✅ Supported | ✅ Supported | ✅ Supported |
| `.game_summary()` | ✅ Supported | ❌ *Unsupported (400)* | ❌ *Unsupported (400)* |
| `.athlete_stats()`| ✅ Supported | ❌ *Unsupported (404)* | ❌ *Unsupported (404)* |
| `.odds()` | ✅ Supported | ❌ *Unsupported (404)* | ❌ *Unsupported (404)* |

*If you attempt to call an unsupported endpoint for an individual sport, the underlying `httpx` client will automatically throw an `HTTPStatusError` (usually a `404 Not Found` or `400 Bad Request`). You should wrap these calls in `try/except` blocks if your app dynamically switches between sports!*