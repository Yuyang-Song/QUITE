# Wordpress Custom URL Rewrites
[Link to question](https://stackoverflow.com/questions/3307352/wordpress-custom-url-rewrites)
**Creation Date:** 1279790293
**Score:** 1
**Tags:** php, wordpress, mod-rewrite, url-rewriting
## Question Body
<p>I have links in my site that pass queries to pages that query from an external database. This works fine e.g.</p>

<pre><code>mysite.com/catalog/?tl=flooring
</code></pre>

<p>however i want to rewrite this url to appear as</p>

<pre><code>mysite.com/catalog/flooring
</code></pre>

<p>Ive tried modifying the rewrite rules in wordpress but it always displays the index page</p>

<pre><code>add_filter('rewrite_rules_array','wp_insertMyRewriteRules');
add_filter('query_vars','wp_insertMyRewriteQueryVars');
add_filter('init','flushRules');

// Remember to flush_rules() when adding rules
function flushRules(){
    global $wp_rewrite;
    $wp_rewrite-&gt;flush_rules();
}

// Adding a new rule
function wp_insertMyRewriteRules($rules)
{
    $newrules = array();
    $newrules['(catalog)/([a-zA-Z0-9 ]+)$'] = '/catalog/?tl=$matches[2]';
    return $newrules + $rules;
}

// Adding the id var so that WP recognizes it
function wp_insertMyRewriteQueryVars($vars)
{
    array_push($vars, 'id');
    return $vars;
}
</code></pre>

## Answers
### Answer ID: 3358014
<p><a href="http://www.rlmseo.com/blog/passing-get-query-string-parameters-in-wordpress-url/" rel="nofollow noreferrer">This article over at Raazorlight</a> goes into a bit more detail on the process of grabbing querystrings and URL rewriting in WP.</p>

<p>Also, check the comments there to see why calling <code>flushRules()</code> may not be necessary if you re-save permalinks. Optionally, <code>flushRules()</code> can be called just once during plugin activation callback. </p>

<p>Digging deeper, commenter 'pmdci' links over to an instructive post/saga on the related topic of <em>passing a query to a custom post type using a custom taxonomy</em>.</p>

### Answer ID: 3308484
<p>Rewrite rules in WordPress don't quite work like how you're expecting them to. All rewrite rules map to a file handler (almost always <code>index.php</code>), not another URL.</p>

<p>Here is a shortened code example;</p>

<pre><code>$rules['catalog/(.*)/?'] = 'index.php?pagename=catalog&amp;tl=$matches[1]';
array_push($query_vars, 'tl'); // note query var should match your query string
</code></pre>

<p>This would map <code>catalog/whatever</code> to the WordPress page 'catalog', and pass along the query var 'tl'. You could create a page template for 'catalog', then pick up the value of 'tl' using <code>get_query_var('tl')</code>.</p>

<p>Also avoid using query vars like <code>id</code> - use something more unique (like 'tl') to avoid clashes with WordPress.</p>

<p>And <strong>don't</strong> flush rules on every init! It's bad practice, and will write to <code>.htaccess</code> and call database updates on <strong>every</strong> page load!</p>

<p>WordPress will always flush permalinks whenever you update a post or your permalink structure (simply update your permalinks when you make changes to your code).</p>

