# VB.NET Access Database 255 Columns Limit
[Link to question](https://stackoverflow.com/questions/22985769/vb-net-access-database-255-columns-limit)
**Creation Date:** 1397126660
**Score:** 0
**Tags:** vb.net, linq, ms-access, limit
## Question Body
<p>I'm currently developing an application for a client using Visual Basic .NET. It's a rewrite of an application that accessed an Oracle database, filtered the columns and performed some actions on the data. Now, for reasons beyond my control, the client wants to use an Access (.mdb) database for the new application. The problem with this is that the tables have more than the 255 columns access supports so the client suggested splitting the data into multiple databases/tables.</p>

<p>Well even when the tables are split, at some point, I have to query all columns simultaneously (I did an INNER JOIN on both tables) which, of course, yields an error. The limit apparently is on number of simultaneously queryable columns not on the total number of columns. 
Is there a possiblility to circumvent the 255 columns limit somehow? I was thinking in the direction of using LINQ to combine queries of both tables, i.e. have an adapter that emulates a single table I can perform queries on. A drawback of this is that .mdb is not a first-class citizen of LINQ-to-SQL (i.e. no insert/update supported etc.).</p>

<p>As a workaround, I might be able to rewrite my stuff so as to only need all columns at one point (I dynamically create control elements depending on the column names in the table). Therefore I would need to query say the first 250 columns and after that the following 150.
Is there a Access-SQL query that can achieve something like this. I thought of something like <code>SELECT TOP 255 * FROM dbname</code> or <code>SELECT * FROM dbname LIMIT 1,250</code> but these are not valid.</p>

<p>Do I have other options?</p>

<p>Thanks a lot for your suggestions.</p>

## Answers
### Answer ID: 22987647
<p>As I know there is no way to directly bypass this problem using Access.
If you cannot change the db your only way I can think of is to make a wrapper that understand you're were the field are, automatically splits the query in more queryes and then regroup it in a custom class containing all the columns for every row.
For example you can split every table in more tables duplicating the field you're making the conditions on.</p>

<pre><code>TABLEA
Id | ConditionFieldOne | ConditionFierldTwo | Data1 | Data2 | ... | Data N |
</code></pre>

<p>in</p>

<pre><code>TABLEA_1
Id | ConditionFieldOne | ConditionFieldTwo | Data1 | Data2 | ... | DataN/2 |

TABLEA_2
Id | ConditionFieldOne | ConditionFieldTwo | Data(N/2)+1 | Data(n/2)+2 | ... | DataN |
</code></pre>

<p>and a query where is</p>

<pre><code>SELECT * FROM TABLEA WHERE CONDITION1 = 'condition'
</code></pre>

<p>become with the wrapper</p>

<pre><code>SELECT * FROM TABLEA_1 WHERE ConditionFieldOne = 'condition'
SELECT * FROM TABLEA_2 WHERE ConditionFieldOne = 'condition'
</code></pre>

<p>and then join the results.</p>

### Answer ID: 22987603
<p>The ADO.NET DataTable object has no real limitations on the number of columns that it could contain.<br>
So, once you have splitted the big table in two tables and set the same primary key in both subtables with less columns, you can use, on the VB.NET side, the <a href="http://msdn.microsoft.com/en-us/library/fk68ew7b%28v=vs.110%29.aspx" rel="nofollow">DataTable.Merge</a> method.</p>

<p>In their example on MSDN they show two tables with the same schema merged together, but it works also if you have two totally different schemas, but just the Primary key in common</p>

<pre><code> Dim firstPart As DataTable = LoadFirstTable()
 Dim secondPart As DataTable = LoadSecondTable()
 firstPart.Merge(secondPart)
</code></pre>

<p>I have tested this just with only one column of difference, so I am not very sure that this is a viable solution in terms of performance. </p>

