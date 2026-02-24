import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        print("=========================================")
        print("   V2 FEATURE 1: LEAGUE STANDINGS")
        print("=========================================")
        
        # 1. Test NFL Standings (Small enough to print comfortably)
        print("\nFetching full NFL standings...")
        nfl_standings = await client.nfl.standings()
        
        print(f"Total NFL Teams returned: {len(nfl_standings)}")
        print("\nExact Dictionary Structure (COMPLETE LIST OF ALL 32 NFL TEAMS):\n")
        
        # Print the exact list of dictionaries for ALL teams
        print(json.dumps(nfl_standings, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
