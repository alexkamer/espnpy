# Core Entities: Sports, Teams & Athletes

These endpoints pull static, highly detailed data regarding the structure of ESPN's sports database.

## 1. Discovering Sports & Leagues
While `espnpy` handles 384+ leagues automatically via dot-notation, you can still manually query ESPN to discover what sports and leagues exist on their backend using the core client methods.

```python
import espnpy
import asyncio

async def test_discovery():
    # 1. Fetch all root sports (e.g. "football", "basketball")
    # You must use the internal _default_client for non-league specific requests
    sports = await espnpy._default_client.get_sports()
    print(f"Total Sports Found: {sports['count']}")

    # 2. Fetch all leagues within a specific sport
    baseball_leagues = await espnpy._default_client.get_leagues("baseball")
    for league in baseball_leagues[:2]:
        print(f"{league['name']} (ID: {league['id']}, Slug: {league['slug']})")
        
    # 3. Fetch general information for a specific league directly from the proxy
    nfl_info = await espnpy.nfl.info()
    print(f"NFL Season: {nfl_info.get('season', {}).get('year')}")

asyncio.run(test_discovery())
```

### Expected Output Structure (For Leagues):
```json
[
  {
    "id": "10",
    "name": "Major League Baseball",
    "displayName": "Major League Baseball",
    "abbreviation": "MLB",
    "shortName": "MLB",
    "slug": "mlb",
    "logo": "https://a.espncdn.com/i/teamlogos/leagues/500/mlb.png"
  },
  ...
]
```

## 2. Get All Teams in a League
Returns a list of every team in a given league, automatically handling backend pagination for massive leagues.

```python
import espnpy
import asyncio

async def test_teams():
    # Fetch all 32 NFL Teams
    teams = await espnpy.nfl.teams()
    print(f"Total Teams: {len(teams)}")
    print(teams[0]["displayName"]) # "Atlanta Falcons"

asyncio.run(test_teams())
```

### Expected Output Structure:
```json
[
  {
    "id": "1",
    "slug": "atlanta-falcons",
    "location": "Atlanta",
    "name": "Falcons",
    "nickname": "Falcons",
    "abbreviation": "ATL",
    "displayName": "Atlanta Falcons",
    "shortDisplayName": "Falcons",
    "color": "a71930",
    "alternateColor": "000000",
    "isActive": true,
    "logo": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
    "standingSummary": "1st in NFC South"
  },
  ...
]
```

## 3. Get a Specific Team
If you just want a single team's details without downloading the entire league, pass their ID.

```python
falcons = await espnpy.nfl.team("1")

print(f"Name: {falcons['displayName']}")
print(f"Abbreviation: {falcons['abbreviation']}")
print(f"Colors: #{falcons['color']}, #{falcons['alternateColor']}")
print(f"Current Status: {falcons['standingSummary']}") # e.g. "1st in NFC South"
```

## 4. Get the Current Roster for a Team
Pass the ESPN Team ID. This exclusively returns the **current** active roster for that specific team. The output is a standardized list of dictionaries containing every player's detailed biographical information.

```python
import espnpy
import asyncio

async def test_roster():
    # '1' is the Atlanta Hawks in the NBA
    roster = await espnpy.nba.roster("1")
    
    print(f"Total Players on Roster: {len(roster)}")
    for player in roster[:3]:
        print(f"{player['fullName']} - #{player['jersey']} {player['positionAbbreviation']}")

asyncio.run(test_roster())
```

### Expected Output Structure (Per Player):
*(Note: This uses the exact same standardized dictionary schema as `athlete` and `athletes`!)*
```json
[
  {
    "id": "4278039",
    "teamId": "1",
    "slug": "nickeil-alexander-walker",
    "firstName": "Nickeil",
    "lastName": "Alexander-Walker",
    "fullName": "Nickeil Alexander-Walker",
    "displayName": "Nickeil Alexander-Walker",
    "shortName": "N. Alexander-Walker",
    "weight": 205.0,
    "displayWeight": "205 lbs",
    "height": 77.0,
    "displayHeight": "6' 5\"",
    "age": 27,
    "dateOfBirth": "1998-09-02T07:00Z",
    "jersey": "7",
    "position": "Guard",
    "positionAbbreviation": "G",
    "active": true,
    "headshot": "https://a.espncdn.com/i/headshots/nba/players/full/4278039.png"
  },
  ...
]
```

## 5. Get All Athletes in a League
This endpoint pulls every active player in the league. It safely downloads thousands of URLs simultaneously without crashing your internet connection.

```python
# If active=True (default None), it filters for only currently playing athletes.
# This prevents pulling 10,000+ historical players.
nhl_players = await espnpy.nhl.athletes(active=True)
print(f"Total Active NHL Players: {len(nhl_players)}")
```

## 6. Get a Specific Athlete
Pass the ESPN Athlete ID to retrieve their biographical details. `teamId` is dynamically inferred and appended.

```python
# '3975' is Stephen Curry
steph = await espnpy.nba.athlete("3975")
```

### Expected Output Structure:
```json
{
  "id": "3975",
  "teamId": "9",
  "slug": "stephen-curry",
  "firstName": "Stephen",
  "lastName": "Curry",
  "fullName": "Stephen Curry",
  "displayName": "Stephen Curry",
  "shortName": "S. Curry",
  "weight": 185.0,
  "displayWeight": "185 lbs",
  "height": 74.0,
  "displayHeight": "6' 2"",
  "age": 36,
  "dateOfBirth": "1988-03-14T08:00Z",
  "jersey": "30",
  "position": "Point Guard",
  "positionAbbreviation": "PG",
  "active": true,
  "headshot": "https://a.espncdn.com/i/headshots/nba/players/full/3975.png"
}
```
