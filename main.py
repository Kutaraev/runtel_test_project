import asyncio
from aiohttp import web
from aiohttp.web import Application

from test_app.routes import setup_routes


async def init_app() -> Application:
    app = Application()
    setup_routes(app=app)
    return app


if __name__ == "__main__":
    app = asyncio.run(init_app())
    web.run_app(app)
