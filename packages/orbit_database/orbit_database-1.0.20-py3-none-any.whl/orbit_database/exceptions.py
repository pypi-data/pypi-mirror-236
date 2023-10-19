"""
███████╗██╗  ██╗ ██████╗███████╗██████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗   ██████╗ ██╗   ██╗
██╔════╝╚██╗██╔╝██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝   ██╔══██╗╚██╗ ██╔╝
█████╗   ╚███╔╝ ██║     █████╗  ██████╔╝   ██║   ██║██║   ██║██╔██╗ ██║███████╗   ██████╔╝ ╚████╔╝ 
██╔══╝   ██╔██╗ ██║     ██╔══╝  ██╔═══╝    ██║   ██║██║   ██║██║╚██╗██║╚════██║   ██╔═══╝   ╚██╔╝  
███████╗██╔╝ ██╗╚██████╗███████╗██║        ██║   ██║╚██████╔╝██║ ╚████║███████║██╗██║        ██║   
╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝        ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚═╝        ╚═╝   

This module contains all the non-standard exceptions that the library
can generate.
"""

class IndexAlreadyExists(Exception):
    """
    Raised when you try to create an index and that index already exists. If you use
    'ensure' to create your indexes, typically this will never be a problem
    """
    pass


class DocumentDoesntExist(Exception):
    """
    Raised if you attempt to update a record that does not exist. If the record doesn't
    exist you should use 'append' first, then use 'save' subsequently to update it
    """
    pass


class InvalidKeySpecifier(Exception):
    """
    Raised if you try to delete a record and supply a key that is not of a valid type. For example
    keys cannot be of type 'dict', although multi-value keys CAN be of type 'list'
    """
    pass


class NoSuchIndex(Exception):
    """
    Raised if you attempt to use an index that does not exist
    """
    pass


class NoSuchTable(Exception):
    """
    Raised if you try to drop a table that does not exist. Typically any other table operation on a
    non-existant table will cause the table to be created
    """
    pass


class DuplicateKey(Exception):
    """
    Raised if you try to write a key into a non-duplicate index and the key already exists
    """
    pass


class TableNotOpen(Exception):
    """
    Raised of you try to train the ZSTD compression module on a table that is not open
    """
    pass


class TrainingDataExists(Exception):
    """
    Raised if you try to re-train the ZSTD module without first removing the old training data
    """
    pass


class InvalidId(ValueError):
    """
    Raised if you try to create a new ObjectId from an invalid source
    """
    pass


class InvalidSerialiser(Exception):
    """
    Raised if you are trying to use a serialiser that isn't available, OR if you are trying to
    open a table with a named serialiser that has previously been serialised with a 'different'
    serialiser
    """
    pass
