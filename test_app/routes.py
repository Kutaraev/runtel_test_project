from aiohttp.web import Application

from test_app.views import UserView, ProfileView, AnimalView


def setup_routes(app: Application) -> None:
    user_view = UserView()
    profile_view = ProfileView()
    animal_view = AnimalView()

    app.router.add_get("/users", user_view.get)
    app.router.add_post("/users", user_view.post)
    app.router.add_put("/users/{id}", user_view.put)
    app.router.add_delete("/users/{id}", user_view.delete)

    app.router.add_get("/users/{user_id}/profile", profile_view.get)
    app.router.add_post("/users/{user_id}/profile", profile_view.post)
    app.router.add_put("/users/{user_id}/profile", profile_view.put)
    app.router.add_delete("/users/{user_id}/profile", profile_view.delete)

    app.router.add_get("/users/{user_id}/animals", animal_view.get)
    app.router.add_post("/users/{user_id}/animals", animal_view.post)
    app.router.add_put("/users/{user_id}/animals/{animal_id}", animal_view.put)
    app.router.add_delete("/users/{user_id}/animals/{animal_id}", animal_view.delete)
