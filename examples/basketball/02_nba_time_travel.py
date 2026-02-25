import asyncio
import json
import espnpy

async def get_historical_nba():
    # Example 1: Use fuzzy search to instantly find a team without knowing their ID
    print("Fuzzy Searching for 'Warriors'...")
    warriors = await espnpy.nba.find_team("Warriors")
    
    if not warriors:
        return
        
    print(f"Found: {warriors['displayName']} (ID: {warriors['id']})")
    
    # Example 2: Use the 'season' parameter to fetch the historic 2016 NBA Standings!
    print("\nFetching Historical 2016 NBA Standings...")
    standings_2016 = await espnpy.nba.standings(season="2016")
    
    # Find the 2016 Warriors in the historical standings
    warriors_2016 = next((t for t in standings_2016 if t['id'] == warriors['id']), None)
    
    if warriors_2016:
        print(f"\n[2016 {warriors_2016['name']} Record]")
        print(f"Wins-Losses: {warriors_2016['wins']}-{warriors_2016['losses']}")
        print(f"Home Record: {warriors_2016['homeRecord']}")
        print(f"Win Percentage: {warriors_2016['winPercent']}")

if __name__ == "__main__":
    asyncio.run(get_historical_nba())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fuzzy Searching for 'Warriors'...
Found: Golden State Warriors (ID: 9)

Fetching Historical 2016 NBA Standings...

[2016 Golden State Warriors Record]
Wins-Losses: 73-9
Home Record: 39-2
Win Percentage: .890
"""