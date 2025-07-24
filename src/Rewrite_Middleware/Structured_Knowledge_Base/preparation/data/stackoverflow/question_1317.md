# Rewrite URL, replacing ID with title in query string
[Link to question](https://stackoverflow.com/questions/6993963/rewrite-url-replacing-id-with-title-in-query-string)
**Creation Date:** 1312881792
**Score:** 3
**Tags:** php, mysql, mod-rewrite
## Question Body
<p>I'm pretty new to mod_rewrite, but I've done some searching around and can't find an answer to this question. I've got a site which has only one PHP page serving up dozens of pages of content depending on the ID passed to it in the query string. I'd like to rewrite the URL so that this ID <em>disappears</em> and is replaced by the page's title as drawn from the database. For example</p>

<pre><code>www.example.com/index.php?id=19
</code></pre>

<p>is replaced by</p>

<pre><code>www.example.com/my-page-title
</code></pre>

<p>where "my-page-title" is the title of a page stored in the database at index 19. </p>

<p>Does anyone have any experience of this kind of rewrite, or is it even possible? </p>

<p>Thanks,</p>

<p>HR</p>

## Answers
### Answer ID: 6993995
<p>It's possible. You rewrite the url to send a $_GET-value, and use this value to find desired row. The url MUST be unique though, elsewise it can't find that unique row.</p>

<p>Example:</p>

<pre><code>RewriteRule ^([\d\w-]+)$ index.php?slug=$1 [L]
</code></pre>

<p>This gives you the value <code>$_GET['slug']</code> in PHP, which you can then use to find the value in the database.</p>

### Answer ID: 6994159
<p>Sure its possible, for a PHP script your .htaccess might look something like this:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteRule ^(.*)$ index.php?url=$1 [QSA,L]
&lt;/IfModule&gt;
</code></pre>

<p>This will rewrite all URLs except for directory or file names to "index.php?url=THE-TYPED-ADDRESS".</p>

<p>In your index.php you could then use the value of $_GET['url'] to determine the ID:</p>

<pre><code>// init DB layer
if (isset($_GET['url']) &amp;&amp; !empty($_GET['url'])) {
  $url = my_filter_function($_GET['url']); // filter input
  $pdo = my_get_pdo_function(); // get configured PDO objected
  $query = "SELECT id FROM my_router_table WHERE url = ? LIMIT 1"; // use prepared statements for security/performance reasons

  $stmt = $pdo-&gt;prepare($query);
  $stmt-&gt;bindValue(1, $url, PDO::PARAM_STR); // bind the value as a string

  // ternary operator expanded for readability
  if ($stmt-&gt;execute()) {
    $id = $stmt-&gt;fetch(PDO::FETCH_ASSOC);
  } else {
    $id = -1; // 404 page
  }

  // fetch content/render page according to ID
}
</code></pre>

<p>This is obviously an overly simplified example and you should really make sure you properly escape your input and use prepared statements to avoid security risks. Also, if you use MySQLi or another database access layer your prepare/execute/fetch code will vary slightly.</p>

