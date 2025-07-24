# Show one numeric value for group of rows with same id when group of rows contain boolean data
[Link to question](https://stackoverflow.com/questions/56788871/show-one-numeric-value-for-group-of-rows-with-same-id-when-group-of-rows-contain)
**Creation Date:** 1561630652
**Score:** 0
**Tags:** sql, sql-server
## Question Body
<p>I'm writing Node js app as a practice and I'm using an existing SQL Server database (trying to rewrite the existing .NET frontend that uses same database but lacking reporting flexibility). </p>

<p>I need to query "survey" table consisting of (guid, questionTag and value). I don't know why this table is designed like this, but I can't change it.</p>

<pre><code>guid     question   value
----------------------------
 1         q1_1     false
 1         q1_2     true
 1         q1_3     false
 1         q2_1     false
 1         q2_2     false
 1         q2_3     true
...
</code></pre>

<p>The <code>guid</code> column is a reference to another table which holds info avout the user that filled the survey.</p>

<p><code>value</code> is coming from an HTML form and represents a radio-button that user selected. User is asked two questions each with 3 possibilties.</p>

<p>I would like the end result of a query to group "q1_X" rows with same guid and "translate" their boolean values to one number - 1,2 or 3 depending on where "true" value is:</p>

<pre><code>guid     question   value
---------------------------
 1          q1        2
 1          q2        3
</code></pre>

## Answers
### Answer ID: 56789048
<p>You need string functions, like <a href="https://learn.microsoft.com/en-us/sql/t-sql/functions/left-transact-sql?view=sql-server-2017" rel="nofollow noreferrer"><code>left()</code></a>, <a href="https://learn.microsoft.com/en-us/sql/t-sql/functions/right-transact-sql?view=sql-server-2017" rel="nofollow noreferrer"><code>right()</code></a> and <a href="https://learn.microsoft.com/en-us/sql/t-sql/functions/charindex-transact-sql?view=sql-server-2017" rel="nofollow noreferrer"><code>charindex()</code></a>:</p>

<pre><code>select 
  guid,
  left(question, charindex('_', question) - 1) question,
  right(question, len(question) - charindex('_', question)) value
from tablename  
where value = 'true'
</code></pre>

<p>See the <a href="https://dbfiddle.uk/?rdbms=sqlserver_2017&amp;fiddle=ad44679ebb9fb540421398d884121b47" rel="nofollow noreferrer">demo</a>.<br/>
Results:</p>

<pre><code>&gt; guid | question | value
&gt; ---: | :------- | :----
&gt;    1 | q1       | 2    
&gt;    1 | q2       | 3    
</code></pre>

