# Unable to use QtSqlDriver to retrieve data from a table with &quot;.&quot; in column names
[Link to question](https://stackoverflow.com/questions/16682409/unable-to-use-qtsqldriver-to-retrieve-data-from-a-table-with-in-column-names)
**Creation Date:** 1369188838
**Score:** 1
**Tags:** sqlite, qt, escaping, pyqt
## Question Body
<p>I have a SQlite database I'm trying to read with the QtSql.QSqlTableModel.  The issue is it won't read any table where the field name contains a "." via the setTable method.</p>

<p>As an example if I have table called MyTable with the column names
(ID, Name.First, Name.Last)
I can manually select it with the query </p>

<pre class="lang-sql prettyprint-override"><code>SELECT * FROM MyTable
</code></pre>

<p>or</p>

<pre><code>SELECT "ID", "Name.First", "Name.Last" and all is ok
</code></pre>

<p>However, the QSqlTableModel won't use that query but will error out with "no such column Name.First Unable to execute statement."</p>

<p>When I dug a little deeper the SQLITE driver in Qt would rewrite the query as </p>

<pre><code>SELECT "ID", "Name"."First", "Name"."Last" FROM MyTable
</code></pre>

<p>But this SELECT statement is wrong and would try and grab columns from another table "Name" but I want a column called "Name.First" in the table "MyTable"</p>

<p>I tried to circumvent this by subclassing the setTable method which worked for getting the data into the TableView:</p>

<pre><code>def tableName(self):
    return self._tableName

def setTable(self, tableName):
    self.clear()
    self._tableName = tableName
    self.setQuery(QtSql.QSqlQuery("SELECT * FROM {0}".format(tableName), self.database()))
</code></pre>

<p>However, reimplementing the method in this fashion broke the method <code>submitAll()</code>.</p>

<p>Inside the File Save method I have the following:</p>

<pre><code>ok = self.tableModel.submitAll()
if not ok:
    logging.error('Error %s' % self.tableModel.lastError().text())
    logging.error('Error %s' % self.tableModel.query().lastQuery())
    return False
</code></pre>

<p>This gives this log:</p>

<pre>
ERROR:root:Error near "SET": syntax error Unable to execute statement
ERROR:root:Error SELECT * FROM MyTable
</pre>

<p>But when I don't reimplement the <code>setTable</code> method, <code>submitAll()</code> works without errors. </p>

<p>So... How do I circumvent the "." in the Column name problem and also have the submitAll() work?</p>

<p>BTW: I agree that having "." in the field names for SQL tables is not a good idea but this is pairing up with another tool that generates the sqlite file in this manner which I have no control over.</p>

## Answers
### Answer ID: 16684581
<p><a href="http://www.qtcentre.org/archive/index.php/t-7565.html" rel="nofollow">http://www.qtcentre.org/archive/index.php/t-7565.html</a></p>

<p><a href="http://www.qtforum.org/article/11245/sqlite-how-to-insert-text-that-contains-character-in-field.html" rel="nofollow">http://www.qtforum.org/article/11245/sqlite-how-to-insert-text-that-contains-character-in-field.html</a></p>

<p>Looks like you just need to call one or both of the functions below before sending it to the database, in order to sanitize the input.</p>

<p><a href="http://qt-project.org/doc/qt-4.8/qsqlquery.html#bindValue" rel="nofollow">http://qt-project.org/doc/qt-4.8/qsqlquery.html#bindValue</a></p>

<p><a href="http://qt-project.org/doc/qt-4.8/qsqlquery.html#prepare" rel="nofollow">http://qt-project.org/doc/qt-4.8/qsqlquery.html#prepare</a></p>

<p><a href="http://xkcd.com/327/" rel="nofollow">http://xkcd.com/327/</a></p>

<p>:)</p>

<p>Hope that helps.</p>

