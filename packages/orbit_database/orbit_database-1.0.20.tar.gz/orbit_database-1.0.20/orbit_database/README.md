# Orbit Classes

The database source code structure has evolved over time and the current version attempt to mimic the database stucture in terms of organisation. This in time may change again but the fundamental code and database structure is remarkably similar to the first version with two notable exceptions.

* The first version of the software read and wrote "dict" objects, although slightly faster this made the implementation of higer level functions like compression and pluggable serialisation more complex. Now we read and write "Doc" objects and any potenential performance implications are probably offset by newer features including things like the lazy loading of actual data objects.
* The first version wrote catalog entries directly into the LMDB primary index, which tended to get a little messy and necessitated the use of a 'metadata' table to hold additional information. Version 2 now uses a dedicated catalog which makes the code (and storage) much cleaner. Currently we support both versions and there is a tool in the source tree that can upgrade an existing database from V1 to v2.

The diagram below gives an idea of the different source modules and how they are related. Manager is presented as an enumeration of Databases, Databases is presented as an enumeration of Tables and Tables is presented as an enumeration of Indexes....

![source_structure_123](../images/source_structure.drawio.png)

So operationally for example, to get a listing of all tables within a database you can do things like;
```python
database = Manager().database('demo-database')
for table in database:
    print(dir(table))
```
To explore a database the best way to get started is to use the database shell. Although there is no formal 'query language' as per SQL databases, the shell provides an 'SQL like' shell experience, although in some respects maybe a somewhat better experience than you may be used to with SQL. For example the shell implements auto-complete for all functions which is something SQL just can't do. If you think about SQL's "select" command;
```sql
SELECT (fields) FROM (table) (etc..)
```
There is no way to auto-complete (fields) until you get to table, so the language itself prevents command line auto-complete. The Orbit DB shell however implements select as;
```sql
SELECT (table) (fields) (etc..)
```
Which DOES make auto-complete not only possible but quite nice to work with if you're not overly familiar with the database.

### Reading and Writing

As mentioned above, when you read or write a database object, you are effectively reading or writing a "Doc" object, and it's the "Doc" object that facilitates side-effects like compression and serialisation. (and in the future, encryption)

In some cases however these "Doc" objects are in turn wrapped, so when you use "filter" which is the "goto" method for revering a selection of records, you will get back "filterresult" objects, each of which wraps a "doc" object. This facilitates a number of features, not least the lazy-loading of data objects which means you can scan an index without actually loading the data per result (unless you want to). So for example linear or expression filtering a result set based on a secondary index is very quick and doesn't require an object read. Also, indexes entries are not serialised on-the-fly which makes them MUCH more efficient to access.

If you use the 'match' facility to search for text in a full-text index, this will return a 'matchresult' object whicg again wraps a "doc" object, but retains metadata relating to the full-text index entry.

### Transactions

All read and write operations are wrapped by transactions objects, whether you supply one or not. This is a feature of the LMDB database and where the ACID compliance comes from. If you do not supply a transaction reference to a given command, the library will (typically) automatically generate one for you. Note however that if you write multiple related items in this way, each will have it's own transaction and there is no rollback facility.

At any given time you can have many active read transactions (see the database config options for limits) but only one active write transaction. If you try to open a second write transaction it will block until the first one has finished. To this end, write transactions should be short and sweet and not lock up or wait for external inputs, so for example don't put an http get within a write transaction (!)

The best way to handle complete write transaction is to use the 'WriteTransaction' class, and a 'with' block, for example;
```python
with WriteTransaction (database) as txn:
    table1.append(doc1)
    table2.append(doc2)
    table3.append(doc3)
```
In this instance, if all three appends work, the transaction will be automatically committed. If on the other hand one of them fails, all three write operations will be rolled back and the transaction will be cancelled. By the same token, if you decide you need to cancel and roll-back the transaction within the "with" block, just raise an exception. The exception will abort an roll-back, then you can catch the exception at a higher level.

### Serialisation

It is relatively easy to implement new serialisers although there is an argument for saying "just use ujson" becuase for most use-cases it's the fastest. That said, if you have a specific data type then other serialised might provide better performance or other desirable features. The other pressing reason for serialisers however is the RAW serialisar. If you want to store raw data blobs in a table (say small images), this can become fairly inefficient as serialising binary data can be slow and bloating. The ability to declare a table with a RAW serialiser means you can efficiently store raw unserialised data which is much faster and more space efficient than converting to a string format a JSON handler can work with.

### Compression

Currenly supported are 'snappy' and 'zstd'. The latter is fairly complex and was implemented historically for a specific purpose and not something you would see generally in use. Snappy on the other hand is relatively transparent (just turn it on) and provides pretty good compression and performance for moderately sized objects. Compression works on both serialised data and RAW data.

### Record sizes

Technically (!) you can have quite large records and the database will 'deal' with it. However, under the hood the LMDB structure works with 4096 byte pages, so anything that falls within this size boundary would tend to exhibit optimal database performance. Once record sizes start to increase objects need to be stored in multiple linked pages, so the database becomes progressively less performant. So lots of 2k sized objects and the occasional 1M sized object will probably be find. If all your objects are 1M in size, things probably won't work as quickly as you might like.

### Database size

This has been the source of some contention for quite some time (always). When you open a database you specify a maximum database size, which although it can be increased, in order to increase it you need to close the database and re-open it with the new size. (and if you have multiple processes using the database, they all need to do this at the same time)

The solution to this is to open the database with a massive maximum (that you will never need) and then you'll never have a problem. The issue with this is that although on a sparse filesystem it will only pre-allocate the space (without actually using it) it will mean that the file shows up in a directory listing as having a massive size. So "ls -lah (file)" might come back and say "64G", whereas if you look at the actual space used with "du -sh (file)" it might come back with "50k".

This "used" to be a real problem for older (no longer supported) Mac's, so maybe anything with an OS pre 2015, which may not have supported sparse filesystems, in which case it would actually allocate the entire size when opening the database (i.e. write a blank 64G file) however on more recent Mac's and Linux systems that's not an issue.

Having files show the "wrong" size in a directory listing is just a "feature" of Unix, or in this case, more specifically, Linux. Why do we need to preallocate this space? Under the hood LMDB gets it's performance and ACID functionality for the main part from the Operating System's paging system. When you open the database it MMAP's the entire database size to virtual memory, then just reads and writes that memory allowing the OS's paging system to do the IO. (which is a very clever mechanism) At the end of the day it should also be the safest and most resilient mechanism as any other mechanism would be "something else" built on top of this.

### Why not just use SQL?

Well to be fair you "could", however maybe consider some of the (subjective) pro's and con's of using a No-SQL databse written in Python vs say MySQL, which is something I've used extensively in the past;

<table style="width:95%;border:1px solid #999;margin-bottom: 1em;padding:0.3em">
<tr><th style="width:50%;background-color:#eee;color:black;border-bottom:1px solid #eee">Orbit Database Con's</th><th style="background-color:#eee;color:black;border-bottom:1px solid #eee">SQL Con's</th><tr>
<tr>
    <td>It's not a discrete system you can host and charge for</td>
    <td>It's a discrete system with significant resource requirements of it's own that need to be taken into consideration</td>
</tr>
<tr>
    <td>Configuration options are limited and defined within the application</td>
    <td>It needs contineous monitoring and tuning to keep it in shape, 'Database Admin' is an actual profession.</td>
</tr>
<tr>
    <td>Access is only via Python and if you need 'C' access and performance, it's not readily available</td>
    <td>Access is via many languages, either via SQL or via a low-level API. This either means learning the "SQL" language or learning a realtively low-evel and not terribly friently API (where you probably still need to learn 'SQL')</td>
</tr>
<tr>
    <td>Skills are hard to find because it's 'new</td>
    <td>Skills are easier to find but expensive</td>
</tr>
</table>

So here comes the good stuff;

<table style="width:95%;border:1px solid #999;margin-bottom: 1em;padding:0.3em">
<tr><th style="width:50%;background-color:#eee;color:black;border-bottom:1px solid #eee">Orbit Database Pro's</th><th style="background-color:#eee;color:black;border-bottom:1px solid #eee">SQL Pro's</th><tr>
<tr>
    <td>It's not a discrete system, just a library, and it costs nothing</td>
    <td>It's a discrete system but you can charge money to set it up and maintain it</td>
</tr>
<tr>
    <td>Configuration options are limited and defined within the application</td>
    <td>There are so many bells and whistles you could turn it into a profession</td>
</tr>
<tr>
    <td>Access is only via Python, which means it's Python friendly and optimised for use with Python</td>
    <td>If you also need to use it from another language you could learn that wrapper too</td>
</tr>
<tr>
    <td>It's been designed and implemented within the last decade for modern use-cases, to run on modern technology and accessed from Python</td>
    <td>SQL is about to celebrate it's 50th birthday, it's been around the block and has been adapted to do everything for everybody</td>
</tr>
</table>

#### Your mission should you choose to accept it: write a benchmark in Python to show that the ACID compliant database of your choice, when accessed from Python, is faster then Orbit-Database (!)

#### Your second mission, to show that your database of your choice is easier to use, was scrubbed. It was deemed that even Mr Cruise would fail.

