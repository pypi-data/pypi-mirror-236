"""
██████╗ ███████╗ ██████╗ ██████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗ ███████╗   ██████╗ ██╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝   ██╔══██╗╚██╗ ██╔╝
██║  ██║█████╗  ██║     ██║   ██║██████╔╝███████║   ██║   ██║   ██║██████╔╝███████╗   ██████╔╝ ╚████╔╝ 
██║  ██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗╚════██║   ██╔═══╝   ╚██╔╝  
██████╔╝███████╗╚██████╗╚██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║███████║██╗██║        ██║   
╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝        ╚═╝   

This module encompasses transaction wrappers. When working with LMDB every read or write operation needs to 
take place with either a read or write transaction. Although you can have many concurrent read transactions, 
there can only be one active write transaction at any point in time and if you try to open a second read 
transaction while the write it active, it will block. Most API calls are wrapped such that if there is no
currently active transaction, it will make a temporary transaction who's lifespan is the length of the API
call. So long as you are not updating multiple objects with an interdependency, it's generally safe to use
the wrappers. If on the other hand you are generating an entry in an audit log and incrementing a matching
account balance, it's best to carry out both operations within a write transaction so either both will 
succeed or neither. So for example this will be automatically wrapped and be Ok;
```
table.append(Doc{'name': 'Fred})
```
On the other hand in an instance where we're updating multiple dependent objects, you might want;
```
amount = 10.1
with WriteTransaction(db) as txn:
    account._balance += amount
    audit_table.save(Doc({'text': f'Added {amount} to account'}), txn=txn)
    account_table.save(account, txn=txn)
```
! If you choose to use "raw" LMDB transactions rather than OrbitTransaction's, the auditing won't work
"""

from typing import Any, Callable, Generator, ParamSpec, TypeVar, Concatenate
from lmdb import MapResizedError, MapFullError, Transaction
import functools

Param = ParamSpec("Param")
RetType = TypeVar("RetType")
OriginalFunc = Callable[Param, RetType]
DecoratedFunc = Callable[Concatenate[str, Param], RetType]
Database = TypeVar('Database')

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    from logging import log  # pragma: no cover


SIZE_MULTIPLIER = 1.2   # how much to scale the map_size by
PAGE_SIZE = 4096        # page size to round to


class OrbitTransaction:
    """
    Generic wrapper for read and write transactions. Typically you will use the 
    ReadTransaction and WriteTransaction classes which subclass this class. There is
    currently map resizing code here, however this will be removed in future as
    dynamic map resizing is deemed unsafe.
    """

    def __init__(self, database: Database, write: bool):
        """
        Instantiate transaction and initiate as either a read-only or read-write artifact
        
        database - a reference to the Orbit database we're working with
        write - True if this is going to be a read-write transaction otherwise False
        """
        self._env = database.env
        self._write = write
        self._semaphore = None
        self.txn = None
        self.journal = []

    def __enter__(self):
        """
        On entering a WITH block we're going to create an LMDB transaction of type based on 'write', 
        currently we will retry this if the database has been resized, however this is legacy code 
        that will be removed. (dynamic resizing is no longer supported)
        """
        while True:
            try:
                self.txn = Transaction(env=self._env, write=self._write)
                return self
            except MapResizedError:  # pragma: no cover
                if 'log' in globals():
                    log.debug(f'database RESIZED')  # pragma: no cover
                self._env.set_mapsize(0)  # pragma: no cover

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        On leaving a WITH block we either commit the transaction if the block completed without error 
        or abort the transaction if an error was detected. In the event there is no error, we also poke 
        the semaphore (if auditing is enabled) to let the change mechanism know that something has changed.
        """
        if exc_type is None:
            self.txn.commit()
            if self._semaphore:
                try:
                    self._semaphore.release()
                except Exception as e:
                    log.error(e)
                    self._semaphore = None
        else:
            self.txn.abort()


class ReadTransaction(OrbitTransaction):
    """
    This is used to wrap all read-only transactions
    """
    def __init__(self, database: Database):
        """
        Instantiate a transaction, typicall as a part of a WITH block
        ```
        with ReadTransaction(db) as txn:
            for result in table.filter(txn=txn):
                print(result)
        ```
        """
        super().__init__(database, False)


class WriteTransaction(OrbitTransaction):
    """
    This is used to wrap all read-write transactions
    """
    def __init__(self, database: Database):
        """
        Instantiate a transaction, typicall as a part of a WITH block
        ```
        with WriteTransaction(db) as txn:
            for result in table.filter(txn=txn):
                doc = result.doc
                doc._balance += 1
                table.save(doc)
        ```
        """        
        super().__init__(database, True)

def wrap_reader_yield(func: Callable) -> Callable[[OriginalFunc], DecoratedFunc]:
    """
    Decorator, use this to decorate any calls that need an explicit read transaction where the
    routine in question returns a generator. If a 'txn' variable is passed in kwargs, it will 
    be used at the transaction wrapper. If not, the decorated routine will be called within a 
    "with ReadTransaction" wrapper with the new 'txn' inserted into kwargs.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Generator[Any, None, None]:
        if kwargs.get('txn'):
            yield from func(*args, **kwargs)
        else:
            if 'txn' in kwargs:
                del kwargs['txn']
            with ReadTransaction(getattr(args[0], '_database', args[0])) as txn:
                yield from func(*args, **kwargs, txn=txn)
                return
    return wrapped


def wrap_reader(func: Callable) -> Callable[[OriginalFunc], DecoratedFunc]:
    """
    Decorator, use this to decorate any calls that need an explicit read transaction. If a 'txn'
    variable is passed in kwargs, it will be used at the transaction wrapper. If not, 
    the decorated routine will be called within a "with ReadTransaction" wrapper with
    the new 'txn' inserted into kwargs.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if kwargs.get('txn'):
            return func(*args, **kwargs)
        else:
            if 'txn' in kwargs:
                del kwargs['txn']
            with ReadTransaction(getattr(args[0], '_database', args[0])) as txn:
                return func(*args, **kwargs, txn=txn)
    return wrapped


def wrap_writer(func: Callable) -> Callable[[OriginalFunc], DecoratedFunc]:
    """
    Decorator, use this to decorate any calls that need a write transaction. If a 'txn'
    variable is passed in kwargs, it will be used at the transaction wrapper. If not, 
    the decorated routine will be called within a "with WriteTransaction" wrapper with
    the new 'txn' inserted into kwargs.
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs) -> Any:
        if kwargs.get('txn'):
            return func(*args, **kwargs)
        else:
            if 'txn' in kwargs:
                del kwargs['txn']
            with WriteTransaction(getattr(args[0], '_database', args[0])) as txn:
                return func(*args, **kwargs, txn=txn)
    return wrapped



