"""
██╗███╗   ██╗██████╗ ███████╗██╗  ██╗   ██████╗ ██╗   ██╗
██║████╗  ██║██╔══██╗██╔════╝╚██╗██╔╝   ██╔══██╗╚██╗ ██╔╝
██║██╔██╗ ██║██║  ██║█████╗   ╚███╔╝    ██████╔╝ ╚████╔╝ 
██║██║╚██╗██║██║  ██║██╔══╝   ██╔██╗    ██╔═══╝   ╚██╔╝  
██║██║ ╚████║██████╔╝███████╗██╔╝ ██╗██╗██║        ██║   
╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   

This module handles all things relating to secondary indexes (primary
indexes are a built-in feature of the underlying LMDB database). Index
definitions can either be based on Python f-strings, or for more
complex indexes, on custom Python functions. Index definitions are 
stored in the table's metadata and effectlively compiled and loaded
into memory when the Index is opened. Indexing is as you would expect
relatively transparent, when a new index is added pre-existing data is
entered into that index and subsequent write operations consider the index
when data is appended / deleted / modified. Access to this library is
generally via the table.ensure() call.
"""
from lmdb import Transaction as TXN, Cursor, BadValsizeError
from typing import Optional, Callable, TypeVar
from orbit_database.doc import Doc
from orbit_database.decorators import wrap_reader, OrbitTransaction, WriteTransaction
from orbit_database.exceptions import DuplicateKey
from orbit_database.iwx import InvertedWordIndex

Table = TypeVar('Table')


try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


class Index(InvertedWordIndex):
    """
    Each index has a number of attributes the most crital of which is 'func' which specifies
    how keys are generated for the index. Either f-strings of anonymous functions can be used,
    for example;
    ```
    func = 'f{forename}_{surname}'
    func = '''def func(doc): return (doc.get("forename")+"_"+doc.get("surname")).encode()'''
    ```
    The former is a far more concise / readable option for simple indexes, but clearly the latter
    has far more potential power (although in this case they both do the same thing) Note that
    for functions, the returned key must always be encoded. Valid configuration options are;
    ```
    conf = {
        'func': str,        # the function or f-string used to generate index keys
        'lower': bool,      # whether keys should be automatically lower-cased
        'duplicates': bool, # wheter duplicates are allowed or not
        'index_name': str,  # the name of the index
        'create': bool,     # whether the index should be created
        'iwx': bool,        # whether the index is a full-text index
    }
    ```
    """
    @property
    def metadata (self) -> dict:
        """
        > Returns the metadata for this index, i.e. the config + func attributes as a dict
        """
        return dict(self._conf)
        # return dict(self._conf, **{'func': self.func})

    def __init__(self, table: Table, name: str, conf: dict):
        """
        When we instantiate an Index we primarily need a back-reference to the table we're
        working with, the name of the index we're instantiating, and a definition of the indexing
        function. The indexing function is held in the 'func' item in the conf dictionary. 

        table - a reference to the table we're working with
        name - the name of the index we're creating a reference to
        conf - a configuration dict containing information specific to this dictionary
        """
        self._table = table
        self._conf = dict(conf)
        self.env = table.env
        self.name = name
        self._db = None
        self._writer = None
        self._lower = False
        self.func = func = self._conf.get('func')

        if func:
            if func[:4] == 'def ':
                self._func = self.anonymous_full(func)
            else:
                if self._conf.get('lower'):
                    self._lower = True
                    skel = '(r): return "{}".format(**r).lower().encode()'
                else:
                    skel = '(r): return "{}".format(**r).encode()'
                self._func = self.anonymous(skel.format(self._conf.get('func')))
        self.duplicates = self._conf.get('dupsort', False)
        # self._conf.pop('func', None)
        # self._conf.pop('lower', None)
        super().__init__()

    def open(self, txn: OrbitTransaction) -> None:
        """
        Open the index and make it available to the table

        txn - an optional transaction
        """
        if self._iwx:
            return super().open(txn)
        conf = dict(self._conf)
        conf.pop('func', None)
        conf.pop('lower', None)
        conf.pop('iwx', None)
        conf['key'] = conf['key'].encode()
        self._db = self.env.open_db(**conf, txn=txn.txn)

    @wrap_reader
    def records(self, txn: Optional[OrbitTransaction]=None) -> int:
        """
        Return the number of records in this index

        txn - an optional transaction
        """
        if self._iwx:
            return super().iwx_oids(txn)
        else:
            return txn.txn.stat(self._db).get('entries', 0)

    def save(self, old_doc: Doc, new_doc: Doc, txn: TXN) -> None:
        """
        Update a pre-existing index entry, we need both the old version of the record in
        order to remove the old index entries, and the new record to generate and insert
        the new ones.

        old_doc - the previous version of the record
        new_doc - the new version of the record
        txn - an optional transaction
        """
        if not super().save(old_doc, new_doc, txn):
            try:
                old_key = self._func(old_doc.doc)
            except (AttributeError, KeyError, TypeError):  # pragma: no cover
                old_key = []  # pragma: no cover
            try:
                new_key = self._func(new_doc.doc)
            except (AttributeError, KeyError, TypeError):
                new_key = []
                # log.error(f'bad key, index={self.name} table={self._table.name} / {e} / {new_doc.doc}')
                # log.error(f'old={old_key} new={new_key}')
            if old_key != new_key:
                if not isinstance(old_key, list):
                    old_key = [old_key]
                if not isinstance(new_key, list):
                    new_key = [new_key]
                # FIXME: we should find the intersections here and only update as necessary .. (!)
                for key in old_key:
                    if key:
                        txn.txn.delete(key, old_doc.oid, db=self._db)
                for key in new_key:
                    if key:
                        txn.txn.put(key, new_doc.oid, db=self._db)

    def get(self, doc: Doc, txn: OrbitTransaction) -> Optional[bytes|None]:
        """
        Get an entry from this index

        doc - the record template for the data to retrieve
        txn - an optional transaction
        """
        return txn.txn.get(self._func(doc.doc), db=self._db) if not self._iwx else None

    def get_last(self, doc: Doc, txn: OrbitTransaction) -> Optional[bytes|None]:
        """
        Get the last entry from a duplicate key index

        doc - the record template for the data to retrieve
        txn - an optional transaction
        """
        cursor = Cursor(self._db, txn.txn)
        if not cursor.get(self._func(doc.doc)):
            return None  # pragma: no cover
        if not cursor.last_dup():
            return None  # pragma: no cover
        return cursor.value()

    def put(self, doc: Doc, txn: OrbitTransaction) -> None:
        """
        Put a new entry in this index, used when createing new records

        doc - the document associated with this index entry
        txn - an optional transaction
        """
        if not super().put(doc, txn):
            try:
                keys = self._func(doc.doc)
            except (KeyError, TypeError, AttributeError):
                return
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                if key:
                    try:
                        if not txn.txn.put(key, doc.oid, db=self._db, overwrite=self.duplicates):
                            if not self.duplicates:
                                raise DuplicateKey(f'trying to add key "{key}"')
                    except BadValsizeError:
                        log.error(f'key error: {keys} / {self.name}')
                        raise

    def put_cursor(self, cursor: Cursor, txn: WriteTransaction) -> None:
        """
        Put a new index entry based on a Cursor rather than a Doc object. This is here
        mainly to make "reindex" more elegant / readable.

        cursor - an LMDB Cursor object
        txn - an optional transaction
        """
        if not super().put_cursor(cursor, txn):
            self.put(Doc(self._table.deserialise(cursor.value()), cursor.key()), txn=txn)

    def delete(self, doc: Doc, txn: OrbitTransaction) -> None:
        """
        Delete an entry from this index

        doc - record associated with the index entry to delete
        txn - an optional transaction
        """
        if not super().delete(doc, txn):
            try:
                keys = self._func(doc.doc)
            except KeyError:  # pragma: no cover
                return        # pragma: no cover
            except AttributeError:
                return
            except TypeError:
                log.error(f'key delete failed for index={self.name} doc={doc.doc}')
                return
            if not isinstance(keys, list):
                keys = [keys]
            for key in keys:
                if key:
                    try:
                        txn.txn.delete(key, doc.oid, self._db)
                    except BadValsizeError:
                        log.error(f'key delete failed for index={self.name} key={key}')
                        raise

    def empty(self, txn: OrbitTransaction) -> None:
        """
        Remove all entries from this index

        txn - an optional transaction
        """
        if not super().empty(txn):
            txn.txn.drop(self._db, delete=False)

    def drop(self, txn: OrbitTransaction) -> None:
        """
        Remove all entries from this index and then remove the index

        txn - an optional transaction
        """
        if not super().drop(txn):
            txn.txn.drop(self._db, delete=True)
            self._table._meta.remove_index(self._table.name, self.name, txn=txn)

    def map_key(self, doc: Doc) -> str:
        """
        > Return the key derived from the supplied record for this particular index

        doc - the record from which we want to derive a key
        """
        return self._func(doc.doc)

    @staticmethod
    def anonymous(text: str) -> Callable:
        """
        An function used to generate anonymous functions for database indecies
        > Returns a callable anonymous function based on an f-string

        text - a Python lambda function
        """
        scope = {}
        exec('def func{0}'.format(text), scope)
        return scope['func']

    @staticmethod
    def anonymous_full(text: str) -> Callable:
        """
        A function used to generate anonymous functions for database indecies
        > Returns a callable anonymous function based on a Python def

        text - a Python lambda function
        """
        scope = {}
        exec(text, scope)
        return scope['func']

    @staticmethod
    def index_path(table_name: str, index_name: str) -> str:
        """
        Produce an index "path" name for this index based on the table name and index name
        > Returns a path string
        """
        return f'_{table_name}_{index_name}'
