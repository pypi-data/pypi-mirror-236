import attr

from abc import ABC, abstractmethod
from enum import Enum, auto
from math import log2
from typing import Generic, TypeVar, Sequence, Union, Optional, Mapping, Callable, AsyncIterable, Awaitable, Any

import dag_cbor
from multiformats import CID, multicodec, multihash

from hamt_sharding import HAMTBucket
from hamt_sharding.buckets import HAMTBucketPosition

from .content import _CONTENT_EXPORTERS, ExportedContent
from .ipfs_unix_fs.unix_fs import UnixFS, FSType
from .ipfs_dag_pb.dag_pb import PBNode, PBLink

T = TypeVar('T')

class ResolveException(Exception): pass

class BlockStore(ABC):
    @abstractmethod
    async def get_block(self, cid: CID) -> bytes:
        pass

async def _iterable_to_async_iterable(x: Sequence[T]) -> AsyncIterable[T]:
    for y in x:
        yield y

class Exportable(ABC, Generic[T]):
    def __init__(self, 
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 node: Union[PBNode, bytes],
                 content: AsyncIterable[T]):
        self.name = name
        self.path = path
        self.cid = cid
        self.depth = depth
        self.size = size
        self.content = content
        self.node = node
    
class FSExportable(Exportable[T]):
    def __init__(self,
                 unix_fs: UnixFS,
                 node: PBNode,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[T]):
        Exportable.__init__(self, name, path, cid, depth, size, node, content)
        self.unix_fs = unix_fs

class UnixFSFile(FSExportable[bytes]):
    def __init__(self,
                 unix_fs: UnixFS,
                 node: PBNode,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[bytes]):
        FSExportable.__init__(self, unix_fs, node, name, path, cid, depth, size, content)

class UnixFSDirectory(FSExportable[Exportable[Any]]):
    def __init__(self,
                 unix_fs: UnixFS,
                 node: PBNode,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[Exportable[Any]]):
        FSExportable.__init__(self, unix_fs, node, name, path, cid, depth, size, content)

class BinaryExportable(FSExportable[T]):
    def __init__(self,
                 node: bytes,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[T]):
        Exportable.__init__(self, name, path, cid, depth, size, node, content)

class ObjectNode(BinaryExportable[object]):
    def __init__(self,
                 node: bytes,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[object]):
        BinaryExportable.__init__(self, node, name, path, cid, depth, size, content)

class RawNode(BinaryExportable[bytes]):
    def __init__(self,
                 node: bytes,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[bytes]):
        BinaryExportable.__init__(self, node, name, path, cid, depth, size, content)

class IdentityNode(BinaryExportable[bytes]):
    def __init__(self,
                 node: bytes,
                 name: str,
                 path: str,
                 cid: CID,
                 depth: int,
                 size: int,
                 content: AsyncIterable[bytes]):
        BinaryExportable.__init__(self, node, name, path, cid, depth, size, content)

@attr.define(slots=True)
class NextResult:
    cid: CID
    name: str
    path: str
    to_resolve: Sequence[str]

@attr.define(slots=True)
class ResolveResult():
    entry: Exportable[Any]
    next: Optional[NextResult]
    
Resolver = Callable[[CID, str, str, Sequence[str], int, BlockStore], Awaitable[ResolveResult]]

async def resolve_raw(cid: CID, name: str, path: str, to_resolve: Sequence[str], depth: int, block_store: BlockStore) -> ResolveResult:
    if len(to_resolve) > 0:
        raise ResolveException(f'no link named {path} found in raw node {cid}')
    block = await block_store.get_block(cid)
    return ResolveResult(
        entry=RawNode(
            node=block,
            name=name,
            path=path,
            cid=cid,
            depth=depth,
            size=len(block),
            content=_iterable_to_async_iterable([block])
        ),
        next=None
    )
        
async def resolve_identity(cid: CID, name: str, path: str, to_resolve: Sequence[str], depth: int, block_store: BlockStore) -> ResolveResult:
    if len(to_resolve) > 0:
        raise ResolveException(f'no link named {path} found in identity node {cid}')
    block = await block_store.get_block(cid)
    return ResolveResult(
        entry=IdentityNode(
            node=block,
            name=name,
            path=path,
            cid=cid,
            depth=depth,
            size=len(block),
            content=_iterable_to_async_iterable([block])
        ),
        next=None
    )

async def resolve_dag_cbor(cid: CID, name: str, path: str, to_resolve: Sequence[str], depth: int, block_store: BlockStore) -> ResolveResult:
    block = await block_store.get_block(cid)
    obj = dag_cbor.decode(block)
    sub_obj = obj
    sub_path = path

    while len(to_resolve) > 0:
        prop = to_resolve[0]
        assert isinstance(sub_obj, Mapping)
        if prop in sub_obj:
            sub_path = f'{sub_path}/{prop}'
            if prop not in sub_obj:
                sub_obj_cid = None
            else:
                raw_cid = sub_obj[prop]
                assert isinstance(raw_cid, (bytes, str))
                sub_obj_cid = CID.decode(raw_cid)
            if sub_obj_cid is not None:
                return ResolveResult(
                    entry=ObjectNode(
                        block,
                        name,
                        path,
                        cid,
                        depth,
                        len(block),
                        _iterable_to_async_iterable([obj]),
                    ),
                    next=NextResult(
                        cid=sub_obj_cid,
                        name=prop,
                        path=sub_path,
                        to_resolve=to_resolve[1:],
                    )
                )
            sub_obj = sub_obj[prop]
        else:
            raise ResolveException(f'no property named {prop} in cbor node {cid}')
        
    return ResolveResult(
        entry=ObjectNode(
            block,
            name,
            path,
            cid,
            depth,
            len(block),
            _iterable_to_async_iterable([obj]),
        ),
        next=None
    )

@attr.define(slots=True)
class _ShardTraversalContext:
    hamt_depth: int
    root_bucket: HAMTBucket[str, bool]
    last_bucket: HAMTBucket[str, bool]

def _pad_length(bucket: HAMTBucket[str, bool]) -> int:
    return len(hex(bucket.table_size - 1)[2:])

def _add_links_to_hamt_bucket(links: Sequence[PBLink], bucket: HAMTBucket[str, bool], root_bucket: HAMTBucket[str, bool]) -> None:
    pad_length = _pad_length(bucket)
    for link in links:
        if len(link.name) == pad_length:
            pos = int(link.name, 16)
            bucket._put_object_at(pos, HAMTBucket[str, bool](root_bucket._bits, root_bucket._infinite_wrapper))
        else:
            root_bucket[link.name[:2]] = True

def _to_prefix(position: int, pad_length: int) -> str:
    return hex(position)[2:].upper().zfill(pad_length)[:pad_length]

def _to_bucket_path(position: HAMTBucketPosition[str, bool]) -> Sequence[HAMTBucket[str, bool]]:
    bucket = position.bucket
    path = []
    while bucket._parent is not None:
        path.append(bucket)
        bucket = bucket._parent
    path.append(bucket)
    return path[::-1]

async def _find_shard_cid(node: PBNode, name: str, block_store: BlockStore, context: Optional[_ShardTraversalContext] = None) -> Optional[CID]:
    if context is None:
        if not node.data:
            raise ResolveException('no data in shard node')
        unix_fs = UnixFS.unmarshal(node.data)
        if unix_fs.fs_type != FSType.HAMTSHARD:
            raise ResolveException(f'not an HAMT sharded directory (is {unix_fs.fs_type})')
        if unix_fs.fanout == 0:
            raise ResolveException('not a valid fanout')

        def _hash_fn(buf: bytes) -> bytes:
            # TODO: Remove this once multihash gets fixed
            if unix_fs.hash_type == 0x22:
                from multiformats.multihash._hashfuns.murmur3 import _murmur3
                return _murmur3('x64', 64)(buf)
            mh = multihash.get(code=unix_fs.hash_type)
            assert mh
            return mh.digest(buf)

        log_2 = log2(unix_fs.fanout)
        if not log_2.is_integer():
            raise ResolveException(f'fanout should be an exponent of 2 (is {unix_fs.fanout})')
        root_bucket = HAMTBucket[str, bool].create_hamt(_hash_fn, int(log_2))
        context = _ShardTraversalContext(1, root_bucket, root_bucket)

    pad_length = _pad_length(context.last_bucket)
    _add_links_to_hamt_bucket(node.links, context.last_bucket, context.root_bucket)
    position = context.root_bucket._find_new_bucket_and_pos(name)
    prefix = _to_prefix(position.pos, pad_length)
    bucket_path = _to_bucket_path(position)
    if len(bucket_path) > context.hamt_depth:
        context.last_bucket = bucket_path[context.hamt_depth]
        prefix = _to_prefix(context.last_bucket._pos_at_parent, pad_length)

    def predicate(link: PBLink) -> bool:
        entry_prefix = link.name[:pad_length]
        entry_name = link.name[pad_length:]
        if entry_prefix != prefix:
            return False
        if entry_name != '' and entry_name != name:
            return False
        return True

    link = next(filter(predicate, node.links), None)
    if link is None: return None
    if link.name[pad_length:] == name:
        return link.cid
    
    context.hamt_depth += 1
    block = await block_store.get_block(link.cid)
    node = PBNode.decode(block)
    return await _find_shard_cid(node, name, block_store, context)

async def resolve_dag_pb(cid: CID, name: str, path: str, to_resolve: Sequence[str], depth: int, block_store: BlockStore) -> ResolveResult:
    block = await block_store.get_block(cid)
    node = PBNode.decode(block)

    name = name or cid.encode()
    path = path or name

    unix_fs = UnixFS.unmarshal(node.data)
    next_result = None

    if len(to_resolve) > 0:
        link_cid = None
        if unix_fs.fs_type == FSType.HAMTSHARD:
            link_cid = await _find_shard_cid(node, to_resolve[0], block_store)
        else:
            link = next(filter(lambda x: x.name == name, node.links), None)
            if link is not None:
                link_cid = link.cid
        if link_cid is None:
            raise ResolveException('file does not exist')

        next_name = to_resolve[0]
        next_path = f'{path}/{next_name}'

        next_result = NextResult(
            link_cid,
            next_name or '',
            next_path,
            to_resolve[1:],
        )

    content = _CONTENT_EXPORTERS[unix_fs.fs_type](cid, node, unix_fs, path, depth, block_store, resolve)
    if unix_fs.is_dir():

        async def validate_directory_results(content: AsyncIterable[ExportedContent]) -> AsyncIterable[Exportable[Any]]:
            async for block in content:
                assert isinstance(block, Exportable)
                yield block

        return ResolveResult(
            UnixFSDirectory(
                unix_fs,
                node,
                name,
                path,
                cid,
                depth,
                unix_fs.file_size(),
                validate_directory_results(content)
            ),
            next_result
        )
    
    async def validate_file_results(content: AsyncIterable[ExportedContent]) -> AsyncIterable[bytes]:
        async for block in content:
            assert isinstance(block, bytes)
            yield block

    return ResolveResult(
        UnixFSFile(
            unix_fs,
            node,
            name,
            path,
            cid,
            depth,
            unix_fs.file_size(),
            validate_file_results(content)
        ),
        next_result
    )

_CONTENT_RESOLVERS: Mapping[int, Resolver] = {
    multicodec.get('dag-pb').code: resolve_dag_pb,
    multicodec.get('raw').code: resolve_raw,
    multicodec.get('dag-cbor').code: resolve_dag_cbor,
    multicodec.get('identity').code: resolve_identity
}

def resolve(cid: CID, name: str, path: str, to_resolve: Sequence[str], depth: int, block_store: BlockStore) -> Awaitable[ResolveResult]:
    return _CONTENT_RESOLVERS[cid.codec.code](cid, name, path, to_resolve, depth, block_store)    
