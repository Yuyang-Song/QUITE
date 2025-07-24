# Slugs breaking after the first word
[Link to question](https://stackoverflow.com/questions/25592098/slugs-breaking-after-the-first-word)
**Creation Date:** 1409489005
**Score:** 0
**Tags:** php, mysql, .htaccess, mod-rewrite
## Question Body
<p>I have a page, <code>project.php</code>. I am attempting to implement slugs. So lets say I have a database entry called <code>A Project</code>, and the slug is <code>a-project</code>. Here's the PHP code</p>

<pre><code>$slug = $_GET['name'];
try {
    $sql = "SELECT id FROM projects WHERE slug = '" . $slug . "' AND display = 1";
    $s = $pdo-&gt;prepare($sql);
    $s-&gt;execute();
} catch(PDOException $e) {
    die("Failed to run query: " . $e-&gt;getMessage());
}
</code></pre>

<p>This works. But when I decide to add in a rewrite rule in .htaccess like so:</p>

<pre><code>RewriteRule ^projects/([0-9a-zA-Z]+) project.php?name=$1 [NC,L]
</code></pre>

<p>This is the result:</p>

<pre><code>Failed to run query: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 1
</code></pre>

<p>Echoing out the query returns <code>SELECT id FROM projects WHERE slug = 'a' AND display = 1</code> which when run in phpMyAdmin works fine, as you'd expect as it runs fine without the rewrite rule.</p>

<p>Using <code>var_dump($_GET);</code> returns <code>array(1) { ["name"]=&gt; string(1) "a" }</code></p>

<p>This only happens on multi word slugs, if the project's slug is simply <code>project</code> it works</p>

<p>Why is my rewrite rule breaking off the slug after the first word and corrupting my query, and how can I fix it?</p>

## Answers
### Answer ID: 25592401
<p><code>([0-9a-zA-Z]+)</code> matches all characters that are between 0 and 9, a and z and A and Z. You will notice that the <code>-</code> character is not between them. Since the path segment that is being used for the slug is most likely not going to be used for anything else, consider matching it with <code>([^/]+)</code> instead. This will match it up until the next <code>/</code>.</p>

<pre><code>RewriteRule ^projects/([^/]+) project.php?name=$1 [NC,L]
</code></pre>

<p>As mentioned by Fabio: Please use prepared statements. Your current code is open to sql injection. If you learn how to properly use prepared statements, you never ever have to worry again about external input causing sql injections.</p>

