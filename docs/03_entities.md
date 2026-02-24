# Core Entities: Teams & Athletes

These endpoints pull static, highly detailed data regarding the structure of the league.

## 1. Get All Teams in a League
Returns a list of every team in a given league.

```python
import espnpy
teams = await espnpy.nfl.teams()
print(f"Total Teams: {len(teams)}")
print(teams[0]["displayName"]) # "Atlanta Falcons"
```

## 2. Get the Current Roster for a Team
Pass the ESPN Team ID. This exclusively returns the **current** active roster.

```python
# '1' is the Atlanta Hawks in the NBA
roster = await espnpy.nba.roster("1")
for player in roster:
    print(f"{player['fullName']} - #{player['jersey']} {player['positionAbbreviation']}")
```

## 3. Get All Athletes in a League
This endpoint pulls every active player in the league. It safely downloads thousands of URLs simultaneously without crashing your internet connection.

```python
# If active=True (default None), it filters for only currently playing athletes.
# This prevents pulling 10,000+ historical players.
nhl_players = await espnpy.nhl.athletes(active=True)
print(f"Total Active NHL Players: {len(nhl_players)}")
```

## 4. Get a Specific Athlete
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
