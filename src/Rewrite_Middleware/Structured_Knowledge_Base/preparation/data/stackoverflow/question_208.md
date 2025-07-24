# SQL Server CASE WHEN without using CASE WHEN
[Link to question](https://stackoverflow.com/questions/1682437/sql-server-case-when-without-using-case-when)
**Creation Date:** 1257444192
**Score:** 0
**Tags:** sql-server, t-sql, case-when
## Question Body
<p>Is there a way to rewrite a Transact SQL statement that uses a CASE WHEN structure to do the same without using the CASE WHEN?</p>

<p>I'm using a product that has a built-in query designer and its own pseudo-SQL. It has limitations on what I can use with SQL Server and Oracle. So I have this column that, when the underlying database is Oracle, uses DECODE (which is supported). However, I need to make it work with SQL Server and CASE WHEN is not supported.</p>

<p>The statement I'm trying to convert is something like</p>

<pre><code>Decode (StatusColumn,  'Value 1',
Decode(Sign(Now()-TargetDateColumn)),1,'Past
Due', 'Outstanding'),  'Value 2',
Decode(Sign(Now()-TargetDateColumn)),1,'Past
Due', 'Outstanding'),  'Value 3',
Decode(Sign(Now()-TargetDateColumn)),1,'Past
Due', 'Outstanding'),  'Value 4')
</code></pre>

<p>I have a limited set of T-SQL options to use and CASE WHEN is not an option. I do have IsNull and Coalesce, but I'm not sure if they will help me with this one.</p>

<p>Don't bother with the date calculations, those are solved.</p>

<p>I searched the CASE WHEN questions here, to no avail.</p>

<p>Thanks!</p>

<p><strong>Update:</strong></p>

<p>I realize that I should have given more details on the reason for the limitations, as this is a developer's resource and it would be assumed that this is a development product. It is not.</p>

<p>I'm using an enterprise software product that has a built-in query designer and its own pseudo-SQL. It has limitations on what I can use with SQL Server and Oracle. Basically, everything that doesn't break the parsing of the built-in query engine is game. That means all the sanctioned functions and expressions, plus all the data abstractions (internal objects that correspond to a physical table in a database and other queries created with the product), plus everything from Oracle SQL or Transact SQL that does not explicitly break the parsing.</p>

<p>The reason why CASE WHEN doesn't work for me is that it breaks the parsing of the pseudo-SQL by the query engine. </p>

<p>Ultimately, I would like to try to:</p>

<ol>
<li>Use only the product's query
designer the SQL that passes the
parsing OR</li>
<li>Use a few extra resources from
the SQL Server database and the
query designer to get it done.</li>
</ol>

<p>Based on the several good answers that I got, here's the approach that worked out for me, so far.</p>

<p>Jason DeFontes suggested that I could use a database view to perform the CASE WHEN rules and that falls into #2 above. It works for me because a view is dynamic enough that I don't have to do maintenance on it (as opposed to richartallent's truth tables approach, which I believe are close to Jason's approach). Pascal's suggestion of creating a function would go along the same lines, but probably break the parse.</p>

<p>So I created a database view that does all the transformation with CASE WHEN and I added it to my query's SQL, joined it with the existing SQL and it worked just fine. I realize that I'm probably adding an overhead to the database engine, as it will have to retrieve the same data set twice (one for the view and one for the query), but it's one of those cases where it's hardly an issue.</p>

<p>Given that this "use a view to obfuscate it" design works for me, I wonder what would be the more efficient approach:</p>

<ul>
<li>Using a select with CASE WHEN; </li>
<li>Using CTE (again, richardtallent); </li>
<li>Using Union All (HLGEM); </li>
<li>Using Subqueries (MisterZimbu);</li>
</ul>

<p>I will still check Aramis wyler's suggestion, as it could probably fall into #1 above.</p>

<p>For now, Jason's answer was accepted. Considering that I used CASE WHEN in the view, perhaps the title for the question ended up being is ill-chosen. I upped everybody that suggested something that helped in the process. I don't know if that makes a difference in your reputation or not, but I thought it was the nice thing to do.</p>

<p>Again, I want to thank you all for your help and ask you kindly to edit anything on the question that you fell is not appropriate (it's my first question and English is my second language).</p>

## Answers
### Answer ID: 1683189
<p>Can you move the CASE/WHEN logic into a view, then have the tool query the view?</p>

### Answer ID: 1682967
<p>I'm not exactly sure I understand your code, but this should give you an idea for a different approach.</p>

<p>First, create a table:</p>

<pre><code>CREATE TABLE StatusLookup(
   value nvarchar(255),
   datesign shortint,
   result varchar(255));
</code></pre>

<p>Now, populate it with a truth table (lots of repeated logic in here apparently, maybe this should be two truth tables with a CROSS JOIN between them):</p>

<pre><code>INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 1', -1, 'Outstanding')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 1', 0, 'Outstanding')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 1', 1, 'Past Due')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 2', -1, 'Outstanding')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 2', 0, 'Outstanding')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 2', 1, 'Past Due')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 3', -1, 'Outstanding')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 3', 0, 'Outstanding')
INSERT INTO StatusLookup(value, datesign, result) VALUES ('Value 3', 1, 'Past Due')
</code></pre>

<p>Finally, join and provide a default answer:</p>

<pre><code>SELECT mytable.*, COALESCE(statuslookup.result, 'Value 4')
FROM
    mytable LEFT JOIN statuslookup ON
        statuslookup.value = StatusColumn
        AND statuslookup.datesign = Sign(Now()-TargetDateColumn)
</code></pre>

<p>One key advantage to this approach is it puts the business logic in data tables, not code, which is often more maintainable and extensible.</p>

### Answer ID: 1682852
<p>It's ugly and depending on the number of values you have it may not be viable.  But strictly speaking, I think something like this would work as a translation from the above query segment:<blockquote>
select 'PastDue' from tablename where Now() > TargetDateColumn and (StatusColumn = 'Value 1' or StatusColumn = 'Value 2' or StatusColumn = 'Value 3')
  union select 'Outstanding' where Now() &lt; TargetDateColumn and (StatusColumn = 'Value 1' or StatusColumn = 'Value 2' or StatusColumn = 'Value 3')
  union select 'Value 4' where NOT (StatusColumn = 'Value 1' or StatusColumn = 'Value 2' or StatusColumn = 'Value 3')</blockquote></p>

### Answer ID: 1682839
<p>Can you write custom subqueries?  Probably not if you don't even have access to CASE WHEN, but this would probably work too:</p>

<pre><code>select
    ...,
    coalesce(c1.value, c2.value, c3.value, ..., &lt;default value&gt;)
from MyTable
left join (select &lt;result 1&gt; as value) c1 on &lt;first condition&gt;
left join (select &lt;result 2&gt; as value) c2 on &lt;second condition&gt;
left join (select &lt;result 3&gt; as value) c3 on &lt;third condition&gt;
</code></pre>

### Answer ID: 1682544
<p>Do you have union all available? Perhaps you could write a query for each of the conditions with the condition of the case inthe where clause and union them together. </p>

### Answer ID: 1682467
<p>Write a function which performs the computation using CASE WHEN.</p>

