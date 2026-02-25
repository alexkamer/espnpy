import asyncio
import json
import espnpy

async def get_nba_stats():
    print("Fetching NBA Standings...")
    nba_standings = await espnpy.nba.standings()
    
    # espnpy automatically sorts standings descending by win percentage
    best_team = nba_standings[0]
    print(f"
[Current League Leader]")
    print(f"Team: {best_team['team']}")
    print(f"Record: {best_team['wins']}-{best_team['losses']} ({best_team['winPercent']})")
    print(f"Conference Record: {best_team['conferenceRecord']}")
    print(f"Point Differential: {best_team['differential']}")

    print("
Fetching Advanced Splits for Stephen Curry (ID: 3975)...")
    steph = await espnpy.nba.athlete_stats("3975")
    
    # Advanced stats are grouped into 'Splits'
    wins = steph.get("Wins", {})
    losses = steph.get("Losses", {})
    
    print(f"
[Steph Curry: Wins vs Losses]")
    print(f"Points Per Game (In Wins):   {wins.get('PTS')}")
    print(f"Points Per Game (In Losses): {losses.get('PTS')}")
    print(f"3PT % (In Wins):   {wins.get('3P%')}")
    print(f"3PT % (In Losses): {losses.get('3P%')}")

if __name__ == "__main__":
    asyncio.run(get_nba_stats())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching NBA Standings...

[Current League Leader]
Team: Boston Celtics
Record: 64-18 (.780)
Conference Record: 41-11
Point Differential: +11.3

Fetching Advanced Splits for Stephen Curry (ID: 3975)...

[Steph Curry: Wins vs Losses]
Points Per Game (In Wins):   28.1
Points Per Game (In Losses): 23.4
3PT % (In Wins):   42.1
3PT % (In Losses): 38.5
"""