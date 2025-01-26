import db
import json
import jsonschema


from aiohttp import web
from jsonschema import validate
import jsonschema.exceptions
from sqlalchemy import select

from test_app.models.user import User
from test_app.schemas import user_schema
from test_app.utils import hash_password


class UserView:
    async def get(self, request) -> web.Response:
        async with db.async_session() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            users = result.scalars().all()
            return web.json_response(
                [
                    {
                        "id": user.id,
                        "username": user.username,
                    }
                    for user in users
                ]
            )

    async def post(self, request) -> web.Response | None:
        try:
            data = await request.json()
            validate(instance=data, schema=user_schema)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except jsonschema.exceptions.ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        async with db.async_session() as session:
            stmt = select(User).where(User.username == data.get("username"))
            result = await session.execute(stmt)
            user_in_db = result.scalars().first()
            if user_in_db:
                return web.json_response(
                    {"error": "username already exists"}, status=400
                )
        new_user = User(
            username=data.get("username"),
            password=hash_password(data.get("password")),
        )
        async with db.async_session() as session:
            session.add(new_user)
            await session.commit()
            return web.json_response(
                {"message": f"user {new_user.username} successfully created!"},
                status=201,
            )

    async def put(self, request) -> web.Response | None:
        try:
            data = await request.json()
            user_id = int(request.match_info["id"])
            validate(instance=data, schema=user_schema)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except jsonschema.exceptions.ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        async with db.async_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return web.json_response({"error": "user not found"}, status=404)
            user.username = data.get("username")
            user.password = data.get("password")
            await session.commit()
            return web.json_response({"id": user.id, "username": user.username})

    async def delete(self, request) -> web.Response | None:
        user_id = int(request.match_info["id"])
        async with db.async_session() as session:
            user = await session.get(User, user_id)
            if not user:
                return web.json_response({"error": "user not found"}, status=404)
            await session.delete(user)
            await session.commit()
            return web.json_response({"message": "user deleted"}, status=204)
