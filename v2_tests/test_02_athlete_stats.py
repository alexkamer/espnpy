import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        print("=========================================")
        print("   V2 FEATURE 2: ATHLETE STATS")
        print("=========================================\n")
        
        # 1. Test NFL Advanced Stats (Patrick Mahomes)
        print("Fetching Patrick Mahomes (ID: 3139477) Stats...\n")
        mahomes_stats = await client.nfl.athlete_stats("3139477")
        
        print("Keys available (These are the different 'Splits' you can analyze):")
        print(list(mahomes_stats.keys())[:10], "... (and more)")
        
        print("\nLet's look at his career performance specifically in WINS vs LOSSES:")
        
        print("\nWhen the Chiefs WIN:")
        # We know from inspecting the labels that CMP is Completions and YDS is Yards
        wins = mahomes_stats.get("Wins/Ties", {})
        print(f"  Completion Percentage: {wins.get('CMP%')}")
        print(f"  Total Passing Yards: {wins.get('YDS')}")
        print(f"  Touchdown Passes: {wins.get('TD')}")
        print(f"  Interceptions: {wins.get('INT')}")
        print(f"  Passer Rating: {wins.get('RTG')}")
        
        print("\nWhen the Chiefs LOSE:")
        losses = mahomes_stats.get("Losses", {})
        print(f"  Completion Percentage: {losses.get('CMP%')}")
        print(f"  Total Passing Yards: {losses.get('YDS')}")
        print(f"  Touchdown Passes: {losses.get('TD')}")
        print(f"  Interceptions: {losses.get('INT')}")
        print(f"  Passer Rating: {losses.get('RTG')}")
        
        print("\n=========================================\n")
        
        # 2. Test NBA Advanced Stats (LeBron James, ID: 1966)
        print("Fetching LeBron James (ID: 1966) Stats...\n")
        lebron_stats = await client.nba.athlete_stats("1966")
        
        print("Let's look at LeBron's career performance HOME vs AWAY:")
        
        home = lebron_stats.get("Home", {})
        print("\nAt HOME:")
        print(f"  Points: {home.get('PTS')}")
        print(f"  Assists: {home.get('AST')}")
        print(f"  Rebounds: {home.get('REB')}")
        print(f"  Blocks: {home.get('BLK')}")
        print(f"  Turnovers: {home.get('TO')}")
        
        away = lebron_stats.get("Road", {})
        print("\nOn the ROAD:")
        print(f"  Points: {away.get('PTS')}")
        print(f"  Assists: {away.get('AST')}")
        print(f"  Rebounds: {away.get('REB')}")
        print(f"  Blocks: {away.get('BLK')}")
        print(f"  Turnovers: {away.get('TO')}")
        
        print("\n=========================================\n")
        
        print("Want to see exactly what one of these dictionary objects looks like raw?")
        print("Here is Patrick Mahomes' complete 'All Splits' (Career Total) Dictionary:")
        print(json.dumps(mahomes_stats.get("All Splits", {}), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
