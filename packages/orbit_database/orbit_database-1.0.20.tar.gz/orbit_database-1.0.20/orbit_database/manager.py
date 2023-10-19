"""
███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗    ██████╗ ██╗   ██╗
████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗   ██╔══██╗╚██╗ ██╔╝
██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝   ██████╔╝ ╚████╔╝ 
██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗   ██╔═══╝   ╚██╔╝  
██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║██╗██║        ██║   
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   

The Manager module is included for instances where you may need to open and manage
multiple databases concurrently. One example of this is the database shell.

"""
from atexit import register
from collections import UserDict
from typing import Optional
from orbit_database.database import Database

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


class Manager(UserDict):
    """
    Manager is a dictionary like object the holds references to all the databases currently
    registered with the running instance. If you only ever reference one database then
    technically you can skip this object and just use the Database object.
    """

    def __init__(self, *args, **kwargs):
        """Initialise this object"""
        self._paths = {}
        self._auditing = False
        super().__init__(*args, **kwargs)
        if kwargs.get('autoclose'):
            register(self.close)

    def close(self):                 # pragma: no cover
        """
        Make sure all databases are closed
        """
        for name in self.data:       # pragma: no cover
            # log.success(f'Closing: {name}')
            self.data[name].close()  # pragma: no cover
        self.data = {}
        self._paths = {}
        # log.debug('manager has closed all databases')

    def __getitem__(self, name: str) -> Database:
        """
        > Returns the Database object associated with the supplied name

        name - the name of database
        """
        if name not in self.data:
            self.data[name] = Database()
        return self.data[name]

    def database(self, name: str, path: Optional[str]=None, config: Optional[dict]=None, auditing: bool=False) -> Database:
        """
        Open a database creating it if necessary

        name - an arbitrary name to reference the database by
        path - the path to the database files
        config - a dictionary containing configuration specifics for this database
        auditing - whether to launch the auditor / flusher process

        > Returns a reference to an open Database
        """
        # log.debug(f'database auditing={auditing}')
        if name in self.data:
            database = self.data[name]
            if database.isopen:
                return database
        if name and not path:
            path = name
            name = None
            if path in self._paths:
                database = self._paths[path]
                if database.isopen:
                    return database
        database = Database()
        database.configure(config)
        if not name:
            name = path
        database.open(path, name=name)
        self.data[name] = database
        self._paths[path] = database
        return database
