# Large select query hangs using Python and unixODBC connecting to SQL Server
[Link to question](https://stackoverflow.com/questions/28860521/large-select-query-hangs-using-python-and-unixodbc-connecting-to-sql-server)
**Creation Date:** 1425488784
**Score:** 0
**Tags:** python, sql-server, odbc, pyodbc, unixodbc
## Question Body
<p>We have to run a number of large select queries against SQL Server from CentOS 6 boxes. On two servers, when using a pretty bland select statement, the rate of data returned from SQL Server starts fast before slowing down and receiving bursts of data every ~30 seconds. On two other servers, the query runs consistently and finishes in less than 2 minutes. The configuration on all of these boxes for unixODBC and msodbcsql is exactly the same.</p>

<p>Example code that is causing the problem:</p>

<pre><code>import datetime
import pyodbc

db_connection_string = '&lt;connection string info&gt;'
print(datetime.datetime.now(), 'Connecting to db...')
db_connection = pyodbc.connect(db_connection_string, autocommit=True)
print(datetime.datetime.now(), '...connected')

cursor = db_connection.cursor()
try:
    sql_statement = 'SELECT data FROM table;'
    num = 0
    print(datetime.datetime.now(), 'Iterating over cursor...')
    for row in cursor.execute(sql_statement):
        num += 1
        if num % 100000 == 0:
            print(datetime.datetime.now(), num)
    print(datetime.datetime.now(), num)
    print(datetime.datetime.now(), '...iteration completed')
finally:
    cursor.close()
    db_connection.close()
</code></pre>

<p>This uses unixODBC <code>2.3.0</code> and msodbc <code>11.0.2270.0</code>. The servers are CentOS <code>6.5/6.6</code> with Python <code>3.4</code>.</p>

<p>We have tried:</p>

<ul>
<li>Monitoring system resources, no spikes in memory or CPU usage except when data is being processed</li>
<li>strace on the process also only shows changes when data is being processed</li>
<li>both SQL Server and the Python server seem to be hanging and waiting for each other to do something</li>
<li>Monitoring network traffic also shows no spikes or packages being dropped or any errors</li>
<li>scp and sftp'ing files to the servers and between the servers has no problem</li>
<li>Connecting to a different database type with the same query has no issues</li>
<li>Rewriting the code in Java and running it had the same issues on the problem servers, but ran fine on the good servers</li>
</ul>

<p>Any other ideas to help track down this issue would be appreciated.</p>

## Answers
### Answer ID: 28973263
<p>The issue appears to have been driver interactions on SQL Server not playing well with CentOS. Changing driver settings preventing the queries from hanging, although results are still returned up to 4x faster on the best performing server when compared to the others. The lesson here seems to be that weird driver interactions will probably come up with trying to use a combination of MS and Linux systems.</p>

