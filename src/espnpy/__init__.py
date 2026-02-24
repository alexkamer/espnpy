from .client import ESPNClient, LeagueProxy

__version__ = "1.0.0"

# Create a global default client for convenience (espnpy.nfl.teams())
_default_client = ESPNClient()

# Expose common leagues explicitly for IDE Auto-complete
nfl = _default_client.nfl
nba = _default_client.nba
mlb = _default_client.mlb
nhl = _default_client.nhl
wnba = _default_client.wnba
college_football = _default_client.college_football
mens_college_basketball = _default_client.mens_college_basketball

def __getattr__(name: str) -> LeagueProxy:
    """
    Fallback for dynamically requested leagues at the module level.
    Example: `espnpy.eng_1.teams()` will automatically resolve here.
    """
    return getattr(_default_client, name)

__all__ = [
    "ESPNClient",
    "nfl", "nba", "mlb", "nhl", "wnba",
    "college_football", "mens_college_basketball"
]
