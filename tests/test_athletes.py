import pytest
import asyncio
from espnpy import ESPNClient
from httpx import HTTPStatusError

@pytest.mark.asyncio
async def test_get_athletes_nba():
    """NBA allows full league athlete scraping."""
    async with ESPNClient() as client:
        athletes = await client.nba.athletes()
        assert len(athletes) > 0
        assert "firstName" in athletes[0]

@pytest.mark.asyncio
async def test_get_athletes_nhl_active():
    """NHL requires active=True or it takes forever, but it allows full league scraping."""
    async with ESPNClient() as client:
        athletes = await client.nhl.athletes(active=True)
        assert len(athletes) > 0

@pytest.mark.asyncio
async def test_get_athlete_has_team_id():
    """Verify that fetching a specific athlete dynamically parses and attaches their teamId."""
    async with ESPNClient() as client:
        # Steph Curry (ID: 3975) is on the Warriors (Team ID: 9)
        steph = await client.nba.athlete("3975")
        assert steph["id"] == "3975"
        assert steph["teamId"] == "9"
        assert steph["firstName"] == "Stephen"
