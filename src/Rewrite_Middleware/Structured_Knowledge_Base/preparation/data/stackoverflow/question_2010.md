# Multiple prepared statements (SELECT)
[Link to question](https://stackoverflow.com/questions/15501809/multiple-prepared-statements-select)
**Creation Date:** 1363702204
**Score:** 0
**Tags:** php, sql, mysqli, statements
## Question Body
<p>I'm trying to change my SQL queries with prepared statements. 
The idea: I'm getting multiple records out of the database with a while loop and then some additional data from the database in the loop.</p>

<p>This is my old SQL code (simplified):</p>

<pre><code>$qry = "SELECT postId,title,userid from post WHERE id='$id'"; 
$rst01 = mysqli_query($mysqli, $qry01);
// loop trough mutiple results/records
while (list($postId,$title,$userid) = mysqli_fetch_array($rst01)) {
// second query to select additional data
$query05 = "SELECT name FROM users WHERE id='$userid";
$result05 = mysqli_query($mysqli, $query05);
$row05 = mysqli_fetch_array($result05);
$name = $row05[name ];

echo "Name: ".$name;

// do more stuff

// end of while loop
}
</code></pre>

<p>Now I want to rewrite this with prepared statements. 
My question: is it possible to run a prepared statement in the fetch of another prepared statement ? I still need the name like in the old SQL code I do for the $name.</p>

<p>This is what've written so far. </p>

<pre><code>$stmt0 = $mysqli-&gt;stmt_init();
$stmt0-&gt;prepare("SELECT postId,title,userid from post WHERE id=?"); 
$stmt0-&gt;bind_param('i', $id);
$stmt0-&gt;execute();
$stmt0-&gt;bind_result($postId,$title,$userid);
// prepare second statement
$stmt1 = $mysqli-&gt;stmt_init();
$stmt1-&gt;prepare("SELECT name FROM users WHERE id= ?");
while($stmt0-&gt;fetch()) {

$stmt1-&gt;bind_param('i', $userid);
$stmt1-&gt;execute();
$res1 = $stmt1-&gt;get_result();
$row1 = $res1-&gt;fetch_assoc();

echo "Name: ".$row1['name'] ;

}
</code></pre>

<p>It returns an error for the second statement in the loop:  </p>

<pre><code> Warning: mysqli_stmt::bind_param(): invalid object or resource mysqli_stmt in ... 
</code></pre>

<p>If I use the old method for the loop and just the prepared statement to fetch the $name it works.</p>

## Answers
### Answer ID: 15501918
<p>You can actually do this with a single <code>JOIN</code>ed query:</p>

<pre class="lang-sql prettyprint-override"><code>SELECT p.postId, p.title, p.userid, u.name AS username
FROM post p
JOIN users u ON u.id = p.userid
WHERE p.id = ?
</code></pre>

<p>In general, if you are running a query in a loop, there is probably a better way of doing it.</p>

