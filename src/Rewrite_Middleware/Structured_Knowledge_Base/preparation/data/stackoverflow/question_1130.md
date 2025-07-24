# Looking for precision on how ROW_OVERFLOW_DATA happen
[Link to question](https://stackoverflow.com/questions/6037724/looking-for-precision-on-how-row-overflow-data-happen)
**Creation Date:** 1305669957
**Score:** 1
**Tags:** sql-server, sql-server-2005, database-design, optimization, normalization
## Question Body
<p>I'm currently in the initial phases of planning a rewrite for a large module in our CRM application.  </p>

<p>One area I am currently looking into is database optimization, I haven't made any decision yet but I just want to make sure I understand the concept of ROW_OVERFLOW_DATA properly - <a href="http://msdn.microsoft.com/en-us/library/ms186981.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/ms186981.aspx</a></p>

<p>We are using SQL server 2005, it's my understanding that the row size limit is 8,060 bytes and that after that overflow will occur.</p>

<p>I ran a query to get my max row size for a particular read intensive database</p>

<pre><code>SELECT OBJECT_NAME (sc.[id]) tablename
, COUNT (1) nr_columns
, SUM (sc.length) maxrowlength
FROM syscolumns sc
join sysobjects so
on sc.[id] = so.[id]
WHERE so.xtype = 'U'
GROUP BY OBJECT_NAME (sc.[id])
ORDER BY SUM (sc.length) desc
</code></pre>

<p>This gave me a few tables with a maxrowlength that was sligtly above 8,000, but under 10,000.  Another query shows that the average row size is actually quite small, around 1,000 bytes.</p>

<p>My question is: is ROW_OVERFLOW_DATA based on each row or is it per column? Once the 8,060 bytes limit is expanded is the entire column that caused it to overflow moved to another page or is it only the specific row?</p>

<p>So for example given the following simplified schema:</p>

<pre><code>col1 (int) | col 2 (varchar (4000)) | col 3(varchar(5000))
    1      |    4000 characters   |    5000 characters ***This row is overflowing
    2      |    4000 characters   |    100 characters
    3      |    150 characters    |    150 characters
    4      |    500 characters    |    600 characters
</code></pre>

<p>Would every the col 3 of row 1 to 4 get replaced by a 24 bytes pointer or only rowID 1?</p>

<p>I am wondering cause if it's every row gets a pointer it becomes important to fix it, if it's only a few rows maybe we can take the performance hit.</p>

<p>Also, I've seen many blogs suggesting to move nullable columns toward the end of the database so that if the values are in fact NULL they don't take any row space.  Is this true? We tend to keep our timestamp and tracking columns at the end cause it's easier to visualize.  Now I am wondering if maybe we shouldn't move them further up as they are never NULL.</p>

## Answers
### Answer ID: 6040013
<p>If you have one row in, say, a 100 million that overflows would you move the whole column? No.</p>
<p>For reference, a <a href="http://technet.microsoft.com/en-us/library/2008.12.sqlqa.aspx" rel="nofollow noreferrer">technet article</a> from Paul Randal who is the God of this stuff (my bold)</p>
<blockquote>
<p>The feature you are using, row-overflow, is great for allowing the <strong>occasional row</strong> to be longer than 8,060 bytes, but it is not well suited for the <strong>majority of rows</strong> being oversized and can lead to a drop in query performance, as you are experiencing.</p>
<p>The reason for this is that when a row is about to become oversized, one of the variable-length columns <strong>in the row</strong> is pushed &quot;off-row.&quot; This means the column is taken from the row on the data or index page and moved to a text page. In place of the old column value, a pointer is substituted that points to the new location of the column value in the data file.</p>
</blockquote>
<p>And <a href="http://msdn.microsoft.com/en-us/library/ms189051.aspx" rel="nofollow noreferrer">MSDN</a> (my bold)</p>
<blockquote>
<p><strong>ROW_OVERFLOW_DATA Allocation Unit</strong></p>
<p>For every partition used by a table (heap or clustered table), index, or indexed view, there is one ROW_OVERFLOW_DATA allocation unit. This allocation unit contains zero (0) pages until a data row with variable length columns (varchar, nvarchar, varbinary, or sql_variant) in the IN_ROW_DATA allocation unit exceeds the 8 KB row size limit. When the size limitation is reached, SQL Server moves the column with the largest width from <strong>that row</strong> to a page in the ROW_OVERFLOW_DATA allocation unit. A 24-byte pointer to this off-row data is maintained on the original page.</p>
</blockquote>
<p>As for your NULLable columns, this is false. NULLable columns are stored at the end of the disk structure anyway regardless of column order in the table definition. And a reference from <a href="http://www.sqlskills.com/blogs/paul/post/Inside-the-Storage-Engine-Anatomy-of-a-record.aspx" rel="nofollow noreferrer">Paul Randal: Inside the Storage Engine: Anatomy of a record</a> again. Any some previous answers <a href="https://stackoverflow.com/search?q=user:27535%20anatomy">from me here on SO</a></p>

### Answer ID: 6037759
<p>Only if a particular row overflows will the offending data <em>for that row</em> be moved off into a separate overflow page - imagine the headache if the entire table needed rebuilding just because one value in one column overflowed!</p>

<p>I'd not heard of the idea of moving NULLables to the end of the table - I'll have to check into that!</p>

