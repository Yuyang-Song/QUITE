# Python using oracledb to connect to Oracle database with Pandas DataFrame Error: &quot;pandas only supports SQLAlchemy connectable (engine/connection)&quot;
[Link to question](https://stackoverflow.com/questions/79228345/python-using-oracledb-to-connect-to-oracle-database-with-pandas-dataframe-error)
**Creation Date:** 1732656938
**Score:** 1
**Tags:** python, pandas, dataframe, sqlalchemy, python-oracledb
## Question Body
<p>I am pretty new to Python and even newer to Pandas and am hoping for some guidance</p>
<p>My company has an on-prem DEV Oracle database that I am trying to connect to using Python &amp; Pandas. After some searching I found that the Python package &quot;oracledb&quot; was recommended to be used.</p>
<p>Using VS code .IPYNB I have the following chunks of code that seem to work with no errors</p>
<pre><code># python -m pip install --upgrade pandas
import oracledb
import pandas as pd
from sqlalchemy import create_engine

connection = oracledb.connect(user=&quot;TEST&quot;, password=&quot;TESTING&quot;, dsn=&quot;TESTDB:1234/TEST&quot;)

print(&quot;Connected&quot;)
print(connection)
</code></pre>
<p>The above code seems to run just fine which is great</p>
<p>I then run the below code as a quick test</p>
<pre><code>cursor=connection.cursor()
query_test='select * from dm_cnf_date where rownum &lt; 2'

for row in cursor.execute(query_test):
    print(row)
</code></pre>
<p>This returns a tuple with a row of data so far so good, looks like I can connect to the database and run a query.</p>
<p>Next I wanted to get the data into a Pandas dataframe and this is where I got stuck</p>
<p>I tried this code</p>
<pre><code>df = pd.read_sql(sql=query_test, con=connection)
</code></pre>
<p>Which then I get hit with the following error</p>
<blockquote>
<p>:1: UserWarning: pandas only supports
SQLAlchemy connectable (engine/connection) or database string URI or
sqlite3 DBAPI2 connection. Other DBAPI2 objects are not tested. Please
consider using SQLAlchemy.   df = pd.read_sql(sql=query_test,
con=connection)</p>
</blockquote>
<p>I was loosely trying to follow this article (&quot;Read data as pandas DataFrame&quot;): <a href="https://kontext.tech/article/1019/python-read-data-from-oracle-database" rel="nofollow noreferrer">https://kontext.tech/article/1019/python-read-data-from-oracle-database</a></p>
<p>but it didnt seem to work.</p>
<p>I tried to take a look at the sqlalchemy site here: <a href="https://docs.sqlalchemy.org/en/20/dialects/oracle.html#module-sqlalchemy.dialects.oracle.oracledb" rel="nofollow noreferrer">https://docs.sqlalchemy.org/en/20/dialects/oracle.html#module-sqlalchemy.dialects.oracle.oracledb</a></p>
<p>Which I tried to rewrite my code a bit as follows</p>
<pre><code>conn_url=&quot;oracle+oracledb://TEST:TESTING@TESTDB:1234/TEST&quot;
engine=create_engine(conn_url)

df = pd.read_sql(sql=query_test, con=engine)
</code></pre>
<p>And I get hit with another error</p>
<blockquote>
<p>OperationalError: DPY-6003: SID &quot;TEST&quot; is not
registered with the listener at host &quot;TESTDB&quot; port
1234. (Similar to ORA-12505)</p>
</blockquote>
<p>Just looking to connect to an Oracle DB and grab data into a Pandas dataframe but keep hitting a wall</p>
<p>Any insight would be very much appreciated</p>

## Answers
### Answer ID: 79228849
<p>Try either of:</p>
<pre><code>#oracledb.defaults.arraysize = 1000 # Tune for big queries

with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
    with connection.cursor() as cursor:
       cursor.execute(&quot;select * from emp&quot;)
       col_names = [c.name for c in cursor.description]
       data = cursor.fetchall()
       df = pandas.DataFrame(data, columns=col_names)
       print(df)
</code></pre>
<p>or</p>
<pre><code>engine = sqlalchemy.create_engine(
    'oracle+oracledb://',
    thick_mode=None,
    connect_args={
        &quot;user&quot;: un,
        &quot;password&quot;: pw,
        &quot;dsn&quot;: cs
    }
    #, echo=True  # SQLAlchemy tracing / logging / debugging
    )

emp_sql = &quot;select * from emp&quot;
df_emp = pd.read_sql(emp_sql, engine)
print(df_emp)
</code></pre>
<p>The latter is slower. You can enable the tracing and see the number of queries that are executed internally by SQLAlchemy.</p>
<p>Regarding the ORA-12505 error using:</p>
<pre><code>&quot;oracle+oracledb://TEST:TESTING@TESTDB:1234/TEST&quot;
</code></pre>
<p>you probably needed to use:</p>
<pre><code>&quot;oracle+oracledb://TEST:TESTING@TESTDB:1234?service_name=TEST&quot;
</code></pre>
<p>see <a href="https://docs.sqlalchemy.org/en/20/dialects/oracle.html#dialect-oracle-oracledb-connect" rel="nofollow noreferrer">https://docs.sqlalchemy.org/en/20/dialects/oracle.html#dialect-oracle-oracledb-connect</a></p>
<p>Back in the old days, 'system identifiers' (SIDs) were commonly used for connecting to Oracle DB.  SQLAlchemy defaults to use these in its syntax.  However most DBs are now connected to via a 'service name', hence the need for the extra connection keyword.  See the note in the SQLAlchemy doc:</p>
<blockquote>
<p>Note that although the SQLAlchemy URL syntax hostname:port/dbname looks like Oracle’s Easy Connect syntax, it is different. SQLAlchemy’s URL requires a system identifier (SID) for the dbname component</p>
</blockquote>
<p>You should continue using your 'service name' TEST, and not try to find what SID to use.</p>

