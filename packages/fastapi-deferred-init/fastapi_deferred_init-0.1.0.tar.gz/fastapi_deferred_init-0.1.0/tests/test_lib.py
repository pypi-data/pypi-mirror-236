from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_deferred_init import patch

from .data.gen_code_ast import create_dependency
from .helpers import load_code


def test_patched():
    create_dependency(300)
    patch()
    generated_code = load_code()

    app = FastAPI()

    app.include_router(generated_code.router)
    client = TestClient(app)

    for route in app.routes:
        resp = client.get(route.path)
        assert resp.status_code == 200
