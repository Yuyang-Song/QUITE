# Using custom rewrite rules in Wordpress
[Link to question](https://stackoverflow.com/questions/30617744/using-custom-rewrite-rules-in-wordpress)
**Creation Date:** 1433328010
**Score:** 1
**Tags:** php, wordpress, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I am trying to create custom rewrite rules in WordPress so that I can pass data to a page based on what is in the query string.</p>

<p>My page works fine:
<code>/retailers-a-z/?merchant=some_merchant</code>
and then also
<code>/retailers-a-z/?merchant=some-merchant&amp;offer=some-offer</code></p>

<p>I first tried to create a rewrite rule for this in .htaccess but since realised WordPress has it's own internal redirection database.. so after a lot of research I managed to come up with the following code... However, it is still not working.. Whenever I try to access
<code>/retailers-a-z/some-retailer</code> or <code>/retailers-a-z/some-retailer/some-offer</code> it just loads the home page.</p>

<p>functions.php:</p>

<pre><code>function wp_raz_rules()
{
  add_rewrite_rule(
    'retailers-a-z/([^/]+)/?$',
    'index.php?merchant=$matches[1]',
    'top'
  );

  add_rewrite_rule(
    'retailers-a-z/([^/]+)/([^/]+)/?$',
    'index.php?merchant=$matches[1]&amp;offer=$matches[2]',
    'top'
  );

  add_rewrite_tag('%merchant%', '([^/]+)');
  add_rewrite_tag('%offer%', '([^/]+)');
}
add_action('init', 'wp_raz_rules');

function wp_raz_vars($vars)
{
  $vars[] = 'merchant';
  $vars[] = 'offer';
  return $vars;
}
add_filter('query_vars', 'wp_raz_vars');
</code></pre>

<p>I then believe I can access them with <code>get_query_var('merchant')</code> and <code>get_query_var('offer')</code> instead of <code>$_GET[]</code></p>

<p>Any ideas? Thanks:)</p>

## Answers
### Answer ID: 30621534
<p>Managed to fix it by explicitly defining the page name in the query string.</p>

<p><code>index.php?pagename=retailers-a-z&amp;merchant=$matches[1]&amp;offer=$matches[2]</code></p>

<p>Not 100% sure if it is the correct way of doing it.</p>

