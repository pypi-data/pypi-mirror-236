import contextvars
import contextlib
import functools
from typing import (
    TypeVar,
    ParamSpec,
    Callable,
    Any,
    cast,
    Generator,
    Awaitable,
    Protocol,
    Hashable,
)


P = ParamSpec("P")
T = TypeVar("T")


class ContextVarAlreadyAssignedToCache(Exception):
    ...


class NestedCaching(Exception):
    ...


class Cache(Protocol):
    def get(self, key: Hashable) -> tuple[bool, Any]:
        """
        Get a value by key from the cache.
        Returns a tuple of (hit, value).
        """
        ...

    def set(self, key: Hashable, value: Any) -> None:
        """
        Set a value by key in the cache.
        """
        ...


class DictCache:
    def __init__(self) -> None:
        self._cache: dict[Hashable, Any] = {}

    def get(self, key: Hashable) -> tuple[bool, Any]:
        try:
            value = self._cache[key]
            return True, value
        except KeyError:
            return False, None

    def set(self, key: Hashable, value: Any) -> None:
        self._cache[key] = value


CacheContextVar = contextvars.ContextVar[Cache | None]

_registry: dict[Callable[..., Any], CacheContextVar] = {}


def enable_caching(
    contextvar: CacheContextVar,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    if contextvar in set(_registry.values()):
        raise ContextVarAlreadyAssignedToCache

    def decorator(f: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = (*args, *sorted(kwargs.items()))
            cache = contextvar.get()
            if cache is not None:
                hit, value = cache.get(cache_key)
                if hit:
                    return cast(T, value)
            result = f(*args, **kwargs)
            if cache is not None:
                cache.set(cache_key, result)
            return result

        _registry[wrapper] = contextvar
        return wrapper

    return decorator


def async_enable_caching(
    contextvar: CacheContextVar,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    if contextvar in set(_registry.values()):
        raise ContextVarAlreadyAssignedToCache

    def decorator(f: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        @functools.wraps(f)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = (*args, *[(k, v) for k, v in kwargs.items()])
            cache = contextvar.get()
            if cache is not None:
                hit, value = cache.get(cache_key)
                if hit:
                    return cast(T, value)
            result = await f(*args, **kwargs)
            if cache is not None:
                cache.set(cache_key, result)
            return result

        _registry[wrapper] = contextvar
        return wrapper

    return decorator


@contextlib.contextmanager
def use_caching(
    f: Callable[..., Any],
    *,
    cache_factory: Callable[[], Cache] = lambda: DictCache(),
    # Is this call to `use_caching` allowed to be nested within another `use_caching` call.
    # If nested within a parent `use_caching` the `cache_factory` will be ignored.
    allow_nested: bool = False,
) -> Generator[None, None, None]:
    contextvar = _registry[f]
    if contextvar.get() is not None:
        if allow_nested:
            yield
            return
        else:
            raise NestedCaching
    contextvar.set(cache_factory())
    try:
        yield
    finally:
        contextvar.set(None)
