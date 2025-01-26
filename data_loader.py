import aiofiles
import asyncio
import db
import json

from sqlalchemy.ext.asyncio import async_sessionmaker

from test_app.models import User, Profile, Animal
from test_app.utils import hash_password


async def load_from_json(
    async_session: async_sessionmaker,
    file_path: str,
    batch_size: int = 10,
) -> None:
    async with aiofiles.open(file_path, mode="r") as f:
        data = json.loads(await f.read())
    async with async_session() as session:
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            users = []
            for user in batch:
                new_user = User(
                    username=user["username"],
                    password=hash_password(user["password"]),
                )
                if "profile" in user:
                    new_user.profile = Profile(
                        firstname=user["profile"]["firstname"],
                        lastname=user["profile"]["lastname"],
                    )
                if "animals" in user:
                    for animal in user["animals"]:
                        new_user.animals.append(
                            Animal(
                                type=animal["type"],
                                name=animal["name"],
                                age=animal["age"],
                            )
                        )
                users.append(new_user)
            session.add_all(users)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(
        load_from_json(file_path="data_to_import.json", async_session=db.async_session)
    )
