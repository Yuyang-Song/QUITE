# Access &amp; VBA, what is best &quot;architecture&quot; for a large, scalable application
[Link to question](https://stackoverflow.com/questions/38453356/access-vba-what-is-best-architecture-for-a-large-scalable-application)
**Creation Date:** 1468917314
**Score:** 1
**Tags:** sql, ms-access, architecture, vba
## Question Body
<p>I would like to know what is the best approach concerning mixing Access, SQL &amp; VBA.
Because I am currently working on a massive application, which is likely to evolve in future and I am asking myself if I did right.</p>

<p>I choosed to "hard code" most of my SQL queries in independant VBA modules, only giving values of criteria (for <code>SELECT/DELETE</code>) or fields (for <code>INSERT/UPDATE</code>) as parameters.
I firstly found this convenient since all I had to do was to make procedure call in my forms code, just passing the wanted values of my controls.</p>

<p>But the problem is that if I add a new field, rename my table or rename a field, I will have to rewrite all queries concerning that table one by one... That's quite annoying</p>

<p>I would like to know if there is existing a "standard architecture" to conveniently work on a scalable application in Access ?</p>

<p>By scalable I mean the database itself AND the application logic.</p>

## Answers
### Answer ID: 38464422
<blockquote>
  <p>... the problem is that if I add a new field, rename my table or
  rename a field, I will have to rewrite all queries concerning that
  table one by one</p>
</blockquote>

<p>I suggest you use <code>QueryDef</code> objects (saved queries) instead of keeping the SQL statement text in code modules.  </p>

<p>Then, when you have queries which reference a table or field name which later gets changed, you need not necessarily manually identify which queries need revision and edit those one at a time.  You could use something like <a href="https://stackoverflow.com/a/1223231/77335">swapTblNamesInQueryDefs()</a>.  I wrote that for table names, but it should work for field names, too.</p>

<p>If you continue to keep your SQL statements in code modules, you could do something similar with find &amp; replace.  However a potential complication there is that the word replacement would not be confined to only SQL statement text.  That would be a problem when the target word is present elsewhere in your VBA code but you don't want those occurrences replaced.  That is not a problem when your SQL is in <code>QueryDef</code> objects.  </p>

<p>Adding new fields is more challenging.  You could use <code>swapTblNamesInQueryDefs()</code> in <em>DisplayOnly</em> mode to examine the SQL from queries which contain the name of the modified table.  However, I don't see any automatable way to identify which of those queries should be modified and make the needed changes.</p>

