from flask import Blueprint, jsonify, request
from flask_limiter.util import get_remote_address
from jsonschema import validate, ValidationError
from app import cache, limiter
from services.tmdb import TMDbService
from api.schemas import SEARCH_SCHEMA, ACTOR_FILTER_SCHEMA, MEDIA_FILTER_SCHEMA
from utils.decorators import handle_tmdb_errors
from utils.errors import APIError

api_bp = Blueprint('api', __name__)
tmdb_service = TMDbService()

@api_bp.errorhandler(APIError)
def handle_api_error(error):
    response = {
        'error': True,
        'message': str(error),
        'code': error.code
    }
    return jsonify(response), error.status_code

@api_bp.route('/actors/search')
@limiter.limit("60/minute")
@handle_tmdb_errors
def search_actors():
    query = request.args.get('query')
    if not query:
        raise APIError("Query parameter is required", 400)
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if page < 1:
        raise APIError("Page number must be greater than 0", 400)
    if per_page < 1 or per_page > 100:
        raise APIError("Per page must be between 1 and 100", 400)
    
    # Get filter parameters
    filters = {
        'min_popularity': request.args.get('min_popularity', type=float),
        'gender': request.args.get('gender', type=int),
        'birth_year_from': request.args.get('birth_year_from', type=int),
        'birth_year_to': request.args.get('birth_year_to', type=int)
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        validate(
            instance={"query": query, **filters},
            schema=ACTOR_FILTER_SCHEMA
        )
    except ValidationError as e:
        raise APIError(str(e), 400)

    @cache.memoize(timeout=300)
    def get_cached_actors(q, f, p, pp):
        return tmdb_service.search_actors(q, f, page=p, per_page=pp)

    results = get_cached_actors(query, filters, page, per_page)
    return jsonify(results)

@api_bp.route('/actors/<int:actor_id>/filmography')
@limiter.limit("60/minute")
@handle_tmdb_errors
def get_actor_filmography(actor_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if page < 1:
        raise APIError("Page number must be greater than 0", 400)
    if per_page < 1 or per_page > 100:
        raise APIError("Per page must be between 1 and 100", 400)

    @cache.memoize(timeout=300)
    def get_cached_filmography(aid, p, pp):
        return tmdb_service.get_actor_filmography(aid, page=p, per_page=pp)

    results = get_cached_filmography(actor_id, page, per_page)
    return jsonify(results)

@api_bp.route('/media/search')
@limiter.limit("60/minute")
@handle_tmdb_errors
def search_media():
    query = request.args.get('query')
    media_type = request.args.get('type', 'movie')  # movie or tv
    
    if not query:
        raise APIError("Query parameter is required", 400)
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if page < 1:
        raise APIError("Page number must be greater than 0", 400)
    if per_page < 1 or per_page > 100:
        raise APIError("Per page must be between 1 and 100", 400)
    
    # Get filter parameters
    filters = {
        'year': request.args.get('year', type=int),
        'genre_id': request.args.get('genre_id', type=int),
        'min_rating': request.args.get('min_rating', type=float),
        'language': request.args.get('language')
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        validate(
            instance={"query": query, **filters},
            schema=MEDIA_FILTER_SCHEMA
        )
    except ValidationError as e:
        raise APIError(str(e), 400)

    @cache.memoize(timeout=300)
    def get_cached_media(q, t, f, p, pp):
        return tmdb_service.search_media(q, t, f, page=p, per_page=pp)

    results = get_cached_media(query, media_type, filters, page, per_page)
    return jsonify(results)

@api_bp.route('/media/<int:media_id>/cast')
@limiter.limit("60/minute")
@handle_tmdb_errors
def get_media_cast(media_id):
    media_type = request.args.get('type', 'movie')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if page < 1:
        raise APIError("Page number must be greater than 0", 400)
    if per_page < 1 or per_page > 100:
        raise APIError("Per page must be between 1 and 100", 400)

    @cache.memoize(timeout=300)
    def get_cached_cast(mid, mt, p, pp):
        return tmdb_service.get_media_cast(mid, mt, page=p, per_page=pp)

    results = get_cached_cast(media_id, media_type, page, per_page)
    return jsonify(results)
