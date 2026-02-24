import asyncio
import json
import httpx

def standardize_boxscore(box_data):
    if not box_data:
        return {}
        
    teams_list = []
    for team_data in box_data.get("teams", []):
        t_info = team_data.get("team", {})
        stats_dict = {}
        for s in team_data.get("statistics", []):
            label = s.get("label") or s.get("name")
            val = s.get("displayValue")
            if label:
                stats_dict[label] = val
                
        teams_list.append({
            "id": t_info.get("id"),
            "name": t_info.get("displayName"),
            "abbreviation": t_info.get("abbreviation"),
            "stats": stats_dict
        })
        
    players_dict = {}
    for team_roster in box_data.get("players", []):
        t_info = team_roster.get("team", {})
        team_id = t_info.get("id")
        
        for category in team_roster.get("statistics", []):
            cat_name = category.get("name")
            labels = category.get("labels", [])
            
            for ath in category.get("athletes", []):
                a_info = ath.get("athlete", {})
                a_id = a_info.get("id")
                
                if not a_id:
                    continue
                    
                if a_id not in players_dict:
                    players_dict[a_id] = {
                        "id": a_id,
                        "teamId": team_id,
                        "name": a_info.get("displayName"),
                        "shortName": a_info.get("shortName"),
                        "stats": {}
                    }
                
                stat_values = ath.get("stats", [])
                zipped_stats = dict(zip(labels, stat_values))
                
                if cat_name:
                    players_dict[a_id]["stats"][cat_name] = zipped_stats
                else:
                    players_dict[a_id]["stats"].update(zipped_stats)
                    
    return {
        "teams": teams_list,
        "players": list(players_dict.values())
    }

async def m():
    async with httpx.AsyncClient() as c:
        r = await c.get("https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401704627")
        parsed_nba = standardize_boxscore(r.json().get("boxscore"))
        print("--- NBA TEAM 1 ---")
        print(parsed_nba["teams"][0])
        print("--- NBA PLAYER 1 ---")
        print(parsed_nba["players"][0])
        
        r2 = await c.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401547403")
        parsed_nfl = standardize_boxscore(r2.json().get("boxscore"))
        bryce = next((p for p in parsed_nfl["players"] if "Bryce Young" in p["name"]), None)
        print("\n--- NFL PLAYER (Bryce Young) ---")
        print(json.dumps(bryce, indent=2))

asyncio.run(m())
