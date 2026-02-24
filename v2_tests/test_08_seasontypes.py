import asyncio
import espnpy

async def main():
    # 1. Test fetching only playoff games without passing a date!
    # By passing seasontype="3", it returns the current active/upcoming playoff games for the entire league
    print("Fetching ALL current/upcoming NFL Playoff Games (SeasonType 3)...")
    playoff_games = await espnpy.nfl.scoreboard(season_type="3")
    print(f"Total Games Found: {len(playoff_games)}")
    if playoff_games:
        print(f"Sample Game: {playoff_games[0]['name']}")
        print(f"Season Slug: {playoff_games[0]['seasonSlug']} (Year: {playoff_games[0]['seasonYear']})")
        
    print("\n" + "="*50 + "\n")
    
    # 2. Check an NBA play-in tournament
    print("Fetching NBA Scoreboard for April 16, 2024...")
    playin_games = await espnpy.nba.scoreboard(date="20240416")
    if playin_games:
        game = playin_games[0]
        print(f"Sample Game: {game['name']}")
        print(f"Season Slug: {game['seasonSlug']}")

if __name__ == "__main__":
    asyncio.run(main())
