# `espnpy` Examples Gallery 🏀🏈⚾️⚽️🎾🏎️

Welcome to the examples gallery! 

This folder contains fully runnable, copy-pasteable Python scripts demonstrating exactly how to use `espnpy` for different sports. 

Each file includes an **"Expected Output"** comment block at the very bottom, so you can instantly see exactly what the parsed dictionaries look like before you even run the script!

### 🏈 Football
*   [**`01_nfl_scoreboard_and_boxscore.py`**](./football/01_nfl_scoreboard_and_boxscore.py): Learn how to fetch the daily scoreboard, detailed betting odds, play-by-play logs, and passing leaders.

### 🏀 Basketball
*   [**`01_nba_standings_and_splits.py`**](./basketball/01_nba_standings_and_splits.py): Learn how to fetch League Standings (point differential) and deeply nested Advanced Player Splits (Home vs Away PPG, 3PT%).
*   [**`02_nba_time_travel.py`**](./basketball/02_nba_time_travel.py): Learn how to **Fuzzy Search** for a team without knowing their ESPN ID, and use the `season="2016"` parameter to travel back in time and pull the 73-9 Golden State Warriors standings!

### ⚽️ Soccer
*   [**`01_epl_roster_and_news.py`**](./soccer/01_epl_roster_and_news.py): Learn how to handle ESPN's soccer dot-notation (`eng.1`), pull current team rosters, and fetch the latest breaking headlines.
*   [**`02_epl_match_summary.py`**](./soccer/02_epl_match_summary.py): Learn how to pull deep-dive soccer data from a match summary, including tactical **Formations** (e.g. `4-2-3-1`) and extracting **Yellow/Red Cards** and Substitutions from the `keyEvents` array.

### 🎾 Tennis
*   [**`01_atp_rankings_and_scores.py`**](./tennis/01_atp_rankings_and_scores.py): Learn how `espnpy` automatically converts Standings into Player Rankings, extracts the specific Tournament Name, and flawlessly parses Set-by-Set Linescores (e.g. `6-3, 6-4`) into readable strings.

### ⛳️ Golf
*   [**`01_pga_leaderboard.py`**](./golf/01_pga_leaderboard.py): Learn how to extract a massive, 150-player live leaderboard from a PGA event, including round-by-round score splits and strokes under par (e.g. `-12`).

### 🏎️ Racing
*   [**`01_f1_standings_and_grid.py`**](./racing/01_f1_standings_and_grid.py): Learn how `espnpy` handles individual sports grids by automatically extracting F1 Drivers instead of Teams, sorting them perfectly by Championship Points.