# How do I run a query to replace text with wildcard variables?
[Link to question](https://stackoverflow.com/questions/22711659/how-do-i-run-a-query-to-replace-text-with-wildcard-variables)
**Creation Date:** 1396006284
**Score:** 0
**Tags:** mysql, phpmyadmin
## Question Body
<p>Normally, I would run the following to replace text within a table in my MySQL database:</p>

<pre><code>UPDATE post SET pagetext = REPLACE(pagetext, '[TEXT1]', '[TEXT2]')
</code></pre>

<p>But how do you replace text that is followed by an alphanumeric set of characters?</p>

<p>This is what I'm trying to replace:</p>

<pre><code>[TEXT:12345678] will be replaced with [TEXT]
[/TEXT:12345678] will be replaced with [/TEXT]
</code></pre>

<p>How do I run the above query with some wildcard variables so anything with </p>

<pre><code>[TEXT:********]
</code></pre>

<p>will be replaced with</p>

<pre><code>[TEXT]
</code></pre>

<p>Forgive my ignorance, but I would like to run this through phpmyadmin - but how do I rewrite the REPLACE portion to accommodate the variables following the text?
Thanks in advance.</p>

## Answers
### Answer ID: 22711748
<p><strong>Daniel try to do this and you will solve your problem :</strong></p>

<ol>
<li>Export your table into a .SQL file using the EXPORT function from
the <code>phpMyAdmin</code> panel.</li>
<li>Using <code>sed</code> command in <code>linux</code> replace your tags using it's
wildcard(.)</li>
<li><p>Run the replace command:<br>
<code>cat post_table.sql | sed 's/latex:......../latex/g' &gt; post_table_complete_output.sql</code></p></li>
<li><p>Then import the output file in your database.</p></li>
</ol>

<p>Done.</p>

