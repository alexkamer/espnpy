import asyncio
from espnpy import ESPNClient
async def m():
    async with ESPNClient() as c:
        d = await c._get("/sports/hockey/leagues/nhl/athletes")
        print(f"Total NHL Athletes Reported: {d.get('count')}")
asyncio.run(m())
