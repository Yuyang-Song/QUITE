# Ho can I execute multiple stored procedure calls in one query?
[Link to question](https://stackoverflow.com/questions/72656354/ho-can-i-execute-multiple-stored-procedure-calls-in-one-query)
**Creation Date:** 1655453995
**Score:** 0
**Tags:** entity-framework-core, entity-framework-6
## Question Body
<p>I'm rewriting the app which uses MS SQL database. There are few stored procedures which are being called. Let's say:</p>
<ul>
<li>InsertFile @fileId, @fileName</li>
<li>DeleteFile @fileId</li>
</ul>
<p>There is the case when you have to call these procedures. For example, request comes and to process this request you have to insert few files and delete few files:</p>
<pre class="lang-sql prettyprint-override"><code>InsertFile 100, file1
InsertFile 101, file2
DeleteFile 5
InsertFile 108, file8
</code></pre>
<p>Current app builds query as a string and then through <code>SqlCommand</code> executes it <strong>in one call</strong>.</p>
<p>In new app I'm using Entity Framework Core 6.0.5. I can call specific procedure in this way:</p>
<pre class="lang-cs prettyprint-override"><code>var fileIdParameter = new SqlParameter(&quot;@Id&quot;, fileId);
var fileNameParameter = new SqlParameter(&quot;@FileName&quot;, fileName);
await _db.Database.ExecuteSqlRawAsync(&quot;InsertFile @Id, @FileName&quot;, fileIdParameter, fileNameParameter);
</code></pre>
<p>But in case I described above there will be 5 separated calls to database. I want to do this <strong>in one database call</strong>.</p>
<p>How can I do this?</p>

## Answers
### Answer ID: 72657367
<p>You can execute multiple statements in one SQL:</p>
<pre class="lang-cs prettyprint-override"><code>var sql = @&quot;
   EXEC InsertFile @id1, @FileName1;
   EXEC InsertFile @id2, @FileName2;
   EXEC DeleteFile @id3;
   EXEC InsertFile @id4, @FileName4;
&quot;;

await _db.Database.ExecuteSqlRawAsync(sql, 
     new SqlParameter(&quot;@Id1&quot;, 100),
     new SqlParameter(&quot;@FileName1&quot;, &quot;file1&quot;),
     new SqlParameter(&quot;@Id2&quot;, 101),
     new SqlParameter(&quot;@FileName2&quot;, &quot;file2&quot;),
     new SqlParameter(&quot;@Id3&quot;, 5),
     new SqlParameter(&quot;@Id4&quot;, 108),
     new SqlParameter(&quot;@FileName4&quot;, &quot;file8&quot;)
);
</code></pre>

