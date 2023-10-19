"""
 ██████╗ █████╗ ████████╗ █████╗ ██╗      ██████╗  ██████╗    ██████╗ ██╗   ██╗
██╔════╝██╔══██╗╚══██╔══╝██╔══██╗██║     ██╔═══██╗██╔════╝    ██╔══██╗╚██╗ ██╔╝
██║     ███████║   ██║   ███████║██║     ██║   ██║██║  ███╗   ██████╔╝ ╚████╔╝ 
██║     ██╔══██║   ██║   ██╔══██║██║     ██║   ██║██║   ██║   ██╔═══╝   ╚██╔╝  
╚██████╗██║  ██║   ██║   ██║  ██║███████╗╚██████╔╝╚██████╔╝██╗██║        ██║   
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝        ╚═╝   

This class is used to manage the V2 style table catalogue. The V1 stye catalog grew 
organically and just stored table names in the primary LLDB index, however this caused
a number of problems including limitations on table naming and the inability to rename
tables. V2 tables are far easier to manage and solve all the historical problems
associated with V1. You can upgrade from V1 -> V2 with the database shell tool, however
there is no reverse process (!)


"""

from lmdb import NotFoundError
from orbit_database.table import Table
from orbit_database.index import Index
from orbit_database.doc import Doc
from orbit_database.objectid import ObjectId
from orbit_database.exceptions import NoSuchIndex
from orbit_database.decorators import OrbitTransaction
from lmdb import Transaction as TXN
from typing import TypeVar, Generator, Optional
from typing_extensions import Self

Database = TypeVar('Database')

try:
    from loguru import logger as log
except Exception:
    import logging as log


class Catalog:
    """
    This is mostly a wrapper class to preserve historical interfaces. Rather than using table
    names directly as keys to the primary LLDB index, we now look up the table names in the
    catalog table and using the resulting ObjectId as the key.
    """

    @property
    def version (self) -> int:
        """
        > Returns the version number of this index (1 or 2)
        """
        return self._version

    def __init__(self, version: int) -> None:
        """
        Instantiate an instance based on a supplied version number
        ! TODO: we should probably add some bounds checking here
        
        version - the version number of this index (1 or 2)
        """
        self._table = None
        self._version = version

    def open (self, database: Database, txn: Optional[OrbitTransaction]=None) -> Self:
        """
        Open the named database, default to version 1 if no version has been set 
        (because for legacy databases this will be the case), otherwise attempt to
        open as a V2, open the catalog if available, otherwise create and open.
        > Returns a reference to self
        
        database - the database we want to open
        txn - an optional transaction wrapper
        """
        if not self._version:
            self._version = 1
            try:
                database.env.open_db(b'@@catalog@@', create=False, txn=txn.txn)
                self._version = 2
            except NotFoundError:
                if txn.txn.stat(database._db).get('entries', 0) == 0:
                    self._version = 2
                    database.env.open_db(b'@@catalog@@', create=True, txn=txn.txn)
        if self._version == 2:
            self._table = Table(database, '@@catalog@@', CatalogEntry).open(txn=txn)
        return self
   
    def drop (self, name: str, txn: TXN=None) -> None:
        """
        Drop the named table. In addition to deleting the entry from the primary index 
        (which should already have been done) for V2 indexes we also need to delete the
        entry from the catalog.
        
        name - the name of the table to drop
        """
        if self._version == 2:
            self._table.delete(name, txn=txn)

    def drop_index (self, table_name: str, index_name: str, txn: TXN=None) -> None:
        """
        Drop the named index from the named table. Again there is only work to do 
        here for V2 indexes, for V1 all we needed to do was delete from the LMDB
        level 1 index.
        
        table_name - the table from which we want to drop the index
        index_name - the name of the index we want to drop
        """
        if not table_name.startswith('@@') and self._version == 2:
            catalog = self._table.get(table_name, txn=txn)
            if not catalog or not catalog._indexes:
                raise NotFoundError
            if index_name not in catalog._indexes:
                raise NoSuchIndex
            catalog._indexes.pop(index_name)
            self._table.save(catalog, txn=txn)

    def indexes (self, name: str, txn: Optional[OrbitTransaction]=None) -> Generator[str, None, None]:
        """
        Return a generator which produces a list of available indexes for the
        specified table name!
        > Returns a generator which produces index names
        
        name - name of the table for which we want indexes
        txn - an optional transaction wrapper
        """
        catalog = self._table.get(name, txn=txn)
        if catalog:
            for name in catalog._indexes or []:
                yield name

    def ensure (self, table_name: str, index_name: str, iwx: bool, txn: OrbitTransaction=None) -> Doc:
        """
        Ensure than in index entry exists in the catalog and create if
        missing. IWX indexes are a special case as each index consists of
        5 files.
        
        table_name - the name of the table we're creating an index for
        index_name - the name of the index
        iwx - whether the index is an IWX index or not
        txn - an optional transaction wrapper
        > Returns a reference to the catalog entry
        """
        catalog = self._table.get(table_name, txn=txn)
        if not catalog:
            raise NotFoundError
        if not catalog._indexes:
            catalog._indexes = {}
        if index_name not in catalog._indexes:
            if iwx:
                catalog._indexes[index_name] = {
                    'iwx': True,
                    'lexicon': str(ObjectId()),
                    'docindx': str(ObjectId()),
                    'docrindx': str(ObjectId()),
                    'bitmap': str(ObjectId()),
                    'words': str(ObjectId())
                }
            else:
                catalog._indexes[index_name] = {
                    'key': str(ObjectId())
                }
            self._table.save(catalog, txn=txn)
        return catalog._indexes[index_name]

    def get_metadata (self, table_name: str, index_name: str, txn: TXN=None) -> dict:
        """
        Recover the metadata for the names index
        > Returns the metadata (as a dict) for the named index
        
        table_name - the name of the table
        index_name - the name of the index within the specified table
        txn - an optionan transaction wrapper
        """
        catalog = self._table.get(table_name, txn=txn)
        if not catalog:
            raise NotFoundError
        if not catalog._indexes:
            catalog._indexes = {}
        index = catalog._indexes.get(index_name)
        if not index:
            log.error(f'index not found: {index_name} :: {str(index)}')
            raise NotFoundError
        return index
    
    def get_conf (self, 
            db: Database,
            table_name: str,
            index_name: str,
            iwx: bool,
            txn: Optional[TXN]=None) -> dict:
        if db.index_version == 1:
            conf = db.meta.fetch_index(table_name, index_name, txn)
            if not conf._conf:
                conf = {'key': Index.index_path(table_name, index_name)}
            else:
                conf = conf._conf
        elif db.index_version == 2:
            conf = self.ensure(table_name, index_name, iwx, txn)
        else:
            raise Exception('bad catalog version number')    
        return conf
    
    def put_conf (self,
            db: Database,
            table_name: str,
            index_name: str,
            conf: dict,
            txn: Optional[TXN]=None) -> None:
        if db.index_version == 1:        
            db.meta.store_index(table_name, index_name, Doc({'conf': conf}), txn=txn)
        elif db.index_version == 2:
            self.store_index(table_name, index_name, conf, txn=txn)
        else:
            raise Exception('bad catalog version number')    

    def store_index (self, table_name: str, index_name: str, conf: dict, txn: TXN=None) -> None:
        """
        Update the catalog with the current index definition.
        
        table_name - the name of the table
        index_name - the name of the index within the specified table
        conf - the index definition (as a dictionary)
        txn - an optionan transaction wrapper
        """
        catalog = self._table.get(table_name, txn=txn)
        if not catalog:
            raise NotFoundError
        if not catalog._indexes:
            catalog._indexes = {}
        catalog._indexes[index_name] = conf
        self._table.save(catalog, txn=txn)

    def get_table_id (self, name: str, txn: TXN=None) -> ObjectId:
        """
        Recover the metadata for the names index
        > Returns table's unique ObjectId
        
        name - the name of the table
        txn - an optionan transaction wrapper
        """
        doc = self._table.get(name)
        if not doc:
            doc = Doc({'id': str(ObjectId())}, oid=name)
            self._table.append(doc, txn=txn)
        return doc._id


class CatalogEntry (Doc):
    """
    This is a dummy class to keep the ORM mechanism happy. Historically the 
    result of a search (filter) operation used to return a sequence of (Doc) 
    items. Now we're a little more specific and can return an object type 
    that is specific to the table, although in this incase we have no custom 
    properties, so essentially all we need is a Doc.
    """
    pass
