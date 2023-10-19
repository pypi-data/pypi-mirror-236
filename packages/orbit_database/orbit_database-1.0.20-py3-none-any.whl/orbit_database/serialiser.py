"""
███████╗███████╗██████╗ ██╗ █████╗ ██╗     ██╗███████╗███████╗██████╗    ██████╗ ██╗   ██╗
██╔════╝██╔════╝██╔══██╗██║██╔══██╗██║     ██║██╔════╝██╔════╝██╔══██╗   ██╔══██╗╚██╗ ██╔╝
███████╗█████╗  ██████╔╝██║███████║██║     ██║███████╗█████╗  ██████╔╝   ██████╔╝ ╚████╔╝ 
╚════██║██╔══╝  ██╔══██╗██║██╔══██║██║     ██║╚════██║██╔══╝  ██╔══██╗   ██╔═══╝   ╚██╔╝  
███████║███████╗██║  ██║██║██║  ██║███████╗██║███████║███████╗██║  ██║██╗██║        ██║   
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   

This module is a means of abstracting the serialisation process in order to provide a choice
of serialisers. Currently the supported libraries all do the same sort of thing, i.e. convert
Python variables to JSON and back again, although we plan to support a more efficient binary
serialiser in the future. Why is this important? Unexpectedly serialisation and deserialisation
is the primary database bottleneck.
"""
from typing import Optional
from enum import Enum
from lmdb import Transaction as TXN
from json import loads, dumps
from orbit_database.exceptions import InvalidSerialiser

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover

try:
    import ujson
except Exception:   # pragma: no cover
    pass            # pragma: no cover

try:
    import orjson
except Exception:   # pragma: no cover
    pass            # pragma: no cover


class SerialiserType(Enum):
    """
    Serilisers need to be defined here before they can be used, currently we support the
    default Python serialiser (json) and two external. Adding more is a relativelu trivial
    operation.
    """
    JSON = 'json'
    UJSON = 'ujson'
    ORJSON = 'orjson'
    RAW = 'raw'
    NONE = 'none'


class Serialiser:
    """
    All attempts to serialise or de-serialise data come through this point. Any new serialiser
    that supports "loads" and "dumps" can simply be imported and plugged into __init__
    """
    @property
    def codec(self) -> SerialiserType:
        """
        > Return the serialiser currently in use for this table
        """
        return self._codec

    def __init__(self, codec: Optional[SerialiserType]=SerialiserType.NONE, txn: TXN=None):
        """
        Set up handlers for serialisation and de-serialisation.

        codec - module that will supply "dumps" and "loads" methods
        """
        if not self._meta:
            self._generic_loads = loads
            self._generic_dumps = dumps
            self._codec = SerialiserType.JSON
            return
        #
        #   Sentinel - make sure we don't use a serialiser on data that's already been
        #              written with a different serialsier.
        #
        config = self._meta.fetch_config(self.name, txn=txn)
        if codec and codec != SerialiserType.NONE:
            if 'codec' in config:
                if codec.value != config._codec:
                    raise InvalidSerialiser(f'trying to use "{codec.value}" but data encoded with "{config._codec}"')
        else:
            if 'codec' in config:
                codec = SerialiserType(config['codec'])
            elif 'ujson' in globals():
                codec = SerialiserType.UJSON
            elif 'orjson' in globals():         # pragma: no cover
                codec = SerialiserType.ORJSON   # pragma: no cover
            else:
                codec = SerialiserType.JSON
            
        if 'codec' not in config:
            config._codec = codec.value
            self._meta.store_config(self.name, config, txn=txn)

        if codec == SerialiserType.UJSON:
            self._generic_dumps = ujson.dumps
            self._generic_loads = ujson.loads
        elif codec == SerialiserType.ORJSON:
            self._generic_dumps = orjson.dumps
            self._generic_loads = orjson.loads
        elif codec == SerialiserType.RAW:
            self._generic_dumps = raw_dumps
            self._generic_loads = raw_loads
        elif codec == SerialiserType.JSON:
            self._generic_dumps = dumps
            self._generic_loads = loads
        else:
            raise InvalidSerialiser(f'invalid serialised "{codec.value}"')
        
        self._codec = codec

    def serialise(self, doc: dict) -> bytes:
        """
        Serialise the provided object by calling the installed "dumps" routine
        > Returns the serialised object as a byte string
        """
        try:
            dump = self._generic_dumps(doc)
            return dump if isinstance(dump, bytes) else dump.encode()
        except Exception as e:
            log.error(f'Error on table: {self.name} doc={doc}')
            raise

    def deserialise(self, blob: bytes) -> dict:
        """
        De-serialise the provided byte string by calling the installed "loads" routine
        > Returns the de-serialised object
        """
        try:
            return self._generic_loads(blob)
        except Exception:
            log.error(f'Error: codec={self._codec} loader={self._generic_loads}')
            return blob


def raw_dumps(doc):
    """
    Dummy "dumps" routine for the RAW serialiser
    """
    return doc

def raw_loads(doc):
    """
    Dummy "loads" routine for the RAW serialiser
    """
    return doc
