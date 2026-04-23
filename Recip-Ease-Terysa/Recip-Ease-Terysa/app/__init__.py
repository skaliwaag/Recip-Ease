from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.blueprints.recipes import recipes_bp
    from app.blueprints.users import users_bp
    from app.blueprints.meal_plans import meal_plans_bp
    from app.blueprints.reviews import reviews_bp

    app.register_blueprint(recipes_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(meal_plans_bp)
    app.register_blueprint(reviews_bp)

    return app