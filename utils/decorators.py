from functools import wraps
from utils.errors import TMDbError, APIError

def handle_tmdb_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except TMDbError as e:
            raise APIError(str(e), e.status_code)
        except Exception as e:
            raise APIError("Internal server error", 500)
    return decorated_function
