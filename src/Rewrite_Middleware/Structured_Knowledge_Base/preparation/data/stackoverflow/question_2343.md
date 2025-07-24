# Different behaviour of postgresql and firebird recordsets
[Link to question](https://stackoverflow.com/questions/30131413/different-behaviour-of-postgresql-and-firebird-recordsets)
**Creation Date:** 1431113088
**Score:** 2
**Tags:** postgresql, vb6, ado, firebird
## Question Body
<p>This question is related to one I asked earlier <a href="https://stackoverflow.com/q/30126619/6164">here</a>. </p>

<p>A query on a firebird database retrieved a single row recordset because
the <strong>Where</strong> clause included the primary key.
However on subsequent Update pretty much every row in the table was updated.
I had been expecting just the one row to be updated.
This was the query:</p>



<pre class="lang-vb prettyprint-override"><code>sQuery = "select memo from clients where clientID = 10021 "
</code></pre>

<p>What is going on seems to be that the select query needed to include
the primary key column in the recordset in order to restrict the update to just one record.</p>

<pre class="lang-vb prettyprint-override"><code>sQuery = "select memo, clientID from clients where clientID = 10021 "
</code></pre>

<p>However in postgresql, the first query works in the way the second query works in firebird.</p>

<p>Can I rely on this behaviour in postgresql or should I rewrite existing queries to include
the primary key column in recordsets that will subsequently be updated?</p>

<p>Is there any way to make firebird queries behave in the way postgresql does?</p>

<p>Although I can now see the logic of the firebird behaviour it is not what
I am used to coming from an MSAccess/DAO background.</p>

<p>Really I just want to know what's going on and which is the more 'normal' behaviour to be expected from ADO recordsets?</p>

<p>This is the full code using firebird.</p>

<pre class="lang-vb prettyprint-override"><code>'FIREBIRD
'vb6 and ms ado 2.8
'windows 7 home edition 64 bit
'Firebird version is 2.5.4.26856 (x64).
'Firebird ODBC driver 2.0.3.154

    Dim cn As New ADODB.Connection
    Dim rs As New ADODB.Recordset

    Dim cs As String
    Dim dbPath As String

    dbPath = "c:\Parkes\Parkes.fdb"
    cs = "DRIVER={Firebird/Interbase(r) Driver}; DBNAME=localhost:" &amp; dbPath &amp; "; UID=SYSDBA; PWD=masterkey;"
    cn.ConnectionString = cs
    cn.Open

    Dim sQuery As String

    sQuery = "select memo from clients where clientID = 10021 "
    rs.Open sQuery, cn, adOpenStatic, adLockOptimistic

    If rs.BOF &lt;&gt; True Or rs.EOF &lt;&gt; True Then
    'putting msgbox rs.recordcount here confirms only 1 record in recordset
        rs.Movefirst
        rs.Fields("memo") = "blah"
        rs.Update

    End If

    Set rs = Nothing
    Set cn = Nothing
</code></pre>

<p>This is the same code using a postgresql database;</p>

<pre class="lang-vb prettyprint-override"><code>'POSTGRESQL
'vb6 and ms ado 2.8
'windows 7 home edition 64 bit
Postgresql version is 9.4 64 bit
psql ODBC driver 9.3.4

    Dim cn As New ADODB.Connection
    Dim rs As New ADODB.Recordset

    Dim cs As String
    Dim dbPath As String

    dbPath = "c:\Parkes\Parkes.fdb"
   cs = "Driver={PostgreSQL ANSI};SERVER=localhost;Port=5432;DATABASE=Parkes;UID=postgres;PWD=masterkey;CONNSETTINGS=SET Datestyle TO 'DMY'%3b;BOOLSASCHAR=0;TEXTASLONGVARCHAR=1;TrueIsMinus1=1;"

    cn.ConnectionString = cs
    cn.Open

    Dim sQuery As String

    sQuery = "select memo from clients where clientID = 10021 "
    rs.Open sQuery, cn, adOpenStatic, adLockOptimistic

    If rs.BOF &lt;&gt; True Or rs.EOF &lt;&gt; True Then
    'putting msgbox rs.recordcount here confirms only 1 record in recordset
        rs.Movefirst
        rs.Fields("memo") = "blah"
        rs.Update

    End If

    Set rs = Nothing
    Set cn = Nothing
</code></pre>

## Answers
### Answer ID: 30215414
<p>Based on the reply <a href="http://tracker.firebirdsql.org/browse/ODBC-186" rel="nofollow">here</a> and the microsoft <a href="https://msdn.microsoft.com/en-us/library/windows/desktop/ms676529%28v=vs.85%29.aspx" rel="nofollow">article</a> that was linked to there, it seems to be the case that the firebird odbc driver operates differently to (most?) other odbc drivers, by design.</p>

<p>The Microsoft ADO API reference states that the Update method should only update the current record.</p>

<p>The Firebird driver works differently and it's easier to explain how via some examples</p>

<p>In the the case below, the recordset contains just one record (because clientid is the primary key and thus unique) and suppose that the value in its memo field is 'bingo'. 
The update method will alter to 'blah' the memo field value of all rows in the table whose existing value is 'bingo'.</p>

<pre><code>sQuery = "select memo from clients where clientID = 10021 "
    rs.Open sQuery, cn, adOpenStatic, adLockOptimistic

    If rs.BOF &lt;&gt; True Or rs.EOF &lt;&gt; True Then
        rs.Movefirst
        rs.Fields("memo") = "blah"
        rs.Update

    End If
</code></pre>

<p>In the next example, the recordset again contains just one record but now 2 columns and suppose that the value in its memo field is 'bingo' and the value in its surname field is 'Jones'. 
The update method will alter to 'blah' the memo field value of all rows in the table whose existing values have'bingo' in their memo field and 'Jones' in their surname field.</p>

<pre><code>sQuery = "select memo, surname from clients where clientID = 10021 "
    rs.Open sQuery, cn, adOpenStatic, adLockOptimistic

    If rs.BOF &lt;&gt; True Or rs.EOF &lt;&gt; True Then
        rs.Movefirst
        rs.Fields("memo") = "blah"
        rs.Update

    End If
</code></pre>

<p>Clearly, this may still not restrict the update to one row. 
To make sure that just one row is updated you need to include a column with unique values in the recordset, for example, the primary key column:</p>

<pre><code>sQuery = "select memo, clientID from clients where clientID = 10021 "
        rs.Open sQuery, cn, adOpenStatic, adLockOptimistic

        If rs.BOF &lt;&gt; True Or rs.EOF &lt;&gt; True Then
            rs.Movefirst
            rs.Fields("memo") = "blah"
            rs.Update

        End If
</code></pre>

