import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # Example NBA team: Atlanta Hawks (id=1). Omit the season, as you noted it only works for current.
        d = await client._get("/sports/basketball/leagues/nba/teams/1/roster")
        print(json.dumps(d, indent=2)[:1000] + "...\n")
asyncio.run(main())
