import asyncio
from espnpy import ESPNClient
import httpx
async def m():
    async with ESPNClient() as c:
        d = await c.wnba.athletes()
        print(f"Total WNBA Athletes dynamically: {len(d)}")
asyncio.run(m())
