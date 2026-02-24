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
