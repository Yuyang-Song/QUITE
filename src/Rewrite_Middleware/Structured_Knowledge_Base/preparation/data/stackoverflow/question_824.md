# Oracle 12.1 strange plan when using string literal against VARCHAR2 column (NLS_COMP=BINARY_AI)
[Link to question](https://stackoverflow.com/questions/44099112/oracle-12-1-strange-plan-when-using-string-literal-against-varchar2-column-nls)
**Creation Date:** 1495383572
**Score:** 1
**Tags:** oracle-database, oracle12c, varchar, literals
## Question Body
<p>I'm having a very specific issue with Oracle 12.1 concerning the handling of string literal ending with space in SQL <code>WHERE</code> clause applied on a <code>VARCHAR2(2500)</code> column (named 'NOTES').</p>

<p>As I need Case-and-Accent-Insensitive string comparison, I alter the <code>NLS_COMP</code> and <code>NLS_SORT</code> in a Logon Database trigger:</p>

<pre><code>ALTER SESSION SET NLS_COMP='LINGUISTIC';  
ALTER SESSION SET NLS_SORT='BINARY_AI';
</code></pre>

<p>Then, if i try this (<em>notice the ' ' space at the end of 'cholera', it is needed as the space is present in the table data, and I can't change it as I only have read-only access to the table</em>):</p>

<pre><code>SELECT NOTES FROM DECCODESIDC WHERE NOTES='cholera ';
</code></pre>

<p>So far, so good, it returns the only row matching the criteria (<em>'Choléra '</em>)</p>

<p>But if i create a View based on the table, and I apply the same criteria, it doesn't return anything:</p>

<p><strong>SELECT NOTES FROM (SELECT NOTES FROM DECCODESIDC) WHERE NOTES='cholera ';</strong></p>

<p>I noticed that the <code>explain plan</code> is different between the two queries</p>

<p>Here is the first query explain plan:</p>

<p><a href="https://i.sstatic.net/TMmO3.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/TMmO3.png" alt="enter image description here"></a></p>

<p>Notice the 6 last digits of <code>HEXTORAW</code> : 61 20 00   -> 61='a', 20=' ' <em>(space)</em>, 00=end </p>

<p>And the second one:</p>

<p><a href="https://i.sstatic.net/cWEfS.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/cWEfS.png" alt="enter image description here"></a></p>

<p>Notice the 6 last digits of <code>HEXTORAW</code> : 72 61 00   -> 72='r', 61='a', 00=end</p>

<p>As we can see, the <code>HEXTORAW</code> function automatically added by Oracle remove the trailing space in the second query, but not in the first...</p>

<p>I'm aware that string literals are considered as <code>CHAR</code> by Oracle and are subject to space padding, but in this case the string literal is compared against a <code>VARCHAR2</code> type column... and it doesn't explain why the execution plans are differents ...</p>

<p>Am I missing something or is it a bug in Oracle ?</p>

<p>Benoit</p>

<p>ps: the fact is that I don't write such queries by hand, but rely on Entity Framework with Oracle Managed Drivers, so I don't have so much options concerning query rewriting :(</p>

<p>ps2: As a temporary workaround, I added a call to the TRIM oracle function on every VARCHAR2 column in my View, but it is suboptimal in term of performance... </p>

## Answers
### Answer ID: 44153950
<p>For anyone facing the same problem: I applied patch bundle 12.1.0.2.170117 and everything seems to be ok now... :/ </p>

