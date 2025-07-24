# Avoid implicit conversion from date to timestamp for selects with Oracle using Hibernate
[Link to question](https://stackoverflow.com/questions/2464502/avoid-implicit-conversion-from-date-to-timestamp-for-selects-with-oracle-using-h)
**Creation Date:** 1268847647
**Score:** 2
**Tags:** java, oracle-database, hibernate
## Question Body
<p>I'm using Hibernate 3.2.7.GA criteria queries to select rows from an Oracle Enterprise Edition 10.2.0.4.0  database, filtering by a timestamp field. The field in question is of type <code>java.util.Date</code> in Java, and <code>DATE</code> in Oracle.</p>

<p><a href="https://stackoverflow.com/questions/1945603/why-is-oracle-so-slow-when-i-pass-a-java-sql-timestamp-for-a-date-column">It turns out</a> that the field gets mapped to <code>java.sql.Timestamp</code>, and Oracle converts all rows to <code>TIMESTAMP</code> before comparing to the passed in value, <a href="https://forum.hibernate.org/viewtopic.php?f=1&amp;t=1001146&amp;p=2427294#p2427294" rel="nofollow noreferrer">bypassing the index</a> and thereby ruining performance.</p>

<p>One solution would be to use Hibernate's <code>sqlRestriction()</code> along with Oracle's <code>TO_DATE</code> function. That would fix performance, but requires rewriting the application code (lots of queries).</p>

<p>So is there a more elegant solution? Since Hibernate already does type mapping, could it be configured to do the right thing?</p>

<p><strong>Update:</strong> The problem occurs in a variety of configurations, but here's one specific example:</p>

<ul>
<li>Oracle Enterprise Edition 10.2.0.4.0</li>
<li>Oracle JDBC Driver 11.1.0.7.0</li>
<li>Hibernate 3.2.7.GA</li>
<li>Hibernate's Oracle10gDialect</li>
<li>Java 1.6.0_16</li>
</ul>

## Answers
### Answer ID: 6284311
<p>According to <a href="http://www.oracle.com/technetwork/database/enterprise-edition/jdbc-faq-090281.html#08_01" rel="nofollow">Oracle JDBC FAQ</a>:</p>

<blockquote>
  <p>"11.1 drivers by default convert SQL DATE to Timestamp when reading from the database"</p>
</blockquote>

<p>So this is an expected behaviour.
To me this means that actual values coming from <code>DATE</code> columns are converted to <code>java.sql.Timestamp</code>, not that bind variables with <code>java.util.Date</code> are converted to <code>java.sql.Timestamp</code>.</p>

<p>An <code>EXPLAIN PLAN</code> output would help identifying the issue. Also, an Oracle trace could tell you exactly what type is assigned to the bind variable in the query.</p>

<p>If that's really happening it could be a Oracle bug.</p>

<p>You can work around it this way:</p>

<ul>
<li><p>Create an FBI (<a href="http://download.oracle.com/docs/cd/B19306_01/server.102/b14220/schema.htm#sthref928" rel="nofollow">Function Based Index</a>) on the <code>DATE</code> column, casting it to a <code>TIMESTAMP</code>. For example:</p>

<pre><code>CREATE INDEX tab_idx ON tab (CAST(date_col AS TIMESTAMP)) COMPUTE STATISTICS;
</code></pre></li>
<li><p>Create a View that contains the same <code>CAST</code> expression. You can keep the same column name if you want:</p>

<pre><code>CREATE VIEW v AS
SELECT CAST(date_col AS TIMESTAMP) AS date_col, col_1, ... FROM tab;
</code></pre></li>
<li><p>Use the View instead of the Table (it's often a good idea anyway, e.g. if you were already using a View, you wouldn't need to change the code at all). When a <code>java.sql.Timestamp</code> variable will be used with <code>date_col</code> in the <code>WHERE</code> condition, (if enough selective) the Index will be used.</p></li>
<li><p>If you find out why there was a <code>java.sql.Timestamp</code> (or Oracle fixes the potential bug), you can always go back just changing the View (and dropping the FBI), and it would be completely transparent to the code</p></li>
</ul>

### Answer ID: 2464621
<p>This might sound drastic, but when faced with this problem we ended up converting all DATE columns to TIMESTAMP types in the database.  There's no drawback to this that I can see, and if Hibernate is your primary application platform then you'll save yourself future aggravation.</p>

<p>Notes:</p>

<ul>
<li><p>The column types may be changed with
a simple "ALTER tableName MODIFY
columnName TIMESTAMP(precisionVal)".</p></li>
<li><p>I was surprised to find that indexes 
on these columns did NOT have to be<br>
rebuilt.</p></li>
</ul>

<p>Again, this only makes sense if you're committed to Hibernate.</p>

