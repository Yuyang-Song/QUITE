# How to properly migrate to MySQLi in PHP 5.5+
[Link to question](https://stackoverflow.com/questions/35793789/how-to-properly-migrate-to-mysqli-in-php-5-5)
**Creation Date:** 1457087625
**Score:** 0
**Tags:** php, mysqli, upgrade, deprecated
## Question Body
<p>I have upgraded PHP from 5.4 to 5.5, and there was a WARNING of mysql functions being deprecated. I have upgraded by using</p>

<pre><code> $conn = mysqli_connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE);
</code></pre>

<p>and using <code>mysqli_query</code> and similar functions, where the syntaxis is almost identical. I am using the procedural method, so I only change <strong>mysql_query</strong> (its counterpart function receives one more parameters, namely the database object) and because it is abstracted in a function, I only need to have a global $conn in one or two functions, and the rest of the code is almost identical, changing <strong>mysql_fetch_object</strong> by <strong>mysqli_fetch_object</strong>, etc., so the impact in code rewriting is minimal. </p>

<p>Is there some better form of upgrading to improve my queries, I find this modification somehow strange and that could not take the best benefits from the upgrade.</p>

