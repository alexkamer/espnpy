import asyncio
import json
from espnpy import ESPNClient

async def fetch_athlete_sample(client, sport, league):
    print(f"--- Fetching athlete sample for {sport}/{league} ---")
    list_response = await client._get(f"/sports/{sport}/leagues/{league}/athletes", params={"limit": 1})
    items = list_response.get("items", [])
    if not items:
        print("No athletes found.")
        return
        
    ref_url = items[0].get("$ref")
    athlete_data = await client.get_url(ref_url)
    
    data = {}
    for k, v in athlete_data.items():
        if not isinstance(v, (dict, list)):
            data[k] = v
        elif k in ["headshot", "position", "jersey"]:
            data[k] = v
            
    print(json.dumps(data, indent=2))

async def main():
    async with ESPNClient() as client:
        await fetch_athlete_sample(client, "basketball", "nba")

if __name__ == "__main__":
    asyncio.run(main())
