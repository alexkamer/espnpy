import asyncio
import json
from espnpy import ESPNClient

async def build_league_mapping():
    mapping = {}
    
    async with ESPNClient() as client:
        print("Fetching all sports...")
        # Get all sports
        sports_data = await client.get_sports(limit=100)
        sport_refs = [item.get("$ref") for item in sports_data.get("items", []) if "$ref" in item]
        
        # Follow all sport refs concurrently to get their slugs
        print("Fetching details for " + str(len(sport_refs)) + " sports...")
        sport_tasks = [client.get_url(ref) for ref in sport_refs]
        sports = await asyncio.gather(*sport_tasks)
        
        for sport in sports:
            sport_slug = sport.get("slug")
            if not sport_slug:
                continue
                
            print("Fetching leagues for " + sport_slug + "...")
            try:
                leagues = await client.get_leagues(sport_slug, limit=1000)
                for league in leagues:
                    league_slug = league.get("slug")
                    if league_slug:
                        mapping[league_slug] = sport_slug
            except Exception as e:
                print("  Error fetching leagues for " + sport_slug + ": " + str(e))
                
    return mapping

async def main():
    mapping = await build_league_mapping()
    
    print("\n--- GENERATED MAPPING ---")
    
    # Format the mapping as a beautiful Python dictionary
    output = "LEAGUE_TO_SPORT = {\n"
    
    # Sort by sport, then by league for readability
    sorted_items = sorted(mapping.items(), key=lambda x: (x[1], x[0]))
    
    current_sport = None
    for league, sport in sorted_items:
        if sport != current_sport:
            output += "\n    # " + sport.replace('-', ' ').title() + "\n"
            current_sport = sport
        output += '    "' + league + '": "' + sport + '",\n'
        
    output += "}\n"
    
    # Write directly to constants.py
    with open("src/espnpy/constants.py", "w") as f:
        f.write("# Auto-generated mapping of all ESPN leagues to their respective sports.\n\n")
        f.write(output)
        
    print("Successfully wrote " + str(len(mapping)) + " leagues to src/espnpy/constants.py!")

if __name__ == "__main__":
    asyncio.run(main())
