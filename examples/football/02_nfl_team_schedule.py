import asyncio
import json
import espnpy

async def get_historical_schedule():
    # 1. Use fuzzy search to find the Patriots without knowing their ID!
    print("Fuzzy Searching for 'Patriots'...")
    patriots = await espnpy.nfl.find_team("Patriots")
    
    if not patriots:
        return
        
    print(f"Found: {patriots['displayName']} (ID: {patriots['id']})")
    
    # 2. Fetch their schedule for the historic 2007 season!
    # (Omit the season parameter to just get their current/upcoming schedule)
    print("\nFetching 2007 Schedule for the New England Patriots...")
    schedule = await espnpy.nfl.schedule(team_id=patriots['id'], season="2007")
    
    # 3. Print the first 3 regular season games
    print("\n[2007 Regular Season - First 3 Games]")
    for game in schedule[:3]:
        # The schedule output is 100% identical to the scoreboard dictionary!
        print(f"Matchup: {game['awayTeam']} @ {game['homeTeam']}")
        print(f"Result: {game['awayScore']} - {game['homeScore']} ({game['status']})\n")
        
    # 4. Did they win the Super Bowl that year? Let's check the last game of the season!
    super_bowl = schedule[-1]
    print(f"[Final Game of 2007 Season]")
    print(f"Matchup: {super_bowl['name']}")
    print(f"Result: {super_bowl['awayScore']} - {super_bowl['homeScore']} ({super_bowl['status']})")

if __name__ == "__main__":
    asyncio.run(get_historical_schedule())
