import asyncio, json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as c:
        d = await c.get_url("http://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/athletes?limit=5")
        refs = [i["$ref"] for i in d["items"]]
        p = await c.get_url(refs[1])
        print(json.dumps(p.get("headshot", {}), indent=2))
        print(json.dumps(p.get("position", {}), indent=2))

asyncio.run(main())
