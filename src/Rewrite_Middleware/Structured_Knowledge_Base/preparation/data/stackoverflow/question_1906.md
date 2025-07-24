# Non-permanent huge external data storage in C++ application
[Link to question](https://stackoverflow.com/questions/11787808/non-permanent-huge-external-data-storage-in-c-application)
**Creation Date:** 1343954728
**Score:** 1
**Tags:** c++, data-structures, shared-libraries
## Question Body
<p>I'm rewriting an application which handles a lot of data (about 100 GB) which is designed as a relational model.</p>

<p>The application is very complex; it is some kind of conversion tool for open street map data of huge sizes (the whole world) and converts it into a map file for our own route planning software. The converter application for example holds the nodes in the open street map with their coordinate and all its tags (a lot of more than that, but this should serve as an example in this question).</p>

<p><strong>Current situation:</strong></p>

<p>Because this data is very huge, I split it into several files: Each file is a map from an ID to an atomic value (let's assume that the list of tags for a node is an atomic value; it is not but the data storage can treat it as such). So for nodes, I have a file holding the node's coords, one holding the node's name and one holding the node's tags, where the nodes are identified by (non-continuous) IDs.</p>

<p>The application once was split into several applications. Each application processes one step of the conversion. Therefore, such an application only needs to handle some of the data stored in the files. For example, not all applications need the node's tags, but a lot of them need the node's coords. This is why I split the relations into files, one file for each "column".</p>

<p>Each processing step can read a whole file at once into a data structure within RAM. This ensures that lookups can be very efficient (if the data structure is a hash map).</p>

<p>I'm currently rewriting the converter. It should now be one single application. And it should now not use separated files for each "column". It should rather use some well-known architecture to <strong><em>hold external data in a relational manner</em></strong>, like a database, but much faster.</p>

<p>=> <strong><em>Which library can provide the following features?</em></strong></p>

<p><strong>Requirements:</strong></p>

<ul>
<li><p>It needs to be very fast in <strong>iterating</strong> over the existing data (while not modifying the set of rows, but some values in the current row).</p></li>
<li><p>It needs to provide constant or near-constant lookup, similar to hash maps (while not modifying the whole relation at all).</p></li>
<li><p>Most of the types of the columns are constantly sized, but in general they are not.</p></li>
<li><p>It needs to be able to append new rows to a relation in constant or logarithmic time per row. Live-updating some kind of search index will not be required. Updating (rebuilding) the index can happen after a whole processing step is complete.</p></li>
<li><p>Some relations are key-value-based, while others are an (continuously indexed) array. Both of them should provide fast lookups.</p></li>
<li><p>It should NOT be a separate process, like a DBMS like MySQL would be. The number of queries will be enormous (around 10 billions) and will be totally the bottle neck of the performance. However, caching queries would be a possible workaround: Iterating over a whole table can be done in a single query while writing to a table (from which no data will be read in the same processing step) can happen in a batch query. But still: I guess that serializing, inter-process-transmitting and de-serializing SQL queries will be the bottle neck.</p></li>
<li><p>Nice-to-have: easy to use. It would be very nice if the relations can be used in a similar way than the C++ standard and Qt container classes.</p></li>
</ul>

<p><strong>Non-requirements</strong> <em>(Why I don't need a DBMS)</em>:</p>

<ul>
<li><p>Synchronizing writing and reading from/to the same relation. The application is split into multiple processing steps; every step has a set of "input relations" it reads from and "output relations" it writes into. However, some steps require to read some columns of a relation while writing in other columns of the same relation.</p></li>
<li><p>Joining relations. There are a few cross-references between different relations, however, they can be resolved within my application if lookup is fast enough.</p></li>
<li><p>Persistent storage. Once the conversion is done, all the data will not be required anymore.</p></li>
<li><p>The key-value-based relations will never be re-keyed; the array-based relations will never be re-indexed.</p></li>
</ul>

## Answers
### Answer ID: 11787898
<p>I can think of several possible solutions depending on lots of factors that you have not quantified in your question.</p>

<p>If you want a simple store to look things up and you have sufficient disk, <a href="http://sqlite.org" rel="nofollow" title="SQLite">SQLite</a> is pretty efficient as a database.  Note that there is no SQLite server, the 'server' is linked into your application.</p>

<p>Personally this job smacks of being <a href="http://en.wikipedia.org/wiki/Embarrassingly_parallel" rel="nofollow">embarrassingly parallel</a>.  I would think that a small <a href="http://hadoop.apache.org/" rel="nofollow">Hadoop cluster</a> would make quick work of the entire job.  You could spin it up in <a href="http://aws.amazon.com" rel="nofollow" title="amazon web services">AWS</a>, process your data, and shut it down pretty inexpensively.</p>

