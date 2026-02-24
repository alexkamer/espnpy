import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # What was the sample URL you provided earlier? 
        # https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/teams/1?lang=en&region=us
        # Let's hit the team endpoint again to see if it returns a 'roster' $ref directly inside the team JSON.
        d = await client._get("/sports/basketball/leagues/nba/seasons/2026/teams/1")
        
        # Check all the links/refs it returns
        print("Finding roster link...")
        for k, v in d.items():
            if k == "roster":
                print("FOUND ROSTER REF:", v)
            if k == "links":
                for link in v:
                    if "roster" in link.get("rel", []):
                        print("FOUND ROSTER LINK:", link)
                        
asyncio.run(main())
