"""
██╗██╗    ██╗██╗  ██╗   ██████╗ ██╗   ██╗
██║██║    ██║╚██╗██╔╝   ██╔══██╗╚██╗ ██╔╝
██║██║ █╗ ██║ ╚███╔╝    ██████╔╝ ╚████╔╝ 
██║██║███╗██║ ██╔██╗    ██╔═══╝   ╚██╔╝  
██║╚███╔███╔╝██╔╝ ██╗██╗██║        ██║   
╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝   

The Inverted Word Index module takes care of all our full-text indexing needs. It's used 
as a base for the 'index' class and provides functionality for both an index and a Lexicon.
The mechanism uses a sparse bitmap to map words into documents, so the amount of storage 
can be approximated to 1 bit per word for every document it appears in. Obviously we're 
storing in batches so it's not quite that efficient, but in principle the storage 
requirements are sensitive to the number of words being trackes, and less-so the number 
of documents. (so plays well with data containing common symbols, i.e. language text)
"""
from collections import Counter
from struct import pack, unpack
from lmdb import Transaction, Cursor, BadValsizeError
from typing import List, Optional
from typing_extensions import Self
from orbit_database.doc import Doc
from orbit_database.bitmap import Bitmap
from orbit_database.decorators import wrap_reader, wrap_writer, OrbitTransaction
from ujson import loads, dumps
from functools import wraps
from time import time
from os import times

try:
    from loguru import logger as log
except Exception:  # pragma: no cover
    import logging as log  # pragma: no cover


class InvertedWordIndex:
    """
    This class is a sub-class of "Index" and extends the functionality of "Index". Note that 
    the more common or repeated words used, the more efficient we are, so disallowing lots of 
    larger words or lots of words unsed very infrequently, makes things more efficient. This 
    is going to be down to your used of tokeniser and choice of 'stop' words. Larger CHUNK's 
    makes searching faster, Smaller CHUMKS makes for more efficient storage
    
    o BITMAP_CHUNK  - how many bits we are going to store in a block
    """
    BITMAP_CHUNK = 1000

    def __init__(self, config=None):
        """
        Instantiate only if the index has been configured as of IWX type
        
        config - is the index configuration dictionary for this index
        """
        config = getattr(self, '_conf', config or {})
        self._iwx = config.get('iwx')
        self._iwx_cache = None
        self._lexicon = None
        self._docindx = None
        self._docrindx = None
        self._bitmap = None
        self._words = None
        self._map = None

    def open(self, txn: OrbitTransaction) -> None:
        """
        Open the IWX meta tables only if we are confifured to be an IWX index
        
        txn - optional transaction wrapper
        """
        if self._iwx:
            if not hasattr(self, 'name') or self._table._database.index_version == 1:
                self._lexicon = self.env.open_db(key=self.iwx_path('lexicon'), txn=txn.txn)
                self._docindx = self.env.open_db(key=self.iwx_path('docindx'), txn=txn.txn)
                self._docrindx = self.env.open_db(key=self.iwx_path('docrindx'), txn=txn.txn)
                self._bitmap = self.env.open_db(key=self.iwx_path('bitmap'), txn=txn.txn)
                self._words = self.env.open_db(key=self.iwx_path('words'), txn=txn.txn)
            else:
                index_name = self.name
                table_name = self._table.name
                catalog = self._table._database._cat
                conf = catalog.get_metadata(table_name, index_name, txn=txn)
                self._lexicon = self.env.open_db(conf['lexicon'].encode(), txn=txn.txn)
                self._docindx = self.env.open_db(conf['docindx'].encode(), txn=txn.txn)
                self._docrindx = self.env.open_db(conf['docrindx'].encode(), txn=txn.txn)
                self._bitmap = self.env.open_db(conf['bitmap'].encode(), txn=txn.txn)
                self._words = self.env.open_db(conf['words'].encode(), txn=txn.txn)

            self._map = Bitmap(self._bitmap)
            return True
        return False
    
    @wrap_reader
    def words (self, txn: Optional[OrbitTransaction]=None) -> int:
        """
        Query the number of words in the lexicon
        
        txn - optional transation wrapper
        
        > Returns the number of words used in the index
        """
        if not self._iwx:
            return 0
        return txn.txn.stat(self._lexicon).get('entries', 0)

    def empty(self, txn: OrbitTransaction) -> None:
        """
        Clear this index without deleting the infrastruture of the index
        
        txn - optional transation wrapper
        """
        if not self._iwx:
            return False
        return self.iwx_empty(txn, False)

    def drop(self, txn: OrbitTransaction) -> None:
        """
        Clear this index and remove the Index infrastructure
        
        txn - optional transation wrapper
        """
        if not self._iwx:
            return False
        txn.txn.drop(self._words, delete=True)
        return self.iwx_empty(txn, True)       

    def save(self, old_doc: Doc, new_doc: Doc, txn: OrbitTransaction):
        """
        Update the Lexicon and Index entries for a given document.
        
        old_doc - the document previously stores which is to be updated
        new_doc - the document to replace the old document with
        txn - a transaction wrapper
        """
        if not self._iwx:
            return False
        Lexicon(self).from_oid(old_doc.oid, txn).delete(txn)
        self.put(new_doc, txn)
        return True

    def delete(self, doc, txn: OrbitTransaction):
        """
        Delete the entries from the Lexicon and Index that relate to a specific document
        
        doc - the document to which the index entries relate
        txn - a transaction wrapper
        """
        if not self._iwx:
            return False
        # self.iwx_delete(doc.oid, txn)
        Lexicon(self).from_oid(doc.oid, txn).delete(txn)
        return True

    def put(self, doc, txn: OrbitTransaction):
        """
        Write Lexicon and Index entries for a new document that wasn't previously 
        present in the index.
        
        doc - the document to write
        txn - a transaction wrapper
        """
        if not self._iwx:
            return False
        self.write(doc.oid, doc.words, txn=txn)
        return True

    def put_cursor(self, cursor: Cursor, txn: Transaction) -> None:
        """
        Put a new index entry based on a Cursor rather than a Doc object. This is here
        mainly to make "reindex" more elegant / readable.

        cursor - an LMDB Cursor object
        txn - an optional transaction
        """
        if not self._iwx:
            return False
        self.write(cursor.key(), None, txn=txn)
        return True
    
    def write(self, oid: str, words: List[dict], txn: OrbitTransaction):
        """
        Write Lexicon and Index entries for a new document that wasn't previously 
        present in the index. This is called by "put" .. FIXME: merge with put
        
        oid - the primary key of the document to write
        words - a list of the words to index against the document
        txn - a transaction wrapper
        """
        if not words:
            lexicon = Lexicon(self).from_oid(oid, txn)
        else:
            lexicon = Lexicon(self).from_words(oid, words, txn)
        lexicon.update_words(txn)
        if words:
            txn.txn.put(oid, dumps(words).encode(), db=self._words)

    def iwx_counts(self, txn: OrbitTransaction) -> dict:
        """
        Recover the number of entries in use for each of the five metadata tables 
        used by a given index. (lexicon, docindx, docrindx, bitmap and words)
        
        txn - a transaction wrapper
        
        > Returns a dict of key+count for each of the five tables
        """
        return {
            'lexicon':  txn.txn.stat(self._lexicon).get('entries', 0),
            'docindx':  txn.txn.stat(self._docindx).get('entries', 0),
            'docrindx': txn.txn.stat(self._docrindx).get('entries', 0),
            'bitmap':   txn.txn.stat(self._bitmap).get('entries', 0),
            'words':    txn.txn.stat(self._words).get('entries', 0)
        }

    def iwx_empty_words(self, txn: OrbitTransaction, delete=False) -> None:
        """
        Empty the words meta table. This is kept separate from the general empty 
        routine because whereas you may want to clear all the indexes, you may not 
        necessarily want to clear the historicay word usage as this can be handy for 
        auto-complete lists. Also useful if you want to rebuild an index but want 
        to retain the word order.
        
        txn - a transaction wrapper
        """
        if self._iwx:
            txn.txn.drop(self._words, delete=False)
            return True
        return False

    def iwx_empty(self, txn: OrbitTransaction, delete=False) -> None:
        """
        Empty all meta tables (except words), used by the generic table empty() method
        
        txn - a transaction wrapper
        """
        if self._iwx:
            txn.txn.drop(self._lexicon, delete=delete)
            txn.txn.drop(self._bitmap, delete=delete)
            txn.txn.drop(self._docindx, delete=delete)
            txn.txn.drop(self._docrindx, delete=delete)
            return True
        return False

    def iwx_path(self, name: str) -> str:
        """
        Produce a path string for a meta table
        
        name - meta table name, typically "lexicon | bitmap | docindx | docrindx | words"
        """
        if hasattr(self, '_table'):
            return f'_{self._table.name}={self.name}={name}'.encode()
        else:
            return f'_pytest=pytest={name}'.encode()

    def iwx_oids(self, txn: OrbitTransaction):
        """
        Get the number of entries in the "docindx" meta table which is a good indication of the 
        number of documents indexed by this index.
        
        txn - a transaction wrapper
        
        > Returns the number of documents indexed in this index
        """
        return txn.txn.stat(self._docindx).get('entries', 0)

    def resolve_idoc(self, idoc: int, txn: OrbitTransaction) -> bytes:
        """
        Lookup a document by it's unique / sequential index number
        
        idoc - the number of the document to lookup
        
        > Returns the matching primary key for this document
        """
        key = pack('>L', idoc)
        doc = txn.txn.get(key, db=self._docrindx)
        if not doc:
            return None
        return doc

    def iwx_get_words(self, oid: bytes) -> list:
        """
        Recover the list of words associated with a given document
        
        oid - the primary key for the document
        
        > Returns a list of words
        """
        with self.env.begin(db=self._words) as txn:
            raw = txn.get(oid, db=self._words)
            return loads(raw) if raw else []

    def iwx_put_words(self, oid: bytes, words: list):
        """
        Store a list of words against a given primary key
        
        oid - the primary key for the document
        words - a list of words to store against that key
        """
        with self.env.begin(db=self._words, write=True) as txn:
            try:
                txn.put(oid, dumps(words).encode(), db=self._words)
            except BadValsizeError:
                log.error(f'issue with key or words, key={oid} words={words}')
                log.error('record not indexed!!')

    def iwx_space(self, stat: dict, suffix: str='B') -> str:
        """
        Utility routine to generate a human readable string to represent the amount of storage 
        used from a given 'stat' buffer.
        
        stat - an MDB_stat buffer
        suffix - the default suffix to use
        
        > Returns a human readable formatted string representing the amount of space used
        """
        num = stat['psize'] * (stat['leaf_pages'] + stat['branch_pages'] + stat['overflow_pages'] + 2)
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def iwx_stat_format(self, name: str, stat: dict) -> str:
        """
        Utility routine used for listing meta tables and the space they use
        
        name - the name of the meta table
        stat - the stat buffer for that table
        
        > Returns a string representing the table name, number of entries and space used
        """
        return f'{name:10} records={stat["entries"]:10} size={self.iwx_space(stat):>10}'

    def iwx_analysis(self, txn: Transaction) -> dict:
        """
        Recover a dictionay of items that represent all the meta tables and the space they 
        consume in the database.

        txn - a transaction wrapper
        
        > Returns a dictional of name: size
        """
        txn = txn if isinstance(txn, Transaction) else txn.txn
        return {
            'lexicon':  self.iwx_space(txn.stat(self._lexicon)),
            'docindx':  self.iwx_space(txn.stat(self._docindx)),
            'docrindx': self.iwx_space(txn.stat(self._docrindx)),
            'bitmap':   self.iwx_space(txn.stat(self._bitmap)),
            'words':    self.iwx_space(txn.stat(self._words))
        }

    def dump(self, debug=False):
        """
        Return the contents of the Lexicon, optionally printing the contents on the console.
        
        debug - whether to 'print' the results on the console
        
        > Returns a dictionary containing "lexicon": [(word, count)]
        """
        lexicon = []
        if debug:
            print('Lexicon')
            print(f'+----------------------+----------+----------+')
            print(f'| Word                 |    Index |     Freq |')
            print(f'+----------------------+----------+----------+')
        with self.env.begin(db=self._lexicon) as txn:
            cursor = txn.cursor()
            while cursor.next():
                key = cursor.key().decode()
                index, count = unpack('>LL', cursor.value())
                lexicon.append([key, count])
                if debug:
                    print(f'| {key.strip():20} | {index:8} | {count:8} |')
        if debug:
            print(f'+----------------------+----------+----------+')

        return {'lexicon': lexicon}

    def iwx_lexicon(self, terms: list, max: int, txn: Optional[OrbitTransaction]=None) -> list[str, int]:
        """
        Query the Lexicon based on a number of terms and return the words that match the 
        partial last term. So for "Fred Blo" it would returns a list of tuples (word, count) for 
        all Lexicon entries starting with "Blo".
        
        terms - list of words to query
        int - maximum number of results to return
        
        > Returns a list of results where each result is a (word, count) tuple
        """
        words = []
        if not len(terms):
            return []
        term = terms[-1].encode()
        if not len(term):
            return []
        with txn.txn.cursor(self._lexicon) as cursor:
            if not cursor.set_range(term):
                return words
            for key, val in cursor:
                if not key.startswith(term):
                    break
                words.append([key, *unpack('>LL', val)])
                if len(words) > max:
                    break

        prefix = []
        for term in terms[:-1]:
            word = txn.txn.get(term.encode(), db=self._lexicon)
            if not word:
                continue
            prefix.append((term, *unpack('>LL', word)))

        results = []
        for word in words:
            found = self._map.find(prefix + [word], txn)
            if found:
                results.append((word[0].decode(), len(found)))
            if len(results) >= max:
                break

        results.sort(key=lambda item: item[1], reverse=True)
        return results

    def ftx_query(self, terms: list, start: int=0, limit: int=None, countonly: bool=False, txn: Optional[OrbitTransaction]=None) -> [int, list]:
        """
        Query the search index based on a number of terms returning a list of the primary keys 
        of all documents contains all of the supplied terms. (logical AND)
        
        terms - an array of words to search the index for
        start - the starting point in the result set to return
        limit - the maximum number of results to return
        countonly - if true, only return a count of the number of results
        txn - an optional transaction wrapper
        
        > Returns a tuple of (count, list) where count is the number of results and list is a list of matching keys
        """
        words = []
        default = (0, [])
        for word in terms:
            item = txn.txn.get(word.encode(), db=self._lexicon)
            if not item:
                log.debug(f'no such term: {word}')
                return default
            words.append((word, *unpack('>LL', item)))

        words.sort(key=lambda item: item[2])
        found = self._map.find(words, txn)
        self._iwx_cache = found
        notfound = 0
        if countonly:
            return len(found), []
        else:
            newfound = []
            for term in found:
                result = self.resolve_idoc(term, txn)
                if result:
                    newfound.append(result)
                else:
                    notfound += 1
            if notfound:
                log.error(f'SEARCH ERROR: {notfound} unresolved documents')
            return len(newfound), list(filter(lambda term: term, newfound))


class Lexicon:
    """
    The Lexicon class keeps track of all the words we're using and how many times 
    each word has been used.
    
    o MAX_WORD_SIZE - is the size of the largest word we're prepared to index
    """
    MAX_WORD_SIZE = 128

    def __init__(self, context: InvertedWordIndex):
        """
        Instantiate a new instance of the class
        
        context - a back reference to the Inverted word index making the call
        """
        self._table_lexicon = context._lexicon
        self._table_words = context._words
        self._table_index = context._docindx
        self._table_rindex = context._docrindx
        self._map = context._map
        self._words = None
        self._oid = None

    def from_oid(self, oid: bytes, txn: OrbitTransaction) -> Self:
        """
        Lookup the words used by a given document, stores the resulting words as a 
        Counter object in "self" and returns a reference to self.
        
        oid - primary key of the document to lookup
        txn - a transaction wrapper
        
        > Returns a reference to Self
        """
        data = txn.txn.get(oid, db=self._table_words)
        self._words = Counter(loads(data.decode()) if data else [])
        self._oid = oid
        return self

    def from_words(self, oid, words, txn: OrbitTransaction):
        """
        Store a list of words against a document reference (primary key)
        
        oid - primary key of the document
        words - the list of words to store
        txn - a transaction wrapper
        
        > Returns a reference to self
        """
        txn.txn.put(oid, dumps(words).encode(), db=self._table_words)
        self._words = words
        self._oid = oid
        return self

    def lookup_word(self, word: str, txn: OrbitTransaction) -> int:
        """
        Attempt to lookup a word in the Lexicon and return it's index number. If the word 
        doesn't currently exist, create the word with a zero count. Words are numbered 
        incrementally from zero using an auto-increment integer key.
        
        word - the word to look up
        txn - the transaction wrapper
        
        > Returns the index number of the requested word
        """
        if len(word) > self.MAX_WORD_SIZE:
            return None
        item = txn.txn.get(word, db=self._table_lexicon)
        if item:
            return unpack('>LL', item)[0]
        word_index = txn.txn.stat(db=self._table_lexicon)['entries'] + 1
        try:
            txn.txn.put(word, pack('>LL', word_index, 0), db=self._table_lexicon)
            return word_index
        except Exception as e:
            log.error(e)
            return None
        
    def lookup_document(self, oid: bytes, txn: OrbitTransaction) -> int:
        """
        Attempt to look up a document and return it's index number. If the document 
        doesn't currently exist, create a new entry.
        
        oid - the primary key of the document
        txn - a transaction wrapper
        
        > Return the index number for the document
        """
        item = txn.txn.get(oid, db=self._table_index)
        if item:
            return unpack('>L', item)[0]
        document_index = txn.txn.stat(db=self._table_index)['entries'] + 1
        try:
            txn.txn.put(oid, pack('>L', document_index), db=self._table_index)
            txn.txn.put(pack('>L', document_index), oid, db=self._table_rindex)
            return document_index
        except Exception as e:
            log.error(e)
            return None

    def update_words(self, txn: OrbitTransaction) -> None:
        """
        Update the Lexicon and Index based on what we currently hold in "words"
        
        txn - a transaction wrapper
        """
        document_index = self.lookup_document(self._oid, txn)
        for word in self._words:
            if word:
                word_index = self.lookup_word(word.encode(), txn)
                if not word_index:
                    continue
                word_index, count = unpack('>LL', txn.txn.get(word.encode(), db=self._table_lexicon))
                txn.txn.put(word.encode(), pack('>LL', word_index, count + self._words[word]), db=self._table_lexicon)
                self._map.update(word_index, document_index, True, txn)
            
    def delete(self, txn: OrbitTransaction) -> None:
        """
        Delete from the Lexicon and Index based on what we currently hold in "words"
        
        txn - a transaction wrapper
        """
        txn.txn.delete(self._oid, db=self._table_words)
        document_index = self.lookup_document(self._oid, txn)
        for word in self._words:
            try:
                word_index, count = unpack('>LL', txn.txn.get(word.encode(), db=self._table_lexicon))
                txn.txn.put(word.encode(), pack('>LL', word_index, count - self._words[word]), db=self._table_lexicon)
                self._map.update(word_index, document_index, False, txn)
            except TypeError as e:
                log.error(str(e))
                log.error(f'word={word}')