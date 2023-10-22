# fastapi-deferring-init

> **WARNING**: This is the very first draft of this project and might not work at all. I only published it to test it in bigger projects of mine.

## The Problem

When using nested routers in a FastAPI project its start-up time can get long quite fast.
That is because every router re-calculates the routes defined by a nested router when including it and the pre-calculated values by the nested router never gets used.

## The Solution

This library provides a modified APIRoute that defers the calculation of values to the first actual attribute access. This also applies to the top-level router, which means that the route is only fully initialized when an API Endpoint is accessed the first time. Utilities for quickly monkey-patching an existing FastAPI application are also provided.
