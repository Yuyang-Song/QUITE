# Am I handling query errors correctly in Medoo Framework?
[Link to question](https://stackoverflow.com/questions/30599875/am-i-handling-query-errors-correctly-in-medoo-framework)
**Creation Date:** 1433257721
**Score:** 3
**Tags:** php, mysql, pdo, medoo
## Question Body
<p>I'm using Medoo Framework to handle my database queries. It is basically a PDO wrapper, I didn't find in their documentation how to handle errors or check the result, sometimes it return empty array, sometimes FALSE sometimes 0 etc.</p>

<p>As I couldn't understand how to handle errors this is what I'm doing currently using empty() because it can handle FALSE , 0 and empty Array I think it's okay here):</p>

<p><strong>On SELECT</strong> (Medoo returns array)</p>

<pre><code>// Same as:
// SELECT username FROM accounts WHERE id=$id AND suspended=0

$select = $database-&gt;select("accounts",["username"], [
    "AND" =&gt; [
        "id" =&gt; $id,
        "suspended"   =&gt; 0
    ]
]);

// I have to check if Query failed also if row was not found

if (empty($select) === FALSE &amp;&amp; count($select) &gt; 0)
{
      // It didn't FAIL
      // So i get username like this:
      $key      = array_keys($select)[0];
      $username = $select[$key]['username'];
}
else
{
      // It FAILED
}
</code></pre>

<p><strong>On INSERT</strong> (Medoo says it returns INSERT ID here)</p>

<pre><code>$insert = $database-&gt;insert("accounts", [
    "username"        =&gt; "$username"
]);

// Check if query didn't fail and actually inserted (affected rows i think?)

if (empty($insert) === TRUE OR $insert &lt; 1)
{
    // It Failed
}
</code></pre>

<p><strong>On UPDATE</strong> (This is actually the only clear query, it returns affected rows)</p>

<pre><code>$update = $database-&gt;update("accounts", ["brute_force[+]" =&gt; 1], ["id" =&gt; $user_id]);

if (empty($update) === TRUE OR $update &lt; 1)
{
     // It FAILED
}
// Check if query didn't fail and also affected row
</code></pre>

<p>I am so confused and unsure about these that I'm paranoid maybe I should just completely rewrite and use CodeIgniter like I always do.</p>

## Answers
### Answer ID: 63567288
<p>I almost didn't look at Medoo as a result of the earlier comments on this post but I'm glad I did so would like to correct some of the statements made in earlier replies to this question so potential MeDoo users are not dissuaded from using it.</p>
<p>Disclaimer - all my work with Medoo has been with mySQL databases.</p>
<p>It is a wrapper around PDO but so are the other tools mentioned so I'm not sure of the purpose of that comment.  The other tools mentioned provide more functionality in terms of ORM.  As a consequence of that, they base all their endpoints/methods on individual tables in the database whereas Medoo is based on the traditional CRUD methods which, in my opinion, makes more sense.  If you don't care about ORM, Medoo is fine.</p>
<p>You can check for any select/get/insert/update/delete errors by looking at key 2 of the error() method.  If it is NULL, no error occurred; if an error occurred it will contain a string error message.</p>
<p>Medoo does use prepared statements, maybe it didn't back in 2015 but it does now.</p>
<p>I'm not sure what the basis is for the statement &quot;it isn't tested&quot;.  I haven't come across any bugs so far.</p>
<p>Bottom line: if you are looking for a simple query builder that uses PDO and don't care about ORM, Medoo will probably work well for you.</p>

### Answer ID: 61499615
<p>The return object of update() is PDOStatement, so you can use its methods to get more information. </p>

<pre><code>$data = $database-&gt;update("account", [
    "age[+]" =&gt; 1
], [
    "user_id[&gt;]" =&gt; 100
]);
</code></pre>

<p>Returns the number of rows affected by the last SQL statement</p>

<pre><code>echo $data-&gt;rowCount();
</code></pre>

<p>You can check if its greater then Zero or is_numeric() function.</p>

### Answer ID: 30844752
<p>To check if <code>SELECT/UPDATE</code> statement succeeded I use:</p>

<p><code>if(!$select){
// SELECT failed
}</code></p>

<p>because MEDOO will return <code>FALSE</code> or <code>0</code> or <code>empty Array</code> if <code>SELECT/UPDATE</code> failed or no data were retrieved/updated, and all of these things are equal <code>FALSE</code> in an <code>if</code> statement. For <code>INSERT</code> you can use the same thing if your table in database has <code>ID</code> field as primary key; if you don't have primary key, then you could use <code>error()</code> method and parse response to check for errors, because <code>MEDOO</code> will return <code>0</code> even though the statement was executed.</p>

