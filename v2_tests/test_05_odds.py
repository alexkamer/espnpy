import asyncio
import json
import espnpy

async def main():
    print("Testing the standalone advanced odds endpoint...")
    
    # Test NBA game odds (Bucks vs Knicks from your initial endpoint link)
    print("\n--- NBA ODDS: MIL vs NYK (Event 401584703) ---")
    nba_odds = await espnpy.nba.odds("401584703")
    
    print("Total Providers Found: " + str(len(nba_odds)))
    print("\nDraftKings Specific Odds:")
    draftkings_nba = next((o for o in nba_odds if o['provider'] == "DraftKings"), None)
    print(json.dumps(draftkings_nba, indent=2))
    
    # Test NFL game odds to verify cross-sport parsing
    print("\n==================================================\n")
    print("--- NFL ODDS: CAR vs ATL (Event 401547403) ---")
    nfl_odds = await espnpy.nfl.odds("401547403")
    
    print("Total Providers Found: " + str(len(nfl_odds)))
    print("\nCaesars Sportsbook Specific Odds:")
    caesars_nfl = next((o for o in nfl_odds if o['provider'] == "Caesars Sportsbook"), None)
    print(json.dumps(caesars_nfl, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
