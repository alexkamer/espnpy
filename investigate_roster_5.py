import asyncio
from espnpy import ESPNClient
import httpx

async def main():
    async with ESPNClient() as client:
        # Check if the team ID can just use the root year '2026' or if it needs to dynamically find the 'current' season
        try:
            # Does the root /leagues/nba endpoint give us the current season year?
            d = await client._get("/sports/basketball/leagues/nba")
            print("Current NBA Season Year:", d.get("season", {}).get("year"))
        except httpx.HTTPStatusError as e:
            print("Failed:", e)
            
asyncio.run(main())
