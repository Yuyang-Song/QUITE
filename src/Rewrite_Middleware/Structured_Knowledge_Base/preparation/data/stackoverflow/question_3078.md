# flask mysql SUM() Decimal in Dictionary from cursor.fetchone()
[Link to question](https://stackoverflow.com/questions/65443949/flask-mysql-sum-decimal-in-dictionary-from-cursor-fetchone)
**Creation Date:** 1608851683
**Score:** 0
**Tags:** python, mysql, flask, sum, decimal
## Question Body
<p>I'am connecting my flask-app to a MySQL-Database like this:</p>
<pre><code>
from flask_mysql_connector import MySQL
from flask_mysqldb import MySQL


# MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Prices'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DATABASE_SOCKET'] = ''
app.config['MYSQL_UNIX_SOCKET'] = ''
app.config['MYSQL_CONNECT_TIMEOUT'] = ''
app.config['MYSQL_READ_DEFAULT_FILE'] = ''
app.config['MYSQL_USE_UNICODE'] = ''
app.config['MYSQL_CHARSET'] = ''
app.config['MYSQL_SQL_MODE'] = ''
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL()
mysql.init_app(app)
</code></pre>
<p>Performing a query like this:</p>
<pre><code>cursor.execute(&quot;SELECT SUM(total) AS sumy FROM tbl&quot;)
total = cursor.fetchone()
total = total[&quot;sumy&quot;]
</code></pre>
<p>returns this:</p>
<pre><code>({'sumy': Decimal('123.4')})
</code></pre>
<p>My Questions now are:</p>
<p>Does every connector, the</p>
<pre><code>MySQL Connector/Python
PyMySQL
MySQLDB
mysqlclient
and the OurSQL
</code></pre>
<p>return a Decimal('123.4') Value from a SUM(column) query?
How would I get rid of this Decimal-feature the easy way? I know there are CAST() and float() suggestions out there.
I like to keep it simple so is there maybe a fetchone() parameter I am missing?
Or a connection parameter like ['raw'] as the MySQL Connector/Python has(I'd have to rewrite my code, if I had to change to that...)</p>
<p>thank you.</p>

## Answers
### Answer ID: 77507680
<p>USE FOR LOOP</p>
<p>import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb</p>
<p>db= MySQLdb.connect(&quot;hostname&quot;, &quot;username&quot;, &quot;password&quot;, &quot;database_name&quot;)</p>
<p>cursor= db.cursor()</p>
<p>cursor.execute(&quot;SELECT SUM(price) AS totalsum FROM CustomerOrders&quot;)</p>
<p>result = cursor.fetchall()</p>
<p>for i in result:
print(i[0])</p>
<p>db.close()</p>

### Answer ID: 65465597
<p>Well, funny as it may seem, even the SUM of floats is returned as Decimal(123.4). I so went on doing all calculations in MySQL and using flask only to show the content.</p>

### Answer ID: 65444262
<p>Decimal is the python way of representing fixed decimal values. The SQL is returning a decimal probably because the <code>sumy</code> is decimal. Its likely all implementation will handle this the same way.</p>
<p>Leaving the python application to handle it as a <code>Decimal</code> is probably the best way to maintain the database being responsible for retrieval and the application for presentation.</p>

