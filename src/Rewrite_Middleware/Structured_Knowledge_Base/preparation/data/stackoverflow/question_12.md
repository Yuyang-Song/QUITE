# How to ignore database tablename case-sensitivity using Spring&#39;s JdbcTemplate?
[Link to question](https://stackoverflow.com/questions/10248812/how-to-ignore-database-tablename-case-sensitivity-using-springs-jdbctemplate)
**Creation Date:** 1334934509
**Score:** 2
**Tags:** java, spring, case-sensitive, jdbctemplate
## Question Body
<p>Our Java (JDK6) application must support different databases, such as Oracle, SQL Server and DB2. We use Spring 3.0 and JDBCTemplate for database access. One of our clients uses SQL Server 2005 with case sensitivity and automatically upper cases table names.</p>

<p>Obviously, queries such as "select * from mytablename m" do not work for said client, as he would have the table MYTABLENAME.</p>

<p>For the following code, for instance, I get a nice exception:</p>

<pre><code>this.jdbcTemplate.queryForOject("select * from mytablename m");
`Exception in thread "main" org.springframework.jdbc.BadSqlGrammarException: PreparedStatementCallback; bad SQL grammar [select * from mytablename m]; nested exception is java.sql.SQLException: Invalid object name 'mytablename'.`
</code></pre>

<p>I'm stuck with having to adapt the code - since I can't change my client's database options - so the most obvious solution would be to upper case all the table names in our queries. I know that'll work for this client, but what if a new client has a database with case sensitivity and lower case table names?</p>

<p>So far I haven't succeeded in finding a broader solution. Most answers I've found required changing the database's case-sensitivity or rewriting the queries. I've tried using: <code>this.jdbcTemplate.setResultsMapCaseInsensitive(true);</code> but if I understood well, it applies only to the results of my query, not the query itself.</p>

<p>Is there a way to execute a case-insensitive query using Spring's JdbcTemplate?</p>

## Answers
### Answer ID: 10249175
<p>If you are supporting a large number of databases you might find more problems than just case sensitive names. This is a great opportunity to stress the importance of abstracting your data access with an interface, and writing implementations for each supported database vendor.</p>

<p>In your app you should code to the interface. As you are using spring you can use dependency injection to use the appropriate DB implementation in your data access layer; its just a trivial change to the application context configuration file.</p>

### Answer ID: 10248985
<p>I think your problem here is that <code>user</code> is a <a href="http://msdn.microsoft.com/en-us/library/aa238507%28v=sql.80%29.aspx" rel="nofollow noreferrer">reserverd keyword</a> on MS-SQL server. </p>

<p>Also take a look at here: <a href="https://stackoverflow.com/q/153944/540286">Is SQL syntax case sensitive?</a></p>

