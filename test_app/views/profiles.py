import db
import json
import jsonschema


from aiohttp import web
from jsonschema import validate
from sqlalchemy import select


from test_app.models import Profile
from test_app.schemas import profile_schema


class ProfileView:
    async def get(self, request) -> web.Response:
        user_id = int(request.match_info["user_id"])
        async with db.async_session() as session:
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalars().first()
            if not profile:
                return web.json_response(
                    {"error": f"profile for user {user_id} not found"}, status=404
                )
            return web.json_response(
                {
                    "profile_id": profile.id,
                    "firstname": profile.firstname,
                    "lastname": profile.lastname,
                    "user_id": profile.user_id,
                }
            )

    async def post(self, request) -> web.Response | None:
        try:
            user_id = int(request.match_info["user_id"])
            data = await request.json()
            validate(instance=data, schema=profile_schema)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except jsonschema.exceptions.ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        new_profile = Profile(
            firstname=data.get("firstname"),
            lastname=data.get("lastname"),
            user_id=user_id,
        )
        async with db.async_session() as session:
            session.add(new_profile)
            await session.commit()
            return web.json_response(
                {"message": f"profile {new_profile.firstname} successfully created!"},
                status=201,
            )

    async def put(self, request) -> web.Response | None:
        try:
            user_id = int(request.match_info["user_id"])
            data = await request.json()
            validate(instance=data, schema=profile_schema)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except jsonschema.exceptions.ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        async with db.async_session() as session:
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalars().first()
            if not profile:
                return web.json_response(
                    {"error": f"profile for user {user_id} not found"}, status=404
                )
            profile.firstname = data.get("firstname")
            profile.lastname = data.get("lastname")
            await session.commit()
            return web.json_response(
                {
                    "id": profile.id,
                    "firstname": profile.firstname,
                    "lastname": profile.lastname,
                }
            )

    async def delete(self, request) -> web.Response | None:
        user_id = int(request.match_info["user_id"])
        async with db.async_session() as session:
            stmt = select(Profile).where(Profile.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalars().first()
            if not profile:
                return web.json_response(
                    {"error": f"profile for user {user_id} not found"}, status=404
                )
            await session.delete(profile)
            await session.commit()
            return web.json_response({"message": "profile deleted"}, status=204)
