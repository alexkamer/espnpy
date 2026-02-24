import asyncio
from espnpy import ESPNClient
import httpx
async def m():
    async with ESPNClient() as c:
        try:
            d = await c._get("/sports/basketball/leagues/nba/athletes", params={"limit": 5})
            print(f"Total NBA Athletes Reported: {d.get('count')}")
        except httpx.HTTPStatusError as e:
            print(f"FAILED: {e}")
asyncio.run(m())
