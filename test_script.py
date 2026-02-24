import asyncio
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        
        print("--- NBA Standings ---")
        nba = await client.nba.standings()
        
        east_leader = next((t for t in nba if t["group"] == "Eastern Conference"), None)
        west_leader = next((t for t in nba if t["group"] == "Western Conference"), None)
        
        if east_leader:
            print(f"East Leader: {east_leader['team']} ({east_leader['wins']}-{east_leader['losses']})")
        if west_leader:
            print(f"West Leader: {west_leader['team']} ({west_leader['wins']}-{west_leader['losses']})")
            
        print("\n--- MLB Standings (Spring Training) ---")
        mlb = await client.mlb.standings()
        
        grapefruit_leader = next((t for t in mlb if t["group"] == "Grapefruit League"), None)
        cactus_leader = next((t for t in mlb if t["group"] == "Cactus League"), None)
        
        if grapefruit_leader:
            print(f"Grapefruit Leader: {grapefruit_leader['team']} ({grapefruit_leader['wins']}-{grapefruit_leader['losses']})")
        if cactus_leader:
            print(f"Cactus Leader: {cactus_leader['team']} ({cactus_leader['wins']}-{cactus_leader['losses']})")

if __name__ == "__main__":
    asyncio.run(main())
