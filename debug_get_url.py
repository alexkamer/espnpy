import asyncio
from espnpy import ESPNClient
import httpx
async def m():
    async with ESPNClient() as c:
        d = await c.get_url("http://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/teams/1?lang=en")
        print("Works!")
asyncio.run(m())
