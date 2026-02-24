import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # Fetch Mahomes to see how his team is referenced
        d = await client._get("/sports/football/leagues/nfl/athletes/3139477")
        print("Team reference:")
        print(json.dumps(d.get("team"), indent=2))
        
asyncio.run(main())
