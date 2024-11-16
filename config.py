import os

class Config:
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 3600
    RATELIMIT_DEFAULT = "100 per minute"
