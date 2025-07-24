# Error when trying to run an update statement and getting &quot;SQL statement is nested too deeply&quot;
[Link to question](https://stackoverflow.com/questions/3545740/error-when-trying-to-run-an-update-statement-and-getting-sql-statement-is-neste)
**Creation Date:** 1282551260
**Score:** 0
**Tags:** sql, sql-server-2008
## Question Body
<p>I am getting this error when I run a certain SQL statement. I have looked into this and haven't really got anywhere.</p>

<blockquote>
  <p>Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries</p>
</blockquote>

<p>I cannot post the actual query with data as it contains some sensative information but basically I am creating an image map using an editor (similar to FCKEditor) and posting that to my database. Everything is Ok up to a point, then I go to add another area tag to the map and it breaks. I don't think this is size of data related as I can type in more characters that the area tag takes and it will still work. For instance, it will raise the error when I add</p>

<pre><code>&lt;area id="" /&gt;
</code></pre>

<p>but is ok when I write a longer piece of text like:</p>

<blockquote>
  <p>this is some test text and I am trying to test if it is a character limit.</p>
</blockquote>

<p>The error occurs when I run the statement in SQL Management Studio as well, not just in my code. Is it something to do with the double quotes? Has SQL had as many as it can cope with?</p>

<p>I am using Windows SQL Server 2008 Web Edition.</p>

<p>Would appreciate some help, thanks.</p>

<p>EDIT: It turns out, all <code>"</code> are being replaced with <code>' + CHAR(34) + '</code>, replacing all these with actual <code>"</code> in the SQL statement has resolved these. Now I just need to figure out why these are being replaced.</p>

## Answers
### Answer ID: 3547283
<p>It turns out, all <code>"</code> are being replaced with <code>' + CHAR(34) + '</code>, replacing all these with actual <code>"</code> in the SQL statement has resolved this issue.</p>

