# Convert multiple SQL code with multiple subqueries into a single query
[Link to question](https://stackoverflow.com/questions/40514666/convert-multiple-sql-code-with-multiple-subqueries-into-a-single-query)
**Creation Date:** 1478720234
**Score:** -1
**Tags:** sql, ms-access, select, left-join, inner-join
## Question Body
<p>I'm starting to handle an old database that was generated years ago with ACCESS. All the queries have been designed with the ACCESS query wizard and they seem to be very time consuming and I would like to improve their performance.</p>
<p>All queries depend on at least three subqueries and I would like to rewrite the SQL code to convert them into a single query.</p>
<p>Here you have an example of what I'm talking about:</p>
<p>This is the main query:</p>
<blockquote>
<p>SELECT Subquery1.pid, Table4.SIB, Subquery1.event,
Subquery1.event_date, Subquery2.GGG, Subquery3.status FROM Subquery1
LEFT JOIN ((Table4  LEFT JOIN Subquery2  ON Table4.SIB =
Subquery2.SIB)  LEFT JOIN Subquery3  ON Table4.SIB = Subquery3.SIB)
ON Subquery1.pid = Table4.PID;</p>
</blockquote>
<p>This main query depends on three subqueries:</p>
<p>Subquery1</p>
<blockquote>
<p>SELECT Table2.id, Table2.pid, Table2.npid, Table3.event_date,
Table3.event, Table3.notes, Table2.other FROM Table2 INNER JOIN Table3
ON Table2.id = Table3.subject_id WHERE (((Table2.pid) Is Not Null) AND
((Table3.event_date)&gt;#XX/XX/XXXX#) AND ((Table3.event) Like &quot;*AAAA&quot; Or
(Table3.event)=&quot;BBBB&quot;)) ORDER BY Table2.pid, Table3.event_date DESC;</p>
</blockquote>
<p>Subquery2</p>
<blockquote>
<p>SELECT Table1.SIB, IIf(Table1.GGG Like &quot;AAA&quot;,&quot;BBB&quot;, IIf(Table1.GGG
Like &quot;CCC&quot;,&quot;BBB&quot;, IIf(Table1.GGG Like &quot;DDD&quot;,&quot;DDD&quot;,&quot;EEE&quot;))) AS GGG FROM
Table1;</p>
</blockquote>
<p>Subquery3</p>
<blockquote>
<p>SELECT Table5.SIB, Table5.PID, IIf(Table5.field1 Like
&quot;1&quot;,&quot;ZZZ&quot;,IIf(Table5.field1 Like &quot;2&quot;,&quot;ZZZ&quot;,IIf(Table5.field1 Like
&quot;3&quot;,&quot;ZZZ&quot;,IIf(Table5.field1 Like &quot;4&quot;,&quot;HHH&quot;,IIf(Table5.field1 Like
&quot;5&quot;,&quot;HHH&quot;,IIf(Table5.field1 Like &quot;6&quot;,&quot;HHH&quot;,&quot;UUU&quot;)))))) AS SSS FROM
Table5;</p>
</blockquote>
<p>Which would be the best way of improving the performance of this query and converting all the subqueries into a single statement?</p>
<p>I can handle each subquery, but I'm having a hard time joining them together.</p>

## Answers
### Answer ID: 72195545
<pre><code>'''you can create transient tables for each sub query'''
CREATE Transient table1 AS
        '''Your sub query goes here'''
CREATE Transient table2 AS
        '''Your sub query goes here'''
'''Main query to merge them into one'''
SELECT '''column names'''
FROM 
table1
LEFT JOIN table2
ON table1.common_column = table2.common_column
LEFT JOIN table3
ON table1.common_column = table3.common_column
'''similarly you can combine all sub queries/transient tables''' 
</code></pre>

### Answer ID: 40514790
<p>If this:</p>

<p><code>Table5.field1 Like "3"</code></p>

<p>is really how some of your subqueries are written (without actual wild characters) you can save a lot of time by changing it to </p>

<p><code>Table5.field1="3"</code></p>

