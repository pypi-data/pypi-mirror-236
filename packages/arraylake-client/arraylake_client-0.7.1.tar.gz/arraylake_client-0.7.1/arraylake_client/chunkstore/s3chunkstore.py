import asyncio
import importlib
import weakref
from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Deque, Dict, Mapping, Optional, Set, Tuple
from urllib.parse import urlparse

import aiobotocore.client
import aiobotocore.session
import numpy as np
from aiobotocore.config import AioConfig
from botocore import UNSIGNED

from arraylake_client.asyn import close_async_context, get_loop, sync
from arraylake_client.chunkstore.abc import Chunkstore
from arraylake_client.config import config
from arraylake_client.log_util import get_logger
from arraylake_client.types import ChunkHash, ReferenceData

logger = get_logger(__name__)


# Below we set up a global cache for aiobotocore clients
# There should be one per each event loop and set of configuration parameters
# dicts aren't hashable, so we sort the keywords into key / value pairs
@dataclass(eq=True, frozen=True)
class ClientKey:
    loop: asyncio.AbstractEventLoop
    service_name: str
    client_kwargs: Tuple[Tuple[str, str], ...]


# tried making these weakref.WeakValueDictionary(), but they were getting garbage collected too early
# TODO: investigate whether use of weakref would be more efficient here
# As is, the clients are cleaned up at the end of the python interpreter session.
_GLOBAL_CLIENTS: Dict[ClientKey, aiobotocore.client.AioBaseClient] = {}

# this is a cache to use hold asyncio tasks so they are not garbage collected before finishing
background_tasks: Set[asyncio.Task] = set()


async def get_client(loop: asyncio.AbstractEventLoop, service_name: str, **client_kws) -> aiobotocore.client.AioBaseClient:
    """
    Attempt to get an aws client for a specific event loop and set of parameters.
    If the client already exists, the global cache will be used.
    If not, a new client will be created.
    """

    key = ClientKey(loop, service_name, tuple(sorted(client_kws.items())))
    logger.debug("%d s3 clients present in cache.", len(_GLOBAL_CLIENTS))
    if key not in _GLOBAL_CLIENTS:
        logger.debug("Creating new s3 client %s. Loop id %s.", key, id(loop))
        anon = client_kws.pop("anon", False)
        if anon:
            client_kws["config"] = AioConfig(signature_version=UNSIGNED)
        client_creator = aiobotocore.session.get_session().create_client(service_name, **client_kws)
        new_client = await client_creator.__aenter__()
        weakref.finalize(new_client, close_client, key)
        _GLOBAL_CLIENTS[key] = new_client
    else:
        logger.debug("Client %s already present. Loop id %s.", key, id(loop))
    return _GLOBAL_CLIENTS[key]


def close_client(key: ClientKey) -> None:
    """
    This is a finalizer function that is called when a global client is
    garbage collected. It cleanly closes the client for the specified key.

    If the event loop associated with this client is already closed, we can't
    call __aexit__. So we attempt to directly close the TCP Socket associated
    with the aiohttp session.

    If the event loop associated with this client is determined to be the
    dedicated io loop, we call `sync` to on __aexit__.

    If the event loop associated with this client is determined to be the currently
    running event loop, we schedule the __aexit__ coroutine for execution.

    If the event loop doesn't match any of these scenarios, we have no way to call
    the closer function and issue a RuntimeWarning

    Note: logging in this function runs the risk of conflicting with pytest#5502. For
    this reason, we have removed debug log statements.
    """
    client = _GLOBAL_CLIENTS.pop(key)

    client_loop = key.loop  # the loop this client was created from

    # this is the underlying thing we have to close
    aio_http_session = client._endpoint.http_session._session
    # sanity checks
    # assert aio_http_session._loop is client_loop
    # assert aio_http_session._connector._loop is client_loop

    if aio_http_session.closed:
        return

    sync_loop = get_loop()  # the loop associated with the synchronizer thread

    try:
        running_loop = asyncio.get_running_loop()
    except RuntimeError:
        running_loop = None

    if client_loop.is_closed():
        # we can never talk to this client again because its loop is closed;
        # just close the sockets directly
        aio_http_session._connector._close()
        assert aio_http_session.closed
    else:
        # client loop is still open -- how can we talk to it?
        if client_loop is sync_loop:
            sync(close_async_context, client, "calling from sync", timeout=1)
        elif client_loop is running_loop:
            coro = close_async_context(client, "closing from loop {}".format(id(client_loop)))
            if client_loop.is_running():
                task = client_loop.create_task(coro)
                # try to prevent this task from being garbage collected before it finishes
                background_tasks.add(task)
            else:
                client_loop.run_until_complete(coro)


class HashValidationError(AssertionError):
    pass


def tokenize(data: bytes, *, hasher: Callable) -> str:
    hash_obj = hasher(data)
    return hash_obj.hexdigest()


@lru_cache(maxsize=None)
def get_hasher(method):
    try:
        mod_name, func_name = method.rsplit(".", 1)
        mod = importlib.import_module(mod_name)
        return getattr(mod, func_name)
    except (ImportError, AttributeError):
        raise ValueError(f"invalid hash method {method}")


class S3Chunkstore(Chunkstore):
    """S3Chunkstore interface"""

    uri: str
    client_kws: Mapping[str, str]
    _OPEN: bool
    _session_client: Optional[aiobotocore.client.AioBaseClient]
    _known_key_cache: Optional[Deque]

    def __init__(self, uri: str, **client_kws):
        """
        Args:
            uri: Address of chunk store service. For example: ``s3://chunkstore``.
            client_kws: Additional keyword arguments to pass to
                ``aiobotocore.session.AIOSession.session.create_client``, by default None.
        """
        if not uri.startswith("s3://"):
            raise ValueError("Chunkstore uri must be a s3 path")
        self.uri = uri
        self.client_kws = client_kws
        self._set_props()
        self._setup_chunk_key_cache()

    def _set_props(self):
        parsed_uri = urlparse(self.uri)
        self._service_name = parsed_uri.scheme
        self._bucket = parsed_uri.netloc
        self._path = parsed_uri.path.lstrip("/")
        self._session_client = None

    def __getstate__(self):
        return self.uri, self.client_kws

    def __setstate__(self, state):
        self.uri, self.client_kws = state
        self._set_props()
        self._setup_chunk_key_cache()

    async def _open(self):
        if self._session_client is not None:
            return
        loop = asyncio.get_running_loop()
        self._session_client = await get_client(loop, self._service_name, **self.client_kws)

    def _setup_chunk_key_cache(self):
        self._known_key_cache = deque(maxlen=5000)  # tunable

    def __repr__(self):
        status = "OPEN" if self._session_client is not None else "CLOSED"
        return f"<arraylake_client.s3_chunkstore.S3Chunkstore uri='{self.uri}' status={status}>"

    async def ping(self):
        await self._open()
        """Check if the chunk store bucket exists."""
        # Should raise an exception if the bucket does not exist
        await self._session_client.head_bucket(Bucket=self._bucket)

    async def add_chunk(self, data: bytes, *, hash_method: str = None) -> ReferenceData:
        await self._open()
        if isinstance(data, np.ndarray):
            # We land here if the data are not compressed by a codec. This happens for 0d arrays automatically.
            data = data.tobytes()

        if hash_method is None:
            hash_method = config.get("chunkstore.hash_method", "hashlib.sha256")

        hasher = get_hasher(hash_method)

        token = tokenize(data, hasher=hasher)
        key = f"{self._path}{token}"

        uri = f"{self._service_name}://{self._bucket}/{key}"
        length = len(data)
        chunk_ref = ReferenceData(uri=uri, offset=0, length=length, hash=ChunkHash(method=hash_method, token=token))

        if token not in self._known_key_cache:
            resp = await self._session_client.put_object(Bucket=self._bucket, Key=key, Body=data)
            self._known_key_cache.append(token)
            logger.debug(resp)

        return chunk_ref

    async def get_chunk(self, chunk_ref: ReferenceData, *, validate: bool = False) -> bytes:
        await self._open()
        logger.debug("get_chunk %s", chunk_ref)

        parsed_uri = urlparse(chunk_ref.uri)
        key = parsed_uri.path.strip("/")
        bucket = parsed_uri.netloc

        start_byte = chunk_ref.offset
        # stop_byte is inclusive, in contrast to python indexing conventions
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Range
        stop_byte = chunk_ref.offset + chunk_ref.length - 1
        byte_range = f"bytes={start_byte}-{stop_byte}"
        response = await self._session_client.get_object(Bucket=bucket, Key=key, Range=byte_range)
        logger.debug(response)
        async with response["Body"] as stream:
            data = await stream.read()

        if validate:
            hasher = get_hasher(chunk_ref.hash["method"])
            h = tokenize(data, hasher=hasher)
            if h != chunk_ref.hash["token"]:
                raise HashValidationError(f"hashes did not match for key: {key}")

        return data
