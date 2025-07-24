# MYSQL optimization and design rules: PHP method vs MYSQL procedure on local host
[Link to question](https://stackoverflow.com/questions/8269705/mysql-optimization-and-design-rules-php-method-vs-mysql-procedure-on-local-host)
**Creation Date:** 1322226998
**Score:** 1
**Tags:** php, mysql, sql, optimization
## Question Body
<p>I don't know if this is a dumb question but I have this two doubts maybe you can help me clear out: </p>

<p>If my database and web server are on the same host, is there any relevant benefit on putting my procedures for conditionally selecting (using more than one SQL query) elements from a table in a SQL database procedure instead of just implementing them in a webserver-side script (in my case PHP) method with the rest of the web application code?</p>

<p>Secondly, and maybe even more important: Am I breaking any design rules doing / not doing this?</p>

<p>More specifically, I made a PHP script to select a random row from a table according to a probability density function determined by the number of previous selections of each row, which goes like this:</p>

<pre><code>function acceptation_rejection_method($link,$tablename,$column,$condition="")
{
    $max=get_col("max(".$column.")",$tablename,$link,$condition);
    $min=get_col("min(".$column.")",$tablename,$link,$condition);
    $bar_value=mt_rand($min,$max);

    $count=get_nelements($tablename, $link,"where ".$column."&lt;=".$bar_value);
    $selected_row=get_row(mt_rand(0,$count-1), $tablename, $link,"where "
    .$column."&lt;=".$bar_value);
    return $selected_row;
}
</code></pre>

<p>My function implements the acceptance rejection method (http://en.wikipedia.org/wiki/Acceptance-rejection_method), and my question is: Taking on account that my database and my web server are on the same host, is it of any improvement to rewrite that script as SQL code returning the row? (Assuming that all users of my app are using it constantly, like almost once in every request)</p>

## Answers
### Answer ID: 8272398
<p>If I'm interpreting your question correctly, you want to know whether you should encode your acceptance/rejection algorithm into a pure database function, or whether what you're doing here is "right", from both an architectural and a performance point of view.</p>

<p>From a performance point of view, if there were a way to represent the query as a single SQL statement, it would likely be faster than your current implementation, but (assuming the column is indexed), probably not all that much faster. </p>

<p>You could, of course, create a stored procedure - but it looks like you're running this on multiple tables and columns, so you'd end up with lots of stored procedures. </p>

<p>Stored procedures have benefits and drawbacks, but in this case I'd say they make the application more fragile. Again, I doubt whether you'd see a huge performance impact.</p>

<p>Architecturally, I think what you're doing is likely the cleanest solution - you're abstracting the algorithm behind a single method. </p>

### Answer ID: 8270075
<blockquote>
  <p>In a simple MVC architecture design where database and web server are on the same host</p>
</blockquote>

<p>Eh? MVC is a design pattern not a system/service architecture.</p>

<blockquote>
  <p>is there any relevant benefit on putting my procedures for conditionally selecting (using more than one SQL query) elements from a table in a SQL database procedure instead of just implementing them in a webserver-side script</p>
</blockquote>

<p>Firstly, for the same population, you shouldn't need "more than one SQL query" regardless if you are looking at the entire sample or just a subset. i.e. your algorithm is flawed regardless of how you implement it.</p>

<p>Secondly, using the script you are hauling large amounts of data between the database and the PHP script which is an overhead. You are processing large amounts of data in PHP. PHP is not explicitly designed form manipulating large data sets - SQL and PL/SQL are. If you do as much processing as is practical on the database, then your application should run faster with less code.</p>

### Answer ID: 8269959
<p>I doubt that the <em>form</em> of requesting the same data from the same source does matter anything.     </p>

<blockquote>
  <p>Assuming that all users of my app are using it constantly, like almost once in every request</p>
</blockquote>

<p><s>Then you may want to think of the changing the approach.</s> </p>

<p>Sorry, I am contradicts with myself. </p>

<p><strong>First of all you have to profile your code and see, if it makes any trouble.</strong></p>

<p>Only if so, then you may want to think of the changing the approach.</p>

<p>Say, you can request all the numbers at once, randomize them and store in the memory cache. and then just request one by one, deleting after use. refresh on exhaust. </p>

