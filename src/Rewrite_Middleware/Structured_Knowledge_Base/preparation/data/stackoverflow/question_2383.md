# Wordpress Rewrite URL from API NOT the database
[Link to question](https://stackoverflow.com/questions/32209080/wordpress-rewrite-url-from-api-not-the-database)
**Creation Date:** 1440519464
**Score:** 0
**Tags:** php, wordpress
## Question Body
<p>I am building a site using WP and the Prosperent API.  I have built out product category pages where the user can see all the "Backpacks" and even sub categories.  I now want to build product detail pages.  Because the data comes from an API, and not stored in my database I don't have an easy want to have pretty links.  </p>

<p>On the category pages, I am linking each product like this:</p>

<pre><code>$pageLink = esc_url( add_query_arg( array (
                'gearID' =&gt; $value['catalogId'],
                'gearTitle' =&gt; $value['keyword']

            ),
            'http://www.example.com/products/g/' ) );
</code></pre>

<p>Which looks like this:</p>

<pre><code>http://www.example.com/products/g/?gearID=65198586171ee0ea97f3e39935468f4d&amp;gearTitle=The%20North%20Face%20Inferno%20Sleeping%20Bag:%20-20%20Degree%20Down%20Asphalt%20Grey/Caution%20Orange,%20Long
</code></pre>

<p>I AM Successfully capturing the "gearID" &amp; gearTitle query variables, This allows me to display the product on the product detail page template.  This is working great.  But the URL has my query strings in it. </p>

<p>I have tried several different variations, but this is my code for the rewrite:</p>

<pre><code>add_filter( 'query_vars', 'add_query_vars_filter' )
  function custom_rewrite_basic() {
    $gearID = get_query_var( 'gearID', false );
    add_rewrite_rule('^products/g/([0-9]+)/?', 'index.php/products/g/?gearID=$matches[1]', 'top');
    flush_rewrite_rules();
}
add_action('init', 'custom_rewrite_basic');
</code></pre>

<p>You can see in the code I have a get_query_var for the gearID, I attempted to insert where $match[1] is placed and didn't work.  Perhaps I need to store data in DB so WP knows what to rewrite?  Can't do it on the fly?</p>

<p>Ultimately, I want it to look like this:</p>

<pre><code>http://www.cascadegear.com/products/g/The%20North%20Face%20Inferno%20Sleeping%20Bag:%20-20%20Degree%20Down%20Asphalt%20Grey/Caution%20Orange,%20Lon
</code></pre>

