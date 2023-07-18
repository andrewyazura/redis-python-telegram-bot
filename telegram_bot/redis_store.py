from collections.abc import MutableMapping
from typing import Any, Iterator, TypeVar

from redis import Redis

from .config import get_settings
from .logging import get_logger

T = TypeVar("T")


logger = get_logger()


class PrefixedMapping(MutableMapping[Any, T]):
    """
    MutableMapping interface for adding a prefix to
    each key in an internal mapping.
    """

    __slots__ = ("_mapping", "_prefixes")

    def __init__(
        self, mapping: MutableMapping[Any, T], prefixes: tuple[Any]
    ) -> None:
        self._mapping = mapping
        self._prefixes = ":".join(str(p) for p in prefixes)

    def _get_key(self, key: str) -> str:
        return f"{self._prefixes}:{key}"

    def __getitem__(self, key: str) -> T:
        return self._mapping[self._get_key(key)]

    def __setitem__(self, key: str, value: T) -> None:
        self._mapping[self._get_key(key)] = value

    def __delitem__(self, key: str) -> None:
        del self._mapping[self._get_key(key)]

    def __len__(self) -> int:
        return len(self._mapping)

    def __iter__(self) -> Iterator:
        return iter(self._mapping)

    def __repr__(self) -> str:
        return f"PrefixedMapping({self._mapping}, {self._prefixes})"


class RedisStore(MutableMapping):
    """
    MutableMapping interface for a Redis database connection.
    """

    __slots__ = ("_store",)

    def __init__(
        self,
        redis_client: "Redis",
        *args,
        **kwargs,
    ) -> None:
        self._store = redis_client
        self.update(*args, **kwargs)

    def __getitem__(self, key: str) -> Any | None:
        value = self._store.get(key)

        if isinstance(value, bytes):
            value = value.decode()

        logger.debug(f"__getitem__({key=}) = {value}")
        return value

    def __setitem__(self, key: str, value: str) -> None:
        self._store.set(key, value)

        logger.debug(f"__setitem__({key=}, {value=})")

    def __delitem__(self, key: str) -> None:
        self._store.delete(key)

        logger.debug(f"__delitem__({key=})")

    def __len__(self) -> int:
        return self._store.dbsize()

    def __iter__(self) -> Iterator:
        return self._store.scan_iter()

    def __repr__(self) -> str:
        return f"RedisStore({repr(self._store)})"


def get_store(redis_db: int) -> RedisStore:
    settings = get_settings()

    return RedisStore(
        Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
            db=redis_db,
        )
    )
