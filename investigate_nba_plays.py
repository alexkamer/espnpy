import asyncio
import httpx
import json

async def m():
    async with httpx.AsyncClient() as c:
        # Let's check an NBA game ID (e.g. 401584689 - Golden State vs Denver from Christmas 2023)
        r = await c.get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401584689")
        data = r.json()
        
        plays = data.get("plays", [])
        print(f"Total NBA Plays: {len(plays)}")
        if plays:
            print("First NBA Play Text:", plays[0].get("text"))

asyncio.run(m())
