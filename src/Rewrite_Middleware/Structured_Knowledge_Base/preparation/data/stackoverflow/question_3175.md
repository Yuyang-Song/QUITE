# not getting SELECT COUNT to work in PHPMYADMIN
[Link to question](https://stackoverflow.com/questions/70112738/not-getting-select-count-to-work-in-phpmyadmin)
**Creation Date:** 1637850253
**Score:** 0
**Tags:** mysql, count, phpmyadmin, mariadb
## Question Body
<p>I am new to phpmyadmin. I am not getting simple COUNT function to work.</p>
<p>I created a database with 8 tables to handle all kinds of contacts, personal and business.
I have been practicing queries and joins (by copying from tutorials) and so far all have worked.
I have been trying to do a COUNT but I am getting an error.
&quot;#1060 - you have an error in your SQL syntax; ......&quot;</p>
<pre><code>SELECT COUNT (*) 
FROM tblcontacts
</code></pre>
<p>if I erase the word count it will give all the rows of tblcontacts
I have tried rewriting and changing puntuation , ; '' &quot;&quot; () capitals, but no result.</p>
<p>any suggestions would be appreciated</p>

## Answers
### Answer ID: 70112816
<p>Query should be</p>
<pre class="lang-sql prettyprint-override"><code>select COUNT(*) from tblcontacts;
</code></pre>

