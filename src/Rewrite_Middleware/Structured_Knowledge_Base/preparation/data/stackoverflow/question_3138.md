# PyODBC + MS SQL Server + OPENROWSET to read/join Excel table with database table not working through PyODBC
[Link to question](https://stackoverflow.com/questions/68135559/pyodbc-ms-sql-server-openrowset-to-read-join-excel-table-with-database-table)
**Creation Date:** 1624645203
**Score:** 0
**Tags:** sql-server, excel, permissions, pyodbc, openrowset
## Question Body
<p>I'm working on an ETL that needs to join a user's Excel spreadsheet with one of our database tables in order to get the Latitude Longitude and return it to our users. For maintainability, I want a pipeline where a DB query does basically all the table work, rather than code, because then I can create a system where non-programmer analysts can patch together similar solutions by rewriting the query.</p>
<p>My proof-of-concept query (below/bottom) works in SQL Server Management Studio, but I've been unable to get it working through a PyODBC connection. Of note: <em>PyODBC is connecting with the same user that can perform this query in SQL Management Studio</em>. I'm getting the error (emphasis mine)..</p>
<blockquote>
<p>[Microsoft][ODBC Driver 17 for SQL Server][SQL Server]<strong>Cannot
initialize the data source</strong> object of OLE DB provider
&quot;Microsoft.ACE.OLEDB.12.0&quot; <strong>for linked server &quot;(null)&quot;</strong>. (7303)
(SQLExecDirectW); [42000] [Microsoft][ODBC Driver 17 for SQL
Server][SQL Server]OLE DB provider &quot;Microsoft.ACE.OLEDB.12.0&quot; for
linked server &quot;(null)&quot; returned message <strong>&quot;Failure creating file.&quot;</strong>.
(7412)')</p>
</blockquote>
<p>I've Googled this every way I can think of. There's a <a href="https://stackoverflow.com/questions/55644978/ad-hoc-access-to-ole-db-provider-microsoft-ace-oledb-12-0-has-been-denied-you/55645237">RegEdit trick</a> that didn't work or change the error. Another promising lead required <a href="https://stackoverflow.com/a/33131833">giving some users' temp folder permissions to the 'Everyone' user and applying full control</a>. I've tried this on several different user accounts to no effect and no change. But it's possible I'm not getting the right accounts or the right temp folders..</p>
<p>It seems like PyODBC connects in a way that is off limits to <code>OPENROWSET</code> &gt; <code>Microsoft.ACE.OLEDB.12.0</code> driver AND/OR, the context of this connection is unable to access/read the file location. For now, I've made sure the file location is accessible to 'Everyone' with Full Control enabled.</p>
<p>One more note, I've reduced this back to <code>SELECT * FROM FROM OPENROWSET(/*params*/)</code> and it throws the same error, so I'm certain the issue is exclusive to this <code>OpenRowSet</code> approach.</p>
<p>I don't have a super-specific question beyond &quot;Does anyone have any additional ideas why this isn't working?&quot; Alternatively, if there is a different way to execute this query in a scripted environment other than Python/PyODBC I'd be interested in that option too! Thanks</p>
<pre><code> select 
      /* THEIR TABLE DATA */
      d.&quot;civic number&quot;, 
      d.&quot;street name&quot;, 
      d.&quot;road type&quot;, 
      /* OUR SPATIAL DATA TABLE */
      a.FULLADDRESS,
      a.STATUS,
      a.SHAPE.STAsText() as wkt
      /* THEIR EXCEL TABLE RESOURCE */
      FROM OPENROWSET(
        ''Microsoft.ACE.OLEDB.12.0'',
        ''Excel 12.0;HDR=YES;Database=C:\Users\GeoTASKS\ETL\addresses.xlsx'',
        ''select * from [sheet1$]'') d 
      /* OUR DATABASE RESOURCE */
      join gis.ADDRESS_POINTS a
        on CONCAT(
                UPPER(RTRIM(LTRIM(d.&quot;civic number&quot;))), '' '',  
                UPPER(RTRIM(LTRIM(d.&quot;street name&quot;))), '' '', 
                UPPER(sde.RCGeoAbbreviateRoadType(d.&quot;road type&quot;))
        ) = upper(a.fulladdress)
      where UPPER(RTRIM(LTRIM(a.STATUS))) = ''FINAL''
</code></pre>

