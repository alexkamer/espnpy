import asyncio
import json
import espnpy

async def get_epl_match_summary():
    # 1. Fetch the daily scoreboard
    print("Fetching English Premier League Scoreboard...")
    scoreboard = await espnpy.eng_1.scoreboard(date="20240224")
    
    first_game = scoreboard[0]
    print(f"
--- {first_game['name']} ({first_game['status']}) ---")
    print(f"Score: {first_game['homeTeam']} {first_game['homeScore']} - {first_game['awayScore']} {first_game['awayTeam']}")
    
    # 2. Fetch the detailed game summary
    print(f"
Fetching detailed Game Summary for Game ID: {first_game['id']}...")
    summary = await espnpy.eng_1.game_summary(first_game['id'])
    
    # 3. Analyze Soccer-specific properties (Formations, Cards)
    print("
[Tactical Formations]")
    for roster in summary['rosters']:
        print(f"Team: {roster['team']} | Formation: {roster['formation']}")
    
    print("
[Key Events (Goals, Cards, Subs)]")
    for event in summary['keyEvents'][:4]:
        print(f"{event['clock']} | {event['type']}: {event['shortText']}")

if __name__ == "__main__":
    asyncio.run(get_epl_match_summary())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching English Premier League Scoreboard...

--- Aston Villa vs Nottingham Forest (Final) ---
Score: Aston Villa 4 - 2 Nottingham Forest

Fetching detailed Game Summary for Game ID: 671289...

[Tactical Formations]
Team: Aston Villa | Formation: 4-2-3-1
Team: Nottingham Forest | Formation: 4-2-3-1

[Key Events (Goals, Cards, Subs)]
 | Kickoff: None
4' | Goal: Goal!  Aston Villa 1, Nottm Forest 0. O. Watkins (Aston Villa) ...
15' | Yellow Card: Murillo (Nottm Forest) is shown the yellow card ...
29' | Goal: Goal!  Aston Villa 2, Nottm Forest 0. Douglas Luiz (Aston Villa) ...
"""