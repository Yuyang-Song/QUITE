# PHP SQL Loop Returns PHP Code
[Link to question](https://stackoverflow.com/questions/33648690/php-sql-loop-returns-php-code)
**Creation Date:** 1447237953
**Score:** 0
**Tags:** php, html, mysql, select, drop-down-menu
## Question Body
<p>I am trying to create a HMTL select box which populates from a table in a SQL database.</p>

<p>This is my test code:</p>

<pre><code>&lt;head&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;?php
mysql_connect('localhost', 'root', 'apassword');
mysql_select_db('webforms');

$sql = "SELECT site FROM sites_rcs";
$result = mysql_query($sql);

echo "&lt;select name='sub1'&gt;";
while ($row = mysql_fetch_array($result)) {
    echo "&lt;option value '" . $row['site'] ."'&gt;" . $row['site'] ."&lt;/option&gt;";
    }
echo "&lt;/select&gt;"            

&lt;/body&gt;
</code></pre>

<p>When I open this page in a web browser I get this result:</p>

<pre><code>"; while ($row = mysql_fetch_array($result)) { echo "" . $row['site'] .""; } echo ""
</code></pre>

<p>I have tried rewriting the code from various examples provided on the internet:
<a href="https://www.youtube.com/watch?v=IVl5GPpMJsY" rel="nofollow">https://www.youtube.com/watch?v=IVl5GPpMJsY</a>
<a href="http://www.yourwebskills.com/mysqldropdown.php" rel="nofollow">http://www.yourwebskills.com/mysqldropdown.php</a></p>

<p>When I run the query <code>SELECT site FROM sites_rcs</code> in phpMyAdmin it returns the values in a list.</p>

<p>Any ideas?</p>

## Answers
### Answer ID: 33648960
<p>1- Make sure you have a server with php installed. 
2- Make sure your file is .php not .html 
3- Make sure your server is running
4- If testing on a local machine, make sure you're running the file through the server and not by double clicking it</p>

### Answer ID: 33648744
<p>Is PHP installed on the web server? Looks like the server just responds with the contents of your php file. Have a look at the page source.</p>

