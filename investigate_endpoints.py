import asyncio
import httpx
import json

async def m():
    async with httpx.AsyncClient() as c:
        print("--- 1. sports.core.api.espn.com (The Data Backend) ---")
        # Used for raw relational data: Teams, Leagues, Athletes
        # Response: Paginated items with $ref links
        r1 = await c.get("https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events/401584689?lang=en&region=us")
        print(f"Status: {r1.status_code}")
        print("Keys:", list(r1.json().keys()))

        print("\n--- 2. site.api.espn.com (The Application API) ---")
        # Used for the website/app: Scoreboards, News, Game Summaries
        # Response: Pre-flattened, nested JSON ready for UI display
        r2 = await c.get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401584689")
        print(f"Status: {r2.status_code}")
        print("Keys:", list(r2.json().keys()))

        print("\n--- 3. cdn.espn.com (The Fast Live Data) ---")
        # Used for ultra-fast, cached updates during live games: Play-by-play, Boxscores
        # Response: Highly specific, lightweight JSON
        r3 = await c.get("https://cdn.espn.com/core/nba/boxscore?xhr=1&gameId=401584689")
        print(f"Status: {r3.status_code}")
        print("Keys:", list(r3.json().keys()))

asyncio.run(m())
