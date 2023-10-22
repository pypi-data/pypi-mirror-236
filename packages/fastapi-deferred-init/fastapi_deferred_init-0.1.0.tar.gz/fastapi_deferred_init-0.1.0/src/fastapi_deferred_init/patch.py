from contextlib import contextmanager

from fastapi import routing

from .routing import DeferringAPIRoute

original_api_route = routing.APIRoute


def patch():
    routing.APIRoute = DeferringAPIRoute


def unpatch():
    routing.APIRoute = original_api_route


@contextmanager
def patch_context():
    patch()
    yield
    unpatch()
