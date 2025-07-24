# PHP Convert array element to string prints &quot;Array&quot;
[Link to question](https://stackoverflow.com/questions/28174205/php-convert-array-element-to-string-prints-array)
**Creation Date:** 1422373012
**Score:** 0
**Tags:** php
## Question Body
<p>I query a database to obtain an array of results.</p>

<pre><code>$usersArray = $db-&gt;getAllUsers();  // db-Query
</code></pre>

<p>If I print out the array's var_dump, its content is structured in form of other arrays:</p>

<pre><code>array(9) { [0]=&gt; **array**(1) { ["column"]=&gt; string(20) "..." } [1]=&gt; **array**(1) { ["column"] (remaining 8 are the same).
</code></pre>

<p>Now I need these values (which are correct, so far) to be casted as strings, so that:</p>

<pre><code>array(9) { [0]=&gt; **string**(1) { ["column"]=&gt; string(20) "..." } [1]=&gt; **string**(1) { ["column"] ....
</code></pre>

<p>There are several answers to this here and elsewhere, such as </p>

<p>-array_map: here I can actually cast the content as string, but- it prints "Array" instead the value. It tried then getting the content via </p>

<pre><code>$users = array_map('strval',implode( $usersArray));
$users = array_map('strval', print_r($usersArray));
</code></pre>

<p>Neither of those worked.</p>

<p>Is there a method through which I could cast the content as string <strong>and</strong> get the content ? Or should I rewrite the query to format the result as strings ? </p>

## Answers
### Answer ID: 28174773
<p>You have a wrong understanding of types or at least this:</p>

<pre><code>array(9) { [0]=&gt; **string**(1) { ["column"]=&gt; string(20) "..." } [1]=&gt; **string**(1) { ["column"] ....
</code></pre>

<p>doesn't make any sense. You believe you want elements to be of type string but yet contain array data which really doesn't work.
What you actually want is a different array structure but you are heading in the wrong direction for that.</p>

<p>You basically have two options:</p>

<ol>
<li><p>Modify the getAllUsers() method in a way that returns your data in a structure you actually need.</p></li>
<li><p>Modify the data after you have received it. Obviously there's no builtin function convert_data_to_how_i_want_them() - so a basic understanding of arrays is required.
Basically you create a new array and copy those values you need to the position you need them at.</p></li>
</ol>

<p>Something like this should do the trick in this case:</p>

<pre><code>$out = array();
foreach($in as =&gt; $value) {
    $out[] = $value['column'];
}
</code></pre>

