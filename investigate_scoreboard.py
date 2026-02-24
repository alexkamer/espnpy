import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # Fetch an NFL scoreboard to see the depth of data (Week 1 Sunday 2023)
        data = await client.nfl.scoreboard(date="20230910")
        
        # Dump the keys of a single event to see what's available
        event = data.get("events", [])[0]
        print("--- Event Keys ---")
        print(list(event.keys()))
        
        # Dump the keys of a single competition to see odds/broadcasts
        comp = event.get("competitions", [])[0]
        print("\n--- Competition Keys ---")
        print(list(comp.keys()))
        print("\n--- Competitors (Teams) ---")
        print(list(comp.get("competitors", [])[0].keys()))

if __name__ == "__main__":
    asyncio.run(main())
