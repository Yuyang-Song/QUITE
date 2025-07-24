# How to join tables together on columns with different datatypes?
[Link to question](https://stackoverflow.com/questions/1228639/how-to-join-tables-together-on-columns-with-different-datatypes)
**Creation Date:** 1249404421
**Score:** 1
**Tags:** sql, database, ms-access, join, types
## Question Body
<p>A Microsoft Access implementation is throwing a type mismatch error while trying to execute a macro that opens up some queries.  Most of the tables are linked to a SQL Server and I need to join two of the tables together that have different datatypes.</p>

<p><strong>Table A:</strong><br>
REFERENCE TEXT</p>

<p><strong>Table B:</strong><br>
REFNO NUMBER</p>

<p>I would ordinarily want to correct the issue on the SQL Server side, but there are multiple apps hitting the same database and it would take a considerable amount of time to test all of them.  Furthermore, we are in the process of completely rewriting this application and any work I do today is completely throw-away...  </p>

<p>If there is a way to make this join possible in access, I would save all kinds of time...</p>

## Answers
### Answer ID: 1228718
<p>You can do the comparison in the criteria.  </p>

<pre><code>SELECT [REFERENCE], [REFNO]
FROM [Table a], [Table b]
WHERE [REFERENCE]=cstr(nz([REFNO],""))
</code></pre>

<p>You can also do a passthrough - a query in access that executes on the sql server and returns only the data.  </p>

<pre><code>SELECT [REFERENCE], [REFNO]
FROM [Table a], [Table b]
WHERE [REFERENCE]=cast([REFNO] as varchar(25))
</code></pre>

<p>HTH</p>

### Answer ID: 1228712
<p>Within Access you could use the CLng (or Cint) function to convert the Table A's REFERENCE values from text to number.  </p>

<p>I would prefer to create a view of Table A in SQL Server to transform the field's data type before Access gets the data.  You shouldn't need to test the view against your other existing apps.  When your re-write make the view no longer useful, just discard it.  </p>

### Answer ID: 1228670
<p>What is the datatype for each of the column, you mentioned?</p>

<p>If you want to compare it stringwise, you could do <code>Cstr(myNumericColumn) = myStringColumn</code>.<br>
OR to compare it in numeric mode, do <code>CLng(myStringColumn) = myNumericColumn</code>.</p>

