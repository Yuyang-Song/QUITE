# SQLite &quot;automatic index on MyTable(Id)&quot; when Field is the primary key of table
[Link to question](https://stackoverflow.com/questions/39128296/sqlite-automatic-index-on-mytableid-when-field-is-the-primary-key-of-table)
**Creation Date:** 1472055127
**Score:** 2
**Tags:** c#, sql, sqlite
## Question Body
<p>I have a complex C# program that uses dynamically built queries to read from a SQLite database.
I notice when I run the program under the debugger, I get lots of output like:</p>

<pre><code>SQLite warning (284): automatic index on MyTable(Id)
</code></pre>

<p>I have looked at the schema for MyTable, and Id is specified as the primary key, like this:</p>

<pre><code>CREATE TABLE MyTable (Id varchar(50) collate nocase primary key not null,
Name varchar(50) not null, 
(etc)
</code></pre>

<p>I thought SQLite made indexes for primary keys anyway, so why is it making another one?</p>

<p>Also, on a related note, I get a lot of automatic index warnings about sub-queries. For instance, on the query:</p>

<pre><code>SELECT MyTable.Id, MyTable.Name, Amount
FROM MyTable
LEFT JOIN (SELECT ArrangementId, Amount, AgreementDate FROM SubTable 
JOIN Organisations ON Organisations.Id = SubTable.OrganisationId AND Organisations.Direction = 1
) AS MyJoin ON MyJoin.ArrangementId = MyTable.Id
ORDER BY Id
</code></pre>

<p>Where</p>

<pre><code>MyTable has Id as the primary key
Organisations has Id as the primary key
SubTable has a unique index on ArrangementId, OrganisationId
</code></pre>

<p>EXPLAIN QUERY PLAN on the query yields:</p>

<pre><code>1|0|0|SCAN TABLE SubTable
1|1|1|SEARCH TABLE Organisations USING INDEX sqlite_autoindex_Organisations_1 (Id=?)
0|0|0|SCAN TABLE Arrangements USING INDEX sqlite_autoindex_Arrangements_1
0|1|1|SEARCH SUBQUERY 1 AS MyJoin USING AUTOMATIC COVERING INDEX (ArrangementId=?)
</code></pre>

<p>I guess SQLite isn't clever enough to realise that the subquery does not need to go into a temporary table?</p>

<p>Is there any way of rewriting the query so a subquery is avoided?</p>

## Answers
### Answer ID: 39130238
<p>A <code>collate nocase</code> column results in a <code>collate nocase</code> index. That index cannot be used if the lookup does not use the same collation.
(Comparisons with that column use <code>nocase</code> by default, but this does not help when the comparison is against another column with a different collation.)</p>

<p>If this query is important, consider creating a second index with the correct collation.</p>

<hr>

<p>In the second query, the database <em>must</em> evaluate the subquery using a temporary table because it is the right operand of a left outer join (<a href="http://www.sqlite.org/optoverview.html#flattening" rel="nofollow">rule 3</a>).</p>

<p>You could try to rewrite the query as a series of simple joins, if you're sure that the meaning stays the same:</p>

<pre class="lang-sql prettyprint-override"><code>FROM MyTable
LEFT JOIN SubTable ON MyTable.Id = SubTable.ArrangementId
LEFT JOIN Organisations ON Organisations.Id = SubTable.OrganisationId
                       AND Organisations.Direction = 1
</code></pre>

### Answer ID: 39129958
<p>Try making the following changes:</p>

<ul>
<li>Make ID an integer primary key.  This will actually be an alias for the internal rowid, not a separate column.</li>
<li>Make your current ID (the varchar column) a separate column.  Optionally, add a unique constraint, if that's important.</li>
<li>In your child tables, use the integer ID instead of the varchar column.  Additionally, add a foreign key on the column.</li>
</ul>

<p>A few notes:</p>

<ul>
<li>Using an INTEGER PRIMARY KEY in <code>MyTable</code> and moving the varchar to a separate column with a unique constraint will make no difference to the size of <code>MyTable</code>.  As I mention above, the primary key column will be an alias for internal rowid column, so you aren't really adding any new columns.</li>
<li>By switching the child tables to using the integer as the foreign key, this will result in a smaller table.  Even with the addition of the foreign key constraint, your database will be smaller than it is now.  This should also make your joins faster (for large datasets, anyhow).</li>
</ul>

