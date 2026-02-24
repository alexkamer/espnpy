import asyncio
from espnpy import ESPNClient
async def m():
    async with ESPNClient() as c:
        d = await c._get("/sports/hockey/leagues/nhl/athletes", params={"active": "true"})
        print(f"Total Active NHL Athletes Reported: {d.get('count')}")
asyncio.run(m())
