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

    async def team(self, team_id: str) -> Dict[str, Any]:
        """Fetch general information for a specific team in this league by their ID.
        
        Args:
            team_id: The ID of the team (e.g. '1' for Atlanta Falcons).
        """
        return await self._client.get_team(self.league, team_id)

    async def schedule(self, team_id: str, season: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch the full schedule of games for a specific team in this league.
        
        Args:
            team_id: The ID of the team.
            season: The explicit year string (e.g. '2023').
        """
        return await self._client.get_team_schedule(self.league, team_id, season=season)

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

    async def athlete_stats(self, athlete_id: str) -> Dict[str, Any]:
        """Fetch advanced statistical splits (Home vs Away, Season Totals) for a specific athlete."""
        return await self._client.get_athlete_stats(self.league, athlete_id)

    async def scoreboard(self, date: Optional[str] = None, group: Optional[str] = None, season_type: Optional[str] = None, limit: int = 1000, raw: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Fetch the scoreboard (schedule, live scores, odds) for a specific date.
        
        Args:
            date: The date string in 'YYYYMMDD' format. If not provided, returns current/upcoming games.
            group: Optional ESPN group ID filter (e.g. group="50" for full Men's College Basketball).
            season_type: Optional ESPN season type ID (1=Preseason, 2=Regular Season, 3=Postseason).
            limit: The maximum number of games to return (max 1000).
            raw: If True, returns the massive raw JSON from ESPN. If False (default), 
                 returns a standardized list of flattened game dictionaries.
        """
        return await self._client.get_scoreboard(self.league, date=date, group=group, season_type=season_type, limit=limit, raw=raw)

    async def game_summary(self, event_id: str) -> Dict[str, Any]:
        """Fetch the detailed game summary (boxscore, play-by-play, odds) for a specific event.
        
        Args:
            event_id: The ID of the game/event.
        """
        return await self._client.get_game_summary(self.league, event_id)

    async def odds(self, event_id: str) -> List[Dict[str, Any]]:
        """Fetch betting lines across all sportsbook providers for a specific event.
        
        Args:
            event_id: The ID of the game/event.
        """
        return await self._client.get_odds(self.league, event_id)

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

    def _standardize_boxscore(self, box_data: Dict[str, Any], game_id: str) -> Dict[str, Any]:
        """Flatten the nested ESPN boxscore JSON into cleanly organized team and player dictionaries."""
        if not box_data:
            return {}
            
        # Standardize Teams
        teams_list = []
        for team_data in box_data.get("teams", []):
            t_info = team_data.get("team", {})
            stats_dict = {}
            for s in team_data.get("statistics", []):
                label = s.get("label") or s.get("name")
                val = s.get("displayValue")
                if label:
                    stats_dict[label] = val
                    
            teams_list.append({
                "gameId": game_id,
                "id": t_info.get("id"),
                "name": t_info.get("displayName"),
                "abbreviation": t_info.get("abbreviation"),
                "logo": t_info.get("logo"),
                "stats": stats_dict
            })
            
        # Standardize Players
        players_dict = {}
        for team_roster in box_data.get("players", []):
            t_info = team_roster.get("team", {})
            team_id = t_info.get("id")
            
            for category in team_roster.get("statistics", []):
                cat_name = category.get("name")
                labels = category.get("labels", [])
                
                for ath in category.get("athletes", []):
                    a_info = ath.get("athlete", {})
                    a_id = a_info.get("id")
                    
                    if not a_id:
                        continue
                        
                    if a_id not in players_dict:
                        players_dict[a_id] = {
                            "gameId": game_id,
                            "id": a_id,
                            "teamId": team_id,
                            "name": a_info.get("displayName"),
                            "shortName": a_info.get("shortName"),
                            "starter": ath.get("starter", False),
                            "jersey": a_info.get("jersey"),
                            "position": a_info.get("position", {}).get("abbreviation") or a_info.get("position", {}).get("name"),
                            "headshot": a_info.get("headshot", {}).get("href"),
                            "stats": {}
                        }
                    
                    # Zip the labels and values
                    stat_values = ath.get("stats", [])
                    zipped_stats = dict(zip(labels, stat_values))
                    
                    if cat_name:
                        players_dict[a_id]["stats"][cat_name] = zipped_stats
                    else:
                        # If there's no category name (like in the NBA), merge directly into the root stats
                        players_dict[a_id]["stats"].update(zipped_stats)
                        
        return {
            "teams": teams_list,
            "players": list(players_dict.values())
        }

    async def get_scoreboard(self, league: str, date: Optional[str] = None, sport: Optional[str] = None, group: Optional[str] = None, season_type: Optional[str] = None, limit: int = 1000, raw: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Fetch the scoreboard (schedule, live scores, odds) for a specific date.
        
        Args:
            league: The league (e.g., 'nfl').
            date: The date string in 'YYYYMMDD' format. If not provided, returns current/upcoming games.
            sport: Automatically inferred if not provided.
            group: An optional ESPN group ID to filter the games. 
                   Extremely useful for college sports where the default scoreboard only shows Top 25 games.
                   (e.g., Use group="50" for all Division I Men's College Basketball games).
            season_type: An optional ESPN season type ID (1=Preseason, 2=Regular Season, 3=Postseason).
            limit: Maximum number of games to return. Defaults to 1000 to ensure full slates are captured.
            raw: If True, returns the massive raw JSON from ESPN. If False (default), 
                 returns a standardized list of flattened game dictionaries.
            
        Returns:
            A list of standardized game dictionaries, or the raw JSON dictionary if raw=True.
        """
        resolved_sport = self._resolve_sport(league, sport)
        params = {"limit": limit}
        if date:
            params["dates"] = date
        if group:
            params["groups"] = group
        if season_type:
            params["seasontype"] = season_type
            
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
                # Team sports and Racing use "competitions" directly on the event
                if "competitions" in event:
                    competitions = event.get("competitions", [])
                # Tennis uses "groupings" which contain the "competitions" (matches)
                elif "groupings" in event:
                    competitions = []
                    for grouping in event.get("groupings", []):
                        competitions.extend(grouping.get("competitions", []))
                else:
                    competitions = []

                for competition in competitions:
                    status_obj = competition.get("status", {})
                    season_obj = event.get("season", {})
                    
                    # Basic Info. Fallback to event name if competition doesn't have one (Tennis)
                    game_id = competition.get("id") or event.get("id")
                    date = competition.get("date") or event.get("date")
                    name = competition.get("name") or event.get("name")
                    tournament_name = event.get("name") # Usually the overall event/tournament
                    short_name = competition.get("shortName") or event.get("shortName")
                    
                    # Season Info
                    season_year = season_obj.get("year")
                    season_type = season_obj.get("type")
                    season_slug = season_obj.get("slug")
                    
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
                    home_linescores, away_linescores = [], []
                    
                    for idx, comp in enumerate(competition.get("competitors", [])):
                        # Competitor can be a team or an athlete
                        team_info = comp.get("team") or comp.get("athlete") or {}
                        t_name = team_info.get("displayName")
                        t_id = team_info.get("id")
                        t_logo = team_info.get("logo") or team_info.get("headshot", {}).get("href") if isinstance(team_info.get("headshot"), dict) else team_info.get("flag", {}).get("href")
                        
                        # Set Scores / Linescores (e.g., [6.0, 6.0])
                        linescores = comp.get("linescores", [])
                        ls_values = [str(int(ls.get("value", 0))) for ls in linescores] if linescores else []
                        
                        # Main Score (Overall wins or sets won)
                        # In Tennis, comp.get("score") is usually null, so we sum the 'winner: true' linescores
                        score_raw = comp.get("score")
                        if score_raw is None and linescores:
                            score_raw = sum(1 for ls in linescores if ls.get("winner"))
                            if not score_raw and status == "Final": # fallback if winner boolean isn't set perfectly
                                score_raw = ls_values[-1] if ls_values else "0"
                        
                        if isinstance(score_raw, dict):
                            score = score_raw.get("displayValue")
                        else:
                            score = str(score_raw) if score_raw is not None else None
                        
                        # For Team sports
                        if comp.get("homeAway") == "home":
                            home_team, home_team_id, home_score, home_logo, home_linescores = t_name, t_id, score, t_logo, ls_values
                        elif comp.get("homeAway") == "away":
                            away_team, away_team_id, away_score, away_logo, away_linescores = t_name, t_id, score, t_logo, ls_values
                        # For Individual sports (Tennis/Racing) where home/away is null
                        else:
                            if idx == 0:
                                home_team, home_team_id, home_score, home_logo, home_linescores = t_name, t_id, score, t_logo, ls_values
                            elif idx == 1:
                                away_team, away_team_id, away_score, away_logo, away_linescores = t_name, t_id, score, t_logo, ls_values

                    # Format linescores into a readable string (e.g., "6-3, 6-4")
                    set_scores = ""
                    if home_linescores and away_linescores and len(home_linescores) == len(away_linescores):
                        set_scores = ", ".join([f"{h}-{a}" for h, a in zip(home_linescores, away_linescores)])

                    games.append({
                        "id": game_id,
                        "date": date,
                        "name": name,
                        "tournamentName": tournament_name, # Specifically added for Tennis/Golf
                        "shortName": short_name,
                        "seasonYear": season_year,
                        "seasonType": season_type,
                        "seasonSlug": season_slug,
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
                        "setScores": set_scores # Specificially added for Tennis/Volleyball
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
        boxscore = self._standardize_boxscore(raw_data.get("boxscore", {}), event_id)
        
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
        
        # Tennis, Golf, and MMA use rankings instead of standings
        if resolved_sport in ["tennis", "golf", "mma"]:
            url = f"https://site.api.espn.com/apis/site/v2/sports/{resolved_sport}/{league}/rankings"
            try:
                raw_data = await self.get_url(url)
            except httpx.HTTPStatusError:
                return []
        else:
            url = f"https://site.api.espn.com/apis/v2/sports/{resolved_sport}/{league}/standings"
            try:
                raw_data = await self.get_url(url)
            except httpx.HTTPStatusError:
                return []
        
        organized_standings = []
        
        # If we pulled Rankings (Tennis/Golf/MMA)
        if "rankings" in raw_data:
            for group in raw_data.get("rankings", []):
                group_name = group.get("name", "Overall")
                for rank_entry in group.get("ranks", []):
                    athlete_info = rank_entry.get("athlete", {})
                    
                    organized_standings.append({
                        "id": athlete_info.get("id", ""),
                        "name": athlete_info.get("displayName", ""),
                        "abbreviation": athlete_info.get("shortname", ""),
                        "logo": athlete_info.get("headshot", "") or athlete_info.get("flag", ""),
                        "group": group_name,
                        "wins": "0", "losses": "0", "ties": "0", "winPercent": "0",
                        "gamesBehind": "-",
                        "points": str(rank_entry.get("points", 0)),
                        "rank": str(rank_entry.get("current", 0)),
                        "streak": rank_entry.get("trend", "-"),
                        "pointsFor": "0", "pointsAgainst": "0", "differential": "0",
                        "homeRecord": "-", "awayRecord": "-", "divisionRecord": "-",
                        "conferenceRecord": "-", "lastTenRecord": "-", "playoffSeed": "-"
                    })
        else:
            # Standings are usually grouped by conference/league (e.g., AFC, NFC or Eastern, Western)
            for group in raw_data.get("children", []):
                group_name = group.get("name", "Overall")
                entries = group.get("standings", {}).get("entries", [])
                
                for entry in entries:
                    # Team sports use "team", Racing/Tennis use "athlete" or "constructor"
                    entity_info = entry.get("team") or entry.get("athlete") or entry.get("constructor") or {}
                    
                    # ESPN provides a list of stats (wins, losses, ties, pct). We flatten this into a dict.
                    raw_stats = entry.get("stats", [])
                    stats_dict = {s.get("name"): s.get("displayValue") for s in raw_stats if "name" in s and "displayValue" in s}
                    
                    organized_standings.append({
                        "id": entity_info.get("id", ""),
                        "name": entity_info.get("displayName", ""),
                        "abbreviation": entity_info.get("abbreviation", ""),
                        "logo": entity_info.get("logos", [{}])[0].get("href") if entity_info.get("logos") else (entity_info.get("flag", {}).get("href")),
                        "group": group_name,
                        "wins": stats_dict.get("wins", "0"),
                        "losses": stats_dict.get("losses", "0"),
                        "ties": stats_dict.get("ties", "0"),
                        "winPercent": stats_dict.get("winPercent", "0"),
                        "gamesBehind": stats_dict.get("gamesBehind", "-"),
                        "points": stats_dict.get("championshipPts") or stats_dict.get("points") or "0", # For Racing/Tennis
                        "rank": stats_dict.get("rank") or "-", # For Racing/Tennis
                        "streak": stats_dict.get("streak", "-"),
                        "pointsFor": stats_dict.get("pointsFor", "0"),
                        "pointsAgainst": stats_dict.get("pointsAgainst", "0"),
                        "differential": stats_dict.get("differential", "0"),
                        "homeRecord": stats_dict.get("Home", "-"),
                        "awayRecord": stats_dict.get("Road", "-"),
                        "divisionRecord": stats_dict.get("vs. Div.", "-"),
                        "conferenceRecord": stats_dict.get("vs. Conf.", "-"),
                        "lastTenRecord": stats_dict.get("Last Ten Games", "-"),
                        "playoffSeed": stats_dict.get("playoffSeed", "-")
                    })
                    
        # Sort standings: If win percentage is valid, sort by it. Otherwise, try to sort by rank or points (Racing/Tennis).
        def parse_sort_val(entry: dict) -> float:
            try:
                # If there is a rank, we want the lowest rank (so we return a negative number to sort descending, or reverse the logic)
                # But since we use reverse=True below, we need the "best" team to have the highest number.
                # So Rank 1 = 1000, Rank 2 = 999.
                rank = entry.get("rank")
                if rank and rank != "-":
                    return 10000 - float(rank)
                    
                # If there are points (like F1), sort by points
                points = entry.get("points")
                if points and points != "0" and points != "-":
                    return float(points)

                # Fallback to standard win percentage
                pct_str = entry.get("winPercent")
                if not pct_str or pct_str == "-":
                    return 0.0
                return float(pct_str)
            except ValueError:
                return 0.0

        organized_standings.sort(key=lambda x: parse_sort_val(x), reverse=True)
                
        return organized_standings

    async def get_athlete_stats(self, league: str, athlete_id: str, sport: Optional[str] = None) -> Dict[str, Any]:
        """Fetch advanced statistical splits (Home vs Away, Wins vs Losses, Season Totals) for an athlete.
        
        Args:
            league: The league (e.g., 'nfl').
            athlete_id: The unique ID of the athlete.
            sport: Automatically inferred if not provided.
            
        Returns:
            A standardized dictionary mapping categories (e.g. 'Wins/Ties', 'Home') to their specific stat totals.
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # Advanced stats live on the v3 COMMON API
        # Example: https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/3139477/splits
        url = f"https://site.web.api.espn.com/apis/common/v3/sports/{resolved_sport}/{league}/athletes/{athlete_id}/splits"
        raw_data = await self.get_url(url)
        
        organized_stats = {}
        
        # ESPN provides a master list of labels (e.g., ['CMP', 'ATT', 'YDS']) for this specific athlete
        labels = raw_data.get("labels", [])
        
        # ESPN then provides a massive array of "splits" (e.g., 'Home', 'Away', 'Wins', 'Losses', 'Last 4 Weeks')
        # Each split contains an array of string values that perfectly map 1-to-1 with the master labels list.
        for category in raw_data.get("splitCategories", []):
            for split in category.get("splits", []):
                split_name = split.get("displayName")
                stat_values = split.get("stats", [])
                
                # Zip the master labels with this specific split's values into a clean dictionary
                if split_name and len(labels) == len(stat_values):
                    stats_dict = dict(zip(labels, stat_values))
                    organized_stats[split_name] = stats_dict
                    
        return organized_stats

    async def get_odds(self, league: str, event_id: str, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch betting lines across all sportsbook providers for a specific game/event.
        
        Args:
            league: The league (e.g., 'nba').
            event_id: The unique ID of the game/event.
            sport: Automatically inferred if not provided.
            
        Returns:
            A list of standardized dictionaries containing odds from various providers (e.g. DraftKings, FanDuel).
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # Odds live on the CORE API
        # Format: /sports/{sport}/leagues/{league}/events/{event_id}/competitions/{event_id}/odds
        endpoint = f"sports/{resolved_sport}/leagues/{league}/events/{event_id}/competitions/{event_id}/odds"
        try:
            raw_data = await self._get(endpoint)
        except httpx.HTTPStatusError as e:
            # If the event doesn't exist or has no odds, safely return an empty list
            if e.response.status_code == 404:
                return []
            raise e
            
        organized_odds = []
        for item in raw_data.get("items", []):
            provider_name = item.get("provider", {}).get("name", "Unknown")
            
            # Extract generic details (NBA / MLB structure)
            details = item.get("details")
            over_under = item.get("overUnder")
            spread = item.get("spread")
            moneyline_away = item.get("awayTeamOdds", {}).get("moneyLine")
            moneyline_home = item.get("homeTeamOdds", {}).get("moneyLine")
            
            # Fallback for complex nesting (NFL / Soccer structure)
            if not details and "bettingOdds" in item:
                team_odds = item["bettingOdds"].get("teamOdds", {})
                
                spread_val = team_odds.get("preMatchSpreadHandicapHome", {}).get("value")
                if spread_val:
                    try: spread = float(spread_val)
                    except ValueError: pass
                    
                ou_val = team_odds.get("preMatchTotalHandicap", {}).get("value")
                if ou_val:
                    try: over_under = float(ou_val)
                    except ValueError: pass
                    
                away_ml = team_odds.get("preMatchMoneyLineAway", {}).get("value")
                home_ml = team_odds.get("preMatchMoneyLineHome", {}).get("value")
                if away_ml: moneyline_away = away_ml
                if home_ml: moneyline_home = home_ml
                
            organized_odds.append({
                "provider": provider_name,
                "details": details or (f"Home {spread}" if spread else None),
                "overUnder": over_under,
                "spread": spread,
                "awayMoneyLine": moneyline_away,
                "homeMoneyLine": moneyline_home
            })
            
        return organized_odds

    async def get_team(self, league: str, team_id: str, sport: Optional[str] = None) -> Dict[str, Any]:
        """Fetch general information for a specific team by their ID.
        
        Args:
            league: The league (e.g., 'nfl').
            team_id: The unique ID of the team.
            sport: Automatically inferred if not provided.
            
        Returns:
            A dictionary containing the team's location, name, colors, and logos.
        """
        resolved_sport = self._resolve_sport(league, sport)
        
        # Team details live on the SITE API
        # Example: https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/1
        raw_data = await self._get(f"sports/{resolved_sport}/{league}/teams/{team_id}", base_url=self.SITE_BASE_URL)
        team_info = raw_data.get("team", {})
        
        return {
            "id": team_info.get("id"),
            "slug": team_info.get("slug"),
            "location": team_info.get("location"),
            "name": team_info.get("name"),
            "nickname": team_info.get("nickname"),
            "abbreviation": team_info.get("abbreviation"),
            "displayName": team_info.get("displayName"),
            "shortDisplayName": team_info.get("shortDisplayName"),
            "color": team_info.get("color"),
            "alternateColor": team_info.get("alternateColor"),
            "isActive": team_info.get("isActive", True),
            "logo": team_info.get("logos", [{}])[0].get("href") if team_info.get("logos") else None,
            "standingSummary": team_info.get("standingSummary")
        }

    async def get_team_schedule(self, league: str, team_id: str, season: Optional[str] = None, sport: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch the full schedule of games for a specific team.
        
        Args:
            league: The league (e.g., 'nfl').
            team_id: The unique ID of the team.
            season: The year string (e.g. '2023'). If omitted, fetches the current season.
            sport: Automatically inferred if not provided.
            
        Returns:
            A standardized list of flattened game dictionaries identical to the `scoreboard()` output.
        """
        resolved_sport = self._resolve_sport(league, sport)
        params = {}
        if season:
            params["season"] = season
            
        # Team schedules live on the SITE API
        raw_data = await self._get(f"sports/{resolved_sport}/{league}/teams/{team_id}/schedule", params=params, base_url=self.SITE_BASE_URL)
        
        # ESPN's team schedule returns an "events" array identical to the scoreboard endpoint!
        # We can magically reuse the exact same flattening function.
        return self._standardize_scoreboard(raw_data)

    # ---------------------------------------------------------
    # Syntactic Sugar / Dot-Notation Handlers
    # ---------------------------------------------------------
    
    # We define the most popular leagues explicitly so IDE Autocomplete (VSCode, PyCharm) works flawlessly.
    @property
    def league_164205(self) -> "LeagueProxy": return LeagueProxy(self, "164205")

    @property
    def league_180659(self) -> "LeagueProxy": return LeagueProxy(self, "180659")

    @property
    def league_2009(self) -> "LeagueProxy": return LeagueProxy(self, "2009")

    @property
    def league_236461(self) -> "LeagueProxy": return LeagueProxy(self, "236461")

    @property
    def league_242041(self) -> "LeagueProxy": return LeagueProxy(self, "242041")

    @property
    def league_244293(self) -> "LeagueProxy": return LeagueProxy(self, "244293")

    @property
    def league_267979(self) -> "LeagueProxy": return LeagueProxy(self, "267979")

    @property
    def league_268565(self) -> "LeagueProxy": return LeagueProxy(self, "268565")

    @property
    def league_270555(self) -> "LeagueProxy": return LeagueProxy(self, "270555")

    @property
    def league_270557(self) -> "LeagueProxy": return LeagueProxy(self, "270557")

    @property
    def league_270559(self) -> "LeagueProxy": return LeagueProxy(self, "270559")

    @property
    def league_270563(self) -> "LeagueProxy": return LeagueProxy(self, "270563")

    @property
    def league_271937(self) -> "LeagueProxy": return LeagueProxy(self, "271937")

    @property
    def league_272073(self) -> "LeagueProxy": return LeagueProxy(self, "272073")

    @property
    def league_282(self) -> "LeagueProxy": return LeagueProxy(self, "282")

    @property
    def league_283(self) -> "LeagueProxy": return LeagueProxy(self, "283")

    @property
    def league_289234(self) -> "LeagueProxy": return LeagueProxy(self, "289234")

    @property
    def league_289237(self) -> "LeagueProxy": return LeagueProxy(self, "289237")

    @property
    def league_289262(self) -> "LeagueProxy": return LeagueProxy(self, "289262")

    @property
    def league_289271(self) -> "LeagueProxy": return LeagueProxy(self, "289271")

    @property
    def league_289272(self) -> "LeagueProxy": return LeagueProxy(self, "289272")

    @property
    def league_289274(self) -> "LeagueProxy": return LeagueProxy(self, "289274")

    @property
    def league_289277(self) -> "LeagueProxy": return LeagueProxy(self, "289277")

    @property
    def league_289279(self) -> "LeagueProxy": return LeagueProxy(self, "289279")

    @property
    def league_3(self) -> "LeagueProxy": return LeagueProxy(self, "3")

    @property
    def absolute(self) -> "LeagueProxy": return LeagueProxy(self, "absolute")

    @property
    def afc_asian_cup(self) -> "LeagueProxy": return LeagueProxy(self, "afc.asian.cup")

    @property
    def afc_challenge_cup(self) -> "LeagueProxy": return LeagueProxy(self, "afc.challenge_cup")

    @property
    def afc_champions(self) -> "LeagueProxy": return LeagueProxy(self, "afc.champions")

    @property
    def afc_cup(self) -> "LeagueProxy": return LeagueProxy(self, "afc.cup")

    @property
    def afc_cupq(self) -> "LeagueProxy": return LeagueProxy(self, "afc.cupq")

    @property
    def afc_saff_championship(self) -> "LeagueProxy": return LeagueProxy(self, "afc.saff.championship")

    @property
    def afc_w_asian_cup(self) -> "LeagueProxy": return LeagueProxy(self, "afc.w.asian.cup")

    @property
    def aff_championship(self) -> "LeagueProxy": return LeagueProxy(self, "aff.championship")

    @property
    def affliction(self) -> "LeagueProxy": return LeagueProxy(self, "affliction")

    @property
    def afl(self) -> "LeagueProxy": return LeagueProxy(self, "afl")

    @property
    def arg_1(self) -> "LeagueProxy": return LeagueProxy(self, "arg.1")

    @property
    def arg_2(self) -> "LeagueProxy": return LeagueProxy(self, "arg.2")

    @property
    def arg_3(self) -> "LeagueProxy": return LeagueProxy(self, "arg.3")

    @property
    def arg_4(self) -> "LeagueProxy": return LeagueProxy(self, "arg.4")

    @property
    def arg_copa(self) -> "LeagueProxy": return LeagueProxy(self, "arg.copa")

    @property
    def arg_copa_de_la_superliga(self) -> "LeagueProxy": return LeagueProxy(self, "arg.copa_de_la_superliga")

    @property
    def arg_supercopa(self) -> "LeagueProxy": return LeagueProxy(self, "arg.supercopa")

    @property
    def arg_supercopa_internacional(self) -> "LeagueProxy": return LeagueProxy(self, "arg.supercopa.internacional")

    @property
    def arg_trofeo_de_la_campeones(self) -> "LeagueProxy": return LeagueProxy(self, "arg.trofeo_de_la_campeones")

    @property
    def atp(self) -> "LeagueProxy": return LeagueProxy(self, "atp")

    @property
    def aus_1(self) -> "LeagueProxy": return LeagueProxy(self, "aus.1")

    @property
    def aus_w_1(self) -> "LeagueProxy": return LeagueProxy(self, "aus.w.1")

    @property
    def aut_1(self) -> "LeagueProxy": return LeagueProxy(self, "aut.1")

    @property
    def bang_fighting(self) -> "LeagueProxy": return LeagueProxy(self, "bang-fighting")

    @property
    def bangabandhu_cup(self) -> "LeagueProxy": return LeagueProxy(self, "bangabandhu.cup")

    @property
    def banni_fight(self) -> "LeagueProxy": return LeagueProxy(self, "banni-fight")

    @property
    def banzay(self) -> "LeagueProxy": return LeagueProxy(self, "banzay")

    @property
    def barracao(self) -> "LeagueProxy": return LeagueProxy(self, "barracao")

    @property
    def battlezone(self) -> "LeagueProxy": return LeagueProxy(self, "battlezone")

    @property
    def bel_1(self) -> "LeagueProxy": return LeagueProxy(self, "bel.1")

    @property
    def bel_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "bel.promotion.relegation")

    @property
    def bellator(self) -> "LeagueProxy": return LeagueProxy(self, "bellator")

    @property
    def benevides(self) -> "LeagueProxy": return LeagueProxy(self, "benevides")

    @property
    def big_fight(self) -> "LeagueProxy": return LeagueProxy(self, "big-fight")

    @property
    def blackout(self) -> "LeagueProxy": return LeagueProxy(self, "blackout")

    @property
    def bol_1(self) -> "LeagueProxy": return LeagueProxy(self, "bol.1")

    @property
    def bol_copa(self) -> "LeagueProxy": return LeagueProxy(self, "bol.copa")

    @property
    def bol_ply_rel(self) -> "LeagueProxy": return LeagueProxy(self, "bol.ply.rel")

    @property
    def bosnia(self) -> "LeagueProxy": return LeagueProxy(self, "bosnia")

    @property
    def boxe(self) -> "LeagueProxy": return LeagueProxy(self, "boxe")

    @property
    def bra_1(self) -> "LeagueProxy": return LeagueProxy(self, "bra.1")

    @property
    def bra_2(self) -> "LeagueProxy": return LeagueProxy(self, "bra.2")

    @property
    def bra_3(self) -> "LeagueProxy": return LeagueProxy(self, "bra.3")

    @property
    def bra_camp_carioca(self) -> "LeagueProxy": return LeagueProxy(self, "bra.camp.carioca")

    @property
    def bra_camp_gaucho(self) -> "LeagueProxy": return LeagueProxy(self, "bra.camp.gaucho")

    @property
    def bra_camp_mineiro(self) -> "LeagueProxy": return LeagueProxy(self, "bra.camp.mineiro")

    @property
    def bra_camp_paulista(self) -> "LeagueProxy": return LeagueProxy(self, "bra.camp.paulista")

    @property
    def bra_carioca_groupa(self) -> "LeagueProxy": return LeagueProxy(self, "bra.carioca.groupa")

    @property
    def bra_carioca_groupb(self) -> "LeagueProxy": return LeagueProxy(self, "bra.carioca.groupb")

    @property
    def bra_copa_do_brazil(self) -> "LeagueProxy": return LeagueProxy(self, "bra.copa_do_brazil")

    @property
    def bra_copa_do_nordeste(self) -> "LeagueProxy": return LeagueProxy(self, "bra.copa_do_nordeste")

    @property
    def bra_supercopa_do_brazil(self) -> "LeagueProxy": return LeagueProxy(self, "bra.supercopa_do_brazil")

    @property
    def brazilian_freestyle(self) -> "LeagueProxy": return LeagueProxy(self, "brazilian-freestyle")

    @property
    def budo(self) -> "LeagueProxy": return LeagueProxy(self, "budo")

    @property
    def caf_champions(self) -> "LeagueProxy": return LeagueProxy(self, "caf.champions")

    @property
    def caf_championship(self) -> "LeagueProxy": return LeagueProxy(self, "caf.championship")

    @property
    def caf_championship_qual(self) -> "LeagueProxy": return LeagueProxy(self, "caf.championship_qual")

    @property
    def caf_confed(self) -> "LeagueProxy": return LeagueProxy(self, "caf.confed")

    @property
    def caf_cosafa(self) -> "LeagueProxy": return LeagueProxy(self, "caf.cosafa")

    @property
    def caf_nations(self) -> "LeagueProxy": return LeagueProxy(self, "caf.nations")

    @property
    def caf_nations_qual(self) -> "LeagueProxy": return LeagueProxy(self, "caf.nations_qual")

    @property
    def caf_w_nations(self) -> "LeagueProxy": return LeagueProxy(self, "caf.w.nations")

    @property
    def cage_warriors(self) -> "LeagueProxy": return LeagueProxy(self, "cage-warriors")

    @property
    def campeones_cup(self) -> "LeagueProxy": return LeagueProxy(self, "campeones.cup")

    @property
    def can_w_nsl(self) -> "LeagueProxy": return LeagueProxy(self, "can.w.nsl")

    @property
    def caribbean_series(self) -> "LeagueProxy": return LeagueProxy(self, "caribbean-series")

    @property
    def cfl(self) -> "LeagueProxy": return LeagueProxy(self, "cfl")

    @property
    def champions_tour(self) -> "LeagueProxy": return LeagueProxy(self, "champions-tour")

    @property
    def chi_1(self) -> "LeagueProxy": return LeagueProxy(self, "chi.1")

    @property
    def chi_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "chi.1.promotion.relegation")

    @property
    def chi_2(self) -> "LeagueProxy": return LeagueProxy(self, "chi.2")

    @property
    def chi_copa_chi(self) -> "LeagueProxy": return LeagueProxy(self, "chi.copa_chi")

    @property
    def chi_super_cup(self) -> "LeagueProxy": return LeagueProxy(self, "chi.super_cup")

    @property
    def chn_1(self) -> "LeagueProxy": return LeagueProxy(self, "chn.1")

    @property
    def chn_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "chn.1.promotion.relegation")

    @property
    def club_friendly(self) -> "LeagueProxy": return LeagueProxy(self, "club.friendly")

    @property
    def col_1(self) -> "LeagueProxy": return LeagueProxy(self, "col.1")

    @property
    def col_2(self) -> "LeagueProxy": return LeagueProxy(self, "col.2")

    @property
    def col_copa(self) -> "LeagueProxy": return LeagueProxy(self, "col.copa")

    @property
    def col_superliga(self) -> "LeagueProxy": return LeagueProxy(self, "col.superliga")

    @property
    def college_baseball(self) -> "LeagueProxy": return LeagueProxy(self, "college-baseball")

    @property
    def college_football(self) -> "LeagueProxy": return LeagueProxy(self, "college-football")

    @property
    def college_softball(self) -> "LeagueProxy": return LeagueProxy(self, "college-softball")

    @property
    def concacaf_central_american_cup(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.central.american.cup")

    @property
    def concacaf_champions(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.champions")

    @property
    def concacaf_champions_cup(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.champions_cup")

    @property
    def concacaf_confederations_playoff(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.confederations_playoff")

    @property
    def concacaf_gold(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.gold")

    @property
    def concacaf_gold_qual(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.gold_qual")

    @property
    def concacaf_leagues_cup(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.leagues.cup")

    @property
    def concacaf_nations_league(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.nations.league")

    @property
    def concacaf_u23(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.u23")

    @property
    def concacaf_w_champions_cup(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.w.champions_cup")

    @property
    def concacaf_w_gold(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.w.gold")

    @property
    def concacaf_womens_championship(self) -> "LeagueProxy": return LeagueProxy(self, "concacaf.womens.championship")

    @property
    def conmebol_america(self) -> "LeagueProxy": return LeagueProxy(self, "conmebol.america")

    @property
    def conmebol_america_femenina(self) -> "LeagueProxy": return LeagueProxy(self, "conmebol.america.femenina")

    @property
    def conmebol_libertadores(self) -> "LeagueProxy": return LeagueProxy(self, "conmebol.libertadores")

    @property
    def conmebol_recopa(self) -> "LeagueProxy": return LeagueProxy(self, "conmebol.recopa")

    @property
    def conmebol_sudamericana(self) -> "LeagueProxy": return LeagueProxy(self, "conmebol.sudamericana")

    @property
    def crc_1(self) -> "LeagueProxy": return LeagueProxy(self, "crc.1")

    @property
    def cyp_1(self) -> "LeagueProxy": return LeagueProxy(self, "cyp.1")

    @property
    def den_1(self) -> "LeagueProxy": return LeagueProxy(self, "den.1")

    @property
    def dominican_winter_league(self) -> "LeagueProxy": return LeagueProxy(self, "dominican-winter-league")

    @property
    def dream(self) -> "LeagueProxy": return LeagueProxy(self, "dream")

    @property
    def ecu_1(self) -> "LeagueProxy": return LeagueProxy(self, "ecu.1")

    @property
    def eng_1(self) -> "LeagueProxy": return LeagueProxy(self, "eng.1")

    @property
    def eng_2(self) -> "LeagueProxy": return LeagueProxy(self, "eng.2")

    @property
    def eng_3(self) -> "LeagueProxy": return LeagueProxy(self, "eng.3")

    @property
    def eng_4(self) -> "LeagueProxy": return LeagueProxy(self, "eng.4")

    @property
    def eng_5(self) -> "LeagueProxy": return LeagueProxy(self, "eng.5")

    @property
    def eng_charity(self) -> "LeagueProxy": return LeagueProxy(self, "eng.charity")

    @property
    def eng_fa(self) -> "LeagueProxy": return LeagueProxy(self, "eng.fa")

    @property
    def eng_league_cup(self) -> "LeagueProxy": return LeagueProxy(self, "eng.league_cup")

    @property
    def eng_trophy(self) -> "LeagueProxy": return LeagueProxy(self, "eng.trophy")

    @property
    def eng_w_1(self) -> "LeagueProxy": return LeagueProxy(self, "eng.w.1")

    @property
    def eng_w_fa(self) -> "LeagueProxy": return LeagueProxy(self, "eng.w.fa")

    @property
    def eng_w_league_cup(self) -> "LeagueProxy": return LeagueProxy(self, "eng.w.league_cup")

    @property
    def esp_1(self) -> "LeagueProxy": return LeagueProxy(self, "esp.1")

    @property
    def esp_2(self) -> "LeagueProxy": return LeagueProxy(self, "esp.2")

    @property
    def esp_copa_de_la_reina(self) -> "LeagueProxy": return LeagueProxy(self, "esp.copa_de_la_reina")

    @property
    def esp_copa_del_rey(self) -> "LeagueProxy": return LeagueProxy(self, "esp.copa_del_rey")

    @property
    def esp_joan_gamper(self) -> "LeagueProxy": return LeagueProxy(self, "esp.joan_gamper")

    @property
    def esp_super_cup(self) -> "LeagueProxy": return LeagueProxy(self, "esp.super_cup")

    @property
    def esp_w_1(self) -> "LeagueProxy": return LeagueProxy(self, "esp.w.1")

    @property
    def eur(self) -> "LeagueProxy": return LeagueProxy(self, "eur")

    @property
    def euroamericana_supercopa(self) -> "LeagueProxy": return LeagueProxy(self, "euroamericana.supercopa")

    @property
    def f1(self) -> "LeagueProxy": return LeagueProxy(self, "f1")

    @property
    def fiba(self) -> "LeagueProxy": return LeagueProxy(self, "fiba")

    @property
    def fifa_concacaf_olympicsq(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.concacaf.olympicsq")

    @property
    def fifa_conmebol_olympicsq(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.conmebol.olympicsq")

    @property
    def fifa_cwc(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.cwc")

    @property
    def fifa_friendly(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.friendly")

    @property
    def fifa_friendly_w(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.friendly.w")

    @property
    def fifa_friendly_u21(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.friendly_u21")

    @property
    def fifa_intercontinental_cup(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.intercontinental.cup")

    @property
    def fifa_intercontinental_cup(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.intercontinental_cup")

    @property
    def fifa_intercontinental_cup_not_used(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.intercontinental_cup_not_used")

    @property
    def fifa_olympics(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.olympics")

    @property
    def fifa_shebelieves(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.shebelieves")

    @property
    def fifa_w_champions_cup(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.w.champions_cup")

    @property
    def fifa_w_concacaf_olympicsq(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.w.concacaf.olympicsq")

    @property
    def fifa_w_olympics(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.w.olympics")

    @property
    def fifa_wcq_ply(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.wcq.ply")

    @property
    def fifa_world(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.world")

    @property
    def fifa_world_u17(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.world.u17")

    @property
    def fifa_world_u20(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.world.u20")

    @property
    def fifa_worldq_afc(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.afc")

    @property
    def fifa_worldq_afc_conmebol(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.afc.conmebol")

    @property
    def fifa_worldq_caf(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.caf")

    @property
    def fifa_worldq_concacaf(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.concacaf")

    @property
    def fifa_worldq_concacaf_ofc(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.concacaf.ofc")

    @property
    def fifa_worldq_conmebol(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.conmebol")

    @property
    def fifa_worldq_ofc(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.ofc")

    @property
    def fifa_worldq_uefa(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.worldq.uefa")

    @property
    def fifa_wwc(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.wwc")

    @property
    def fifa_wwcq_ply(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.wwcq.ply")

    @property
    def fifa_wworld_u17(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.wworld.u17")

    @property
    def fifa_wworldq_uefa(self) -> "LeagueProxy": return LeagueProxy(self, "fifa.wworldq.uefa")

    @property
    def fng(self) -> "LeagueProxy": return LeagueProxy(self, "fng")

    @property
    def fra_1(self) -> "LeagueProxy": return LeagueProxy(self, "fra.1")

    @property
    def fra_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "fra.1.promotion.relegation")

    @property
    def fra_2(self) -> "LeagueProxy": return LeagueProxy(self, "fra.2")

    @property
    def fra_coupe_de_france(self) -> "LeagueProxy": return LeagueProxy(self, "fra.coupe_de_france")

    @property
    def fra_super_cup(self) -> "LeagueProxy": return LeagueProxy(self, "fra.super_cup")

    @property
    def fra_w_1(self) -> "LeagueProxy": return LeagueProxy(self, "fra.w.1")

    @property
    def friendly_emirates_cup(self) -> "LeagueProxy": return LeagueProxy(self, "friendly.emirates_cup")

    @property
    def ger_1(self) -> "LeagueProxy": return LeagueProxy(self, "ger.1")

    @property
    def ger_2(self) -> "LeagueProxy": return LeagueProxy(self, "ger.2")

    @property
    def ger_2_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "ger.2.promotion.relegation")

    @property
    def ger_a_bayernliganorth(self) -> "LeagueProxy": return LeagueProxy(self, "ger.a.bayernliganorth")

    @property
    def ger_dfb_pokal(self) -> "LeagueProxy": return LeagueProxy(self, "ger.dfb_pokal")

    @property
    def ger_playoff_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "ger.playoff.relegation")

    @property
    def ger_super_cup(self) -> "LeagueProxy": return LeagueProxy(self, "ger.super_cup")

    @property
    def gha_1(self) -> "LeagueProxy": return LeagueProxy(self, "gha.1")

    @property
    def global_arnold_clark_cup(self) -> "LeagueProxy": return LeagueProxy(self, "global.arnold.clark_cup")

    @property
    def global_champs_cup(self) -> "LeagueProxy": return LeagueProxy(self, "global.champs_cup")

    @property
    def global_club_challenge(self) -> "LeagueProxy": return LeagueProxy(self, "global.club_challenge")

    @property
    def global_finalissima(self) -> "LeagueProxy": return LeagueProxy(self, "global.finalissima")

    @property
    def global_gulf_cup(self) -> "LeagueProxy": return LeagueProxy(self, "global.gulf_cup")

    @property
    def global_pinatar_cup(self) -> "LeagueProxy": return LeagueProxy(self, "global.pinatar_cup")

    @property
    def global_toulon(self) -> "LeagueProxy": return LeagueProxy(self, "global.toulon")

    @property
    def global_u20_intercontinental_cup(self) -> "LeagueProxy": return LeagueProxy(self, "global.u20.intercontinental_cup")

    @property
    def global_w_finalissima(self) -> "LeagueProxy": return LeagueProxy(self, "global.w.finalissima")

    @property
    def global_wchamps_cup(self) -> "LeagueProxy": return LeagueProxy(self, "global.wchamps_cup")

    @property
    def gre_1(self) -> "LeagueProxy": return LeagueProxy(self, "gre.1")

    @property
    def gua_1(self) -> "LeagueProxy": return LeagueProxy(self, "gua.1")

    @property
    def hockey_world_cup(self) -> "LeagueProxy": return LeagueProxy(self, "hockey-world-cup")

    @property
    def hon_1(self) -> "LeagueProxy": return LeagueProxy(self, "hon.1")

    @property
    def idn_1(self) -> "LeagueProxy": return LeagueProxy(self, "idn.1")

    @property
    def ifc(self) -> "LeagueProxy": return LeagueProxy(self, "ifc")

    @property
    def ifl(self) -> "LeagueProxy": return LeagueProxy(self, "ifl")

    @property
    def ind_1(self) -> "LeagueProxy": return LeagueProxy(self, "ind.1")

    @property
    def ind_2(self) -> "LeagueProxy": return LeagueProxy(self, "ind.2")

    @property
    def ir1_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "ir1.1.promotion.relegation")

    @property
    def irl(self) -> "LeagueProxy": return LeagueProxy(self, "irl")

    @property
    def irl_1(self) -> "LeagueProxy": return LeagueProxy(self, "irl.1")

    @property
    def ita_1(self) -> "LeagueProxy": return LeagueProxy(self, "ita.1")

    @property
    def ita_2(self) -> "LeagueProxy": return LeagueProxy(self, "ita.2")

    @property
    def ita_coppa_italia(self) -> "LeagueProxy": return LeagueProxy(self, "ita.coppa_italia")

    @property
    def ita_super_cup(self) -> "LeagueProxy": return LeagueProxy(self, "ita.super_cup")

    @property
    def jpn_1(self) -> "LeagueProxy": return LeagueProxy(self, "jpn.1")

    @property
    def jpn_world_challenge(self) -> "LeagueProxy": return LeagueProxy(self, "jpn.world_challenge")

    @property
    def k1(self) -> "LeagueProxy": return LeagueProxy(self, "k1")

    @property
    def ken_1(self) -> "LeagueProxy": return LeagueProxy(self, "ken.1")

    @property
    def ksa_1(self) -> "LeagueProxy": return LeagueProxy(self, "ksa.1")

    @property
    def ksa_kings_cup(self) -> "LeagueProxy": return LeagueProxy(self, "ksa.kings.cup")

    @property
    def ksw(self) -> "LeagueProxy": return LeagueProxy(self, "ksw")

    @property
    def lfa(self) -> "LeagueProxy": return LeagueProxy(self, "lfa")

    @property
    def lfc(self) -> "LeagueProxy": return LeagueProxy(self, "lfc")

    @property
    def liv(self) -> "LeagueProxy": return LeagueProxy(self, "liv")

    @property
    def llb(self) -> "LeagueProxy": return LeagueProxy(self, "llb")

    @property
    def lls(self) -> "LeagueProxy": return LeagueProxy(self, "lls")

    @property
    def lpga(self) -> "LeagueProxy": return LeagueProxy(self, "lpga")

    @property
    def m1(self) -> "LeagueProxy": return LeagueProxy(self, "m1")

    @property
    def mens_college_basketball(self) -> "LeagueProxy": return LeagueProxy(self, "mens-college-basketball")

    @property
    def mens_college_hockey(self) -> "LeagueProxy": return LeagueProxy(self, "mens-college-hockey")

    @property
    def mens_college_lacrosse(self) -> "LeagueProxy": return LeagueProxy(self, "mens-college-lacrosse")

    @property
    def mens_college_volleyball(self) -> "LeagueProxy": return LeagueProxy(self, "mens-college-volleyball")

    @property
    def mens_college_water_polo(self) -> "LeagueProxy": return LeagueProxy(self, "mens-college-water-polo")

    @property
    def mens_olympics_basketball(self) -> "LeagueProxy": return LeagueProxy(self, "mens-olympics-basketball")

    @property
    def mens_olympics_golf(self) -> "LeagueProxy": return LeagueProxy(self, "mens-olympics-golf")

    @property
    def mex_1(self) -> "LeagueProxy": return LeagueProxy(self, "mex.1")

    @property
    def mex_2(self) -> "LeagueProxy": return LeagueProxy(self, "mex.2")

    @property
    def mex_campeon(self) -> "LeagueProxy": return LeagueProxy(self, "mex.campeon")

    @property
    def mexican_winter_league(self) -> "LeagueProxy": return LeagueProxy(self, "mexican-winter-league")

    @property
    def mfc(self) -> "LeagueProxy": return LeagueProxy(self, "mfc")

    @property
    def mlb(self) -> "LeagueProxy": return LeagueProxy(self, "mlb")

    @property
    def mys_1(self) -> "LeagueProxy": return LeagueProxy(self, "mys.1")

    @property
    def nascar_premier(self) -> "LeagueProxy": return LeagueProxy(self, "nascar-premier")

    @property
    def nascar_secondary(self) -> "LeagueProxy": return LeagueProxy(self, "nascar-secondary")

    @property
    def nascar_truck(self) -> "LeagueProxy": return LeagueProxy(self, "nascar-truck")

    @property
    def nba(self) -> "LeagueProxy": return LeagueProxy(self, "nba")

    @property
    def nba_development(self) -> "LeagueProxy": return LeagueProxy(self, "nba-development")

    @property
    def nba_summer_california(self) -> "LeagueProxy": return LeagueProxy(self, "nba-summer-california")

    @property
    def nba_summer_golden_state(self) -> "LeagueProxy": return LeagueProxy(self, "nba-summer-golden-state")

    @property
    def nba_summer_las_vegas(self) -> "LeagueProxy": return LeagueProxy(self, "nba-summer-las-vegas")

    @property
    def nba_summer_orlando(self) -> "LeagueProxy": return LeagueProxy(self, "nba-summer-orlando")

    @property
    def nba_summer_sacramento(self) -> "LeagueProxy": return LeagueProxy(self, "nba-summer-sacramento")

    @property
    def nba_summer_utah(self) -> "LeagueProxy": return LeagueProxy(self, "nba-summer-utah")

    @property
    def nbl(self) -> "LeagueProxy": return LeagueProxy(self, "nbl")

    @property
    def ned_1(self) -> "LeagueProxy": return LeagueProxy(self, "ned.1")

    @property
    def ned_2(self) -> "LeagueProxy": return LeagueProxy(self, "ned.2")

    @property
    def ned_3(self) -> "LeagueProxy": return LeagueProxy(self, "ned.3")

    @property
    def ned_3_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "ned.3.promotion.relegation")

    @property
    def ned_cup(self) -> "LeagueProxy": return LeagueProxy(self, "ned.cup")

    @property
    def ned_playoff_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "ned.playoff.relegation")

    @property
    def ned_supercup(self) -> "LeagueProxy": return LeagueProxy(self, "ned.supercup")

    @property
    def ned_w_1(self) -> "LeagueProxy": return LeagueProxy(self, "ned.w.1")

    @property
    def ned_w_eredivisie_cup(self) -> "LeagueProxy": return LeagueProxy(self, "ned.w.eredivisie_cup")

    @property
    def ned_w_knvb_cup(self) -> "LeagueProxy": return LeagueProxy(self, "ned.w.knvb_cup")

    @property
    def nfl(self) -> "LeagueProxy": return LeagueProxy(self, "nfl")

    @property
    def nga_1(self) -> "LeagueProxy": return LeagueProxy(self, "nga.1")

    @property
    def nhl(self) -> "LeagueProxy": return LeagueProxy(self, "nhl")

    @property
    def nll(self) -> "LeagueProxy": return LeagueProxy(self, "nll")

    @property
    def nonfifa(self) -> "LeagueProxy": return LeagueProxy(self, "nonfifa")

    @property
    def nor_1(self) -> "LeagueProxy": return LeagueProxy(self, "nor.1")

    @property
    def nor_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "nor.1.promotion.relegation")

    @property
    def ntw(self) -> "LeagueProxy": return LeagueProxy(self, "ntw")

    @property
    def ofc(self) -> "LeagueProxy": return LeagueProxy(self, "ofc")

    @property
    def olympics_baseball(self) -> "LeagueProxy": return LeagueProxy(self, "olympics-baseball")

    @property
    def olympics_mens_ice_hockey(self) -> "LeagueProxy": return LeagueProxy(self, "olympics-mens-ice-hockey")

    @property
    def olympics_womens_ice_hockey(self) -> "LeagueProxy": return LeagueProxy(self, "olympics-womens-ice-hockey")

    @property
    def other(self) -> "LeagueProxy": return LeagueProxy(self, "other")

    @property
    def pancrase(self) -> "LeagueProxy": return LeagueProxy(self, "pancrase")

    @property
    def par_1(self) -> "LeagueProxy": return LeagueProxy(self, "par.1")

    @property
    def par_1_supercopa(self) -> "LeagueProxy": return LeagueProxy(self, "par.1.supercopa")

    @property
    def per_1(self) -> "LeagueProxy": return LeagueProxy(self, "per.1")

    @property
    def pfl(self) -> "LeagueProxy": return LeagueProxy(self, "pfl")

    @property
    def pga(self) -> "LeagueProxy": return LeagueProxy(self, "pga")

    @property
    def pll(self) -> "LeagueProxy": return LeagueProxy(self, "pll")

    @property
    def por_1(self) -> "LeagueProxy": return LeagueProxy(self, "por.1")

    @property
    def por_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "por.1.promotion.relegation")

    @property
    def por_taca_portugal(self) -> "LeagueProxy": return LeagueProxy(self, "por.taca.portugal")

    @property
    def pride(self) -> "LeagueProxy": return LeagueProxy(self, "pride")

    @property
    def proelite(self) -> "LeagueProxy": return LeagueProxy(self, "proelite")

    @property
    def puerto_rican_winter_league(self) -> "LeagueProxy": return LeagueProxy(self, "puerto-rican-winter-league")

    @property
    def rfa(self) -> "LeagueProxy": return LeagueProxy(self, "rfa")

    @property
    def rizin(self) -> "LeagueProxy": return LeagueProxy(self, "rizin")

    @property
    def roc(self) -> "LeagueProxy": return LeagueProxy(self, "roc")

    @property
    def rsa_1(self) -> "LeagueProxy": return LeagueProxy(self, "rsa.1")

    @property
    def rsa_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "rsa.1.promotion.relegation")

    @property
    def rsa_2(self) -> "LeagueProxy": return LeagueProxy(self, "rsa.2")

    @property
    def rsa_mtn8(self) -> "LeagueProxy": return LeagueProxy(self, "rsa.mtn8")

    @property
    def rus_1(self) -> "LeagueProxy": return LeagueProxy(self, "rus.1")

    @property
    def rus_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "rus.1.promotion.relegation")

    @property
    def sco_1(self) -> "LeagueProxy": return LeagueProxy(self, "sco.1")

    @property
    def sco_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "sco.1.promotion.relegation")

    @property
    def sco_2(self) -> "LeagueProxy": return LeagueProxy(self, "sco.2")

    @property
    def sco_2_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "sco.2.promotion.relegation")

    @property
    def sco_challenge(self) -> "LeagueProxy": return LeagueProxy(self, "sco.challenge")

    @property
    def sco_cis(self) -> "LeagueProxy": return LeagueProxy(self, "sco.cis")

    @property
    def sco_tennents(self) -> "LeagueProxy": return LeagueProxy(self, "sco.tennents")

    @property
    def sfl(self) -> "LeagueProxy": return LeagueProxy(self, "sfl")

    @property
    def sgp_1(self) -> "LeagueProxy": return LeagueProxy(self, "sgp.1")

    @property
    def shark_fights(self) -> "LeagueProxy": return LeagueProxy(self, "shark-fights")

    @property
    def shooto_brazil(self) -> "LeagueProxy": return LeagueProxy(self, "shooto-brazil")

    @property
    def shooto_japan(self) -> "LeagueProxy": return LeagueProxy(self, "shooto-japan")

    @property
    def shoxc(self) -> "LeagueProxy": return LeagueProxy(self, "shoxc")

    @property
    def slv_1(self) -> "LeagueProxy": return LeagueProxy(self, "slv.1")

    @property
    def strikeforce(self) -> "LeagueProxy": return LeagueProxy(self, "strikeforce")

    @property
    def swe_1(self) -> "LeagueProxy": return LeagueProxy(self, "swe.1")

    @property
    def swe_1_promotion_relegation(self) -> "LeagueProxy": return LeagueProxy(self, "swe.1.promotion.relegation")

    @property
    def tfc(self) -> "LeagueProxy": return LeagueProxy(self, "tfc")

    @property
    def tgl(self) -> "LeagueProxy": return LeagueProxy(self, "tgl")

    @property
    def tha_1(self) -> "LeagueProxy": return LeagueProxy(self, "tha.1")

    @property
    def tpf(self) -> "LeagueProxy": return LeagueProxy(self, "tpf")

    @property
    def tur_1(self) -> "LeagueProxy": return LeagueProxy(self, "tur.1")

    @property
    def uefa_champions(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.champions")

    @property
    def uefa_champions_qual(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.champions_qual")

    @property
    def uefa_euro(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.euro")

    @property
    def uefa_euro_u19(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.euro.u19")

    @property
    def uefa_euro_u21(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.euro_u21")

    @property
    def uefa_euro_u21_qual(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.euro_u21_qual")

    @property
    def uefa_europa(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.europa")

    @property
    def uefa_europa_conf(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.europa.conf")

    @property
    def uefa_europa_conf_qual(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.europa.conf_qual")

    @property
    def uefa_europa_qual(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.europa_qual")

    @property
    def uefa_euroq(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.euroq")

    @property
    def uefa_nations(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.nations")

    @property
    def uefa_super_cup(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.super_cup")

    @property
    def uefa_w_europa(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.w.europa")

    @property
    def uefa_w_nations(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.w.nations")

    @property
    def uefa_wchampions(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.wchampions")

    @property
    def uefa_weuro(self) -> "LeagueProxy": return LeagueProxy(self, "uefa.weuro")

    @property
    def ufc(self) -> "LeagueProxy": return LeagueProxy(self, "ufc")

    @property
    def ufl(self) -> "LeagueProxy": return LeagueProxy(self, "ufl")

    @property
    def uga_1(self) -> "LeagueProxy": return LeagueProxy(self, "uga.1")

    @property
    def uru_1(self) -> "LeagueProxy": return LeagueProxy(self, "uru.1")

    @property
    def uru_2(self) -> "LeagueProxy": return LeagueProxy(self, "uru.2")

    @property
    def usa_1(self) -> "LeagueProxy": return LeagueProxy(self, "usa.1")

    @property
    def usa_ncaa_m_1(self) -> "LeagueProxy": return LeagueProxy(self, "usa.ncaa.m.1")

    @property
    def usa_ncaa_w_1(self) -> "LeagueProxy": return LeagueProxy(self, "usa.ncaa.w.1")

    @property
    def usa_nwsl(self) -> "LeagueProxy": return LeagueProxy(self, "usa.nwsl")

    @property
    def usa_nwsl_cup(self) -> "LeagueProxy": return LeagueProxy(self, "usa.nwsl.cup")

    @property
    def usa_nwsl_summer_cup(self) -> "LeagueProxy": return LeagueProxy(self, "usa.nwsl.summer.cup")

    @property
    def usa_open(self) -> "LeagueProxy": return LeagueProxy(self, "usa.open")

    @property
    def usa_usl_1(self) -> "LeagueProxy": return LeagueProxy(self, "usa.usl.1")

    @property
    def usa_usl_l1(self) -> "LeagueProxy": return LeagueProxy(self, "usa.usl.l1")

    @property
    def usa_usl_l1_cup(self) -> "LeagueProxy": return LeagueProxy(self, "usa.usl.l1.cup")

    @property
    def usa_w_usl_1(self) -> "LeagueProxy": return LeagueProxy(self, "usa.w.usl.1")

    @property
    def ven_1(self) -> "LeagueProxy": return LeagueProxy(self, "ven.1")

    @property
    def venezuelan_winter_league(self) -> "LeagueProxy": return LeagueProxy(self, "venezuelan-winter-league")

    @property
    def vfc(self) -> "LeagueProxy": return LeagueProxy(self, "vfc")

    @property
    def wec(self) -> "LeagueProxy": return LeagueProxy(self, "wec")

    @property
    def wnba(self) -> "LeagueProxy": return LeagueProxy(self, "wnba")

    @property
    def womens_college_basketball(self) -> "LeagueProxy": return LeagueProxy(self, "womens-college-basketball")

    @property
    def womens_college_field_hockey(self) -> "LeagueProxy": return LeagueProxy(self, "womens-college-field-hockey")

    @property
    def womens_college_hockey(self) -> "LeagueProxy": return LeagueProxy(self, "womens-college-hockey")

    @property
    def womens_college_lacrosse(self) -> "LeagueProxy": return LeagueProxy(self, "womens-college-lacrosse")

    @property
    def womens_college_volleyball(self) -> "LeagueProxy": return LeagueProxy(self, "womens-college-volleyball")

    @property
    def womens_college_water_polo(self) -> "LeagueProxy": return LeagueProxy(self, "womens-college-water-polo")

    @property
    def womens_olympics_basketball(self) -> "LeagueProxy": return LeagueProxy(self, "womens-olympics-basketball")

    @property
    def womens_olympics_golf(self) -> "LeagueProxy": return LeagueProxy(self, "womens-olympics-golf")

    @property
    def world_baseball_classic(self) -> "LeagueProxy": return LeagueProxy(self, "world-baseball-classic")

    @property
    def wta(self) -> "LeagueProxy": return LeagueProxy(self, "wta")

    @property
    def xfc(self) -> "LeagueProxy": return LeagueProxy(self, "xfc")

    @property
    def xfl(self) -> "LeagueProxy": return LeagueProxy(self, "xfl")

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
