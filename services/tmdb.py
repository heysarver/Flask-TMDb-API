import requests
import os
from flask import current_app
from utils.errors import TMDbError

class TMDbService:
    def __init__(self):
        self.base_url = "https://api.themoviedb.org/3"
        self.api_key = os.environ.get('TMDB_API_KEY')
        if not self.api_key:
            raise TMDbError("TMDB API key not found in environment variables", 500)

    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            raise TMDbError("Rate limit exceeded", 429)
        else:
            raise TMDbError(f"TMDb API error: {response.status_code}", response.status_code)

    def search_actors(self, query, filters=None, page=1, per_page=20):
        endpoint = "/search/person"
        params = {
            "query": query,
            "page": page
        }

        if filters:
            if 'min_popularity' in filters:
                params['vote_average.gte'] = filters['min_popularity']
            if 'gender' in filters:
                params['with_gender'] = filters['gender']
            
        response = self._make_request(endpoint, params)
        results = response.get("results", [])

        # Apply post-filtering for birth year if specified
        if filters and ('birth_year_from' in filters or 'birth_year_to' in filters):
            filtered_results = []
            for actor in results:
                if 'birthday' in actor and actor['birthday']:
                    birth_year = int(actor['birthday'].split('-')[0])
                    if ('birth_year_from' in filters and birth_year < filters['birth_year_from']):
                        continue
                    if ('birth_year_to' in filters and birth_year > filters['birth_year_to']):
                        continue
                filtered_results.append(actor)
            results = filtered_results[:per_page]

        return {
            "results": results,
            "total_results": response.get("total_results", len(results)),
            "page": response.get("page", page),
            "total_pages": response.get("total_pages", 1),
            "per_page": per_page
        }

    def get_actor_filmography(self, actor_id, page=1, per_page=20):
        endpoint = f"/person/{actor_id}/combined_credits"
        response = self._make_request(endpoint)
        
        # Manual pagination since TMDb doesn't support it for credits
        cast = response.get("cast", [])
        crew = response.get("crew", [])
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_cast = cast[start_idx:end_idx] if start_idx < len(cast) else []
        paginated_crew = crew[start_idx:end_idx] if start_idx < len(crew) else []
        
        total_items = len(cast) + len(crew)
        total_pages = (total_items + per_page - 1) // per_page
        
        return {
            "cast": paginated_cast,
            "crew": paginated_crew,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_results": total_items
        }

    def search_media(self, query, media_type='movie', filters=None, page=1, per_page=20):
        endpoint = f"/search/{media_type}"
        params = {
            "query": query,
            "page": page
        }

        if filters:
            if 'year' in filters:
                params['year'] = filters['year']
            if 'genre_id' in filters:
                params['with_genres'] = filters['genre_id']
            if 'min_rating' in filters:
                params['vote_average.gte'] = filters['min_rating']
            if 'language' in filters:
                params['language'] = filters['language']

        response = self._make_request(endpoint, params)
        results = response.get("results", [])[:per_page]
        
        return {
            "results": results,
            "total_results": response.get("total_results", 0),
            "page": response.get("page", page),
            "total_pages": response.get("total_pages", 1),
            "per_page": per_page
        }

    def get_media_cast(self, media_id, media_type='movie', page=1, per_page=20):
        endpoint = f"/{media_type}/{media_id}/credits"
        response = self._make_request(endpoint)
        
        # Manual pagination since TMDb doesn't support it for credits
        cast = response.get("cast", [])
        crew = response.get("crew", [])
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_cast = cast[start_idx:end_idx] if start_idx < len(cast) else []
        paginated_crew = crew[start_idx:end_idx] if start_idx < len(crew) else []
        
        total_items = len(cast) + len(crew)
        total_pages = (total_items + per_page - 1) // per_page
        
        return {
            "cast": paginated_cast,
            "crew": paginated_crew,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_results": total_items
        }
