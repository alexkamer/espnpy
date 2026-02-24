import asyncio
import espnpy

async def main():
    print("Testing the new module-level global client!")
    
    # Notice we don't have to instantiate `async with ESPNClient() as client:` anymore!
    # We can just call `espnpy.nba` directly.
    print("\n1. Fetching NBA Standings...")
    nba = await espnpy.nba.standings()
    print("Top NBA Team: " + nba[0]['team'])
    
    print("\n2. Fetching MLB News...")
    mlb = await espnpy.mlb.news(limit=2)
    print("Top MLB Headline: " + mlb[0]['headline'])
    
    print("\n3. Testing dynamic fallback (English Premier League)...")
    epl = await espnpy.eng_1.standings()
    print("Top EPL Team: " + epl[0]['team'])

if __name__ == "__main__":
    asyncio.run(main())
