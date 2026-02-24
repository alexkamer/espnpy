import asyncio
import json
from espnpy import ESPNClient

async def main():
    async with ESPNClient() as client:
        print("===== ESPNPY V2.0.0 FEATURE TESTER =====\n")
        
        # 1. Standings
        print("1. STANDINGS (NBA)")
        nba_standings = await client.nba.standings()
        print(f"Top Team: {nba_standings[0]['team']} ({nba_standings[0]['wins']}-{nba_standings[0]['losses']})")
        print(f"Division Record: {nba_standings[0]['divisionRecord']}")
        print(f"Differential: {nba_standings[0]['differential']}\n")
        
        # 2. Advanced Athlete Stats
        print("2. ATHLETE STATS (Patrick Mahomes, ID: 3139477)")
        mahomes = await client.nfl.athlete_stats("3139477")
        wins = mahomes.get("Wins/Ties", {})
        losses = mahomes.get("Losses", {})
        print(f"Passer Rating in Wins: {wins.get('RTG')}")
        print(f"Passer Rating in Losses: {losses.get('RTG')}\n")
        
        # 3. Scoreboard
        print("3. SCOREBOARD (NFL Week 1, 2023)")
        scoreboard = await client.nfl.scoreboard(date="20230910")
        game = scoreboard[0]
        print(f"Matchup: {game['awayTeam']} at {game['homeTeam']}")
        print(f"Score: {game['awayScore']} - {game['homeScore']}")
        print(f"Status: {game['status']} | TV: {', '.join(game['broadcasts'])}\n")
        
        # 4. Game Summary
        print(f"4. GAME SUMMARY (Game ID: {game['id']})")
        summary = await client.nfl.game_summary(game['id'])
        print(f"Odds Spread: {summary['odds'].get('spread')}")
        print(f"Over/Under: {summary['odds'].get('overUnder')}")
        print("Final 2 Plays:")
        for play in summary['plays'][-2:]:
            print(f"  Q{play['period']} | {play['clock']} | {play['text']}\n")
            
        # 5. Roster
        print("5. ROSTER (Atlanta Hawks, ID: 1)")
        hawks = await client.nba.roster("1")
        print(f"Total Players: {len(hawks)}")
        print(f"Sample: {hawks[0]['fullName']} (#{hawks[0]['jersey']} {hawks[0]['positionAbbreviation']})\n")
        
        # 6. News
        print("6. NEWS (MLB)")
        news = await client.mlb.news(limit=2)
        for article in news:
            print(f"- {article['headline']}")

if __name__ == "__main__":
    asyncio.run(main())
