# Media & News

These endpoints hit ESPN's media APIs to return high-quality editorial content.

## 1. Latest Headlines
Returns the top news articles published by ESPN journalists. You can fetch league-wide news or filter it down to a specific team.

```python
import espnpy
import asyncio

async def test_news():
    # General MLB News
    mlb_news = await espnpy.mlb.news(limit=5)
    for article in mlb_news:
        print(article['headline'])
        print(article['url'])

    # Team-Specific News (e.g., '1' for Atlanta Falcons)
    falcons_news = await espnpy.nfl.news(team_id="1", limit=3)
    for article in falcons_news:
        print(f"[{'Premium' if article['premium'] else 'Free'}] {article['headline']}")

asyncio.run(test_news())
```

### Expected Output Structure:
```json
[
  {
    "id": 48024734,
    "headline": "Kevin Stefanski's mindset as Falcons' new head coach",
    "description": "Kevin Stefanski joins "The Rich Eisen Show" and breaks down his mindset going into his first season as head coach of the Atlanta Falcons.",
    "published": "2026-02-24T20:46:54Z",
    "lastModified": "2026-02-24T20:46:54Z",
    "author": "ESPN PR",
    "premium": false,
    "image": "https://a.espncdn.com/media/motion/2026/0224/...",
    "url": "https://www.espn.com/video/clip?id=48024734"
  }
]
```
