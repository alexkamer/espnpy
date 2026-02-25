import asyncio
import json
import espnpy

async def get_golf_leaderboard():
    # Fetching the historic 2024 Masters leaderboard using date="YYYYMMDD"
    # Omit the date parameter to fetch the live, currently ongoing PGA tournament!
    print("Fetching PGA Leaderboard (The 2024 Masters)...")
    leaderboard = await espnpy.pga.leaderboard(date="20240414")
    
    print(f"Total Golfers on Leaderboard: {len(leaderboard)}")
    
    for golfer in leaderboard[:3]:
        print(f"
[{golfer['rank']}] {golfer['name']}")
        print(f"Tournament: {golfer['tournamentName']} ({golfer['status']})")
        print(f"Score to Par: {golfer['scoreToPar']}")
        print(f"Total Strokes: {golfer['totalStrokes']}")
        print(f"Rounds: {golfer['rounds']}")

if __name__ == "__main__":
    asyncio.run(get_golf_leaderboard())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching PGA Leaderboard (The 2024 Masters)...
Total Golfers on Leaderboard: 89

[1] Scottie Scheffler
Tournament: Masters Tournament (Final)
Score to Par: -11
Total Strokes: 277
Rounds: ['66', '72', '71', '68']

[2] Ludvig Åberg
Tournament: Masters Tournament (Final)
Score to Par: -7
Total Strokes: 281
Rounds: ['73', '69', '70', '69']

[3] Tommy Fleetwood
Tournament: Masters Tournament (Final)
Score to Par: -4
Total Strokes: 284
Rounds: ['72', '71', '72', '69']
"""