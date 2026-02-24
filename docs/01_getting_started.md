# Getting Started with `espnpy`

`espnpy` is a highly-optimized, fully asynchronous Python wrapper for ESPN's undocumented internal APIs. It completely abstracts away ESPN's complex JSON and aggressive pagination, providing developers with clean, flattened dictionaries.

## Installation

```bash
pip install espnpy
```

## How to Initialize

Because `espnpy` uses HTTP/2 and connection pooling to download thousands of URLs in seconds, you **must** use it asynchronously. There are two ways to use the library:

### Method 1: The Global Module (Recommended for Simplicity)
For quick scripts, `espnpy` automatically creates a global client behind the scenes. You can access leagues directly from the module.

```python
import asyncio
import espnpy

async def main():
    # Automatically uses the global connection pool
    nba_standings = await espnpy.nba.standings()
    print(nba_standings[0]["team"])

asyncio.run(main())
```

### Method 2: The Context Manager (Recommended for Large Applications)
If you are building a larger application (like a Discord bot or FastAPI server), it's best practice to manage the client lifecycle yourself using an asynchronous context manager.

```python
import asyncio
from espnpy import ESPNClient

async def main():
    # Explicitly opens and closes the connection pool
    async with ESPNClient() as client:
        nba_standings = await client.nba.standings()
        print(nba_standings[0]["team"])

asyncio.run(main())
```

---

## Documentation Guide
Check out the rest of the documentation folder to learn how to master the library!

1.  [`01_getting_started.md`](./01_getting_started.md)
2.  [`02_league_proxies.md`](./02_league_proxies.md) - Learn how `espnpy` magically maps 384+ leagues for perfect IDE autocomplete.
3.  [`03_entities.md`](./03_entities.md) - Fetching Teams, Athletes, and Rosters.
4.  [`04_data_and_stats.md`](./04_data_and_stats.md) - Fetching Advanced Splits and Standings.
5.  [`05_live_action.md`](./05_live_action.md) - Fetching Scoreboards, Boxscores, and Live Odds.
6.  [`06_news.md`](./06_news.md) - Fetching the latest headlines.
7.  [`07_popular_leagues.md`](./07_popular_leagues.md) - A cheat sheet of the most commonly requested `espnpy` league properties.
8.  [`08_individual_sports.md`](./08_individual_sports.md) - Learn how `espnpy` automatically adapts to handle Tennis Rankings and F1 Grids.
