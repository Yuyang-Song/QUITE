# PHP: how to switch from raw SQL query to laravel raw query?
[Link to question](https://stackoverflow.com/questions/61591303/php-how-to-switch-from-raw-sql-query-to-laravel-raw-query)
**Creation Date:** 1588592084
**Score:** 0
**Tags:** php, sql, laravel
## Question Body
<p>When switching to Laravel, SQL queries are changed. </p>

<p>From this:</p>

<pre><code>$sql = "SELECT * FROM table";
$result = mysqli_query($db, $sql);
</code></pre>

<p>to:</p>

<pre><code>$sql = 'SELECT * FROM table';
$result = DB::select($sql);
</code></pre>

<p>(I want to use SQL raw queries in LARAVEL to make rewriting the code easier <a href="https://laravel.com/docs/7.x/database#running-queries" rel="nofollow noreferrer">https://laravel.com/docs/7.x/database#running-queries</a>)</p>

<p>Sorry if this question is obvious, but I'm a beginner and don't understand the other answers I've found. Now what to add to the new code, so the old $result and new $result behave the same? </p>

<p>Because new $result is an array, right? I need to have the new $result behave like the old $result  to change the code easily.</p>

<p>Optional: do you know which topics I need to learn to understand this better myself?</p>

