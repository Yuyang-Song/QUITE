# Unknown table &#39;table_name&#39; in information_schema
[Link to question](https://stackoverflow.com/questions/40251700/unknown-table-table-name-in-information-schema)
**Creation Date:** 1477440600
**Score:** 0
**Tags:** mysql, information-schema, database-indexes
## Question Body
<p>I want to <code>show index</code> from each table that has <code>table_schema='foo'</code> (database name).</p>

<pre><code>mysql&gt; show index from table_name from information_schema.tables where table_schema='foo';
ERROR 1109 (42S02): Unknown table 'table_name' in information_schema
</code></pre>

<p>From the error, I see that the query treats <code>'table_name'</code> as a table in <code>information_schema</code>.  How do I rewrite the query to treat <code>'table_name'</code> as a column in <code>information_schema.tables</code>?</p>

## Answers
### Answer ID: 40251807
<p>You're approaching this wrong, and you're making up syntax that doesn't exist.</p>

<p>I suggest the way you want to get the indexes is by reading the <code>INFORMATION_SCHEMA.STATISTICS</code> table, not the <code>TABLES</code> table.</p>

<p>The following query has the same columns as <code>SHOW INDEXES</code>:</p>

<pre><code>SELECT table_name AS `Table`, Non_unique, index_name AS Key_name,
  Seq_in_index, Column_name, Collation, Cardinality, Sub_part,
  Packed, Nullable, Index_type, Comment, Index_comment 
FROM INFORMATION_SCHEMA.STATISTICS 
WHERE table_schema = 'foo';
</code></pre>

<p>You might think there should be an I_S table called "INDEXES" but in fact the system table for index objects is named "STATISTICS". Go figure.</p>

