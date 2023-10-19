"""
 ██████╗ ██████╗      ██╗███████╗ ██████╗████████╗██╗██████╗    ██████╗ ██╗   ██╗
██╔═══██╗██╔══██╗     ██║██╔════╝██╔════╝╚══██╔══╝██║██╔══██╗   ██╔══██╗╚██╗ ██╔╝
██║   ██║██████╔╝     ██║█████╗  ██║        ██║   ██║██║  ██║   ██████╔╝ ╚████╔╝ 
██║   ██║██╔══██╗██   ██║██╔══╝  ██║        ██║   ██║██║  ██║   ██╔═══╝   ╚██╔╝  
╚██████╔╝██████╔╝╚█████╔╝███████╗╚██████╗   ██║   ██║██████╔╝██╗██║        ██║   
 ╚═════╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   ╚═╝╚═════╝ ╚═╝╚═╝        ╚═╝   

Each table in the database has a primary key and whereas you can use your own primary
key it makes sense to let the system generate it's own unique primary key for you.
Object Ids generated from by class should be unique across multiple machine so long
as each machine has a unique hostname. Typical use-cases;
```
key = str(ObjectId())                 # generate a new / unique key string
print(ObjectId(key).generation_time)  # get the key generation time


```
"""
from os import getpid
from time import time
from socket import gethostname
from struct import pack, unpack
from typing import Any, Optional
from orbit_database.exceptions import InvalidId


def _fnv_1a(data: bytes):
    """
    Implementation of the Fowler-Noll-Vo hash function (fnv-1a)
    
    data - the bytes representation of the string to hash
    > Returns 
    """
    HASH_SIZE = 2 ** 32
    FNV_32_PRIME = 16777619
    FNV_1A_HASH = 2166136261  # 32-bit FNV-1 offset basis
    for elt in data:
        fnv_1a_hash = FNV_1A_HASH ^ elt
        fnv_1a_hash = (fnv_1a_hash * FNV_32_PRIME) % HASH_SIZE
    return (fnv_1a_hash >> 24) ^ (fnv_1a_hash & 0xffffff)

MACHINE_BYTES = _fnv_1a(gethostname().encode())


class ObjectId:
    """
    An ObjectId is a 16-byte unique identifier consisting of:

    - a 8-byte value representing the nano seconds since the Unix epoch
    - a 4-byte machine identifier
    - a 4-byte process id

    This code is based on the ObjectId class found in the Python BSON module.
    """
    @property
    def generation_time(self) -> float:
        """
        > Returns the generation time of this ObjectId as a float (timestamp)
        """
        return unpack('>d', self.__id[:8])[0]

    @property
    def binary(self) -> bytes:
        """
        > Returns a 16-byte binary representation of this ObjectId.
        """
        return self.__id

    def __init__(self, oid: Optional[bytes|str]=None) -> None:
        """
        Generate a new ObjectId either from a pre-existing sequence if bytes, or
        based on information from this machine including the time, the machine
        identifier, and the current process id.

        oid - can be a bytes(16) or a str(32) which should represent an ObjectId
        """
        if oid is None:
            self.__id = pack(">dII", time(), MACHINE_BYTES, getpid() % 0xFFFFFFFF)
        elif isinstance(oid, bytes) and len(oid) <= 16:
            self.__id = oid
        elif isinstance(oid, str) and len(oid) <= 32:
            try:
                self.__id = bytes.fromhex(oid)
            except ValueError:
                raise InvalidId(
                    f'{oid!r} is not a valid ObjectId, it must be a 16-byte input'
                    ' or a 32-character hex string'
                )               
        else:
            raise InvalidId(
                f'{oid!r} is not a valid ObjectId, it must be a 16-byte input'
                ' or a 32-character hex string'
            )

    def __getstate__(self) -> bytes:
        """
        > Returns the object's internal value
        """
        return self.__id

    def __setstate__(self, value: bytes) -> None:
        """
        Set the objects internal value
        """
        self.__id = value

    def __str__(self) -> str:
        """
        > Returns the objects internal value as a hex string suitable for use as a key
        """
        return self.__id.hex()

    def __eq__(self, other: Any) -> bool:
        """
        Boolean Equality check: EQ
        """
        if isinstance(other, ObjectId):
            return self.__id == other.binary
        return NotImplemented  # pragma: no cover

    def __ne__(self, other: Any) -> bool:
        """
        Boolean Equality check: NE
        """
        if isinstance(other, ObjectId):
            return self.__id != other.binary
        return NotImplemented  # pragma: no cover

    def __lt__(self, other: Any) -> bool:
        """
        Boolean Equality check: LT
        """
        if isinstance(other, ObjectId):
            return self.__id < other.binary
        return NotImplemented  # pragma: no cover

    def __le__(self, other: Any) -> bool:
        """
        Boolean Equality check: LE
        """
        if isinstance(other, ObjectId):
            return self.__id <= other.binary
        return NotImplemented  # pragma: no cover

    def __gt__(self, other: Any) -> bool:
        """
        Boolean Equality check: GT
        """
        if isinstance(other, ObjectId):
            return self.__id > other.binary
        return NotImplemented  # pragma: no cover

    def __ge__(self, other: Any) -> bool:
        """
        Boolean Equality check: GE
        """
        if isinstance(other, ObjectId):
            return self.__id >= other.binary
        return NotImplemented  # pragma: no cover

    def __hash__(self) -> int:
        """
        > Return the hash value for this Object
        """
        return hash(self.__id)
