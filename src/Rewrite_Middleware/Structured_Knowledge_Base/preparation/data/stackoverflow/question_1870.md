# How can I make this query work in D7?
[Link to question](https://stackoverflow.com/questions/10435688/how-can-i-make-this-query-work-in-d7)
**Creation Date:** 1336063145
**Score:** 3
**Tags:** mysql, sql, drupal, drupal-7
## Question Body
<p>I'm trying to rewrite this database query from the line 52 of my template.php D6 site</p>

<pre><code>  $uid = db_query('SELECT pm.author FROM {pm_message} pm INNER JOIN {pm_index} pmi ON pmi.mid = pm.mid AND pmi.thread_id = %d WHERE pm.author &lt;&gt; %d ORDER BY pm.timestamp DESC LIMIT 1', $thread['thread_id'], $user-&gt;uid);
</code></pre>

<p>into D7 standards.</p>

<p>But it keeps giving me</p>

<blockquote>
  <p>Recoverable fatal error: Argument 2 passed to db_query() must be an
  array, string given, called in
  C:\wamp2\www\site-name\sites\all\themes\simpler\template.php on line
  52 and defined in db_query() (line 2313 of
  C:\wamp2\www\site-name\includes\database\database.inc).</p>
</blockquote>

<p>This DB query is part of a template.php snippet that shows user pictures in Private Messages module, and makes it look like Facebook or other social networking site.  You can see the full snippet here.  Because Private Messages has a unified value $participants (or the message thread) this DB query is basically trying to isolate the last author except the current user. </p>

<p>What is the correct syntax?</p>

## Answers
### Answer ID: 10441165
<p>As the error message says: 'Argument 2 passed to db_query() must be an array ...'.</p>

<p>Drupal 7 switched the database layer to use <a href="http://php.net/manual/en/book.pdo.php" rel="nofollow">PDO</a>, so placeholder replacement in <a href="http://api.drupal.org/api/drupal/includes!database!database.inc/function/db_query/7" rel="nofollow">db_query()</a> changed a bit - try:</p>

<pre><code>$query = 'SELECT pm.author FROM {pm_message} pm'
  . ' INNER JOIN {pm_index} pmi ON pmi.mid = pm.mid AND pmi.thread_id = :thread_id'
  . ' WHERE pm.author &lt;&gt; :uid'
  . ' ORDER BY pm.timestamp DESC LIMIT 1';
$args = array(
  ':thread_id' =&gt; $thread['thread_id'],
  ':uid' =&gt; $user-&gt;uid,
);
$uid = db_query($query, $args)-&gt;fetchField();
</code></pre>

<p>Splitted and reformatted for readability. Untested, so beware of typos.</p>

<p>Note the <a href="http://api.drupal.org/api/drupal/includes!database!database.inc/function/DatabaseStatementInterface%3A%3AfetchField/7" rel="nofollow"><code>-&gt;fetchField()</code></a> at the end - this will only work for queries returning exactly one field (like this one). If you need to fetch more fields or records, look at the <a href="http://api.drupal.org/api/drupal/includes!database!database.inc/interface/DatabaseStatementInterface/7" rel="nofollow">DatabaseStatementInterface</a> documentation.</p>

