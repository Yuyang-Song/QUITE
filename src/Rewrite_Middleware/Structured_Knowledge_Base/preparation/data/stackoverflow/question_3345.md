# Query in MS Access returns &quot;#Funktion!&quot;
[Link to question](https://stackoverflow.com/questions/76943521/query-in-ms-access-returns-funktion)
**Creation Date:** 1692605987
**Score:** 0
**Tags:** sql, ms-access
## Question Body
<p>I have to write a subquery to allow for easier sorting in an old access database.</p>
<p>What i have so far:</p>
<pre><code>Select Anschluss,
       AnschlussOhnePunkt,
       switch(
           IsNumeric(LEFT(AnschlussOhnePunkt,1)) = True, 
           len(AnschlussOhnePunkt), IsNumeric(LEFT(AnschlussOhnePunkt,1)) = False, 9999) as ordnung
from (
    select Anschluss, 
           switch(isnull(Anschluss), Anschluss,
           instr(Anschluss, '.') = 0, Anschluss, 
           instr(Anschluss, '.') = 1, left(Anschluss, instr(Anschluss, '.')-1)) as AnschlussOhnePunkt
    from T_Anschluss
)
</code></pre>
<p>Basically the subquery is supposed to return &quot;Anschluss&quot; and if it contains a dot it should remove that and return it as &quot;AnschlussOhnePunkt&quot;.</p>
<p>So 2.1 should become 2 etc.</p>
<p>But for some reason &quot;AnschlussOhnePunkt&quot; returns &quot;#Funktion!&quot; and I have no idea or explanation why.
Can someone explain why it comes or how to solve this problem?</p>
<ul>
<li>Rewriting the Query</li>
<li>Casting to string value</li>
<li>Using only the subquery alone</li>
</ul>
<p>None of it solved the problem and did apparently nothing.</p>

## Answers
### Answer ID: 76943635
<p><code>left(Anschluss, instr(Anschluss, '.')-1)</code> is a problematic statement, since if <code>instr(Anschluss)</code> is 0, that's a <code>Left(Anschluss, -1)</code> and the second argument of <code>Left</code> needs to be 0 or positive.</p>
<p>You may think this can never occur, since the <code>Switch</code> breaks earlier, but all arguments to a <code>Switch</code> are always evaluated, regardless if an earlier option is returned.</p>
<p>This means we have to escape that case with an <code>IIF</code>:</p>
<pre class="lang-sql prettyprint-override"><code>Left(
   Anschluss,
   InStr(Anschluss, '.') - 
      Iif(InStr(Anschluss, '.') &gt; 0, 1, 0) 
)
</code></pre>
<p>Note that this statement is predicated on <code>instr(Anschluss, '.') = 1</code> so it doesn't really make sense. I assume you'd want <code>instr(Anschluss, '.') &gt; 0</code> to detect if there's a dot somewhere in the string, not if there's a dot at the first position in the string.</p>

