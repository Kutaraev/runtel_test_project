import db
import json
import jsonschema

from aiohttp import web
from jsonschema import validate
from sqlalchemy import select


from test_app.models import Animal
from test_app.schemas import animal_schema


class AnimalView:
    async def get(self, request) -> web.Response:
        user_id = int(request.match_info["user_id"])
        async with db.async_session() as session:
            stmt = select(Animal).where(Animal.user_id == user_id)
            result = await session.execute(stmt)
            animals = result.scalars().all()
            return web.json_response(
                [
                    {
                        "id": animal.id,
                        "type": animal.type,
                        "name": animal.name,
                        "age": animal.age,
                    }
                    for animal in animals
                ]
            )

    async def post(self, request) -> web.Response | None:
        try:
            user_id = int(request.match_info["user_id"])
            data = await request.json()
            validate(instance=data, schema=animal_schema)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except jsonschema.exceptions.ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        new_animal = Animal(
            type=data.get("type"),
            name=data.get("name"),
            age=data.get("age"),
            user_id=user_id,
        )
        async with db.async_session() as session:
            session.add(new_animal)
            await session.commit()
            return web.json_response(
                {"message": f"animal {new_animal.name} successfully created!"},
                status=201,
            )

    async def put(self, request) -> web.Response | None:
        try:
            user_id = int(request.match_info["user_id"])
            animal_id = int(request.match_info["animal_id"])
            data = await request.json()
            validate(instance=data, schema=animal_schema)
        except json.JSONDecodeError:
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except jsonschema.exceptions.ValidationError as e:
            return web.json_response({"error": str(e)}, status=400)

        async with db.async_session() as session:
            stmt = (
                select(Animal)
                .where(Animal.user_id == user_id)
                .where(Animal.id == animal_id)
            )
            result = await session.execute(stmt)
            animal = result.scalars().first()
            if not animal:
                return web.json_response(
                    {"error": f"animal {animal_id} for user {user_id} not found"},
                    status=404,
                )
            animal.type = data.get("type")
            animal.name = data.get("name")
            animal.age = data.get("age")
            await session.commit()
            return web.json_response(
                {
                    "type": animal.type,
                    "name": animal.name,
                    "age": animal.age,
                }
            )

    async def delete(self, request) -> web.Response | None:
        user_id = int(request.match_info["user_id"])
        animal_id = int(request.match_info["animal_id"])
        async with db.async_session() as session:
            stmt = (
                select(Animal)
                .where(Animal.user_id == user_id)
                .where(Animal.id == animal_id)
            )
            result = await session.execute(stmt)
            animal = result.scalars().first()
            if not animal:
                return web.json_response(
                    {"error": f"animal {animal_id} for user {user_id} not found"},
                    status=404,
                )
            await session.delete(animal)
            await session.commit()
            return web.json_response({"message": "animal deleted"}, status=204)
