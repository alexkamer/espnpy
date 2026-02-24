import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # Check general NFL News
        print("--- NFL News ---")
        data = await client._get(f"sports/football/nfl/news?limit=2", base_url=client.SITE_BASE_URL)
        articles = data.get("articles", [])
        if articles:
            print(list(articles[0].keys()))
            
        print("\n--- Team News (Falcons, ID=1) ---")
        data = await client._get(f"sports/football/nfl/news?team=1&limit=2", base_url=client.SITE_BASE_URL)
        team_articles = data.get("articles", [])
        if team_articles:
            print(json.dumps(team_articles[0].get("headline", ""), indent=2))
            print(json.dumps(team_articles[0].get("description", ""), indent=2))
            
if __name__ == "__main__":
    asyncio.run(main())
