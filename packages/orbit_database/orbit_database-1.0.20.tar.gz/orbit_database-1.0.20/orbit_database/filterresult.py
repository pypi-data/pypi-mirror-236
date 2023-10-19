"""
███████╗██╗██╗  ████████╗███████╗██████╗ ██████╗ ███████╗███████╗██╗   ██╗██╗  ████████╗██████╗ ██╗   ██╗
██╔════╝██║██║  ╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██║   ██║██║  ╚══██╔══╝██╔══██╗╚██╗ ██╔╝
█████╗  ██║██║     ██║   █████╗  ██████╔╝██████╔╝█████╗  ███████╗██║   ██║██║     ██║   ██████╔╝ ╚████╔╝ 
██╔══╝  ██║██║     ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║   ██╔═══╝   ╚██╔╝  
██║     ██║███████╗██║   ███████╗██║  ██║██║  ██║███████╗███████║╚██████╔╝███████╗██║██╗██║        ██║   
╚═╝     ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝╚═╝╚═╝        ╚═╝   

Wrapper for results returned from the "filter" API call. Sse the "doc" method to access the resulting data.
Additional public properties; (note that count is only useful for the results of searching a secondary index 
with duplicates enabled and suppress enabled for the filter request)
"""
from typing import TypeVar
from lmdb import Transaction as TXN, Cursor
from orbit_database.index import Index
from orbit_database.doc import Doc

Table = TypeVar('Table')


class FilterResult:
    """   
    o count   the number of duplicate keys that apply to this result
    o key     the key used to acquire this result
    o raw     loads and returns the raw bytes value for this object (for the raw serialiser)
    """
    @property
    def doc(self) -> Doc:
        """
        > Returns the uncompressed data associted with this search result.
        """
        if not self._dat:
            self._dat = self._txn.get(self._oid, db=self._table._db)
        return self._table._cls(None, self._oid, self._table._decompressor(self._dat), integerkey=self._table.integerkey)

    @property
    def oid(self) -> str:
        """
        > Returns the matching key for this result object
        """
        return self._oid  # pragma: no cover

    @property
    def raw(self) -> bytes:
        """
        > Returns the raw serialised data directly from the KV store
        """
        if not self._dat:
            self._dat = self._txn.get(self._oid, db=self._table._db)  # pragma: no cover
        return self._dat

    def __init__(self, table: Table, index: Index, cursor: Cursor, txn: TXN) -> None:
        """
        An instance is typically created for each result item returned from a table.filter
        call. When searching on a primary key we return they key and associated data item.
        When searching on a secondary key we return the key and a Doc object. The data
        component of the Doc object is subject to a lazy-load, so if we only want to scan
        through the keys and do not reference the doc object, then the actual data is not
        referenced (making secondary index scans much quicker than primary)
        
        table - the table from which the result originated
        index - the index we were searching on (None for primary key)
        cursor - the LMDB cursor object we're using
        txn - a transaction to wrap this operation
        """
        self._txn = txn
        self._table = table
        if index is None:
            self._oid = cursor.key()
            self._dat = cursor.value()
        else:
            self.key = cursor.key()  # this is used by filter() / context
            self._oid = cursor.value()
            self._dat = None
            self.count = cursor.count() if index.duplicates else 1
