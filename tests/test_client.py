import pytest
from espnpy import ESPNClient

@pytest.mark.asyncio
async def test_get_sports():
    async with ESPNClient() as client:
        data = await client.get_sports(limit=5)
        assert "items" in data
        assert isinstance(data["items"], list)

@pytest.mark.asyncio
async def test_get_leagues():
    async with ESPNClient() as client:
        leagues = await client.get_leagues("basketball", limit=3)
        assert isinstance(leagues, list)
        assert len(leagues) > 0
        assert "id" in leagues[0]
        assert "name" in leagues[0]
        assert "slug" in leagues[0]

@pytest.mark.asyncio
async def test_get_teams_inference():
    async with ESPNClient() as client:
        # NBA shouldn't require the 'sport' parameter
        teams = await client.get_teams("nba")
        assert len(teams) >= 30
        assert any(t["abbreviation"] == "ATL" for t in teams)

@pytest.mark.asyncio
async def test_get_teams_pagination():
    async with ESPNClient() as client:
        # Men's College Basketball has > 1000 teams, which tests pagination
        teams = await client.get_teams("mens-college-basketball")
        assert len(teams) > 1000
        assert any(t["abbreviation"] == "DUKE" for t in teams)

@pytest.mark.asyncio
async def test_missing_league_raises_error():
    async with ESPNClient() as client:
        # Trying a league that doesn't exist in constants and omitting sport should raise ValueError
        with pytest.raises(ValueError, match="Could not automatically infer the sport"):
            await client.get_teams("some-made-up-league")
