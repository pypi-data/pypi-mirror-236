from __future__ import annotations

import inspect
import typing as t
from enum import Enum, IntEnum
from typing import Any, Callable, Sequence

from fastapi import params, routing
from fastapi._compat import ModelField, lenient_issubclass
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.dependencies.utils import (
    get_body_field,
    get_dependant,
    get_parameterless_sub_dependant,
    get_typed_return_annotation,
)
from fastapi.responses import JSONResponse, Response
from fastapi.routing import APIRoute
from fastapi.types import IncEx
from fastapi.utils import (
    create_cloned_field,
    create_response_field,
    generate_unique_id,
    is_body_allowed_for_status_code,
)
from starlette.routing import BaseRoute, compile_path, get_name, request_response
from starlette.types import ASGIApp, Lifespan

from .lib import DeferringProxy


def get_route_dependant(route: routing.APIRoute, *args, **kwargs):
    dependant = get_dependant(*args, **kwargs)
    for depends in route.dependencies[::-1]:
        route.dependant.dependencies.insert(
            0,
            get_parameterless_sub_dependant(depends=depends, path=route.path_format),
        )
    return dependant


class DeferringAPIRoute(routing.APIRoute):
    def __init__(
        self,
        path: str,
        endpoint: t.Callable[..., t.Any],
        *,
        response_model: t.Any = Default(None),
        status_code: t.Optional[int] = None,
        tags: t.Optional[t.List[t.Union[str, Enum]]] = None,
        dependencies: t.Optional[t.Sequence[params.Depends]] = None,
        summary: t.Optional[str] = None,
        description: t.Optional[str] = None,
        response_description: str = "Successful Response",
        responses: t.Optional[t.Dict[t.Union[int, str], t.Dict[str, t.Any]]] = None,
        deprecated: t.Optional[bool] = None,
        name: t.Optional[str] = None,
        methods: t.Optional[t.Union[t.Set[str], t.List[str]]] = None,
        operation_id: t.Optional[str] = None,
        response_model_include: t.Optional[IncEx] = None,
        response_model_exclude: t.Optional[IncEx] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: t.Union[t.Type[Response], DefaultPlaceholder] = Default(
            JSONResponse
        ),
        dependency_overrides_provider: t.Optional[t.Any] = None,
        callbacks: t.Optional[t.List[routing.BaseRoute]] = None,
        openapi_extra: t.Optional[t.Dict[str, t.Any]] = None,
        generate_unique_id_function: t.Union[
            t.Callable[[routing.APIRoute], str], DefaultPlaceholder
        ] = Default(generate_unique_id),
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        if isinstance(response_model, DefaultPlaceholder):
            return_annotation = get_typed_return_annotation(endpoint)
            if lenient_issubclass(return_annotation, Response):
                response_model = None
            else:
                response_model = return_annotation
        self.response_model = response_model
        self.summary = summary
        self.response_description = response_description
        self.deprecated = deprecated
        self.operation_id = operation_id
        self.response_model_include = response_model_include
        self.response_model_exclude = response_model_exclude
        self.response_model_by_alias = response_model_by_alias
        self.response_model_exclude_unset = response_model_exclude_unset
        self.response_model_exclude_defaults = response_model_exclude_defaults
        self.response_model_exclude_none = response_model_exclude_none
        self.include_in_schema = include_in_schema
        self.response_class = response_class
        self.dependency_overrides_provider = dependency_overrides_provider
        self.callbacks = callbacks
        self.openapi_extra = openapi_extra
        self.generate_unique_id_function = generate_unique_id_function
        self.tags = tags or []
        self.responses = responses or {}
        self.name = get_name(endpoint) if name is None else name
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        if methods is None:
            methods = ["GET"]
        self.methods: t.Set[str] = {method.upper() for method in methods}
        if isinstance(generate_unique_id_function, DefaultPlaceholder):
            current_generate_unique_id: t.Callable[
                [routing.APIRoute], str
            ] = generate_unique_id_function.value
        else:
            current_generate_unique_id = generate_unique_id_function
        self.unique_id = self.operation_id or current_generate_unique_id(self)
        # normalize enums e.g. http.HTTPStatus
        if isinstance(status_code, IntEnum):
            status_code = int(status_code)
        self.status_code = status_code
        if self.response_model:
            assert is_body_allowed_for_status_code(
                status_code
            ), f"Status code {status_code} must not have a response body"
            response_name = "Response_" + self.unique_id
            self.response_field = DeferringProxy(
                lambda: create_response_field(  # type: ignore
                    name=response_name,
                    type_=self.response_model,
                    mode="serialization",
                )
            )
            # Create a clone of the field, so that a Pydantic submodel is not returned
            # as is just because it's an instance of a subclass of a more limited class
            # e.g. UserInDB (containing hashed_password) could be a subclass of User
            # that doesn't have the hashed_password. But because it's a subclass, it
            # would pass the validation and be returned as is.
            # By being a new field, no inheritance will be passed as is. A new model
            # will always be created.
            # TODO: remove when deprecating Pydantic v1
            self.secure_cloned_response_field: t.Optional[ModelField] = DeferringProxy(
                lambda: create_cloned_field(self.response_field)
            )  # type: ignore
        else:
            self.response_field = None  # type: ignore
            self.secure_cloned_response_field = None
        self.dependencies = list(dependencies or [])
        self.description = description or inspect.cleandoc(self.endpoint.__doc__ or "")
        # if a "form feed" character (page break) is found in the description text,
        # truncate description text to the content preceding the first "form feed"
        self.description = self.description.split("\f")[0].strip()
        response_fields = {}
        for additional_status_code, response in self.responses.items():
            assert isinstance(response, dict), "An additional response must be a dict"
            model = response.get("model")
            if model:
                assert is_body_allowed_for_status_code(
                    additional_status_code
                ), f"Status code {additional_status_code} must not have a response body"
                response_name = f"Response_{additional_status_code}_{self.unique_id}"
                response_field = DeferringProxy(lambda: create_response_field(name=response_name, type_=model))  # type: ignore
                response_fields[additional_status_code] = response_field
        if response_fields:
            self.response_fields: t.Dict[t.Union[int, str], ModelField] = response_fields  # type: ignore
        else:
            self.response_fields = {}

        assert callable(endpoint), "An endpoint must be a callable"
        self.dependant = DeferringProxy(
            lambda: get_route_dependant(  # type: ignore
                self, path=self.path_format, call=self.endpoint
            )
        )

        self.body_field = DeferringProxy(lambda: get_body_field(dependant=self.dependant, name=self.unique_id))  # type: ignore
        self.app = DeferringProxy(lambda: request_response(self.get_route_handler()))  # type: ignore

    def __getattribute__(self, name: str):
        obj = object.__getattribute__(self, name)
        if hasattr(obj, "__get__"):
            return obj.__get__(self, type(self))
        return obj


class DeferringAPIRouter(routing.APIRouter):
    def __init__(
        self,
        *,
        prefix: str = "",
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[params.Depends] | None = None,
        default_response_class: type[Response] = Default(JSONResponse),
        responses: dict[int | str, dict[str, Any]] | None = None,
        callbacks: list[BaseRoute] | None = None,
        routes: list[BaseRoute] | None = None,
        redirect_slashes: bool = True,
        default: ASGIApp | None = None,
        dependency_overrides_provider: Any | None = None,
        route_class: type[APIRoute] = DeferringAPIRoute,
        on_startup: Sequence[Callable[[], Any]] | None = None,
        on_shutdown: Sequence[Callable[[], Any]] | None = None,
        lifespan: Lifespan[Any] | None = None,
        deprecated: bool | None = None,
        include_in_schema: bool = True,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            lifespan=lifespan,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            generate_unique_id_function=generate_unique_id_function,
        )
