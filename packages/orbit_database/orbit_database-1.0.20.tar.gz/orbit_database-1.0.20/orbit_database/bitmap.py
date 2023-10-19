"""
██████╗ ██╗████████╗███╗   ███╗ █████╗ ██████╗ ██████╗ ██╗   ██╗
██╔══██╗██║╚══██╔══╝████╗ ████║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
██████╔╝██║   ██║   ██╔████╔██║███████║██████╔╝██████╔╝ ╚████╔╝ 
██╔══██╗██║   ██║   ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝  
██████╔╝██║   ██║   ██║ ╚═╝ ██║██║  ██║██║  ██╗██║        ██║   
╚═════╝ ╚═╝   ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   

Bitmap is responsible for managing the bitmap chains that drive the Inverted Word 
Indexes (full-text indexes). A full write-up is needed to properly describe 
how these indexes work, but essential for each word there is a bitmap that represents
whether that word is present in any given document. (so unoptimised, bits required = 
documents * unique words) The trick is to only store bits when they're set .. (!)
"""

from struct import pack, unpack
from lmdb import Transaction as TXN
from orbit_database.decorators import OrbitTransaction
import re
from functools import reduce
from typing import TypeVar

Table = TypeVar('Table')

try:
    from loguru import logger as log
except Exception:
    import logging as log


class Bitmap:
    """
    o CHUNK_SIZE - the size of each item in the bitmap chain
    """

    CHUNK_SIZE = 1000
    PAGE_SIZE = CHUNK_SIZE * 8

    def __init__(self, table: Table) -> None:
        """
        Instantiate the structure against a reference to the table that holds bitmaps
        
        table - the table that holds bitmap records
        """
        self._bitmap = table

    def update(self, word_index: int, document_index: int, value: bool, txn: OrbitTransaction) -> None:
        """
        Update a bitmap to indicate whether a given word appears in a given document
        
        word_index - the index number of the word to be updated
        document_index - the index number of the document within which the word appears
        value - True if the word appears in the document, otherwise False
        """
        section, offset = divmod(document_index, self.PAGE_SIZE)
        page_key = pack('>LL', word_index, section)
        bitmap = txn.txn.get(page_key, db=self._bitmap)
        bitmap = bytearray(self.CHUNK_SIZE if not bitmap else bitmap)
        byte, bits = divmod(offset, 8)
        if value:
            bitmap[byte] |= 1 << bits
        else:
            bitmap[byte] &= ~(1 << bits)
        txn.txn.put(page_key, bitmap, db=self._bitmap)

    def fetch(self, word_index: int, document_index: int, txn: OrbitTransaction) -> str:
        """
        Fetch a page from the bitmap index, this is a utility routine used for testing and 
        debugging, not typicall used by indexing in production.
        > Returns the bitmap page associated with the specified word / document
        
        word_index - the index number of the word to be updated
        document_index - the index number of the document within which the word appears
        """
        section, offset = divmod(document_index, self.PAGE_SIZE)
        page_key = pack('>LL', word_index, section)
        return txn.txn.get(page_key, db=self._bitmap)

    def find(self, words: list[str], txn: OrbitTransaction) -> list[int]:
        """
        This is the main search routine. It's job is to find a list of all documents in which
        all of the supplies words can be found. It's kinda horrible code to read, however top
        priority here is performance, linked with minimal complexity. For the first word is simply
        scans the bitmap and returns a list of index numbers. For subsequent words, it scans then
        logical AND's with the previous results retaining only index numbers appearing in all scans.
        Note that to optimise performance the words should appear in order of least frequent first.
        > Returns the index numbers of the documents containing all words
        
        words - a list of words to search for
        transaction - an optional transaction to wrap the operation
        """
        with txn.txn.cursor(self._bitmap) as cursor:
            word_index = words[0][1]
            if not cursor.set_range(pack('>LL', word_index, 0)):
                return None
            results = []
            for key, val in cursor:
                index, section = unpack('>LL', key)
                if word_index != index:
                    break
                masks = [int.from_bytes(val, 'little')]
                for word in words[1:]:
                    mask = txn.txn.get(pack('>LL', word[1], section), db=self._bitmap)
                    if not mask:
                        break
                    masks.append(int.from_bytes(mask, 'little'))
                else:
                    #   Here comes the magic (sorry!)...
                    #   reduce "bitwise and's" all the bitmaps together
                    #   bin converts the integer binmap to a string of 0's and 1's
                    #   [::-1] reverse sorts the string (endian convert)
                    #   finditer then find's all the 1's
                    #
                    results += [
                        section * self.PAGE_SIZE + i.start() 
                        for i in re.finditer('1', bin(reduce(lambda a,b: a & b, masks))[::-1])
                    ]
            return results

