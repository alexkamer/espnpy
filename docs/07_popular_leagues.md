# Popular Leagues Cheat Sheet

`espnpy` automatically supports over **384+ global sports leagues**. Every single one of them is explicitly exposed via the `espnpy.` dot-notation for perfect IDE Autocomplete.

If you don't want to scroll through the autocomplete menu, here is a quick reference guide to the most popular leagues, organized by sport!

## 🏈 American Football
| League | Python Property |
| :--- | :--- |
| **NFL** | `espnpy.nfl` |
| **College Football (NCAA)** | `espnpy.college_football` |
| **UFL** | `espnpy.ufl` |
| **CFL (Canadian)** | `espnpy.cfl` |

## 🏀 Basketball
| League | Python Property |
| :--- | :--- |
| **NBA** | `espnpy.nba` |
| **WNBA** | `espnpy.wnba` |
| **Men's College (NCAA)** | `espnpy.mens_college_basketball` |
| **Women's College (NCAA)** | `espnpy.womens_college_basketball` |
| **FIBA** | `espnpy.fiba` |
| **NBA G-League** | `espnpy.nba_development` |

## ⚾️ Baseball & Softball
| League | Python Property |
| :--- | :--- |
| **MLB** | `espnpy.mlb` |
| **College Baseball** | `espnpy.college_baseball` |
| **College Softball** | `espnpy.college_softball` |
| **World Baseball Classic** | `espnpy.world_baseball_classic` |

## 🏒 Hockey
| League | Python Property |
| :--- | :--- |
| **NHL** | `espnpy.nhl` |
| **Men's College Hockey** | `espnpy.mens_college_hockey` |

## ⚽️ Soccer
*ESPN designates soccer leagues using dot-notation (e.g. `eng.1`). Because dots are invalid syntax in Python property names, `espnpy` automatically translates them to underscores for you!*

| League | Python Property |
| :--- | :--- |
| **English Premier League** | `espnpy.eng_1` |
| **La Liga (Spain)** | `espnpy.esp_1` |
| **Bundesliga (Germany)** | `espnpy.ger_1` |
| **Serie A (Italy)** | `espnpy.ita_1` |
| **Ligue 1 (France)** | `espnpy.fra_1` |
| **Major League Soccer (US)**| `espnpy.usa_1` |
| **NWSL (Women's US)** | `espnpy.usa_nwsl` |
| **UEFA Champions League** | `espnpy.uefa_champions` |
| **UEFA Europa League** | `espnpy.uefa_europa` |
| **FIFA World Cup** | `espnpy.fifa_world` |

## 🏎️ Racing
| League | Python Property |
| :--- | :--- |
| **Formula 1** | `espnpy.f1` |
| **NASCAR** | `espnpy.nascar_premier` |
| **IndyCar** | `espnpy.irl` |

## ⛳️ Golf
| League | Python Property |
| :--- | :--- |
| **PGA Tour** | `espnpy.pga` |
| **LIV Golf** | `espnpy.liv` |
| **LPGA** | `espnpy.lpga` |

## 🥊 MMA
| League | Python Property |
| :--- | :--- |
| **UFC** | `espnpy.ufc` |
| **PFL** | `espnpy.pfl` |

## 🎾 Tennis
| League | Python Property |
| :--- | :--- |
| **ATP (Men's)** | `espnpy.atp` |
| **WTA (Women's)** | `espnpy.wta` |

---
*Note: This is just a fraction of what is available! If you are looking for an obscure league (e.g. Mexican Winter League Baseball), just type `espnpy.mexican_winter_league` into your code editor!*
