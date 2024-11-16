from flask import Flask, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask extensions
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    cache.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'error': True,
            'message': 'Resource not found',
            'code': 404
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': True,
            'message': 'Internal server error',
            'code': 500
        }), 500

    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'TMDb API service is running'
        })

    return app
