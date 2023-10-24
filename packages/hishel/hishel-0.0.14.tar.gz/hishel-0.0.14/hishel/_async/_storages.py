import logging
import time
import typing as tp
from pathlib import Path

from httpcore import Request, Response

from hishel._serializers import BaseSerializer

from .._files import AsyncFileManager
from .._serializers import JSONSerializer, Metadata
from .._synchronization import AsyncLock

logger = logging.getLogger("hishel.storages")

__all__ = ("AsyncFileStorage", "AsyncRedisStorage")

try:
    import redis.asyncio as redis
except ImportError:  # pragma: no cover
    redis = None  # type: ignore


class AsyncBaseStorage:
    def __init__(self, serializer: tp.Optional[BaseSerializer] = None) -> None:
        if serializer:  # pragma: no cover
            self._serializer = serializer
        else:
            self._serializer = JSONSerializer()

    async def store(
        self, key: str, response: Response, request: Request, metadata: Metadata
    ) -> None:
        raise NotImplementedError()

    async def retreive(
        self, key: str
    ) -> tp.Optional[tp.Tuple[Response, Request, Metadata]]:
        raise NotImplementedError()

    async def aclose(self) -> None:
        raise NotImplementedError()


class AsyncFileStorage(AsyncBaseStorage):
    """
    A simple file storage.

    :param serializer: Serializer capable of serializing and de-serializing http responses, defaults to None
    :type serializer: tp.Optional[BaseSerializer], optional
    :param base_path: A storage base path where the responses should be saved, defaults to None
    :type base_path: tp.Optional[Path], optional
    :param ttl: Specifies the maximum number of seconds that the response can be cached, defaults to None
    :type ttl: tp.Optional[int], optional
    """

    def __init__(
        self,
        serializer: tp.Optional[BaseSerializer] = None,
        base_path: tp.Optional[Path] = None,
        ttl: tp.Optional[int] = None,
    ) -> None:
        super().__init__(serializer)

        self._base_path = (
            Path(base_path) if base_path is not None else Path(".cache/hishel")
        )

        if not self._base_path.is_dir():
            self._base_path.mkdir(parents=True)

        self._file_manager = AsyncFileManager(is_binary=self._serializer.is_binary)
        self._ttl = ttl
        self._lock = AsyncLock()

    async def store(
        self, key: str, response: Response, request: Request, metadata: Metadata
    ) -> None:
        """
        Stores the response in the cache.

        :param key: Hashed value of concatenated HTTP method and URI
        :type key: str
        :param response: An HTTP response
        :type response: httpcore.Response
        :param request: An HTTP request
        :type request: httpcore.Request
        :param metadata: Additional information about the stored response
        :type metadata: Metadata
        """
        response_path = self._base_path / key

        async with self._lock:
            await self._file_manager.write_to(
                str(response_path),
                self._serializer.dumps(
                    response=response, request=request, metadata=metadata
                ),
            )
        await self._remove_expired_caches()

    async def retreive(
        self, key: str
    ) -> tp.Optional[tp.Tuple[Response, Request, Metadata]]:
        """
        Retreives the response from the cache using his key.

        :param key: Hashed value of concatenated HTTP method and URI
        :type key: str
        :return: An HTTP response and his HTTP request.
        :rtype: tp.Optional[tp.Tuple[Response, Request, Metadata]]
        """

        response_path = self._base_path / key

        async with self._lock:
            if response_path.exists():
                return self._serializer.loads(
                    await self._file_manager.read_from(str(response_path))
                )
        await self._remove_expired_caches()
        return None

    async def aclose(self) -> None:
        return

    async def _remove_expired_caches(self) -> None:
        if self._ttl is None:
            return

        async with self._lock:
            for file in self._base_path.iterdir():
                if file.is_file():
                    age = time.time() - file.stat().st_mtime
                    if age > self._ttl:
                        file.unlink()


class AsyncRedisStorage(AsyncBaseStorage):
    """
    A simple redis storage.

    :param serializer: Serializer capable of serializing and de-serializing http responses, defaults to None
    :type serializer: tp.Optional[BaseSerializer], optional
    :param client: A client for redis, defaults to None
    :type client: tp.Optional["redis.Redis"], optional
    :param ttl: Specifies the maximum number of seconds that the response can be cached, defaults to None
    :type ttl: tp.Optional[int], optional
    """

    def __init__(
        self,
        serializer: tp.Optional[BaseSerializer] = None,
        client: tp.Optional["redis.Redis"] = None,  # type: ignore
        ttl: tp.Optional[int] = None,
    ) -> None:
        if redis is None:  # pragma: no cover
            raise RuntimeError(
                (
                    f"The `{type(self).__name__}` was used, but the required packages were not found. "
                    "Check that you have `Hishel` installed with the `redis` extension as shown.\n"
                    "```pip install hishel[redis]```"
                )
            )
        super().__init__(serializer)

        if client is None:
            self._client = redis.Redis()  # type: ignore
        else:  # pragma: no cover
            self._client = client
        self._ttl = ttl

    async def store(
        self, key: str, response: Response, request: Request, metadata: Metadata
    ) -> None:
        """
        Stores the response in the cache.

        :param key: Hashed value of concatenated HTTP method and URI
        :type key: str
        :param response: An HTTP response
        :type response: httpcore.Response
        :param request: An HTTP request
        :type request: httpcore.Request
        :param metadata: Additioal information about the stored response
        :type metadata: Metadata
        """
        await self._client.set(
            key,
            self._serializer.dumps(
                response=response, request=request, metadata=metadata
            ),
            ex=self._ttl,
        )

    async def retreive(
        self, key: str
    ) -> tp.Optional[tp.Tuple[Response, Request, Metadata]]:
        """
        Retreives the response from the cache using his key.

        :param key: Hashed value of concatenated HTTP method and URI
        :type key: str
        :return: An HTTP response and its HTTP request.
        :rtype: tp.Optional[tp.Tuple[Response, Request, Metadata]]
        """

        cached_response = await self._client.get(key)
        if cached_response is None:
            return None

        return self._serializer.loads(cached_response)

    async def aclose(self) -> None:  # pragma: no cover
        await self._client.close()
