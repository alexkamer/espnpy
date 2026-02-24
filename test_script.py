import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        
        # Test 1: General NFL News
        print("Fetching Top 2 General NFL Headlines...")
        nfl_news = await client.nfl.news(limit=2)
        
        for article in nfl_news:
            print(f"- {article['headline']}")
            if article['premium']:
                print("  (This is an ESPN+ exclusive!)")
            print(f"  {article['url']}")
        
        print("\n" + "="*50 + "\n")
        
        # Test 2: Team Specific News (Atlanta Falcons, ID: 1)
        print("Fetching Top 2 News stories specifically about the Atlanta Falcons...")
        falcons_news = await client.nfl.news(team_id="1", limit=2)
        
        for article in falcons_news:
            print(f"- {article['headline']}")
            print(f"  {article['url']}")
            
        print("\n--- Example JSON of an Article ---")
        print(json.dumps(falcons_news[0], indent=2))

if __name__ == "__main__":
    asyncio.run(main())
