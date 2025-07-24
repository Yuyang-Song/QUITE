# Export a set of rewriting rules from php to apache: is that possible?
[Link to question](https://stackoverflow.com/questions/57461194/export-a-set-of-rewriting-rules-from-php-to-apache-is-that-possible)
**Creation Date:** 1565612800
**Score:** 0
**Tags:** php, apache, mod-rewrite, url-rewriting
## Question Body
<p>I have a Drupal website that I'm migrating to a custom php cms.</p>

<p>I have two types of drupal links:</p>

<p><strong>node/123</strong></p>

<p><strong>title-of-my-link</strong></p>

<p>With the new custom version, and after a database import, I've got:</p>

<p><strong>content.php?id=852</strong></p>

<p>I'm resolving this with an Apache rewrite rule that sends everything to a php file that does a mysql query and forward everything.</p>

<p><strong>Here's my process:</strong></p>

<h2>.htaccess</h2>

<pre><code>RewriteRule ^.*$ ./reenvio.php
</code></pre>

<h2>reenvio.php</h2>

<pre><code>//I get the part of the url that I need to and put it inside an $urlString variable, extracting just what is after the forwardslash symbol.

$x = $conectarDB-&gt;prepare("
    SELECT id, alias1, alias2
    FROM contenidos
    WHERE alias1 = ? OR alias2 = ?
");
$x-&gt;bindParam(1, $urlString);
$x-&gt;bindParam(2, $urlString);
$x-&gt;execute();
$urlDrupal = $x-&gt;fetch(PDO::FETCH_ASSOC);

$alias1 = strtolower($urlDrupal["alias1"]);
$alias2 = strtolower($urlDrupal["alias2"]);

//Then I do forward everything according to the id that I've found in the database that corresponds to the alias:

//I get the variables for the server first
$http = $_SERVER['REQUEST_SCHEME'];
$sitio = $_SERVER['HTTP_HOST'];

$id = $urlDrupal["contenidoID"];
$reenvioA = $http.'://'.$sitio.'/contenido.php?id='.$id;  

//and I do sent the user to the unfriendly link
header('Location: '.$reenvioA);
exit();
</code></pre>

<p>My question being:</p>

<h2>Is there a way to do that all into .htaccess?</h2>

## Answers
### Answer ID: 57467489
<p>When having a lot of <code>RewriteRules</code> that conform to the same pattern, you can use <a href="https://httpd.apache.org/docs/2.4/rewrite/rewritemap.html" rel="nofollow noreferrer"><code>RewriteMap</code></a>. 
<code>RewriteMap</code> supports lookup from a variety of sources, one being SQL with the use of <a href="https://httpd.apache.org/docs/2.4/mod/mod_dbd.html#connecting" rel="nofollow noreferrer"><code>mod_dbd</code></a>. However, if all your content has been already migrated and it's basically a static lookup, you can dump all your rules to a file and use another map type to avoid the <code>dbd</code> dependency.</p>

<p>A <code>RewriteMap</code> can only be defined in the <code>VirtualHost</code> context. If you don't have access to the main configuration this will not work for you.</p>

<p>First define your <code>Map</code> in the <code>VirtualHost</code> config and configure <code>dbd</code> if necessary (step omitted):</p>

<pre><code>RewriteMap drupalmap "dbd:SELECT id FROM contenidos WHERE alias1 = %s OR alias2 = %s"
</code></pre>

<p>A lookup map takes a <em>Pattern</em> and a <em>Substitution</em>, just like <code>RewriteRule</code>, so if you go with a file-backed map you can just dump the result of <code>SELECT alias1, id FROM contenidos UNION SELECT alias2, id FROM contenidos</code>. The format is quite straightforward, but you have examples in <a href="https://httpd.apache.org/docs/2.4/rewrite/rewritemap.html#txt" rel="nofollow noreferrer">the docs</a>.</p>

<p>Then change the <code>RewriteRule</code>:</p>

<pre><code>RewriteCond ${drupalmap:%1}  &gt;""      # Apply the rule if there is a result
RewriteRule ^(.*)$ contenido.php?id=${drupalmap:$1}
</code></pre>

<p>If you don't have access to the main server config, and your mapping doesn't have any logic, the "dirty" solution can be to dump all mappings to <code>RewriteRule</code> and paste them in <code>.htaccess</code> so you end up with a bunch of </p>

<pre><code>RewriteRule ^node/123$ contenido.php?id=852
RewriteRule ^title-of-my-link$ contenido.php?id=852
...
</code></pre>

<p>You can do this with a little script and the query suggested before but if you have <em>a lot</em> of rules this might have performance implications.</p>

