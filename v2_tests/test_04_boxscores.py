import asyncio
import json
import espnpy

async def main():
    game_id = "401704627"
    print("Fetching NBA Game Summary for " + game_id + "...\n")
    
    summary = await espnpy.nba.game_summary(game_id)
    boxscore = summary.get("boxscore", {})
    
    # 2. Print a sample PLAYER stat
    print("--- PLAYER BOXSCORES ---")
    
    # Let's find Jalen Brunson
    players = boxscore.get("players", [])
    brunson = next((p for p in players if "Brunson" in p["name"]), None)
    
    if brunson:
        print("Found: " + brunson['name'])
        print(json.dumps(brunson, indent=2))
        
    print("\n==================================================\n")
    
    print("Fetching NFL Boxscore to test multi-category logic...")
    nfl_summary = await espnpy.nfl.game_summary("401547403") # Falcons vs Panthers
    nfl_box = nfl_summary.get("boxscore", {})
    
    bryce = next((p for p in nfl_box.get("players", []) if "Bryce Young" in p["name"]), None)
    if bryce:
        print("Found: " + str(bryce['name']))
        print(json.dumps(bryce, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
