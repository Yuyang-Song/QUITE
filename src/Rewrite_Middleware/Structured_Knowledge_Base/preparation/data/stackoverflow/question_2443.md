# Sphinxql with PDO php
[Link to question](https://stackoverflow.com/questions/34479944/sphinxql-with-pdo-php)
**Creation Date:** 1451215533
**Score:** 0
**Tags:** php, mysql, pdo, sphinxql
## Question Body
<p>I am integrating Sphinxsearch into my site, and rewriting my old code to use Sphinx.
The problem i got is with special characters inside MATCH in SphinxQL.<br>
Example : want to search for H&amp;M<br>
With plain mysql i get thousand of records, so im quite sure i got title's containing that word in my database.<br>
I don't need extended query syntax in MATCH.</p>

<pre><code>$q = "h&amp;m";  
$spxq = "SELECT * FROM sphinx_index WHERE MATCH(:query) LIMIT 0,10";  
$stmt = $DB-&gt;prepare($spxq);  
$stmt-&gt;bindValue(':query', $q, PDO::PARAM_STR);  
$stmt-&gt;execute();  
$res = $stmt-&gt;fetchAll(PDO::FETCH_ASSOC); 
</code></pre>

<p>This isn't returning any results.<br>
After this i tried escaping $q so :  </p>

<pre><code>$q = "h\&amp;m";
</code></pre>

<p>Still not working.Tried with double escaping too, still not working.<br>
Any help would be appriciated.</p>

## Answers
### Answer ID: 34824700
<p>Ok, i got this, if anyone in the future has this same problem.
The solution is to add the special characters you want to be able to search for in the <strong>sphinx.conf</strong> file, in the <strong>charset_table</strong>.</p>

<p>So for my case of H&amp;M, you need to add the &amp; character (U+026) in to the charset table.</p>

