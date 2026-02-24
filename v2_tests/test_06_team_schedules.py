import asyncio
import json
import espnpy

async def main():
    print("Testing the final two Entity endpoints (Team & Schedule)...")
    
    # Test 1: Fetch a specific team directly without downloading all 32 teams
    print("\n--- 1. SINGLE TEAM LOOKUP ---")
    falcons = await espnpy.nfl.team("1")
    print("Name: " + falcons['displayName'])
    print("Abbreviation: " + falcons['abbreviation'])
    print("Colors: #" + str(falcons['color']) + ", #" + str(falcons['alternateColor']))
    print("Current Status: " + str(falcons['standingSummary']))
    
    print("\n==================================================\n")
    
    # Test 2: Fetch the schedule for a specific team (The Falcons in 2023)
    print("--- 2. TEAM SCHEDULE ---")
    print("Fetching 2023 Schedule for Atlanta Falcons (Team ID 1)...")
    schedule = await espnpy.nfl.schedule("1", season="2023")
    
    print("Total Games Scheduled: " + str(len(schedule)) + "\n")
    
    for game in schedule[:3]: # Let's just look at the first 3 weeks
        # Look familiar? It reuses the exact same dictionary structure as the scoreboard!
        print("[" + str(game['date']) + "] " + str(game['awayTeam']) + " at " + str(game['homeTeam']))
        print("Result: " + str(game['awayScore']) + " - " + str(game['homeScore']) + " (" + str(game['status']) + ")\n")

if __name__ == "__main__":
    asyncio.run(main())
