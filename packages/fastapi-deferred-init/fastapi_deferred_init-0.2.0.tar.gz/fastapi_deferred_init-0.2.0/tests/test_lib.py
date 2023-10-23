from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_deferred_init import DeferringAPIRoute, DeferringAPIRouter

from .data.gen_code_ast import create_code
from .helpers import load_code


def test_basic():
    create_code(300)

    generated_code = load_code()

    app = FastAPI()
    router = generated_code.router

    app.include_router(router)

    assert isinstance(router, DeferringAPIRouter)
    client = TestClient(app)
    assert len(app.routes) == 304
    for route in app.routes:
        if route in router.routes:
            assert isinstance(route, DeferringAPIRoute)
        resp = client.get(route.path)
        assert resp.status_code == 200
