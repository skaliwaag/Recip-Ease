from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware


def create_app():
    app = FastAPI(title="Recip-Ease")

    app.add_middleware(SessionMiddleware, secret_key="recip-ease-dev-key")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    from app.blueprints.views import router as views_router
    from app.blueprints.dashboard import router as dashboard_router
    from app.blueprints.recommendations import router as recommendations_router
    from app.blueprints.recipes import router as recipes_router
    from app.blueprints.users import router as users_router
    from app.blueprints.meal_plans import router as meal_plans_router
    from app.blueprints.reviews import router as reviews_router

    app.include_router(views_router)
    app.include_router(dashboard_router)
    app.include_router(recommendations_router)
    app.include_router(recipes_router)
    app.include_router(users_router)
    app.include_router(meal_plans_router)
    app.include_router(reviews_router)

    return app
