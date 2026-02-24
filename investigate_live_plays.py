import asyncio
import httpx
import json

async def m():
    async with httpx.AsyncClient() as c:
        # Check if the fast live data endpoint (cdn) has play-by-play
        r = await c.get("https://cdn.espn.com/core/nfl/playbyplay?xhr=1&gameId=401547403")
        data = r.json()
        
        plays = data.get("gamepackageJSON", {}).get("plays", [])
        print(f"Total Live Plays: {len(plays)}")
        if plays:
            print("First Play Text:", plays[0].get("text"))

asyncio.run(m())
