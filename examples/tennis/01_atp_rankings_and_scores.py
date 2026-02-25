import asyncio
import json
import espnpy

async def get_tennis():
    print("Fetching ATP Rankings (espnpy.atp)...")
    # For Tennis, espnpy natively translates standings() into ESPN's Rankings!
    rankings = await espnpy.atp.standings()
    
    print(f"Total Ranked Players: {len(rankings)}")
    
    # Get the top 3 ranked players
    print("
[Current ATP Top 3]")
    for idx, player in enumerate(rankings[:3], 1):
        print(f"{idx}. {player['name']} ({player['points']} Pts)")
        
    print("
Fetching ATP Match Scoreboard...")
    # Passing a specific date during a major tournament (e.g. Dubai Duty Free)
    matches = await espnpy.atp.scoreboard(date="20240224")
    
    print(f"Total Matches Found: {len(matches)}")
    
    if matches:
        match = matches[0]
        # In Tennis, espnpy adds the overarching tournament name to the match dict
        print(f"
[Tournament]: {match['tournamentName']}")
        print(f"{match['homeTeam']} vs {match['awayTeam']}")
        print(f"Status: {match['status']}")
        
        # In Tennis, espnpy natively parses Set-by-Set scores!
        if match.get('homeScore'):
            print(f"Sets Won: {match['homeScore']} - {match['awayScore']}")
            print(f"Linescores (Sets): {match['setScores']}")

if __name__ == "__main__":
    asyncio.run(get_tennis())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching ATP Rankings (espnpy.atp)...
Total Ranked Players: 150

[Current ATP Top 3]
1. Carlos Alcaraz (13550.0 Pts)
2. Novak Djokovic (8890.0 Pts)
3. Jannik Sinner (8310.0 Pts)

Fetching ATP Match Scoreboard...
Total Matches Found: 282

[Tournament]: Dubai Duty Free Tennis Championships
Elisabetta Cocciaretto vs Zeynep Sonmez
Status: Final
Sets Won: 2 - 0
Linescores (Sets): 6-3, 6-0
"""