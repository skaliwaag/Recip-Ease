from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    # fallback so sessions still work when running locally without a .env
    app.secret_key = os.getenv("SECRET_KEY", "recip-ease-dev-key")

    # imports go in here instead of the top of the file to avoid circular imports
    # (blueprints import from app.db, which causes a cycle if this is at module level)
    from app.blueprints.recipes import recipes_bp
    from app.blueprints.users import users_bp
    from app.blueprints.meal_plans import meal_plans_bp
    from app.blueprints.reviews import reviews_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.recommendations import recommendations_bp
    from app.blueprints.views import register_routes

    app.register_blueprint(recipes_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(meal_plans_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(recommendations_bp)
    register_routes(app)

    return app
