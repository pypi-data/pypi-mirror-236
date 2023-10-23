from __future__ import annotations

import typing as t

T = t.TypeVar("T")


class NotPopulated:
    pass


class DeferringProxy(t.Generic[T]):
    __call: t.Callable[[], T]
    __value: T | NotPopulated = NotPopulated()

    def __init__(self, call: t.Callable[[], T]) -> None:
        self.__call = call

    def __get_populated_value(self) -> T:
        if isinstance(self.__value, NotPopulated):
            self.__value = self.__call()
        return self.__value

    def __get__(self, obj, objtype=None) -> T:
        return self.__get_populated_value()

    def __getattr__(self, name: str):
        if name.startswith(f"_{type(self).__name__}__"):
            return object.__getattr__(self, name)  # type: ignore
        return getattr(self.__get_populated_value(), name)

    def __setattr__(self, name: str, value: t.Any):
        if name.startswith(f"_{type(self).__name__}__"):
            return object.__setattr__(self, name, value)
        return setattr(self.__get_populated_value(), name, value)
