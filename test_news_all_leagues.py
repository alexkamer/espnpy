import asyncio
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        print("--- NBA News ---")
        nba_news = await client.nba.news(limit=2)
        for article in nba_news:
            print("-", article["headline"])
            
        print("\n--- MLB News ---")
        mlb_news = await client.mlb.news(limit=2)
        for article in mlb_news:
            print("-", article["headline"])
            
        print("\n--- NHL News ---")
        nhl_news = await client.nhl.news(limit=2)
        for article in nhl_news:
            print("-", article["headline"])
            
        print("\n--- College Football News ---")
        cfb_news = await client.college_football.news(limit=2)
        for article in cfb_news:
            print("-", article["headline"])

if __name__ == "__main__":
    asyncio.run(main())
