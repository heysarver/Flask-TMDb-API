# TMDb API Service

A Flask-based REST API service that provides a clean interface to The Movie Database (TMDb) with advanced search capabilities, filtering, and pagination support.

## Features

- **Actor Search**: Search for actors with advanced filters
  - Filter by popularity
  - Filter by gender
  - Filter by birth year range
  - Pagination support

- **Media Search**: Search for movies and TV shows with filters
  - Filter by year
  - Filter by genre
  - Filter by minimum rating
  - Filter by language
  - Pagination support

- **Filmography**: Get complete actor filmography
  - Combined cast and crew credits
  - Paginated results

- **Cast Information**: Get cast and crew details for media
  - Support for both movies and TV shows
  - Paginated results

- **Built-in Features**:
  - Rate limiting (100 requests per minute)
  - Response caching (5 minutes)
  - Input validation
  - Error handling
  - Health monitoring

## Setup

1. Clone the repository
2. Set up environment variables:
   ```bash
   export TMDB_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

The server will start on `http://localhost:5000`

## API Documentation

### Health Check
```http
GET /health
```
Verify if the service is running.

### Actor Search
```http
GET /api/v1/actors/search
```

**Query Parameters:**
- `query` (required): Search term
- `min_popularity` (optional): Minimum popularity score
- `gender` (optional): Filter by gender (0: not specified, 1: female, 2: male, 3: non-binary)
- `birth_year_from` (optional): Minimum birth year
- `birth_year_to` (optional): Maximum birth year
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Results per page (default: 20, max: 100)

**Example:**
```http
GET /api/v1/actors/search?query=Tom&min_popularity=7.5&gender=2&page=1&per_page=20
```

### Actor Filmography
```http
GET /api/v1/actors/{actor_id}/filmography
```

**Path Parameters:**
- `actor_id`: TMDb actor ID

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Results per page (default: 20, max: 100)

### Media Search
```http
GET /api/v1/media/search
```

**Query Parameters:**
- `query` (required): Search term
- `type` (optional): Media type ('movie' or 'tv', default: 'movie')
- `year` (optional): Release year
- `genre_id` (optional): TMDb genre ID
- `min_rating` (optional): Minimum rating (0-10)
- `language` (optional): ISO 639-1 language code
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Results per page (default: 20, max: 100)

**Example:**
```http
GET /api/v1/media/search?query=inception&type=movie&min_rating=8&language=en&page=1
```

### Media Cast
```http
GET /api/v1/media/{media_id}/cast
```

**Path Parameters:**
- `media_id`: TMDb media ID

**Query Parameters:**
- `type` (optional): Media type ('movie' or 'tv', default: 'movie')
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Results per page (default: 20, max: 100)

## Rate Limiting

The API implements rate limiting of 100 requests per minute per IP address. When the rate limit is exceeded, the API will return a 429 status code.

## Caching

Responses are cached for 5 minutes to improve performance and reduce load on the TMDb API. The cache is implemented using Flask-Caching with SimpleCache backend.

## Error Handling

The API returns consistent error responses in the following format:
```json
{
    "error": true,
    "message": "Error description",
    "code": 400
}
```

Common error codes:
- 400: Bad Request (invalid parameters)
- 404: Resource Not Found
- 429: Rate Limit Exceeded
- 500: Internal Server Error

## Environment Variables

- `TMDB_API_KEY` (required): Your TMDb API key
