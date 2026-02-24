import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        # A recent NFL Sunday
        data = await client.nfl.scoreboard(date="20230910")
        
        events = data.get("events", [])
        for e in events[:1]:
            # Dig out the core info
            id = e.get("id")
            name = e.get("name")
            date = e.get("date")
            
            c = e.get("competitions", [])[0]
            
            # The status description ("Final", "Scheduled", "3rd Quarter")
            status = c.get("status", {}).get("type", {}).get("description")
            
            # Venue
            venue = c.get("venue", {}).get("fullName")
            
            # TV Networks
            broadcasts = [b.get("names", [])[0] for b in c.get("broadcasts", []) if b.get("names")]
            
            # Score logic
            home_team = None
            home_score = None
            away_team = None
            away_score = None
            
            for comp in c.get("competitors", []):
                t_name = comp.get("team", {}).get("displayName")
                score = comp.get("score")
                if comp.get("homeAway") == "home":
                    home_team = t_name
                    home_score = score
                else:
                    away_team = t_name
                    away_score = score
            
            print(f"[{id}] {date}")
            print(f"Matchup: {away_team} ({away_score}) at {home_team} ({home_score})")
            print(f"Status: {status} | TV: {', '.join(broadcasts)} | Venue: {venue}")

if __name__ == "__main__":
    asyncio.run(main())
