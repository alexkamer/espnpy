import httpx
import asyncio
from typing import Any, Dict, List, Optional, Union
from .constants import LEAGUE_TO_SPORT

class LeagueProxy:
    """A proxy class that allows accessing league endpoints cleanly via dot-notation (e.g. client.nba.teams())."""
    def __init__(self, client: "ESPNClient", league: str):
        self._client = client
        self.league = league
        
    async def info(self) -> Dict[str, Any]:
        """Fetch general information for this league."""
        return await self._client.get_league(self.league)

    async def teams(self) -> List[Dict[str, Any]]:
        """Fetch all teams for this league."""
        return await self._client.get_teams(self.league)

    async def athletes(self, active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Fetch all athletes/players for this league.
        
        Args:
            active: If True, explicitly requests only active athletes. 
                    If False, explicitly requests all historical athletes.
                    If None (default), returns whatever the API provides natively.
        """
        return await self._client.get_athletes(self.league, active=active)

    async def athlete(self, athlete_id: str) -> Dict[str, Any]:
        """Fetch details for a specific athlete in this league by their ID.
        
        Args:
            athlete_id: The ID of the athlete (e.g. '3975' for Steph Curry).
        """
        return await self._client.get_athlete(self.league, athlete_id)

    async def scoreboard(self, date: Optional[str] = None, raw: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Fetch the scoreboard (schedule, live scores, odds) for a specific date.
        
        Args:
            date: The date string in 'YYYYMMDD' format. If not provided, returns current/upcoming games.
            raw: If True, returns the massive raw JSON from ESPN. If False (default), 
                 returns a standardized list of flattened game dictionaries.
        """
        return await self._client.get_scoreboard(self.league, date=date, raw=raw)

    async def game_summary(self, event_id: str) -> Dict[str, Any]:
        """Fetch the detailed game summary (boxscore, play-by-play, odds) for a specific event.
        
        Args:
            event_id: The ID of the game/event.
        """
        return await self._client.get_game_summary(self.league, event_id)

    async def news(self, team_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch the latest news headlines for this league.
        
        Args:
            team_id: If provided, filters news down to only a specific team (e.g. '1').
            limit: The maximum number of articles to return (max 100).
        """
        return await self._client.get_news(self.league, team_id=team_id, limit=limit)

    async def standings(self) -> List[Dict[str, Any]]:
        """Fetch the current standings (wins, losses, win percentage) for the league."""
        return await self._client.get_standings(self.league)

    async def roster(self, team_id: str) -> List[Dict[str, Any]]:
        """Fetch the current roster for a specific team in this league.
        Note: Historical rosters are not supported by the API.
        
        Args:
            team_id: The ID of the team (e.g. '1' for Atlanta Hawks).
        """
        return await self._client.get_team_roster(self.league, team_id)


class ESPNClient:
    """The main asynchronous client for interacting with ESPN's hidden API."""
    
    # The Data Backend (Entities: Sports, Leagues, Teams, Athletes)
    CORE_BASE_URL = "https://sports.core.api.espn.com/v2"
    # The Application API (Action: Scoreboards, Summaries, News)
    SITE_BASE_URL = "https://site.api.espn.com/apis/site/v2"
    # The Fast Live Data (Action: Live Boxscores, Play-by-Play)
    CDN_BASE_URL = "https://cdn.espn.com/core"

    def __init__(self, timeout: float = 10.0, lang: str = "en", region: str = "us"):
        """Initialize the ESPN Client.
        
        Args:
            timeout (float): The maximum time to wait for a response before timing out. Defaults to 10.0.
            lang (str): The language code for the API response. Defaults to "en".
            region (str): The region code for the API response. Defaults to "us".
        """
        self.default_params = {
            "lang": lang,
            "region": region,
        }
        # Using AsyncClient for concurrent requests without a hardcoded base_url
        # HTTP/2 is often faster for many concurrent small requests
        self._session = httpx.AsyncClient(
            timeout=timeout,
            params=self.default_params,
            http2=True
        )

    # ---------------------------------------------------------
    # Core API Methods
    # ---------------------------------------------------------

    def _resolve_sport(self, league: str, sport: Optional[str] = None) -> str:
        """A helper to infer the sport if the user only passed the league name."""
        if sport:
            return sport
        
        inferred_sport = LEAGUE_TO_SPORT.get(league.lower())
        if not inferred_sport:
            raise ValueError(
                f"Could not automatically infer the sport for league '{league}'. "
                "Please provide the sport parameter explicitly: client.get_teams(league='{league}', sport='your_sport')"
            )
        return inferred_sport

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, base_url: str = CORE_BASE_URL) -> Dict[str, Any]:
        """A helper method to make GET requests and handle errors across different ESPN domains.
        
        Args:
            endpoint: The API path (e.g. '/sports/football/leagues/nfl').
            params: Optional query parameters.
            base_url: The ESPN domain to hit. Defaults to the Core Entity API.
            
        Returns:
            The parsed JSON dictionary from the response.
        """
        # Ensure there is no double-slash issue
        if endpoint.startswith("/"):
            endpoint = endpoint[1:]
        url = f"{base_url}/{endpoint}"
        
        response = await self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_url(self, url: str) -> Dict[str, Any]:
        """Helper to fetch data directly from a full URL, useful for following $ref links."""
        response = await self._session.get(url)
        response.raise_for_status()
        return response.json()

    async def get_sports(self, limit: int = 1000) -> Dict[str, Any]:
        """Get the top-level list of all sports."""
        params = {"limit": limit}
        return await self._get("/sports", params=params)

    async def get_sport(self, sport: str) -> Dict[str, Any]:
        """Get details for a specific sport (e.g., 'football', 'basketball')."""
        return await self._get(f"/sports/{sport}")

    async def get_leagues(self, sport: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get all leagues for a specific sport and fetch their details concurrently.
        
        Returns:
            A list of dictionaries containing specific league details: id, name, displayName, 
            abbreviation, shortName, slug, and a single logo href.
        """
        params = {"limit": limit}
        # 1. Fetch the list of references
        list_response = await self._get(f"/sports/{sport}/leagues", params=params)
        items = list_response.get("items", [])
        
        # 2. Extract the $ref URLs
        urls_to_fetch = [item.get("$ref") for item in items if "$ref" in item]
        
        # 3. Fetch all URLs concurrently using asyncio.gather
        tasks = [self.get_url(url) for url in urls_to_fetch]
        raw_leagues = await asyncio.gather(*tasks)
        
        # 4. Filter and organize the returned data
        organized_leagues = []
        for league in raw_leagues:
            # Safely grab the first logo href if the logos list exists and is not empty
            logos = league.get("logos", [])
            logo_href = logos[0].get("href") if logos else None
            
            organized_leagues.append({
                "id": league.get("id"),
                "name": league.get("name"),
                "displayName": league.get("displayName"),
                "abbreviation": league.get("abbreviation"),
                "shortName": league.get("shortName"),
                "slug": league.get("slug"),
                "logo": logo_href
            })
            
        return organized_leagues

    async def get_league(self, league: str, sport: Optional[str] = None) -> Dict[str, Any]:
        """Get details for a specific league within a sport (e.g., league='nfl').
        The sport is automatically inferred for common leagues.
        """
        resolved_sport = self._resolve_sport(league, sport)
        return await self._get(f"/sports/{resolved_sport}/leagues/{league}")

    async def get_teams(self, league: str, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all teams for a specific league, handling pagination automatically.
        The sport is automatically inferred for common leagues.
        
        Returns:
            A standardized list of dictionaries containing team details.
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # 1. Fetch the first page of references with max limit
        params = {"limit": 1000, "page": 1}
        first_page = await self._get(f"/sports/{resolved_sport}/leagues/{league}/teams", params=params)
        
        items = first_page.get("items", [])
        page_count = first_page.get("pageCount", 1)
        
        # 2. If there are multiple pages (e.g., > 1000 teams), fetch the remaining pages of URLs
        if page_count > 1:
            page_tasks = [
                self._get(f"/sports/{resolved_sport}/leagues/{league}/teams", params={"limit": 1000, "page": page_idx})
                for page_idx in range(2, page_count + 1)
            ]
            additional_pages = await asyncio.gather(*page_tasks)
            for page in additional_pages:
                items.extend(page.get("items", []))
                
        # 3. Extract all $ref URLs
        urls_to_fetch = [item.get("$ref") for item in items if "$ref" in item]
        
        # 4. Fetch all individual team URLs concurrently, but use a Semaphore to avoid connection pool timeouts.
        #    ESPN and httpx.AsyncClient can be overwhelmed by 300+ simultaneous connection requests.
        semaphore = asyncio.Semaphore(50)  # Limit to 50 concurrent requests at a time
        
        async def fetch_with_semaphore(url):
            async with semaphore:
                return await self.get_url(url)
                
        team_tasks = [fetch_with_semaphore(url) for url in urls_to_fetch]
        raw_teams = await asyncio.gather(*team_tasks)
        
        # 5. Standardize the resulting team dictionaries
        organized_teams = []
        for team in raw_teams:
            logos = team.get("logos", [])
            logo_href = logos[0].get("href") if logos else None
            
            organized_teams.append({
                "id": team.get("id"),
                "slug": team.get("slug"),
                "location": team.get("location"),
                "name": team.get("name"),
                "nickname": team.get("nickname"),  # Note: Some sports omit nickname
                "abbreviation": team.get("abbreviation"),
                "displayName": team.get("displayName"),
                "shortDisplayName": team.get("shortDisplayName"),
                "color": team.get("color"),
                "alternateColor": team.get("alternateColor"),
                "isActive": team.get("isActive", True),
                "logo": logo_href
            })
            
        return organized_teams

    async def get_scoreboard(self, league: str, date: Optional[str] = None, sport: Optional[str] = None, raw: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Fetch the scoreboard (schedule, live scores, odds) for a specific date.
        
        Args:
            league: The league (e.g., 'nfl').
            date: The date string in 'YYYYMMDD' format (e.g., '20240101'). 
                  If not provided, returns today's/current week's scoreboard.
            sport: Automatically inferred if not provided.
            raw: If True, returns the massive raw JSON from ESPN. If False (default), 
                 returns a standardized list of flattened game dictionaries.
            
        Returns:
            A list of standardized game dictionaries, or the raw JSON dictionary if raw=True.
        """
        resolved_sport = self._resolve_sport(league, sport)
        params = {}
        if date:
            params["dates"] = date
            
        # The Scoreboard lives on the SITE API
        raw_data = await self._get(f"sports/{resolved_sport}/{league}/scoreboard", params=params, base_url=self.SITE_BASE_URL)
        
        if raw:
            return raw_data
            
        return self._standardize_scoreboard(raw_data)

    def _standardize_scoreboard(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Flatten the massive, nested ESPN scoreboard JSON into a clean list of games."""
        games = []
        for event in raw_data.get("events", []):
            try:
                competition = event.get("competitions", [])[0]
                status_obj = competition.get("status", {})
                
                # Basic Info
                game_id = event.get("id")
                date = event.get("date")
                name = event.get("name")
                short_name = event.get("shortName")
                
                # Status (e.g., "Scheduled", "Final", "3rd Quarter")
                status = status_obj.get("type", {}).get("description")
                clock = status_obj.get("displayClock")
                period = status_obj.get("period")
                
                # Venue and TV Networks
                venue = competition.get("venue", {}).get("fullName")
                broadcasts = [b.get("names", [])[0] for b in competition.get("broadcasts", []) if b.get("names")]
                
                # Teams and Scores
                home_team, home_team_id, home_score, home_logo = None, None, None, None
                away_team, away_team_id, away_score, away_logo = None, None, None, None
                
                for comp in competition.get("competitors", []):
                    team_info = comp.get("team", {})
                    t_name = team_info.get("displayName")
                    t_id = team_info.get("id")
                    t_logo = team_info.get("logo")
                    score = comp.get("score")
                    
                    if comp.get("homeAway") == "home":
                        home_team, home_team_id, home_score, home_logo = t_name, t_id, score, t_logo
                    else:
                        away_team, away_team_id, away_score, away_logo = t_name, t_id, score, t_logo

                games.append({
                    "id": game_id,
                    "date": date,
                    "name": name,
                    "shortName": short_name,
                    "status": status,
                    "clock": clock,
                    "period": period,
                    "venue": venue,
                    "broadcasts": broadcasts,
                    "homeTeam": home_team,
                    "homeTeamId": home_team_id,
                    "homeScore": home_score,
                    "homeLogo": home_logo,
                    "awayTeam": away_team,
                    "awayTeamId": away_team_id,
                    "awayScore": away_score,
                    "awayLogo": away_logo,
                })
            except Exception:
                # If a game's JSON is malformed, skip it rather than crashing the whole scoreboard
                pass
                
        return games

    async def get_game_summary(self, league: str, event_id: str, sport: Optional[str] = None) -> Dict[str, Any]:
        """Fetch the detailed game summary (boxscore, play-by-play, odds) for a specific event.
        
        Args:
            league: The league (e.g., 'nba').
            event_id: The unique ID of the game/event.
            sport: Automatically inferred if not provided.
            
        Returns:
            A dictionary containing the standardized game summary data.
        """
        resolved_sport = self._resolve_sport(league, sport)
        params = {"event": event_id}
        
        # Game Summary lives on the SITE API
        raw_data = await self._get(f"sports/{resolved_sport}/{league}/summary", params=params, base_url=self.SITE_BASE_URL)
        
        # Standardize the output
        boxscore = raw_data.get("boxscore", {})
        
        # Extract betting odds safely
        pickcenter = raw_data.get("pickcenter", [])
        odds = {}
        if pickcenter:
            primary_odds = pickcenter[0]
            odds = {
                "provider": primary_odds.get("provider", {}).get("name", "Unknown"),
                "details": primary_odds.get("details"),
                "overUnder": primary_odds.get("overUnder"),
                "spread": primary_odds.get("spread")
            }
            
        # Standardize Play-by-Play
        plays = []
        for play in raw_data.get("plays", []):
            plays.append({
                "id": play.get("id"),
                "text": play.get("text"),
                "clock": play.get("clock", {}).get("displayValue"),
                "period": play.get("period", {}).get("number"),
                "scoringPlay": play.get("scoringPlay", False),
                "scoreValue": play.get("scoreValue")
            })
            
        return {
            "gameInfo": raw_data.get("gameInfo", {}),
            "boxscore": boxscore,
            "odds": odds,
            "plays": plays,
            "scoringPlays": raw_data.get("scoringPlays", []),
            "videos": raw_data.get("videos", []),
            "articles": raw_data.get("article", {})
        }

    async def get_news(self, league: str, team_id: Optional[str] = None, sport: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch the latest news articles and headlines for a specific league or team.
        
        Args:
            league: The league (e.g., 'nfl').
            team_id: Optional. The specific team ID to filter news for (e.g., '1' for Falcons).
            sport: Automatically inferred if not provided.
            limit: Maximum number of articles to return. Defaults to 50.
            
        Returns:
            A standardized list of dictionary objects representing news articles.
        """
        resolved_sport = self._resolve_sport(league, sport)
        params = {"limit": limit}
        if team_id:
            params["team"] = team_id
            
        # News lives on the SITE API
        raw_data = await self._get(f"sports/{resolved_sport}/{league}/news", params=params, base_url=self.SITE_BASE_URL)
        
        organized_news = []
        for article in raw_data.get("articles", []):
            # Try to grab the largest image/thumbnail available
            image_url = None
            images = article.get("images", [])
            if images:
                image_url = images[0].get("url")
                
            # Safely grab the first web link
            link_url = None
            links = article.get("links", {}).get("web", {})
            if links:
                link_url = links.get("href") or links.get("short", {}).get("href")

            organized_news.append({
                "id": article.get("id", ""),
                "headline": article.get("headline", ""),
                "description": article.get("description", ""),
                "published": article.get("published", ""),
                "lastModified": article.get("lastModified", ""),
                "author": article.get("byline", ""),
                "premium": article.get("premium", False), # Is it an ESPN+ exclusive article?
                "image": image_url,
                "url": link_url
            })
            
        return organized_news

    async def get_standings(self, league: str, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch the current standings (wins, losses, win percentage) for the league.
        
        Args:
            league: The league (e.g., 'nfl').
            sport: Automatically inferred if not provided.
            
        Returns:
            A standardized list of dictionaries containing team standings, ordered by rank.
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # Standings live on the v2 SITE API
        # Example: https://site.api.espn.com/apis/v2/sports/football/nfl/standings
        # We manually build this URL because the structure is slightly different than /apis/site/v2
        url = f"https://site.api.espn.com/apis/v2/sports/{resolved_sport}/{league}/standings"
        raw_data = await self.get_url(url)
        
        organized_standings = []
        
        # Standings are usually grouped by conference/league (e.g., AFC, NFC or Eastern, Western)
        for group in raw_data.get("children", []):
            group_name = group.get("name", "Overall")
            entries = group.get("standings", {}).get("entries", [])
            
            for entry in entries:
                team_info = entry.get("team", {})
                
                # ESPN provides a list of stats (wins, losses, ties, pct). We flatten this into a dict.
                raw_stats = entry.get("stats", [])
                stats_dict = {s.get("name"): s.get("displayValue") for s in raw_stats if "name" in s and "displayValue" in s}
                
                organized_standings.append({
                    "teamId": team_info.get("id", ""),
                    "team": team_info.get("displayName", ""),
                    "group": group_name,
                    "wins": stats_dict.get("wins", "0"),
                    "losses": stats_dict.get("losses", "0"),
                    "ties": stats_dict.get("ties", "0"),
                    "winPercent": stats_dict.get("winPercent", "0"),
                    "gamesBehind": stats_dict.get("gamesBehind", "-"),
                    "streak": stats_dict.get("streak", "-"),
                    "pointsFor": stats_dict.get("pointsFor", "0"),
                    "pointsAgainst": stats_dict.get("pointsAgainst", "0"),
                    "differential": stats_dict.get("differential", "0")
                })
                
        # Sort standings descending by win percentage (so index 0 is always the actual leader)
        def parse_win_percent(pct_str: str) -> float:
            try:
                # Handle standard "0.500" or ".500" strings. If missing, return 0.
                if not pct_str or pct_str == "-":
                    return 0.0
                return float(pct_str)
            except ValueError:
                return 0.0

        organized_standings.sort(key=lambda x: parse_win_percent(x["winPercent"]), reverse=True)
                
        return organized_standings

    # ---------------------------------------------------------
    # Syntactic Sugar / Dot-Notation Handlers
    # ---------------------------------------------------------
    
    # We define the most popular leagues explicitly so IDE Autocomplete (VSCode, PyCharm) works flawlessly.
    @property
    def nfl(self) -> LeagueProxy: return LeagueProxy(self, "nfl")

    @property
    def nba(self) -> LeagueProxy: return LeagueProxy(self, "nba")

    @property
    def mlb(self) -> LeagueProxy: return LeagueProxy(self, "mlb")

    @property
    def nhl(self) -> LeagueProxy: return LeagueProxy(self, "nhl")
    
    @property
    def wnba(self) -> LeagueProxy: return LeagueProxy(self, "wnba")
    
    @property
    def college_football(self) -> LeagueProxy: return LeagueProxy(self, "college-football")

    @property
    def mens_college_basketball(self) -> LeagueProxy: return LeagueProxy(self, "mens-college-basketball")

    def __getattr__(self, name: str) -> LeagueProxy:
        """
        Dynamically fallback to intercepting ANY league if an explicit property wasn't defined above.
        This allows `client.eng_1.teams()` or `client.fiba.teams()` without defining 384 explicit properties!
        """
        # Convert pythonic snake_case to the API's hyphenated-slug (e.g., college_softball -> college-softball)
        hyphen_slug = name.replace("_", "-")
        if hyphen_slug in LEAGUE_TO_SPORT:
            return LeagueProxy(self, hyphen_slug)
            
        # Convert pythonic snake_case to dot notation (e.g. eng_1 -> eng.1) for soccer leagues
        dot_slug = name.replace("_", ".")
        if dot_slug in LEAGUE_TO_SPORT:
            return LeagueProxy(self, dot_slug)
            
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


    # ---------------------------------------------------------
    # Session Management
    # ---------------------------------------------------------

    async def get_athletes(self, league: str, sport: Optional[str] = None, active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get all athletes/players for a specific league, handling pagination automatically.
        The sport is automatically inferred for common leagues.
        
        Args:
            league: The league to fetch athletes for.
            sport: The explicit sport (optional).
            active: If True, explicitly requests only active athletes via the API. 
                    Warning: Some leagues (like WNBA) throw a 400 Bad Request if this flag is passed.
                    If None (default), returns whatever the API provides natively.
                    
        Returns:
            A standardized list of dictionaries containing athlete details.
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # 1. Fetch the first page of references with max limit
        params = {"limit": 1000, "page": 1}
        if active is not None:
            params["active"] = "true" if active else "false"
            
        first_page = await self._get(f"/sports/{resolved_sport}/leagues/{league}/athletes", params=params)
        
        items = first_page.get("items", [])
        page_count = first_page.get("pageCount", 1)
        
        # 2. If there are multiple pages (e.g., > 1000 athletes), fetch the remaining pages of URLs
        if page_count > 1:
            page_tasks = []
            for page_idx in range(2, page_count + 1):
                page_params = {"limit": 1000, "page": page_idx}
                if active is not None:
                    page_params["active"] = "true" if active else "false"
                page_tasks.append(
                    self._get(f"/sports/{resolved_sport}/leagues/{league}/athletes", params=page_params)
                )
            
            additional_pages = await asyncio.gather(*page_tasks)
            for page in additional_pages:
                items.extend(page.get("items", []))
                
        # 3. Extract all $ref URLs
        urls_to_fetch = [item.get("$ref") for item in items if "$ref" in item]
        
        # 4. Fetch all individual athlete URLs concurrently
        semaphore = asyncio.Semaphore(50)  # Limit to 50 concurrent requests at a time
        
        async def fetch_with_semaphore(url):
            async with semaphore:
                return await self.get_url(url)
                
        athlete_tasks = [fetch_with_semaphore(url) for url in urls_to_fetch]
        raw_athletes = await asyncio.gather(*athlete_tasks)
        
        # 5. Standardize the resulting athlete dictionaries
        return [self._standardize_athlete(athlete) for athlete in raw_athletes]

    async def get_team_roster(self, league: str, team_id: str, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get the current active roster for a specific team.
        Note: ESPN's hidden API only supports current rosters for this endpoint.
        
        Args:
            league: The league (e.g., 'nba').
            team_id: The unique ID of the team (e.g., '1' for Atlanta Hawks).
            sport: Automatically inferred if not provided.
            
        Returns:
            A standardized list of athlete dictionaries currently on the roster.
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # Look up the league's current active season because the URL requires it
        league_info = await self._get(f"/sports/{resolved_sport}/leagues/{league}")
        season = str(league_info.get("season", {}).get("year"))
        if not season or season == "None":
            raise ValueError(f"Could not determine the current active season for {league}.")
                
        # 1. Fetch the first page of references with max limit
        params = {"limit": 1000, "page": 1}
        first_page = await self._get(f"/sports/{resolved_sport}/leagues/{league}/seasons/{season}/teams/{team_id}/athletes", params=params)
        
        items = first_page.get("items", [])
        page_count = first_page.get("pageCount", 1)
        
        # 2. If there are multiple pages
        if page_count > 1:
            page_tasks = [
                self._get(f"/sports/{resolved_sport}/leagues/{league}/seasons/{season}/teams/{team_id}/athletes", params={"limit": 1000, "page": page_idx})
                for page_idx in range(2, page_count + 1)
            ]
            additional_pages = await asyncio.gather(*page_tasks)
            for page in additional_pages:
                items.extend(page.get("items", []))
                
        # 3. Extract all $ref URLs
        urls_to_fetch = [item.get("$ref") for item in items if "$ref" in item]
        
        # 4. Fetch all individual athlete URLs concurrently
        semaphore = asyncio.Semaphore(50)
        
        async def fetch_with_semaphore(url):
            async with semaphore:
                return await self.get_url(url)
                
        athlete_tasks = [fetch_with_semaphore(url) for url in urls_to_fetch]
        raw_athletes = await asyncio.gather(*athlete_tasks)
        
        # 5. Standardize the resulting athlete dictionaries (same format as league-wide athletes)
        return [self._standardize_athlete(athlete) for athlete in raw_athletes]

    def _extract_team_id(self, ref_url: str) -> Optional[str]:
        """Helper to extract a team ID from a team $ref URL (e.g., '.../teams/12?lang=en')."""
        if not ref_url:
            return None
        # Split by '/teams/' and grab the next part, then remove any query parameters
        try:
            parts = ref_url.split("/teams/")
            if len(parts) > 1:
                return parts[1].split("?")[0]
        except Exception:
            pass
        return None

    def _standardize_athlete(self, athlete: Dict[str, Any]) -> Dict[str, Any]:
        """Helper to standardize the raw athlete dictionary returned from ESPN."""
        headshot = athlete.get("headshot", {}).get("href")
        position = athlete.get("position", {})
        position_name = position.get("displayName") or position.get("name")
        position_abbr = position.get("abbreviation")
        
        # Extract the team ID if they are currently linked to a team
        team_id = None
        team_ref = athlete.get("team", {}).get("$ref")
        if team_ref:
            team_id = self._extract_team_id(team_ref)

        return {
            "id": athlete.get("id"),
            "teamId": team_id,
            "slug": athlete.get("slug"),
            "firstName": athlete.get("firstName"),
            "lastName": athlete.get("lastName"),
            "fullName": athlete.get("fullName"),
            "displayName": athlete.get("displayName"),
            "shortName": athlete.get("shortName"),
            "weight": athlete.get("weight"),
            "displayWeight": athlete.get("displayWeight"),
            "height": athlete.get("height"),
            "displayHeight": athlete.get("displayHeight"),
            "age": athlete.get("age"),
            "dateOfBirth": athlete.get("dateOfBirth"),
            "jersey": athlete.get("jersey"),
            "position": position_name,
            "positionAbbreviation": position_abbr,
            "active": athlete.get("active", False),
            "headshot": headshot
        }

    async def get_athlete(self, league: str, athlete_id: str, sport: Optional[str] = None) -> Dict[str, Any]:
        """Get details for a specific athlete by their ID.
        
        Args:
            league: The league (e.g., 'nba').
            athlete_id: The unique ID of the athlete.
            sport: Automatically inferred if not provided.
            
        Returns:
            A standardized dictionary containing the athlete's details.
        """
        resolved_sport = self._resolve_sport(league, sport)
        athlete = await self._get(f"/sports/{resolved_sport}/leagues/{league}/athletes/{athlete_id}")
        return self._standardize_athlete(athlete)

    async def close(self):
        """Close the underlying HTTP session."""
        await self._session.aclose()

    # Async context manager support (async with ESPNClient() as client:)
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
