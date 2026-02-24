import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # Check if the 2020 Bucs roster actually contains Tom Brady
        print("--- 2020 NFL: TAMPA BAY BUCCANEERS ---")
        bucs_2020_roster = await client.nfl.roster("27", season="2020")
        print(f"Total Players: {len(bucs_2020_roster)}")
        
        brady = next((p for p in bucs_2020_roster if p.get("lastName") == "Brady"), None)
        if brady:
            print("Found Tom Brady!")
        else:
            print("Tom Brady NOT FOUND. This is likely the current roster, not historical.")
            
        print("\nChecking for current players on the 2020 roster request...")
        # Check for Baker Mayfield (who joined the Bucs in 2023, so he should NOT be on a true 2020 roster)
        baker = next((p for p in bucs_2020_roster if p.get("lastName") == "Mayfield"), None)
        if baker:
            print("Found Baker Mayfield! ESPN is ignoring the 'season' parameter and returning the current roster.")
        else:
            print("Baker Mayfield NOT FOUND.")
        
        print("\nLet's check the URL that was actually called:")
        try:
            d = await client._get("/sports/football/leagues/nfl/seasons/2020/teams/27/athletes")
            print("The 2020 URL succeeded. Checking its season reference...")
            # Look at a ref URL in the response
            ref = d.get("items", [])[0].get("$ref")
            print("Sample Athlete Ref:", ref)
            if "2020" not in ref:
                print("WARNING: ESPN returned a non-2020 athlete reference!")
        except Exception as e:
            print("Failed:", e)

if __name__ == "__main__":
    asyncio.run(main())
