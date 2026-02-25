import asyncio
import json
import espnpy

async def get_f1_grid():
    print("Fetching F1 Driver Standings (espnpy.f1)...")
    # For F1, espnpy correctly extracts the drivers instead of teams,
    # and automatically sorts them by Championship Points!
    driver_standings = await espnpy.f1.standings()
    
    print(f"Total Ranked Drivers: {len(driver_standings)}")
    
    print("
[Current Top 3 F1 Drivers]")
    for idx, driver in enumerate(driver_standings[:3], 1):
        print(f"{idx}. {driver['name']} ({driver['points']} Pts)")
        
    print("
Fetching F1 Weekend Scoreboard...")
    # F1 scoreboards return scheduled sessions (like FP1, Qualifying, Race Day)
    sessions = await espnpy.f1.scoreboard()
    
    print(f"Total Upcoming Sessions: {len(sessions)}")
    
    if sessions:
        race_day = next((s for s in sessions if "Grand Prix" in s['name']), sessions[0])
        print(f"
[Upcoming Event]: {race_day['name']}")
        print(f"Status: {race_day['status']}")
        print(f"Date: {race_day['date']}")
        print(f"TV Broadcast: {', '.join(race_day['broadcasts'])}")

if __name__ == "__main__":
    asyncio.run(get_f1_grid())

"""
===================================================
EXPECTED OUTPUT:
===================================================
Fetching F1 Driver Standings (espnpy.f1)...
Total Ranked Drivers: 22

[Current Top 3 F1 Drivers]
1. Max Verstappen (575.0 Pts)
2. Sergio Perez (285.0 Pts)
3. Lewis Hamilton (234.0 Pts)

Fetching F1 Weekend Scoreboard...
Total Upcoming Sessions: 5

[Upcoming Event]: Heineken Las Vegas Grand Prix
Status: Scheduled
Date: 2024-11-23T06:00Z
TV Broadcast: ESPN
"""