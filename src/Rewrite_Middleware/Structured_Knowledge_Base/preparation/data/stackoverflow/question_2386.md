# Database Views to simulate normalised tables from a single denormalised one
[Link to question](https://stackoverflow.com/questions/32269452/database-views-to-simulate-normalised-tables-from-a-single-denormalised-one)
**Creation Date:** 1440759395
**Score:** 0
**Tags:** sql-server, view, database-normalization
## Question Body
<p>We have a report store with a denormalised flat table that stores identical data to a multi-table model in a different database.</p>

<p>Flat table (example):</p>

<pre><code>| col 1 | col 2 | col 3 | timestamp |
|-------|-------|-------|-----------|
| val1  | val2  | val3  | 1/1/1990  |
| val1  | val9  | val3  | 1/1/1990  |
</code></pre>

<p>In multiple tables:</p>

<pre><code>| id1 | id2 | timestamp |
|-----|-----|-----------|
| 001 | 111 | 1/1/1990  |
| 001 | 112 | 1/1/1990  |

| id1 | col 1 | col 3 |
|-----|-------|-------|
| 001 | val1  | val3  |

| id2 | col 2 |
|-----|-------|
| 111 | val2  |
| 112 | val9  |
</code></pre>

<p>There are several old reporting queries that we would like to port over to the new flat table without having to rewrite them all up front - there are many of them and they are complex.</p>

<p>Is there a way of writing Views that can simulate a set of relational tables from the single flat table, so that the old reporting queries work without modification?</p>

## Answers
### Answer ID: 32271287
<p>HereI create <em>dynamical</em> IDs. You could also initialy make that table with fix keys, and always when adding or removing a row in the flattable do the same with  the key here. Otherwise instead of Groub by use the <code>OVER</code> statement.</p>

<pre><code>CREATE VIEW multitabkey AS
SELECT ROW_NUMBER() as key, col1, col3
FROM flattable
Group by col1, col3
</code></pre>

<p><strong>WARNING: those keys are not persistent:</strong> if you delete the first row, all others get their id one smaler than before. You have <em>dynamic</em> IDs, but they are <em>consistnet</em>.</p>

<p>If you have a translation for your Keys you can use them as following:</p>

<pre><code>CREATE VIEW multitabone AS
SELECT f.timestamp
FROM flattable as f
JOIN multitabkey as m ON m.col1 = f.col1 AND m.col3 = f.col3
Group by col1, col3
</code></pre>

<p>I assumed col1 , col2 are together a natural key.</p>

<p><strong>As mentioned, this is a workaround, your DB is not in 3rd normalform what can cause inconsistency.</strong></p>

