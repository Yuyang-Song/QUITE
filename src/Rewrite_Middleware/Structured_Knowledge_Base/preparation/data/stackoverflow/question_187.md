# Elegant way to SELECT a column based upon a variable / query result?
[Link to question](https://stackoverflow.com/questions/16041423/elegant-way-to-select-a-column-based-upon-a-variable-query-result)
**Creation Date:** 1366127200
**Score:** 3
**Tags:** sql, sql-server, sql-server-2008
## Question Body
<p>I have a scalar function which returns a <code>VARCHAR</code> of a column name.</p>

<p>I would like to use this result to base a select query upon, so:</p>

<pre><code>SELECT dbo.udf_GetColName('Val1', ColumnFromThisTable, etc) AS myCol
FROM tbl_ThisTable WHERE ...
</code></pre>

<p>At the moment, this is correctly listing the actual output of the UDF, the column name, for each value.</p>

<p>What I would like is for the select statement to return the <em>value of the column</em> returned from the function, so:</p>

<pre><code>SET @sql = 'SELECT ' + dbo.udf_GetColName('Val1', ColumnFromThisTable, etc) + ' AS myCol
FROM tbl_ThisTable WHERE ... '
</code></pre>

<p>And run <code>EXEC sp_executesql</code></p>

<p>Is there a better way than the dynamic SQL route? Some way that SQL can query that column as output from the UDF?</p>

<hr>

<p><em><strong>EDIT TO ADD</em></strong></p>

<p>This is where the business need to manage the rules upon which the output is selected hence they need to be in an updateable table. If they're hardcoded into the <code>SELECT</code> of Table-Valued functions then it is no longer the business that control them.</p>

<p>So yes, the query is very customisable but would be, in this instance "a good thing".</p>

<p>Additionally, there is a finite number of parameters into <code>udf_GetColName</code>. It receives a source column name, a source column value, which makes a lookup in the rules table. Should the rule find a match of that column to that value, an <code>output column</code> is selected and returned otherwise a default <code>output column</code> is used. This is the column that needs to be selected, hence could potentially be quite different to the input or input value.</p>

<p>As said, I'm happy to hear any other ideas and of course if this is silly and another route should be picked!</p>

<hr>

<p><em><strong>FINAL EDIT FOR THE DAY BEFORE I GO HOME</em></strong></p>

<p>I'm looking for a way to select which columns to use from <code>tbl_ThisTable</code>, based upon other columns values in <code>tbl_ThisTable</code>.</p>

<p>These rules as to which column to use need to be easily updateable within a table - a major limitation is the interface / front end to the database - we can only return straight datasets so can't use the front end to make this decision / concatenate multiple datasets etc...</p>

<p>If there's a good way to deploy these rules, which can be updated within the database without rewriting code, I'd love to hear them. I'm just testing this at the moment, so design is flexible.</p>

## Answers
### Answer ID: 16041826
<p>Rewind,</p>

<p>rather than</p>

<pre><code>SET @sql = 
    'SELECT ' + dbo.udf_GetColName('Val1', ColumnFromThisTable, etc) +
        ' AS myCol FROM tbl_ThisTable WHERE ... '
</code></pre>

<p>why not just do</p>

<pre><code>SELECT Val1 [myCol] FROM tbl_ThisTable WHERE ...
</code></pre>

<p>in the first place?</p>

<p>Make the caller do the branching.</p>

<hr>

<p>What I mean is, generate your SQL in the client using an ORM of your choice.</p>

<p><strong>EDIT</strong></p>

<hr>

<p>use <code>sp_executesql</code> and read <a href="http://www.sommarskog.se/dynamic_sql.html" rel="nofollow">Sommarskog</a></p>

<p>More generally, I believe your data could be normalised in such a way that you could achieve what you want with join conditions rather than dynamic column selection. Without the actual schema and example data I can't quite visualise the answer.</p>

### Answer ID: 16041532
<p>The only other way that I can think of is to use a case statement:</p>

<pre><code>select (case when udf_GetColName('Val1', . . .) = 'Col1' then Col1
             when udf_GetColName('Val1', . . .) = 'Col2' then Col2
             . . .
       ) as MyCol
from tbl_ThisTable . . .
</code></pre>

<p>The dynamic SQL seems simpler.  In both cases, though, be careful about types.  With the <code>case</code>, this would return the type of the first <code>then</code>.  With the dynamic SQL, the type of the return value depends on the type of the underlying column.</p>

