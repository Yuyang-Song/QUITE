# wordpress search on multiple tables by default search query
[Link to question](https://stackoverflow.com/questions/16883341/wordpress-search-on-multiple-tables-by-default-search-query)
**Creation Date:** 1370180719
**Score:** 0
**Tags:** database, wordpress, preg-replace
## Question Body
<p>at least spending days in an MySQL nightmare hope someone can help me. I work on a tagging plugin for WP.</p>

<p>My problem sounds so easy: to keep the wordpress database clean and performant I decided to save additional fields (tags, titles, free text, urls, ...) in some extra tables and not adding typical meta fields. Now the search query must include these fields too.</p>

<p>After hours I found that (<a href="http://codex.wordpress.org/Custom_Queries" rel="nofollow">geoteagging wordpress example</a>):</p>

<pre><code>add_filter('posts_join', 'geotag_search_join' );
add_filter('posts_where', 'geotag_search_where' );
add_filter('posts_groupby', 'geotag_search_groupby' );
</code></pre>

<p>so far so good. Now its time to rewrite the query (geotag_search_where) but here the nightmare begins...</p>

<p>the custom table name is: "abc_tags" and the fields called "abc_title" and "abc_tags". 
"abc_tags" is a long text field with comma separated plain text items.</p>

<p>I dont understand the preg_replace manipulation with the query...I hope someone can help.</p>

<pre><code>function geotag_search_where( $where )
{
  if( is_search() ) {
    $where = preg_replace(
       "/\(\s*post_title\s+LIKE\s*(\'[^\']+\')\s*\)/",
       "(post_title LIKE $1) OR (geotag_city LIKE $1) OR (geotag_state LIKE $1) OR (geotag_country LIKE $1)", $where );
   }

  return $where;
}
</code></pre>

<p>Thanks.</p>

## Answers
### Answer ID: 16884532
<p>They're taking the <code>$where</code> string in the search <code>SQL</code> and rather than making it only search for the <code>post_title</code> variable, they're appending to the MySQL query string with the addition of <code>geotag_city</code>, <code>geotag_state</code> or <code>geotag_country</code> to cross check for other matches.</p>

<p>This way if you search for <em>"New York"</em> it will return results where the geotag_city matches as well as the title. (It's not good form to list every possible keyword in a title.)</p>

