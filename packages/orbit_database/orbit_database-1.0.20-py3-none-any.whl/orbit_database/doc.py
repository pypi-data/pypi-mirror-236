"""
██████╗  ██████╗  ██████╗   ██████╗ ██╗   ██╗
██╔══██╗██╔═══██╗██╔════╝   ██╔══██╗╚██╗ ██╔╝
██║  ██║██║   ██║██║        ██████╔╝ ╚████╔╝ 
██║  ██║██║   ██║██║        ██╔═══╝   ╚██╔╝  
██████╔╝╚██████╔╝╚██████╗██╗██║        ██║   
╚═════╝  ╚═════╝  ╚═════╝╚═╝╚═╝        ╚═╝   

Records (or documents in NoSQL terminology) recovered from or stored in the database are
always wrapped in a Doc object. It performs a number of crucial functions including;

o Associating a data buffer with a key (OID)
o Tracking updated attributes between the last read record and the current buffer
o Tracking deleted attributes
o Serialising and deserialising data between the database and user buffers
o Providing a dict and object-like interfaces to interact with the data
"""
from __future__ import annotations
from typing import Any, Optional, KeysView, ItemsView, ValuesView, TypeVar
from typing_extensions import Self
from lmdb import Transaction as TXN
from struct import pack, unpack
from orbit_database.objectid import ObjectId

Table = TypeVar('Table')

try:
    from loguru import logger as log
except ModuleNotFoundError:
    import logging as log


class Doc(object):
    """
    This class represents a database records (or document) and provides some very powerful features.
    It behaves a little like an enhanced dictionary so you can access the fields within the record
    either by using dictionary notation and supplying the field name in square brackets, or by using
    an underscore folled by the field name. You can also initialise a Doc object from a dictionary,
    so for example;
    ```
    doc = Doc({'name': 'Fred', 'age': 21})
    print(f'{doc["name"]} is {doc._age} years old')
    ```
    Whereas the latter notation is much more readable, the ability access using normal dictionary
    notation is often useful when the field name is dynamic.
    """

    def __init__(
            self,
            doc: Optional[dict]=None,
            oid: Optional[bytes|str]=None,
            dat: Optional[dict]=None,
            words: Optional[list[str]]=None,
            integerkey=False) -> None:
        """
        Instantiate a Doc object either based on a Dict or Cursor object. In the event a Cursor object
        is supplied, the (upd) field is set to cursor.value() and (oid) is set to cursor.key(). If a dict
        is supplied, (upd) is set to the value of the dict supplied, and oid is either set to the supplied
        oid or left as None by default.

        doc - the data to associate with this object
        oid - a primary key to associate with this object
        """
        if isinstance(oid, str):
            self.oid = oid.encode()
        elif isinstance(oid, int):
            self.oid = pack('=Q', oid)
        else:
            self.oid = oid
        self.integerkey = integerkey
        self.upd = doc or {}
        self.old = {}
        self.dat = dat or {}
        self.rem = []
        self.words = words or []

    @property
    def changed(self) -> bool:
        """
        The object records changes so that it can report those changes to the auditing sub-system. This
        property indicates whether the document has been changed since it was first instantiated or
        read from the database.
        > Returns True is the Doc has changed since it was read from the database otherwise False
        """
        return len(self.upd) != 0 or len(self.rem) != 0
       
    @property
    def doc(self) -> dict:
        """
        > Return the current data within the buffer, typically this is initial state + changes
        """
        if isinstance(self.dat, dict) and isinstance(self.upd, dict):
            return dict(self.dat, **self.upd)
        return self.upd or self.dat

    @property
    def doc_with_id(self) -> dict:
        """
        > Return the current data within the buffer, typically this is initial state + changes + _id
        """
        if isinstance(self.dat, dict) and isinstance(self.upd, dict):
            return dict(self.dat, **self.upd, _id=self.key)
        return self.upd or self.dat

    @property
    def key(self) -> str:
        """
        > Returns the current key (oid) for this document
        """
        if not self.oid:
            return None
        try:
            return unpack('=Q', self.oid)[0] if self.integerkey else self.oid.decode()
        except UnicodeDecodeError:
            return unpack('=Q', self.oid)[0]

    def __bool__(self):
        """
        > Always return True for a Doc object
        """
        return True
    
    def __contains__(self, key: str) -> bool:
        """
        Determine whether a given field name is present within the
        current document, typically accessed as;
        ```
        if 'field' in doc:
            ...
        ```
        > Return True if the field exists in this instance otherwise False
        """
        return key in self.doc

    def __delitem__(self, key: str):
        """
        Delete the field associated with the named key, typically accessed by;
        ```
        del doc['field']
        ```
        key - the field name to delete
        """
        if key in self.upd:
            del self.upd[key]
        if key in self.dat:
            del self.dat[key]
            self.rem.append(key)

    def __eq__(self, doc: object):
        """
        The Equality operator for the doc object taking into account the type, oid, field contents
        and deleted field contents.
        > Returns True if both objects contain the same details, otherwise False
        doc - The 'other' document to compare to (typically of type Doc)
        """
        return (type(self) == type(doc)) and (self.oid == doc.oid) and \
                (self.doc == doc.doc) and (self.rem == doc.rem)

    def __getattr__(self, key: str) -> Any:
        """
        Recover a value from this structure. If the key begins with an underscore, the field
        with matching name (after dropping the '_') will be recovered. Otherwise, the
        appropriate attribite will be returned.
        > Returns the data item associated with 'key' (dropping the '_' prefix)

        key - item to recover, prefix with an '_' to recover field names
        """
        try:
            return object.__getattribute__(self, key)
        except AttributeError as e:            
            if key[0] == '_':
                return self.upd.get(key[1:], self.dat.get(key[1:]))
            raise e

    def __getitem__(self, key: str) -> Any:
        """
        Return the data item associated with 'key'

        key - data item name
        """
        return self.upd.get(key, self.dat.get(key))

    def __len__(self) -> int:
        """
        > Return the length of the current buffer
        """
        return len(self.dat) + len(self.upd)

    def __repr__(self) -> str:
        """
        > Returns a string representation of the Doc object
        """
        return f'{type(self)} with id={self.oid}'

    def __setattr__(self, key: str, val: Any):
        """
        If the key is prefixed with an underscore then set the matching field
        (after dropping the '_') to the value specified. Otherwise set the matching
        property of this object to the value specified.

        key - field name (if prefixed with '_') or property name
        val - actual data item to associate with key
        """
        if key[0] == '_':
            k = key[1:]
            if k not in self.old:
                self.old[k] = self.upd.get(k, self.dat.get(k))
            self.upd[k] = val
        else:
            object.__setattr__(self, key, val)

    def __setitem__(self, key: str, val: Any):
        """
        Set the named field to be the specified value.

        key - data item name prefixed with an underscore
        val - actual data item to associate with key
        """
        if key not in self.old:
            self.old[key] = self.upd.get(key, self.dat.get(key))
        self.upd[key] = val

    def get(self, table: Table, txn: OrbitTransaction) -> Optional[Self|None]:
        """
        Populate this structure by reading data from the database

        table - open table reference
        txn - active database transaction

        > Returns a reference to self or None if the document doesn't exist
        """
        dat = txn.txn.get(self.oid, db=table._db)
        if dat:
            self.dat = table._decompressor(dat)
            return self
        return None

    def items(self) -> ItemsView:
        """
        This is the equivalent of dict.items() the difference being we are
        incorporating the original state of the object and subsequent changes.
        > Returns a list of tuples where each tuple is (key, val)
        """
        return dict(self.dat, **self.upd).items()

    def keys(self) -> KeysView:
        """
        This is the equivalent of dict.keys() the difference being we are
        incorporating the original state of the object and subsequent changes.
        > Returns a list of keys
        """
        return dict(self.dat, **self.upd).keys()

    def pop (self, key: str) -> Optional[bytes|None]:
        """
        Remove the named key from the record removing it from both the origin
        buffer and the update buffer as appropriate.
        > Return the value removed IF it was present in the origin buffer else None
        """
        if key in self.upd:
            self.upd.pop(key)
        if key in self.dat:
            ret = self.dat.pop(key)
            self.rem.append(key)
            return ret
        return None

    def put(self, table: Table, append: bool=False, txn: TXN=None) -> None:
        """
        Store the current document buffer back to the database

        table - an active table reference
        append - whether to use "append" mode
        txn - active database transaction
        """
        if not self.oid:
            self.oid = str(ObjectId()).encode()
        txn.put(self.oid, table._compressor(self), append=append, db=table._db)

    def update(self, raw: bytes) -> None:
        """
        Set the update buffer using a RAW string, this is used exclusively by the RAW serialiser

        raw - bytes to assign to doc data component
        """
        self.upd = raw

    def values(self) -> ValuesView:
        """
        This is the equivalent of dict.values() the difference being we are
        incorporating the original state of the object and subsequent changes.
        > Returns a list of values
        """
        return dict(self.dat, **self.upd).values()
