import asyncio
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        print("===== ESPNP V2.0.0 INDIVIDUAL SPORTS TESTER =====\n")
        
        # --- 1. TENNIS (ATP) ---
        print("--- 1. TENNIS (ATP) ---")
        
        # Test Rankings
        try:
            atp_rankings = await client.atp.standings()
            print(f"Top Ranked Player: {atp_rankings[0]['name']} (Points: {atp_rankings[0]['points']})")
        except Exception as e:
            print(f"ATP Rankings Failed: {e}")
            
        # Test Tournament Scoreboard
        try:
            atp_scoreboard = await client.atp.scoreboard(date="20240224") # Specific date during a tournament
            print(f"Total Matches Found: {len(atp_scoreboard)}")
            match = atp_scoreboard[0]
            print(f"Tournament: {match.get('tournamentName')}")
            print(f"Sample Match: {match['homeTeam']} vs {match['awayTeam']} ({match['status']})")
            print(f"Set Scores: {match.get('setScores', 'None')}")
        except Exception as e:
            print(f"ATP Scoreboard Failed: {e}")
            
            
        print("\n--- 2. RACING (F1) ---")
        
        # Test Standings
        try:
            f1_standings = await client.f1.standings()
            print(f"Top Ranked Driver: {f1_standings[0]['name']}")
            print(f"Second Ranked Driver: {f1_standings[1]['name']}")
        except Exception as e:
            print(f"F1 Standings Failed: {e}")
            
        # Test Race Scoreboard
        try:
            f1_scoreboard = await client.f1.scoreboard()
            print(f"Total Upcoming/Recent Sessions: {len(f1_scoreboard)}")
            race = f1_scoreboard[0]
            print(f"Sample Race: {race['name']} ({race['status']})")
        except Exception as e:
            print(f"F1 Scoreboard Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
