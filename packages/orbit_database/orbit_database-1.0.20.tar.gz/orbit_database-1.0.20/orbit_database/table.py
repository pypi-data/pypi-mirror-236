"""
████████╗ █████╗ ██████╗ ██╗     ███████╗   ██████╗ ██╗   ██╗
╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝   ██╔══██╗╚██╗ ██╔╝
   ██║   ███████║██████╔╝██║     █████╗     ██████╔╝ ╚████╔╝ 
   ██║   ██╔══██║██╔══██╗██║     ██╔══╝     ██╔═══╝   ╚██╔╝  
   ██║   ██║  ██║██████╔╝███████╗███████╗██╗██║        ██║   
   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝        ╚═╝   

The Table module controls all aspects of tables and does most of heavy lifting
for the library. A table object behaves like a dictionary and it's contents
enumerate to any indexes that have been defined for the table.
"""
from sys import maxsize as MAXSIZE
from collections import UserDict
from typing import Generator, Optional, Union, Callable, Type, TypeVar, Collection
from lmdb import Transaction as TXN, NotFoundError, IncompatibleError
from struct import pack, unpack
from orbit_database.index import Index
from orbit_database.doc import Doc
from orbit_database.compression import Compression, CompressionType
from orbit_database.serialiser import Serialiser, SerialiserType
from orbit_database.cursor import Cursor
from orbit_database.objectid import ObjectId
from orbit_database.filterresult import FilterResult
from orbit_database.matchresult import MatchResult
from orbit_database.decorators import wrap_reader, wrap_reader_yield, ReadTransaction, WriteTransaction, OrbitTransaction, wrap_writer
from orbit_database.exceptions import IndexAlreadyExists, DocumentDoesntExist, InvalidKeySpecifier, NoSuchIndex
from pathlib import Path
from operator import gt as greater, lt as less
from json import load, dump

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover

ZERO = 0
Database = TypeVar("Database")
Table = TypeVar("Table")
OID = TypeVar('OID', str, bytes)
OIDS = Collection[OID]


class Table(UserDict, Compression, Serialiser):
    """
    The Table class is used to wrap access to individual database tables and incorporates
    pluggable transparent compression and pluggable transparent serialisation on a per
    table basis. 
    """
    @property
    def isopen(self) -> bool:
        """
        > Returns True if the table if open, otherwise False
        """
        return False if self._db is None else True

    @property
    def oid (self) -> ObjectId:
        """
        The oid is the table's unique identifier. For version #1 indexes this will be the
        name of the table, but for version #2 this will be an "ObjectId" which relates to
        it's primary key in the LMDB primary index.
        
        > Returns the 'oid' for this table
        """
        return self._oid

    @property
    def read_transaction(self) -> ReadTransaction:
        """
        Use with "with" to begin a Read-Only transaction
        """
        return ReadTransaction(self._database)

    @property
    def write_transaction(self) -> WriteTransaction:
        """
        Use with "with" to begin a Read-Write transaction
        """
        return WriteTransaction(self._database)

    def __init__(self, database: Database, name: str, cls: Type[Doc]=Doc):
        """
        Intantiate a table instance based on the name of the table required.

        database - a reference to the containing database object
        name - the name of the table to reference
        cls - the class to use as the default return type for seek and filterresult
        """
        self.name = name
        self.env = database.env
        self._database = database
        self._cls = cls
        self._db = None
        self._oid = None
        self._meta = database.meta
        UserDict.__init__(self)
        Compression.__init__(self)

    def __setitem__(self, name: str, conf: dict):
        """
        Create an entry for an index with the specified name

        name - the name of the index to create
        conf - configuration options for the index we're creating
        """
        if name in self.data:
            raise IndexAlreadyExists(name)
        self.data[name] = Index(self, name, conf)

    def __repr__(self) -> str:
        """
        > Returns a string representation of this object
        """
        return f'<{__name__}.Table instance> name="{self.name}" status={"open" if self.isopen else "closed"}'

    @wrap_reader
    def records(self, txn: Optional[OrbitTransaction]=None) -> int:
        """
        > Returns the number of records in this table

        txn - an transaction to wrap the operation
        """
        return txn.txn.stat(self._db).get('entries', 0)

    @wrap_reader
    def stat(self, txn: Optional[TXN]=None) -> int:
        """
        > Returns the stat() buffer for this table

        txn - an transaction to wrap the operation
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        return transaction.stat(self._db)

    @wrap_reader
    def storage_used(self, txn: Optional[OrbitTransaction]=None) -> int:
        """
        > Return the amount of storage space used by data contained within this table

        txn - optional transaction to wrap this operation
        """
        stat = txn.txn.stat(self._db)
        return stat['psize'] * (stat['leaf_pages'] + stat['branch_pages'] + stat['overflow_pages'] + 2)

    @wrap_writer
    def open(
            self,
            compression_type: Optional[CompressionType]=CompressionType.NONE,
            compression_level: Optional[int]=None,
            codec: SerialiserType=SerialiserType.NONE,
            integerkey: int=False,
            compress_existing: bool=False,
            auditing: bool=False,
            callback: Callable=None,
            txn: Optional[WriteTransaction]=None) -> Table:
        """
        Open this table and make it available for use, if the compression type is set to
        anything other than NONE, the following the call the table will be set to read and
        write data using the selected compression mechanism, and any data in the table will
        be compressed.

        compression_type - the type of compression to use
        compression_level - the compression level to set
        txn - an optional transaction to wrap this request
        > Returns a reference to the opened table
        """
        if self.isopen:
            return self
        self._compression_type = compression_type
        self._compression_level = compression_level
        self._codec = codec
        self.integerkey = integerkey
        self._auditing = auditing

        if not self.name.startswith('@@') and self._database.index_version == 2:
            self._oid = name = self._database._cat.get_table_id(self.name, txn)
        else:
            self._oid = self.name
            
        try:
            self._db = self.env.open_db(self._oid.encode(), integerkey=integerkey, txn=txn.txn)
        except NotFoundError:
            self._db = self.env.open_db(self._oid.encode(), integerkey=integerkey, txn=txn.txn)
        except IncompatibleError as e:
            log.error(f'{self.name} => {self._oid}:: {str(e)}')
            return self
        try:
            Serialiser.__init__(self, codec, txn=txn)
            if not self._meta:
                return self
            for index_name in self.indexes(txn=txn):
                if index_name in self.data:
                    # means the index is open so we're doing a 're-open'
                    self.data[index_name].open(txn=txn)  # pragma: no cover
                else:
                    if self._database.index_version == 1:
                        doc = self._meta.fetch_index(self.name, index_name, txn=txn)
                        if not doc['conf']:
                            break  # pragma: no cover
                        self.__setitem__(index_name, doc['conf'])
                    else:
                        # log.success(f'get meta: {self.name}/{index_name} => {self._database._cat.get_metadata(self.name, index_name)}')
                        self.__setitem__(index_name, self._database._cat.get_metadata(self.name, index_name))
                    
                    self.data[index_name].open(txn=txn)
            if compression_type and compression_type != CompressionType.NONE:
                do_compress = self.compression_select(compression_type, compression_level, txn=txn)
                Compression.open(self, txn=txn)
                if compress_existing and do_compress and self.records(txn=txn):
                    self.compress_existing_data(txn=txn)
            else:
                Compression.open(self, txn=txn)
            if auditing:
                self._database._auditor.watch(self.name, callback)
            
        except Exception:
            try:
                self.close()  # pragma: no cover
            except Exception:  # pragma: no cover
                pass
            raise

        return self

    @wrap_writer
    def droptable(self, txn: Optional[TXN|WriteTransaction]=None) -> None:
        """
        Drop the current table, this will empty the table, remove all the indexes,
        remote the table itself, and remove all associated metadata

        txn - a write transaction to wrap this operation
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        for index_name in self.data:
            self.data[index_name].drop(txn=txn)
        transaction.drop(self._db, True)
        self._database._cat.drop(self.name, txn)
        self._meta.remove(self.name, txn=txn)

    def close(self) -> None:
        """
        Close a table by essentially losing all references to it
        """
        self._db = None
        self.data.clear()
        Compression.close(self)

    @wrap_writer
    def reopen(
        self,
        auditing: bool=False,
        callback: Optional[Callable]=None,
        txn: Optional[TXN|WriteTransaction]=None) -> None:
        """
        ReOpen a table, used following a change to the map size. Everything should be the
        same, we just need new database handles.
        
        auditing - True is auditing is to be enabled on this table for this session
        callback - The default routine to call when some data is changed within this table
        txn - an optional transaction to wrap this request        
        """
        self.close()
        self.env = self._database.env
        self.open(
            self._compression_type,
            self._compression_level,
            self._codec,
            self.integerkey,
            auditing = auditing,
            callback = callback,
            txn=txn)

    @wrap_reader_yield
    def indexes(self, txn: Optional[ReadTransaction]=None) -> Generator[str, None, None]:
        """
        Generate a list if indexs (names) available for this table

        txn - an optional transaction
        """
        if self.name.startswith('@@'):
            return []
        if self._database.index_version == 1:
            metadata = self._database.table('__metadata__', txn=txn.txn)
            index_key = Index.index_path(self.name, '')
            offset = len(index_key)
            with txn.txn.cursor(db=metadata._db) as cursor:
                cursor.set_range(index_key.encode())
                name = cursor.key().decode()
                while name.startswith(index_key):
                    yield name[offset:]
                    if not cursor.next():
                        break
                    name = cursor.key().decode()
        elif self._database.index_version == 2:
            for name in self._database._cat.indexes(self.name, txn):
                yield name

    @wrap_writer
    def ensure(
            self,
            index_name: str,
            func: str=None,
            duplicates: bool=False,
            force: bool=False,
            lower: bool=False,
            iwx: bool=False,
            progress: Optional[Callable]=None,
            txn: Optional[WriteTransaction]=None) -> Index:
        """
        Ensure that the specified index exists, if it does by default do nothing. If the
        index does not exist, or if the 'force' flag is true, the index will be (re)created
        using the new index function.

        index_name - the name of the required index
        func - a description of how index keys should be generated
        duplicates - whether this is a duplicate index or not
        force - whether to re-index the index if it already exists
        lower - whether to force keys to lower case
        iwx - true if this index is an inverted word index
        progress - a routine to call to display progress updates
        txn - an optional transaction

        The "func" parameter can take one of two forms, it can either be a Python format
        string (the only option in v1) or it can be a complete python function if prefixed
        with a 'def'. So for example as a format string;
        ```
        func = '{name}'         # index by name
        func = '{name}|{age}'   # index by name + age
        func = '{age:03d}'      # index by age with leading zero for correct numerical sort order
        ```
        Or if you want to use a function which allows for more flexibility;
        ```
        func = 'def func(doc): return "{:03d}".format(doc["age"]).encode()'
        ```
        For a complete working example, the natural order is in descending on age,
        but when iterating using either of the example indexes, you should see the order
        as ascending order of age.
        ```
        #!/usr/bin/env python
        from orbit-database import Manager, Doc
        from shutil import rmtree
        rmtree('.database')
        db = Manager().database('database', '.database')
        people = db.table('people')
        people.append(Doc({'name': 'Tom', 'age': 21}))
        people.append(Doc({'name': 'Harry', 'age': 19}))
        people.ensure('by_age_fs', '{age:03d}')
        people.ensure('by_age_func', 'def func(doc): return "{:03d}".format(doc["age"]).encode()')
        [print(person.doc) for person in people.find()]
        print('--')
        [print(person.doc) for person in people.find('by_age_fs')]
        print('--')
        [print(person.doc) for person in people.find('by_age_func')]
        ```
        """
        old_conf = self._database._cat.get_conf(self._database,
            self.name, index_name, iwx, txn)
        new_conf = dict(old_conf, **{'dupsort': duplicates, 'create': True,
            'func': func, 'iwx': iwx, 'lower': lower })
        force = old_conf != new_conf or force       
        if index_name not in self.data or force:
            if index_name in self.data:
                self.drop(index_name, txn=txn)
            self.__setitem__(index_name, new_conf)
            self._database._cat.put_conf(self._database,
                self.name, index_name, new_conf, txn)
            self.data[index_name].open(txn=txn)
            if force:
                self.reindex(index_name, progress=progress, txn=txn)
                
        self.data[index_name].reindexed = force
        return self.data[index_name]
                    
    @wrap_writer
    def reindex(self, index_name: str, progress: Optional[Callable]=None, txn: Optional[WriteTransaction]=None) -> None:
        """
        Reindex the named index, assuming the index exists. The index is first emptied
        and then each record is reindexed, for a large table this can take some time
        and will lock the database while in progress.

        index_name - the name of the index to reindex
        progress - a routine to call to display progress updates
        txn - a write transaction to wrap the operation
        """
        if index_name not in self.data:
            raise NoSuchIndex
        self.data[index_name].empty(txn=txn)
        with txn.txn.cursor(self._db) as cursor:
            while cursor.next():
                if progress:
                    progress.update(1)  # pragma: no cover
                self.data[index_name].put_cursor(cursor, txn=txn)

    @wrap_writer
    def append(self, doc: Doc, txn: Optional[WriteTransaction]=None) -> Doc:
        """
        Append a new record to this table

        doc - the data to append
        txn - an optional transaction object
        """
        if not doc.oid:
            if self.integerkey:
                with txn.txn.cursor(db=self._db) as cursor:
                    if not cursor.last():
                        oid = 0
                    else:
                        oid = unpack('=Q', cursor.key())[0] + 1
                    doc.oid = pack('=Q', oid)
            else:
                doc.oid = str(ObjectId()).encode()
        txn.txn.put(doc.oid, self._compressor(doc), db=self._db)
        if self._auditing:
            self._database._auditor.append(self, doc, txn)
        for index_name in self.data:
            self.data[index_name].put(doc, txn=txn)
        return doc

    @wrap_writer
    def save(self, doc: Doc, txn: Optional[WriteTransaction]=None) -> None:
        """
        Update the current record in the table

        doc - the record to update
        txn - an optional transaction
        """
        if not doc.oid:
            raise DocumentDoesntExist
        old_doc = Doc(None, doc.oid).get(self, txn=txn)
        if self._auditing:
            if old_doc:
                self._database._auditor.save(self, old_doc, txn)
            else:
                log.error(f'Audit: no old document for oid: {doc.oid}')
        txn.txn.put(doc.oid, self._compressor(doc), db=self._db)
        for index_name in self.data:
            self.data[index_name].save(old_doc, doc, txn=txn)

    @wrap_reader_yield
    def find(
            self,
            index_name: str=None,
            expression: str=None,
            limit: int = MAXSIZE,
            txn: Optional[OrbitTransaction]=None) -> Generator[Doc, None, None]:
        """
        Find records in this table either in natural (date) order, or in index order

        index_name - an optional index name for ordering
        expression - the expression to filter the sort on
        limit - the maximum number of records to return
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        #
        with txn.txn.cursor(db) as cursor:
            count = 0
            while count < limit and cursor.next():
                count += 1
                record = cursor.value()
                if index_name:
                    key = record
                    record = txn.txn.get(record, db=self._db)
                else:
                    key = cursor.key()

                record = self._decompressor(record)
                if callable(expression) and not expression(record):
                    continue
                yield Doc(None, key, record)

    @wrap_reader
    def get(self, oid: bytes|str, txn: Optional[WriteTransaction]=None) -> Doc:
        """
        Recover a single record from the database based on it's primary key

        oid - primary key of record to recover
        txn - an optional active transaction
        """
        try:
            return Doc(None, pack('=Q', oid) if self.integerkey else oid).get(self, txn=txn)
        except Exception as e:  # pragma: no cover
            log.exception(e)  # pragma: no cover
            log.error(f'key was: {oid}')  # pragma: no cover

    @wrap_writer
    def delete(self, keyspec: Union[OID, OIDS, Doc], txn: Optional[WriteTransaction]=None) -> None:
        """
        Delete one or more records from the database based on a key specification that
        should reference one or more records by primary key.

        keyspec - we accept either a key, a list of keys or a Doc, keys may be str or bytes
        txn - an optional transaction
        """
        if isinstance(keyspec, str):
            keys = [keyspec]
        elif isinstance(keyspec, list):
            keys = keyspec
        elif isinstance(keyspec, Doc):
            keys = [keyspec.oid]
        elif isinstance(keyspec, bytes):
            keys = [keyspec]
        elif isinstance(keyspec, int) and self.integerkey:
            keys = [keyspec]
        else:
            raise InvalidKeySpecifier(keyspec)

        for key in keys:
            if isinstance(key, str):
                key = key.encode()
            doc = self.get(key, txn=txn)
            if doc:
                txn.txn.delete(doc.oid, db=self._db)
                if self._auditing:
                    self._database._auditor.delete(self, doc, txn)

                for index_name in self.data:
                    self.data[index_name].delete(doc, txn=txn)
            else:
                log.error(f'unable to delete key: "{key}" from table "{self.name}"')  # pragma: no cover

    @wrap_writer
    def empty(self, txn: Optional[WriteTransaction]=None) -> None:
        """
        Remove all data from the current table leaving the indexing structure in-tact

        txn - an optional transaction
        """
        txn.txn.drop(self._db, False)
        for index_name in self.data:
            self.data[index_name].empty(txn=txn)

    @wrap_writer
    def drop(self, index_name: str, txn: Optional[WriteTransaction]=None) -> None:
        """
        Drop an index from the current table

        index_name - the name of the index to drop
        txn - an optional transaction
        """
        if index_name not in self.data:
            raise NoSuchIndex(index_name)

        index = self.data[index_name]
        del self.data[index_name]
        index.drop(txn)
        self._database._cat.drop_index(self.name, index_name, txn)

    @wrap_reader_yield
    def tail(self, key: Optional[OID]=None, txn: Optional[ReadTransaction]=None) -> Generator[Doc, None, None]:
        """
        Generates a sequence of records starting from the key after the primary key supplied. If no
        key is supplied, all records are returned, if a misssing key is supplied, no records are
        returned. Typically use this against the last-seen key to access new keys since the last
        check.

        key - the key to start from
        txn - an optional transaction

        TODO: add index to allow tailing based on indexes
        """
        with txn.txn.cursor(db=self._db) as cursor:
            if key:
                if not isinstance(key, bytes):
                    key = key.encode()
                #
                #   We need this behaviour, when someone empties the table, tail needs to know
                #   to go back to the start of the table and continue, rather then being left
                #   on a non-existant key forever ...
                #
                if not cursor.get(key):
                    if not cursor.first():
                        return None
                elif not cursor.next():
                    return None

            for key, val in cursor.iternext(keys=True, values=True):
                yield Doc(None, key, self._decompressor(val))

    @wrap_reader
    def first(self,
            index_name: Optional[str]=None,
            doc: Optional[Doc]=None,
            txn: Optional[OrbitTransaction]=None) -> Optional[Doc]:
        """
        Return the first record in the table or None if there are no records

        index_name - the name of the index to use (defaults to primary)
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        with txn.txn.cursor(db=db) as cursor:
            if not cursor.first():
                return None
            if index_name:
                if doc:
                    index_entry = self.data[index_name].get(doc, txn=txn)
                else:
                    index_entry = cursor.value()
                doc = txn.txn.get(index_entry, db=self._db)
                return Doc(None, cursor.value(), self._decompressor(doc), integerkey=self.integerkey)
            else:
                return Doc(None, cursor.key(), self._decompressor(cursor.value()), integerkey=self.integerkey)

    @wrap_reader
    def last(
            self,
            index_name: Optional[str]=None,
            doc: Optional[Doc]=None,
            txn: Optional[WriteTransaction]=None) -> Optional[Doc]:
        """
        Return the last record in the table or None if there are no records

        index_name - the name of the index to use (defaults to primary)
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex(index_name)
            db = self.data[index_name]._db
        else:
            db = self._db
        with txn.txn.cursor(db=db) as cursor:
            if not cursor.last():
                return None
            if index_name:
                if doc:
                    index_entry = self.data[index_name].get_last(doc, txn=txn)
                    if not index_entry:
                        return None  # pragma: no cover
                else:
                    index_entry = cursor.value()
                doc = txn.txn.get(index_entry, db=self._db)
                return Doc(None, cursor.value(), self._decompressor(doc), integerkey=self.integerkey)
            else:
                return Doc(None, cursor.key(), self._decompressor(cursor.value()), integerkey=self.integerkey)

    @wrap_reader_yield
    def range(
            self,
            index_name: Optional[str]=None,
            lower: Optional[Doc]=None,
            upper: Optional[Doc]=None,
            keyonly: bool=False,
            inclusive: bool=True,
            limit: int=MAXSIZE,
            page_number: int=0,
            nodups: bool=False,
            txn: Optional[OrbitTransaction]=None) -> Generator[Doc, None, None]:
        """
        Find all records within a range of keys, optionally including keys at each end
        and optionally returning just the keys rather than the entire record.

        index_name - an optional index name, if no index is supplied, use primary keys
        lower - the record at the lower end of the range
        upper - the record at the upper end of the range
        keyonly - if set to True, only returns keys rather than the entire records
        inclusive - if set to True, include the keys at each end, i.e. use <=|=> rather than <|>
        limit - maximum number of records to return
        page_number - index of the page (starts from 0) with a size `limit` to return results from
        nodups - no duplicate keys, return only unique key values and ignore duplicates
        txn - an optional transaction
        """
        if index_name:
            if index_name not in self.data:
                raise NoSuchIndex()
            index = self.data[index_name]
            db = index._db

            lower_keys = index.map_key(lower) if lower else [None]
            upper_keys = index.map_key(upper) if upper else [None]

            if not isinstance(lower_keys, list):
                lower_keys = [lower_keys]
            if not isinstance(upper_keys, list):
                upper_keys = [upper_keys]

        else:
            db = self._db
            lower_keys = [lower.oid] if lower else [None]
            upper_keys = [upper.oid] if upper else [None]

        skip = page_number * limit

        with txn.txn.cursor(db) as cursor:
            for lower_key in lower_keys:
                upper_key = upper_keys.pop(0)
                next_record = cursor.next_nodup if nodups else cursor.next
                cursor.set_range(lower_key) if lower_key else cursor.first()
                if cursor.key() == lower_key and not inclusive:
                    next_record()
                count = 0
                while cursor.key() and count < limit:
                    if upper_key and (cursor.key() > upper_key or (cursor.key() == upper_key and not inclusive)):
                        break
                    if skip:
                        skip -= 1
                    else:
                        count += 1
                        if not index_name:
                            yield cursor.key().decode() if keyonly else Doc(None,
                                cursor.key(), self._decompressor(cursor.value()))
                        else:
                            yield Cursor(index, cursor) if keyonly else Doc(
                                None, cursor.value()).get(self, txn=txn)
                    next_record()

    @wrap_reader
    def seek_one(self, index_name: str, doc: Doc, txn: Optional[OrbitTransaction]=None) -> Doc:
        """
        Find the first matching record from an index

        index_name - the name of the index to search
        doc - the template record to find
        txn - an optional transaction
        """
        if index_name not in self.data:
            raise NoSuchIndex()
        index_entry = self.data[index_name].get(doc, txn=txn)
        return self._cls(None, index_entry).get(self, txn=txn) if index_entry else None

    def seek(
            self,
            index_name: str,
            doc: Doc,
            limit: int=MAXSIZE,
            page_number: int=0,
            keyonly: bool = False,
            txn: Optional[TXN]=None) -> Generator[Doc, None, None]:
        """
        Return a selection of records from the selected table matching the template record provided in "doc".
        Should return a maximum of 1 record for unique indexes.
        index_name - the name of the index to search
        doc - the template record to find
        limit - the maximum number of results to return
        page_number - index of the page (starts from 0) with a size `limit` to return results from
        keyonly - return a Cursor object relating to the key instead of the data item
        txn - an optional transaction
        """
        return self.range(
            index_name=index_name,
            lower=doc,
            upper=doc,
            limit=limit,
            page_number=page_number,
            keyonly=keyonly,
            txn=txn)

    @wrap_reader_yield
    def filter(
            self,
            index_name: Optional[str]=None,
            lower: Optional[Doc]=None,
            upper: Optional[Doc]=None,
            expression: Optional[Callable[[Doc], bool]]=None,
            context: Optional[FilterResult]=None,
            page_size: Optional[int]=0,
            inclusive: Optional[bool]=True,
            suppress_duplicates: Optional[bool]=False,
            reverse: Optional[bool]=False,
            txn: Optional[TXN]=None) -> Generator[FilterResult, None, None]:
        """
        Filter the table specified based on a criteria defined by the parameters passed.

        * Paging  To use the paging function, you need to supply both a page_size and context. If the
                  context is None and the page_size is positive, paging will start from the begininning
                  of theindex, and if the context is None and the page size is negative, paging will start
                  from the end. A positive page_size moves forwards through the index based on the context
                  and a negative page size moves backwards. For forward paging, the context will be the
                  last result from the previous page, and for moving backwards, the context will be the
                  first result from the previous page.
        * lambda  The "expression" parameter should be a lambda (or function) which will receive the
                  document and return a True/False based on whether the document should be included in
                  the search results. For example;
        ```
            filter(expression=lambda doc: doc['age'] > 19)
        ```

        index_name - the name of an index to search on, or None to use the primary key
        lower - the record at the lower end of the range
        upper - the record at the upper end of the range
        expression - an lambda expression to filter the results
        context - a paging context to determine where to start tge next page (see comments)
        page_size - maximum number of records to return
        inclusive - if set to True, include the keys at each end, i.e. use <=|=> rather than <|>
        suppress_duplicates - no duplicate keys, return only unique key values and ignore duplicates
        reverse - navigate the index in reverse order
        txn - an optional transaction
        """
        transaction = txn if isinstance(txn, TXN) else txn.txn
        if index_name is not None:
            if index_name not in self.data:
                raise NoSuchIndex()
            index = self.data[index_name]
            db = index._db
            lower_keys = index.map_key(lower) if lower else [None]
            upper_keys = index.map_key(upper) if upper else [None]
            if not isinstance(lower_keys, list):
                lower_keys = [lower_keys]
            if not isinstance(upper_keys, list):
                upper_keys = [upper_keys]
        else:
            db = self._db
            index = None
            lower_keys = [None] if lower is None else [lower.oid]
            upper_keys = [None] if upper is None else [upper.oid]

        with transaction.cursor(db) as cursor:
            next_record = cursor.next_nodup if suppress_duplicates else cursor.next
            prev_record = cursor.prev_nodup if suppress_duplicates else cursor.prev
            if reverse:
                prev_record, next_record = next_record, prev_record
                lower_keys, upper_keys = upper_keys, lower_keys
                first = cursor.last
                greater_than = less
                less_than = greater
            else:
                first = cursor.first
                greater_than = greater
                less_than = less

            for lower_key in lower_keys:
                upper_key = upper_keys.pop(0)
                if index is None:
                    if not context:
                        first()
                    else:
                        cursor.set_key(context._oid)
                        if not next_record():
                            return
                else:
                    if not context:
                        if lower_key is None or not cursor.set_range(lower_key):
                            first()
                        else:
                            # welcome to duplicate key hell!
                            # if in reverse mode, for duplicates we're on the first matching dup
                            # and we need to be on the last, so skip to the next non-dup, then skip
                            # back 1. If next nodup failes, we're at the end of the index ...
                            if reverse:
                                cursor.last_dup()
                                if cursor.key() != upper_key:
                                    cursor.prev_nodup()
                    else:
                        if index.duplicates:
                            cursor.set_key_dup(context.key, context._oid)
                        else:
                            cursor.set_key(context.key)
                        if not next_record():
                            return

                if lower_key:
                    if cursor.key() and (less_than(cursor.key(), lower_key) or (cursor.key() == lower_key and not inclusive)):
                        next_record()
                        if cursor.key() and less_than(cursor.key(), lower_key):
                            return

                results = 0
                while cursor.key() and not (page_size and results == page_size) and not (
                    upper_key and (greater_than(cursor.key(), upper_key) or (cursor.key() == upper_key and not inclusive))):
                    result = FilterResult(self, index, cursor, txn=transaction)
                    if not callable(expression) or expression(result.doc):
                        results += 1
                        yield result
                    next_record()

    @wrap_reader_yield
    def match(
            self,
            index_name: str = None,
            text: str = None,
            start: Optional[int] = 0,
            limit: Optional[int] = 0,
            countonly: bool=False,
            txn: Optional[TXN]=None) -> Generator[MatchResult, None, None]:
        """
        Provides an indexed lookup into an Inverted Word (full-text) Index.This provides a 
        list of primary keys relating to the results of the search. Note that for large
        datasets that may result in thousands of responses, using "limit" is advisable. A 
        combination of start+limit can be used to provide pages result sets.

        index_name - the name of the IWX index to search
        text - the text to search for (sequence of words)
        start - the index into the result set to start from
        limit - the maximum number of results to return
        countonly - if true, just return the number of matches found
        txn - an optional transaction wrapper
        
        > Returns generator for "MatchResult" objects
        """
        if index_name is None or index_name not in self.data:
            raise NoSuchIndex()  # pragma: no cover
        index = self.data[index_name]
        return index.ftx_query(text, start, limit, countonly, txn)

    @wrap_reader
    def lexicon(
            self,
            index_name: str = None,
            text: str = None,
            max: int=0,
            txn: Optional[TXN]=None) -> Generator[str|int, None, None]:
        """
        Query the Lexicon for an IWX index. For a given partial string it will return a list
        of matching words together with the number of times the word appears in a document.
        
        index_name - the name of the index whose Lexicon we want to query
        text - the partial string to look up
        max - the maximum number of results to return
        txn - an optional transaction wrapper
        
        > Returns a generator for (word, count)
        """
        if index_name is None or index_name not in self.data:
            raise NoSuchIndex()  # pragma: no cover
        index = self.data[index_name]
        return index.iwx_lexicon(text, max=max, txn=txn)

    def dump(self, index_name, debug=False):
        """
        Debugging only - DO NOT USE
        """
        index = self.data[index_name]
        return index.dump(debug)

    def watch(self, callback: Callable=None) -> None:
        """
        Set up a handler to be executed when this table is changed. This should be done once per
        session when the table is opened.
        
        callback - the async function to be called when the table is changed
        """
        self._database._auditor.watch(self.name, callback)

    def unwatch(self, callback: Callable=None, txn: Optional[TXN|WriteTransaction]=None) -> None:
        """
        Clear a table change handler entry for this table. The callback passed should be the same
        as the handler passed to 'watch'.
        
        callback - the async function to be called when the table is changed
        """
        self._database._auditor.unwatch(self.name, callback)

    def export_to_file (self, filename, force=False):
        """
        Utility routine to dump the contents of a tabel to a file in JSON format.
        
        filename - the name of the file to dump the table to
        force - overwrite the file if it already exists
        
        > Returns the number of records dumped to the file
        """
        path = Path(filename)
        if path.exists() and not force:
            raise FileExistsError
        with open(filename, 'w') as io:
            count = 0
            io.write('{\n')
            for result in self.filter():
                if count: io.write(',\n')
                io.write('  "' + result.doc.key + '": ')
                dump(result.doc.doc, io)
                count += 1
            io.write('\n}\n')
        return count

    def import_from_file (self, filename):
        """
        Utility routine to load a table from a JSON format file, ideally one previously exported,
        otherwise you will need to ensure the appropriate JSON format manually. 
        
        filename - name of the file to load
        
        > Returns the size of the imported file
        """
        path = Path(filename)
        if not path.exists():
            raise FileNotFoundError
        with open(filename, 'r') as io:
            data = load(io)
            for key in data:
                doc = Doc(dict(data[key], **{'key': key}))
                self.append(doc)
        return len(data)
