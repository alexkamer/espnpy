import asyncio
import espnpy

async def get_epl_info():
    print("Fetching English Premier League Teams (espnpy.eng_1)...")
    # In espnpy, soccer leagues use underscores instead of dots (eng.1 -> eng_1)
    teams = await espnpy.eng_1.teams()
    
    # Let's find Arsenal (Usually ID '359')
    arsenal = next((t for t in teams if t['name'] == "Arsenal"), None)
    
    if arsenal:
        print(f"
Found Team: {arsenal['displayName']} (ID: {arsenal['id']})")
        print(f"Colors: #{arsenal['color']}, #{arsenal['alternateColor']}")
        
        print(f"
Fetching Current Roster for {arsenal['displayName']}...")
        roster = await espnpy.eng_1.roster(arsenal['id'])
        print(f"Total Players: {len(roster)}")
        
        for player in roster[:3]: # Print first 3 players
            print(f"- {player['fullName']} (Position: {player['position']})")
            
    print("
Fetching Latest EPL News Headlines...")
    news = await espnpy.eng_1.news(limit=3)
    
    for idx, article in enumerate(news, 1):
        print(f"{idx}. {article['headline']}")
        print(f"   Link: {article['url']}")

if __name__ == "__main__":
    asyncio.run(get_epl_info())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching English Premier League Teams (espnpy.eng_1)...

Found Team: Arsenal (ID: 359)
Colors: #EF0107, #063672

Fetching Current Roster for Arsenal...
Total Players: 30
- Bukayo Saka (Position: Attacker)
- Martin Ødegaard (Position: Midfielder)
- Declan Rice (Position: Midfielder)

Fetching Latest EPL News Headlines...
1. Arteta says Arsenal must 'suffer' to win title
   Link: https://www.espn.com/soccer/story/...
2. Premier League title race: Arsenal, Man City, Liverpool predictions
   Link: https://www.espn.com/soccer/story/...
3. Saka injury update ahead of massive Champions League clash
   Link: https://www.espn.com/soccer/story/...
"""