# MySQL &amp; PHP - Looping a query AND &quot;mapping&quot; the results of each loop to a unique array WITHOUT &quot;MySQL&quot; functions
[Link to question](https://stackoverflow.com/questions/24602488/mysql-php-looping-a-query-and-mapping-the-results-of-each-loop-to-a-unique)
**Creation Date:** 1404702048
**Score:** -1
**Tags:** php, mysql, arrays, loops
## Question Body
<p>I'll note that this is a very <strong>special case</strong>, hence the question to begin with. Under normal circumstances, such a function would be simple:</p>

<ol>
<li>I have an array named <code>$post_id</code>, which contains <strong>5</strong> values
(Each numerical)</li>
<li>In order to print each value in the array, I use the following loop:</li>
</ol>

<p>.</p>

<pre><code>for ($i = 0; $i &lt; $num; $i++)
            {
        echo $post_id[$i] . '&amp;nbsp;';
            }
</code></pre>

<p>...Which prints the following: <code>49, 48, 47, 46, 43</code></p>

<p>&nbsp;&nbsp;&nbsp;3. In my database, I have a table that looks like this:</p>

<pre><code>   post_categories
_____________________
 post_id  | category
__________|__________
    43    |  puppies
    43    |   trucks
    46    |   sports
    46    |      rio
    46    | dolphins
    49    |     fifa
</code></pre>

<p>&nbsp;&nbsp;&nbsp;4. So, using the data in the array <code>$post_id</code>, I'd like to loop a <strong>database query</strong> to retrieve each value in the <strong>category</strong> column from the <strong>post_categories</strong> table, and place them into uniquely named arrays based on the "<strong>post id</strong>", so that something like...</p>

<pre><code>echo $post_id_49[0] . '&amp;nbsp;', $post_id_46[1];
</code></pre>

<p>...Would print "<strong><code>fifa rio</code></strong>", assuming you use the above table.</p>

<p>An example of such a query:</p>

<pre><code>//Note - This is "false" markup, you'll find out why below

for ($i = 0; $i &lt; $num; $i++)
            {
    $query = "SELECT category FROM post_categories WHERE post_id = $post_id[$i]";
    fakeMarkup_executeQuery($query);

            }
</code></pre>

<p><strong>Why is this a "special" case?</strong> For the same reason the above query is "false".</p>

<p>To elaborate, I'm working inside of a software package that doesn't allow for "normal" queries so to say, it uses it's own query markup so that the same code can work with multiple database types, leaving it up to the user to specify their database type which leaves the program to interpret the query according to the type of database. It does, however, allow the query to be stored in the same "form" that all queries are, like "<code>$result = *query here*</code>" (With the only difference being that it executes itself).</p>

<p>For that reason, functions such as <code>mysql_fetch_array</code> (Or any MySQL/MySQLi function akin to that) cannot, and will not work. The software does not provide any form of built in alternatives either, effectively leaving the user to invent their own methods to achieve the same results. I know, pretty lame.</p>

<p>So, this is where I'm stuck. As you'd expect, all and any information you find on the Internet assumes you can use these MySQL &amp; MySQLi functions. <strong>What I need, is an alternative method to grab one array from the results of a looped query per loop.</strong> I simply cannot come to any conclusion that actually works.</p>

<p><strong>tl;dr</strong> I need to be able to <strong>(1)</strong> loop a query, <strong>(2)</strong> get the output from each loop as it's own array with it's own name, and <strong>(3)</strong>, do so <strong>without</strong> the use of functions like <code>mysql_fetch_array</code>. <strong>The query itself does not actually matter, so don't focus on that. I know what do with the query.</strong></p>

<p>I understand this is horrifically confusing, long, and complicated. I've been trudging through this mess for days - Close to the point of "cheating" and storing the data I'm trying to get here as raw code in the database. Bad practice, but sure as heck a lot easier on my aching mind.</p>

<p>I salute any brave soul who attempts to unravel this mess, good luck. If this is genuinely impossible, let me know so that I can send the software devs an angry letter. All I can guess is that they never considered that a case like mine would come up. Maybe this is much more simple then I make it to be, but regardless, I personally cannot come to an logical conclusion.</p>

<p><em>Additional note: I had to rewrite this <strong>twice</strong> due to some un explained error eliminating it. For the sake of my own sanity, I'm going to take a break after posting, so I may not be able to answer any follow up questions right away. Refer to the <strong>tl;dr</strong> for the simplest explanation of my need.</em></p>

## Answers
### Answer ID: 24602885
<p>Ok, assuming you can run a <em>function</em> (we'll call it <strike><code>find</code></strike> <code>select</code>) that accepts your query / ID and returns an array (list of rows) of associative arrays of column names to values (row), try this...</p>

<pre><code>$post_categories = [];
foreach ($post_id as $id) {
    $rows = select("SOME QUERY WHERE post_id = $id");
    /*
    for example, for $id = 46
    $rows = [
        ['category' =&gt; 'sports'],
        ['category' =&gt; 'rio'],
        ['category' =&gt; 'dolphins']
    ];
    */
    if ($rows) { // check for empty / no records found
        $post_categories[$id] = array_map(function($row) {
            return $row['category'];
        }, $rows);
    }
}
</code></pre>

<p>This will result in something like the following array...</p>

<pre><code>Array
(
    [49] =&gt; Array
        (
            [0] =&gt; fifa
        )

    [46] =&gt; Array
        (
            [0] =&gt; sports
            [1] =&gt; rio
            [2] =&gt; dolphins
        )

    [43] =&gt; Array
        (
            [0] =&gt; puppies
            [1] =&gt; trucks
        )

)
</code></pre>

### Answer ID: 24603397
<p>Sure you can do this , here ( assuming $post_ids is an array of post_id that you stated you had in the OP ), can I then assume that I could get category in a similar array with a similar query?</p>

<p>I don't see why you couldn't simply do this.</p>

<pre><code>$post_id = array(49, 48, 47, 46, 43);

$result = array();
foreach($post_id as $id)
{
    //without knowing the data returned i cant write exact code, what is returned?
    $query = "SELECT category FROM post_categories WHERE post_id = $id";
    $cats =   fakeMarkup_executeQuery($query);

    if(!empty($cats)) { 
        if(!isset($result[$id])){
            $result[$id] = array();
        }
        foreach( $cats as $cat ){ 
              $result[$id][] =&gt; $cat;
        }
   }
}
</code></pre>

<p>Output should be.</p>

<pre><code>Array
(
    [49] =&gt; Array
        (
            [0] =&gt; fifa
        )

    [46] =&gt; Array
        (
            [0] =&gt; sports
            [1] =&gt; rio
            [2] =&gt; dolphins
        )

    [43] =&gt; Array
        (
            [0] =&gt; puppies
            [1] =&gt; trucks
        )

)
</code></pre>

