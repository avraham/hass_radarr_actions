"""Constants for Radarr."""
import logging
from typing import Final

DOMAIN: Final = "radarr_actions"

# Defaults
DEFAULT_NAME = "Radarr Actions"

ATTR_HOST = "host"
ATTR_API_KEY = "api_key"
ATTR_MOVIE_TITLE = "movie_title"
ATTR_PROFILE_ID = "profile_id"
ATTR_ROOT_DIRECTORY= "root_directory"
ATTR_TMDBID_API_V3 = "tmdbid_api_key_v3"
ATTR_LAST_N_YEARS= "exclude_older_than_n_years"
ATTR_SEARCH_RELEASE= "search_release"

DEFAULT_LAST_N_YEARS = -1
DEFAULT_SEARCH_RELEASE = False

BASE_URL = "/api/v3/movie"
TMDBID_BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
            'Content-type':'application/json',
            'Accept':'application/json',
            'X-Api-Key': 'APIKEY'
        }


LOGGER = logging.getLogger(__package__)

