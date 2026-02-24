import asyncio
import json
import espnpy

async def main():
    # Let's test the specific NBA game you requested!
    game_id = "401704627"
    print("Fetching NBA Game Summary for " + game_id + "...\n")
    
    summary = await espnpy.nba.game_summary(game_id)
    boxscore = summary.get("boxscore", {})
    
    # 1. Print the TEAM stats
    print("--- TEAM BOXSCORES ---")
    for team in boxscore.get("teams", []):
        print("\n" + team['name'] + " (" + str(team.get('abbreviation', '')) + ")")
        
        stats = team["stats"]
        print("  Field Goals: " + str(stats.get('FG')) + " (" + str(stats.get('Field Goal %')) + "%)")
        print("  3-Pointers: " + str(stats.get('3PT')) + " (" + str(stats.get('Three Point %')) + "%)")
        print("  Rebounds: " + str(stats.get('Rebounds')) + " | Assists: " + str(stats.get('Assists')) + " | Turnovers: " + str(stats.get('Turnovers')))
        
    print("\n==================================================\n")
    
    # 2. Print a sample PLAYER stat
    print("--- PLAYER BOXSCORES ---")
    
    # Let's find Jalen Brunson (who played in this game)
    players = boxscore.get("players", [])
    brunson = next((p for p in players if "Brunson" in p["name"]), None)
    
    if brunson:
        print("Found: " + brunson['name'])
        print(json.dumps(brunson["stats"], indent=2))
        
    print("\n==================================================\n")
    
    # 3. Test how it handles the complex, multi-category NFL stats
    print("Fetching NFL Boxscore to test multi-category logic...")
    nfl_summary = await espnpy.nfl.game_summary("401547403") # Falcons vs Panthers
    nfl_box = nfl_summary.get("boxscore", {})
    
    # Let's find Bryce Young (who threw AND ran the ball)
    bryce = next((p for p in nfl_box.get("players", []) if "Bryce Young" in p["name"]), None)
    if bryce:
        print("Found: " + str(bryce['name']))
        print(json.dumps(bryce["stats"], indent=2))

if __name__ == "__main__":
    asyncio.run(main())
