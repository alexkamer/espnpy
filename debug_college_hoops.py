import asyncio
from espnpy import ESPNClient
import httpx
async def m():
    async with ESPNClient() as c:
        d = await c.get_teams("mens-college-basketball")
        print(f"Total teams: {len(d)}")
asyncio.run(m())
