"""          
 █████╗ ██╗   ██╗██████╗ ██╗████████╗   ██████╗ ██╗   ██╗
██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝   ██╔══██╗╚██╗ ██╔╝
███████║██║   ██║██║  ██║██║   ██║      ██████╔╝ ╚████╔╝ 
██╔══██║██║   ██║██║  ██║██║   ██║      ██╔═══╝   ╚██╔╝  
██║  ██║╚██████╔╝██████╔╝██║   ██║   ██╗██║        ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝                   

This module is responsible for the AUDITING sub-system which drives Real Time 
change monitoring and Replication. Open the database with auditing enabled in only 
ONE process at a time. That process will run the flusher which in turn activates 
associated actions when changes are detected. Typically include this feature in the 
process which accepts client connections.
"""
from posix_ipc import Semaphore, ExistentialError, O_CREAT
from enum import Enum
from threading import Thread
from struct import pack, unpack
from asyncio import get_event_loop, run_coroutine_threadsafe
from hashlib import new as new_hash
from orbit_database.doc import Doc
from orbit_database.serialiser import SerialiserType
from typing import TypeVar, List, Callable
from typing_extensions import Self
from lmdb import Transaction as TXN

try:
    from loguru import logger as log
except Exception:
    import logging as log

Database = TypeVar('Database')
EventLoop = TypeVar('EventLoop')
Table = TypeVar('Table')


class AuditEntry(Enum):
    """
    AuditEntry is used to classify each record written to the 'autit table', assuming
    that auditing is enabled for the table in question. Meaning is relatively obvious and NONE
    should never be used.
    """
    NONE = 0
    APPEND = 1
    SAVE = 2
    DELETE = 3


class Auditor:
    """   
    o   MAX_DOCS - the maximum number of audit records the flusher will process at a time
    """

    # UUID_KEY = '__uuid__'
    MAX_DOCS = 250

    @property
    def uuid (self) -> str:
        """
        Return the unique identified for this database based on the databased path    
        """
        return self._uuid
    
    def __init__(self, database: Database):
        """
        Set up an instance of the Audior Object
        
        database - an Orbit Database object
        """
        self._database = database
        self._thread = None
        self._table = None
        self._uuid = None
        self._semaphore = None
        self._handlers = {}
        self._finished = False
        self._auditing = False
        self._tasks = []

    def open(self, auditing: bool=False) -> Self:
        """
        Each process needs to open the auditor so that each process has the
        ability to write to the audit log. Only one process should call open
        with auditing enabled.
        > Returns a reference to self
        
        auditing - whether the flusher process should be executed
        """
        hObj = new_hash('sha1')
        hObj.update(str(self._database._path).encode())
        self._uuid = hObj.hexdigest()
        if self._database.index_version == 1:
            audit_table_name = '__audit_table__'
        elif self._database.index_version == 2:
            audit_table_name = '@@audit_table@@'

        self._table = self._database.table(audit_table_name)
        try:
            self._semaphore = Semaphore(f'/{self._uuid}', flags=O_CREAT)
        except (ExistentialError, ValueError) as e:                   # pragma: no cover
            raise Exception(f'audit error: {str(e)} // {self._uuid}')   # pragma: no cover
        self._auditing = auditing                   
        if auditing:
            self._finished = False
            self._thread = Thread(target=self._flusher, args=(get_event_loop(),), daemon=True)
            self._thread.start()
        return self

    def _flusher (self, loop: EventLoop) -> None:
        """
        The flusher should be run in one process at any given time. It is responsible for
        listening to database changes and calling any event handlers that have been set up
        to respond to said changes.
        
        loop - the Event Loop to pass through to event handlers
        """
        try:
            while True:
                self._semaphore.acquire()
                if self._finished:
                    break
                while self._table.records():
                    self._flush(loop)
        except KeyboardInterrupt:       # pragma: no cover
            pass                        # pragma: no cover
        except Exception as e:          # pragma: no cover
            log.exception(e)            # pragma: no cover
        finally:
            self._semaphore.close()
            self._table.close()
       
    def _flush (self, loop: EventLoop) -> None:
        """
        This routine is exclusively called by the flusher when changes have been detected
        and runs until there are no outstanding records in the audit table. When there are
        multiple changes outstanding it will attempt to process up to MAX_DOCS change record
        at a time and submit them to change handlers as batches. This allows multiple change
        handlers to run in parallel and also leaves a little room for progress bars / indicators
        to get a little air from time to time.
        
        loop - the Event Loop to pass through to event handlers
        """
        while True:
            results = {}
            to_delete = []
            for result in self._table.filter(page_size=self.MAX_DOCS):
                try:
                    if result.doc._t not in results:
                        results[result.doc._t] = []
                    event = result.doc
                    results[result.doc._t].append(event)
                    to_delete.append(event.key)
                except UnicodeDecodeError:
                    log.error(f'failed to remove audit entry: {event.oid}')
            for table, events in results.items():
                try:
                    if table not in self._handlers:
                        run_coroutine_threadsafe(self.default_handler(table, events), loop)
                    else:               
                        for fn in self._handlers[table]:
                            run_coroutine_threadsafe(fn(events), loop)
                except Exception as e:      # pragma: no cover
                    log.exception(e)        # pragma: no cover
            self._table.delete(to_delete)
            if len(results) < self.MAX_DOCS:
                break
            
    async def default_handler(self, table: Table, docs: List[Doc]) -> None:
        """
        This is called when you enable auditing for a given table but do not implement a handler 
        (with table->watch).
        > Returns a reference to self
        
        table - the table on which the change was detected
        docs - a list of change records
        """
        for doc in docs:
            log.success(f'default[{table}]: {str(doc.doc)}')
            
    def close(self) -> None:
        """
        Close the auditor and release the associated semaphore
        > Returns a reference to self
        """
        self._finished = True
        self._semaphore.release()
        return self
            
    def watch(self, table: Table, callback: Callable) -> None:
        """
        Install a handler to be called when a change is detected on the specified table.
        > Returns a reference to self
        
        table - the table to monitor
        callback - the asynchronous routine to call when a change is detected
        """
        if callback:
            if table not in self._handlers:
                self._handlers[table] = []
            self._handlers[table].append(callback)
        return self
    
    def unwatch(self, table: Table, callback: Callable) -> None:
        """
        Un-install a handler to be called when a change is detected on the specified table.
        > Returns a reference to self
        
        table - the table to monitor
        callback - the asynchronous routine to call when a change is detected
        """
        if table in self._handlers:
            self._handlers[table] = list(filter(lambda entry: entry != callback, self._handlers[table]))
        return self

    def save(self, table: Table, doc: Doc, txn: TXN) -> bool:
        """
        Add a record to the audit table to record a 'save' event (record update). This will 
        be called automatically when a table with auditing turned on is updated.
        > Return True on success or False on failure
        
        table - the table which was updated
        doc - the changed record
        txn - an transaction to wrap the operation
        """
        return self.put(table, doc, AuditEntry.SAVE.value, transaction=txn)

    def delete(self, table: Table, doc: Doc, txn: TXN) -> bool:
        """
        Add a record to the audit table to record a 'delete' event. This will 
        be called automatically when a table with auditing turned on is subject 
        to a record deletion.
        > Return True on success or False on failure
        
        table - the table which was updated
        doc - the changed record
        txn - an transaction to wrap the operation        
        """        
        return self.put(table, doc, AuditEntry.DELETE.value, transaction=txn)

    def append(self, table: Table, doc: Doc, txn: TXN) -> bool:
        """
        Add a record to the audit table to record a 'append' event. This will 
        be called automatically when a table with auditing turned on has a new 
        record appended.
        > Return True on success or False on failure
        
        table - the table which was updated
        doc - the changed record
        txn - an transaction to wrap the operation
        """        
        return self.put(table, doc, AuditEntry.APPEND.value, transaction=txn)
    
    def put(self, table: Table, doc: Doc, type: AuditEntry, transaction: TXN=None):
        """
        Common put routine to actually add a record to the audit table. The table uses 
        integer primary key in order to ensure consisten sequential record numbering. Audit
        table records have primary keys 0..n where (n) is the number of records in the table. 
        Once the table has been flushed, number starts again at zero.
        > Return True on success or False on failure
        
        table - the table on which a change was detected
        doc - the changed record
        type - the action type (SAVE, DELETE, APPEND)
        transaction - an transaction to wrap the operation
        """
        if not transaction._semaphore:
            transaction._semaphore = self._semaphore
        with transaction.txn.cursor(db=self._table._db) as cursor:
            if not cursor.last():
                oid = 0
            else:
                try:
                    oid = unpack('=Q', cursor.key())[0] + 1
                except Exception as e:                                          # pragma: no cover
                    log.exception(e)                                            # pragma: no cover
                    log.error(f'Key={cursor.key()} / {cursor.value()}')         # pragma: no cover
                    return
            oid = pack('=Q', oid)
            record = Doc({
                't': table.name,
                'o': doc.oid.decode(),
                'e': type,
                'c': '' if table.codec == SerialiserType.RAW else doc.doc
            })
            return transaction.txn.put(oid, self._table._compressor(record), db=self._table._db)
    