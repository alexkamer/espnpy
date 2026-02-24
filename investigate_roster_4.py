import asyncio
import json
from espnpy import ESPNClient
import httpx

async def main():
    async with ESPNClient() as client:
        # Based on typical ESPN structure, what is the exact roster endpoint?
        # Try team/{id}/athletes 
        try:
            d = await client._get("/sports/basketball/leagues/nba/seasons/2026/teams/1/athletes")
            print(json.dumps(d, indent=2)[:1000] + "...\n")
        except httpx.HTTPStatusError as e:
            print("Failed 1:", e)
            
        try:
            d = await client._get("/sports/basketball/leagues/nba/teams/1/athletes")
            print(json.dumps(d, indent=2)[:1000] + "...\n")
        except httpx.HTTPStatusError as e:
            print("Failed 2:", e)
            
asyncio.run(main())
