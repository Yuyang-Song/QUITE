# Strict Standards: Only variables should be passed by reference in with IF statement
[Link to question](https://stackoverflow.com/questions/26346785/strict-standards-only-variables-should-be-passed-by-reference-in-with-if-statem)
**Creation Date:** 1413225840
**Score:** 1
**Tags:** php
## Question Body
<p>Having issues with the following and I have not found an answer that would fit in yet...</p>

<p>Strict Standards: Only variables should be passed by reference in ...
Code is :
public function query($query)
    {</p>

<pre><code>    mysql_query('SET NAMES \'utf8\'', $this-&gt;connection);

    $result = mysql_query($query, $this-&gt;connection);
    $this-&gt;counter++;

    if (!$result) {
        throw new Exception('A MySQL error (#' . mysql_errno() . ' / ' . mysql_error() . ') occured in the following query: \'' . $this-&gt;parseQuery($query) . '\'');
    }

    if (in_array(strtoupper(array_shift(explode(' ', $this-&gt;parseQuery($query)))), array('SELECT', 'SHOW', 'EXPLAIN', 'DESCRIBE'))) 
    {
       $this-&gt;queries[] = $result;
    } 
</code></pre>

<p>Problem is in this part : if (in_array(strtoupper(array_shift(explode(' ', $this->parseQuery($query)))), array('SELECT', 'SHOW', 'EXPLAIN', 'DESCRIBE'))) </p>

<p>I tried to rewrite so it is not "nested"anymore...but no luck. I could use some help on this as my programming skills are not good enough</p>

## Answers
### Answer ID: 26346888
<p>try this : </p>

<pre><code>&lt;?php
    mysql_query('SET NAMES \'utf8\'', $this-&gt;connection);

    $result = mysql_query($query, $this-&gt;connection);
    $this-&gt;counter++;

    if (!$result) {
        throw new Exception('A MySQL error (#' . mysql_errno() . ' / ' . mysql_error() . ') occured in the following query: \'' . $this-&gt;parseQuery($query) . '\'');
    }
    $arr = array_shift(explode(' ', $this-&gt;parseQuery($query)));
    if (in_array(strtoupper($arr), array('SELECT', 'SHOW', 'EXPLAIN', 'DESCRIBE'))) 
    {
       $this-&gt;queries[] = $result;
    } 
</code></pre>

### Answer ID: 26346840
<p>It's in <code>array_shift</code> it only accepts variable reference:</p>

<pre><code>$arr = explode(' ', $this-&gt;parseQuery($query));

if (in_array(strtoupper(array_shift($arr)), array('SELECT', 'SHOW', 'EXPLAIN', 'DESCRIBE'))) 
{
    $this-&gt;queries[] = $result;
}
</code></pre>

<p>This will work</p>

