import asyncio
import espnpy

async def main():
    print("Testing the 'group' parameter for massive college scoreboards!")
    
    date = "20240224" # A random busy Saturday in late February
    
    # 1. Men's College Basketball (Default)
    print("\nFetching CBB Scoreboard for " + date + " (DEFAULT)...")
    # By default, ESPN only returns Top 25 matchups and highly ranked conference games
    default_cbb = await espnpy.mens_college_basketball.scoreboard(date=date)
    print("Total Games Returned: " + str(len(default_cbb)))
    
    # 2. Men's College Basketball (Division 1 Overall Group: 50)
    print("\nFetching CBB Scoreboard for " + date + " (GROUP = 50)...")
    # Passing group=50 tells ESPN to return every single Division 1 game being played
    div1_cbb = await espnpy.mens_college_basketball.scoreboard(date=date, group="50")
    print("Total Division 1 Games Returned: " + str(len(div1_cbb)))
    
    # Let's peek at a random obscure game that was hidden in the default view
    obscure_game = div1_cbb[-1]
    print("\nExample Obscure Game Found:")
    print("[" + str(obscure_game['date']) + "] " + str(obscure_game['awayTeam']) + " vs " + str(obscure_game['homeTeam']) + " (" + str(obscure_game['status']) + ")")
    
    print("\n==================================================\n")
    
    # 3. College Football
    date_cfb = "20231111" # A busy Saturday in November
    
    print("Fetching CFB Scoreboard for " + date_cfb + " (DEFAULT)...")
    default_cfb = await espnpy.college_football.scoreboard(date=date_cfb)
    print("Total Games Returned: " + str(len(default_cfb)))
    
    # Passing group=80 returns all FBS games
    print("\nFetching CFB Scoreboard for " + date_cfb + " (GROUP = 80 - FBS)...")
    fbs_cfb = await espnpy.college_football.scoreboard(date=date_cfb, group="80")
    print("Total FBS Games Returned: " + str(len(fbs_cfb)))
    
    # Passing group=90 returns all FCS games
    print("\nFetching CFB Scoreboard for " + date_cfb + " (GROUP = 90 - FCS)...")
    fcs_cfb = await espnpy.college_football.scoreboard(date=date_cfb, group="90")
    print("Total FCS Games Returned: " + str(len(fcs_cfb)))

if __name__ == "__main__":
    asyncio.run(main())
