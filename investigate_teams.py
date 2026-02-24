import asyncio
import json
from espnpy import ESPNClient

async def fetch_team_sample(client, sport, league):
    print("--- Fetching team sample for " + sport + "/" + league + " ---")
    list_response = await client._get(f"/sports/{sport}/leagues/{league}/teams", params={"limit": 1})
    items = list_response.get("items", [])
    if not items:
        print("No teams found.")
        return
        
    ref_url = items[0].get("$ref")
    team_data = await client.get_url(ref_url)
    
    data = {}
    for k, v in team_data.items():
        if not isinstance(v, (dict, list)):
            data[k] = v
        elif k in ["logos", "links"]:
            data[k] = v
            
    print(json.dumps(data, indent=2))

async def main():
    async with ESPNClient() as client:
        await fetch_team_sample(client, "basketball", "nba")
        await fetch_team_sample(client, "football", "nfl")
        await fetch_team_sample(client, "soccer", "eng.1")

if __name__ == "__main__":
    asyncio.run(main())
