# Oracle SQL: SELECT date FROM outcome_o Code: (936) ORA-00936: missing expression
[Link to question](https://stackoverflow.com/questions/36941262/oracle-sql-select-date-from-outcome-o-code-936-ora-00936-missing-expression)
**Creation Date:** 1461940997
**Score:** 1
**Tags:** oracle-database
## Question Body
<p>When I do this query:</p>

<pre><code>SELECT date FROM income_o;
</code></pre>

<p>I have this error:</p>

<blockquote>
  <p>Error in query. Code: (936) ORA-00936: missing expression</p>
</blockquote>

<p>Here is <a href="http://www.sql-ex.ru/help/select13.php#db_2" rel="nofollow">database schema</a></p>

<p>I do not really know what to do or what is missing :(</p>

<p>And how should I rewrite it for this form <code>income_o.date</code> to work?</p>

## Answers
### Answer ID: 46924593
<p>Below query will work.</p>

<pre><code> SELECT t."date" FROM tableName t;
</code></pre>

### Answer ID: 36941380
<p>It is unfortunate that your tables contain a column "date" - that is a reserved word in Oracle, used to input date literals. The date literal is what is missing and throws the error.</p>

<p>In fact that is not YOUR error; what you want is the column named date. Put it in double-quotes, like so:</p>

<pre><code>SELECT "date" FROM income_o;
</code></pre>

