# Convert ASP code using Chr(13) to PHP
[Link to question](https://stackoverflow.com/questions/4033881/convert-asp-code-using-chr13-to-php)
**Creation Date:** 1288186859
**Score:** 0
**Tags:** php, asp-classic
## Question Body
<p>I am trying to move a old Classic ASP site to run in PHP. I am rewriting bits of it, however I have come across the following function that is causing me some problems. Basically the function <code>FixForSQL</code> is run on everything before adding it to the database and then <code>FixForHTML</code> is run on data returned with a SQL query to format it for display.</p>

<p>At the moment if I display a block of text retrieved from the database in PHP it shows as one huge block of text with no paragraph breaks, I presume because I haven't done the replace of <code>Chr(13)</code> and whatever <code>Chr(9)</code> is!</p>

<p>Does anyone know how to reproduce whatever is happening in PHP 5?</p>

<pre><code> Function FixForHTML(tmpText1)
    Dim tmpText2
    tmpText2 = tmpText1
    tmpText2 = Replace(tmpText2,Chr(13),"&lt;/p&gt;&lt;p&gt;" &amp; vbCrLf)
    tmpText2 = Replace(tmpText2,Chr(9),"&amp;#xa0;&amp;#xa0;&amp;#xa0;&amp;#xa0;")
    FixForHTML = tmpText2
 End Function

 Function FixForSQL(tmpText1)
    Dim tmpText2
    tmpText2 = tmpText1
    tmpText2 = Replace(tmpText1,vbCrLf,Chr(13))
    tmpText2 = Replace(tmpText2,Chr(39),String(2,39))
    FixForSQL = tmpText2
 End Function
</code></pre>

## Answers
### Answer ID: 4033916
<p><code>Chr(13)</code> is the the character whose ASCII code is 13. You can get it in PHP with, you guessed, <code>chr(13)</code>.</p>

<p><code>13</code> is the code for <em>Cariage return</em>. While <code>9</code> is for <em>Horizontal tab</em>. In PHP you can also get those characters in a parsable string (one delimited by <code>"</code>s) with <code>\n</code>, respectively <code>\t</code>.</p>

<p><a href="http://www.hobbyprojects.com/ascii-table/images/ascii-table1.gif" rel="nofollow">ASCII table</a></p>

<p>Sample code for PHP:</p>

<pre><code>$text = str_replace(array("\n", "\r"), array("&lt;/p&gt;&lt;p&gt;", "&amp;#xa0;&amp;#xa0;&amp;#xa0;&amp;#xa0;"), $text);
</code></pre>

<hr>

<p>As for the <code>FixForSQL</code> function, it just replaces <code>'</code> characters with <code>''</code> to escape them for the SQL query. </p>

