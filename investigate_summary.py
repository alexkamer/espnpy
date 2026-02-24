import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # Check an NFL game to see if odds populate there (NFL Week 1: Panthers at Falcons 2023)
        data = await client.nfl.game_summary("401547403")
        print("Odds:", json.dumps(data.get("odds"), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
