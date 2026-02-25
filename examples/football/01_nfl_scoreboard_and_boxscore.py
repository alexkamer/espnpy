import asyncio
import json
import espnpy

async def get_nfl_gameday():
    print("Fetching NFL Week 1 Scoreboard (2023)...")
    # Date must be in YYYYMMDD format
    scoreboard = await espnpy.nfl.scoreboard(date="20230910")
    
    first_game = scoreboard[0]
    print(f"
--- {first_game['name']} ({first_game['status']}) ---")
    print(f"Broadcast: {', '.join(first_game['broadcasts'])}")
    print(f"Score: {first_game['awayScore']} - {first_game['homeScore']}")
    
    print(f"
Fetching detailed Game Summary for Game ID: {first_game['id']}...")
    summary = await espnpy.nfl.game_summary(first_game['id'])
    
    print("
[Betting Odds]")
    print(json.dumps(summary['odds'], indent=2))
    
    print("
[Play-by-Play] (Final 2 Plays)")
    for play in summary['plays'][-2:]:
        print(f"Q{play['period']} | {play['clock']} | {play['text']}")
        
    print("
[Boxscore Leaders]")
    # The boxscore returns lists of 'teams' and 'players'
    panthers_qb = next((p for p in summary['boxscore']['players'] if p['position'] == "QB" and p['teamId'] == "29"), None)
    if panthers_qb:
        print(f"Panthers QB: {panthers_qb['name']}")
        print(f"Passing Stats: {json.dumps(panthers_qb['stats'].get('passing'), indent=2)}")

if __name__ == "__main__":
    asyncio.run(get_nfl_gameday())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching NFL Week 1 Scoreboard (2023)...

--- Carolina Panthers at Atlanta Falcons (Final) ---
Broadcast: FOX
Score: 10 - 24

Fetching detailed Game Summary for Game ID: 401547403...

[Betting Odds]
{
  "provider": "consensus",
  "details": "ATL -3.5",
  "overUnder": 40.5,
  "spread": -3.5
}

[Play-by-Play] (Final 2 Plays)
Q4 | 0:24 | Bryce Young pass complete short right to ...
Q4 | 0:00 | End of 4th Quarter

[Boxscore Leaders]
Panthers QB: Bryce Young
Passing Stats: {
  "YDS": "146",
  "TD": "1",
  "INT": "2"
}
"""