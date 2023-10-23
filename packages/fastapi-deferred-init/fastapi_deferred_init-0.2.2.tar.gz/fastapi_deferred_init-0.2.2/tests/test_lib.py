from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from fastapi_deferred_init import DeferringAPIRoute, DeferringAPIRouter

from .data.gen_code_ast import create_code
from .helpers import load_code


def test_basic():
    create_code(50, True)  # switch bool to compare

    generated_code = load_code()

    app = FastAPI()
    router = generated_code.router

    app.include_router(router)

    assert isinstance(router, DeferringAPIRouter)
    client = TestClient(app)
    assert len(app.routes) == 54
    for route in app.routes:
        if route in router.routes:
            assert isinstance(route, DeferringAPIRoute)
        resp = client.get(route.path)
        assert resp.status_code == 200


def test_with_pydantic_model():
    app = FastAPI()
    router = DeferringAPIRouter()

    class Login(BaseModel):
        username: str
        password: str

    @router.post("/login")
    async def do_login(json: Login):
        assert isinstance(json, Login)
        assert isinstance(json.username, str)
        assert isinstance(json.password, str)

        return {"userdata": "[...]"}

    app.include_router(router)

    client = TestClient(app)

    resp = client.post("/login", json={"username": "jvllmr", "password": "password"})
    assert resp.status_code == 200
