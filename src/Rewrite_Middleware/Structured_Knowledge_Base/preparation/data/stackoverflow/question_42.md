# What are the details for using CF_SQL_NVARCHAR in ColdFusion 10?
[Link to question](https://stackoverflow.com/questions/10802388/what-are-the-details-for-using-cf-sql-nvarchar-in-coldfusion-10)
**Creation Date:** 1338306171
**Score:** 12
**Tags:** coldfusion, coldfusion-10
## Question Body
<p>The ColdFusion 10 documentation on Updating Your Database has a section on <a href="http://help.adobe.com/en_US/ColdFusion/10.0/Developing/WSc3ff6d0ea77859461172e0811cbec0e02b-7ff3.html#WSe61e35da8d318518-9efe7cf1358680a71d-8000" rel="nofollow noreferrer">Database-related enhancements in ColdFusion 10</a>.  That page mentions that there is now support for <code>CF_SQL_NVARCHAR</code> among others, but with no details about them.  Additionally, the <a href="http://help.adobe.com/en_US/ColdFusion/10.0/CFMLRef/WSc3ff6d0ea77859461172e0811cbec22c24-7f6f.html" rel="nofollow noreferrer">cfqueryparam documentation</a> hasn't been updated to include their existence.</p>

<p>The <a href="http://help.adobe.com/en_US/ColdFusion/9.0/CFMLRef/WSc3ff6d0ea77859461172e0811cbec22c24-7f6f.html" rel="nofollow noreferrer">ColdFusion 9 documentation for cfqueryparam</a> mentions that <code>CF_SQL_VARCHAR</code> maps to <code>varchar</code> in MSSQL.  This is true unless the ColdFusion Administrator <a href="http://help.adobe.com/en_US/ColdFusion/9.0/Admin/WSc3ff6d0ea77859461172e0811cbf364104-7fe5.html" rel="nofollow noreferrer">datasource settings</a> has the <code>String Format</code> setting enabled.  In which case <code>CF_SQL_VARCHAR</code> maps to <code>nvarchar</code>.  This poorly documented feature is a hack which can <a href="https://stackoverflow.com/questions/10543755/slow-query-with-cfqueryparam-searching-on-indexed-column-containing-hashes">cause performance issues</a> within ColdFusion.</p>

<p>So it's great that they have introduced <code>CF_SQL_NVARCHAR</code>, but it would be good to understand how it works.  It is simply an alias for <code>CF_SQL_VARCHAR</code> making it pointless?  Does it always send strings as <code>nvarchar</code>?  If so, does <code>CF_SQL_VARCHAR</code> always send in <code>varchar</code>?</p>

<p>I would hope that for backward compatibility's sake it is implemented as such:</p>

<p>If <code>String Format</code> is enabled <code>CF_SQL_VARCHAR</code> and <code>CF_SQL_NVARCHAR</code> both map to <code>nvarchar</code>.</p>

<p>If <code>String Format</code> is disabled then <code>CF_SQL_VARCHAR</code> maps to <code>varchar</code> and <code>CF_SQL_NVARCHAR</code> maps to <code>nvarchar</code>.</p>

<p>This would mean any pre-CF10 sites can move to CF10 and work, with the same performance considerations pre-CF10.</p>

<p>New sites, or sites that rewrite all queries to match <code>CF_SQL_VARCHAR</code> and <code>CF_SQL_NVARCHAR</code> with the database design will not get the performance penalty that is unavoidable pre-CF10.</p>

<p>Can anyone confirm if this is the case; even better if with something official?</p>

## Answers
### Answer ID: 77361727
<p>Anyone who runs into this, try adding <code>sendStringParametersAsUnicode=false</code> to the db connection string in cf administrator.</p>

### Answer ID: 10848136
<p>While you are waiting for something more official, I will throw in my $0.02 ... </p>

<p>I did some digging and based on my observations (with an MS SQL datasource) I believe that:</p>

<ul>
<li><p><code>CF_SQL_NVARCHAR</code> is not just an alias for <code>CF_SQL_VARCHAR</code>. It maps to the newer <a href="http://docs.oracle.com/javase/6/docs/api/java/sql/Types.html#NVARCHAR" rel="noreferrer">NVARCHAR jdbc type</a>, which lets you to handle unicode values at a more granular level.</p></li>
<li><p><code>CF_SQL_NVARCHAR</code> values are always treated as <code>nvarchar</code></p></li>
<li>The handling of <code>CF_SQL_VARCHAR</code> depends on the <a href="http://technet.microsoft.com/en-US/library/ms378857%28v=SQL.90%29.aspx" rel="noreferrer"><code>String Format</code></a> setting, same as in previous versions. </li>
</ul>

<p><strong>CF_SQL_NVARCHAR Test/Results:</strong></p>

<p>If you enable datasource logging, you can see the driver invokes the special <a href="http://docs.oracle.com/javase/6/docs/api/java/sql/PreparedStatement.html#setNString%28int,%20java.lang.String%29" rel="noreferrer"><code>setNString</code></a> method whenever <code>CF_SQL_NVARCHAR</code> is used. So ultimately the value is sent to the database as <code>nvarchar</code>. (You can confirm this with a SQL Profiler)</p>

<pre><code>    // Query
    SELECT  ID
    FROM    Test
    WHERE   NVarcharColumn = &lt;cfqueryparam value="#form.value#" cfsqltype="cf_sql_nvarchar"&gt;

    // Log 
    spy(...)&gt;&gt; PreparedStatement[9].setNString(int parameterIndex, String value)

    // Profiler
    exec sp_prepexec @p1 output,N'@P1 nvarchar(4000)',N'SELECT  ID
            FROM    Test
            WHERE   NVarcharColumn = @P1 ',N'Стоял он, дум великих полн'
</code></pre>

<p><strong>CF_SQL_VARCHAR Test/Results:</strong> </p>

<p>In the case of <code>CF_SQL_VARCHAR</code>, it is technically flagged as <code>varchar</code>. However, the <code>String Format</code> setting ultimately controls how it is handled by the database. When the setting is enabled, it is handled as <code>nvarchar</code>. When it is disabled, it is treated as <code>varchar</code>. Again, you can verify this with a SQL Profiler.</p>

<p>Bottom line, everything I have seen so far says you are right on target about the implementation.</p>

<pre><code>    // Query
    SELECT  ID
    FROM    Test
    WHERE   PlainVarcharColumn = &lt;cfqueryparam value="#form.value#" cfsqltype="cf_sql_varchar"&gt;

    // Log
    spy(..)&gt;&gt; PreparedStatement[8].setObject(int parameterIndex, Object x, int targetSqlType)
    spy(..)&gt;&gt; parameterIndex = 1
    spy(..)&gt;&gt; x = ????? ??, ??? ??????? ????
    spy(..)&gt;&gt; targetSqlType = 12  (ie CF_SQL_VARCHAR)

    // Profiler (Setting ENABLED)
    exec sp_prepexec @p1 output,N'@P1 nvarchar(4000)',N'SELECT  ID
            FROM    Test
            WHERE   PlainVarcharColumn = @P1 ',N'Стоял он, дум великих полн'

    // Profiler (Setting DIS-abled)
    exec sp_prepexec @p1 output,N'@P1 varchar(8000)',N'SELECT  ID
            FROM    Test
            WHERE   PlainVarcharColumn = @P1 ','????? ??, ??? ??????? ????'
</code></pre>

