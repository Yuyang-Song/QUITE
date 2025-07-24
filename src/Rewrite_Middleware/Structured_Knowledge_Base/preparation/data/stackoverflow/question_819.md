# Optimizing a Wordpress Query
[Link to question](https://stackoverflow.com/questions/43904571/optimizing-a-wordpress-query)
**Creation Date:** 1494462046
**Score:** 0
**Tags:** mysql, wordpress
## Question Body
<p>I'm working on a WordPress site with a large product database. I need to make a listing of all the products with a single taxonomy term exception. Using wp_query() creates a huge object and takes a long time. Also, for some reason, my arguments will not exclude products from the one taxonomy term I don't want listed. Here is my current query:</p>

<pre><code>$args = array(
    'post_type' =&gt; 'products',
    'post_status' =&gt; 'publish',
    'orderby' =&gt; 'post_title',
    'numberposts' =&gt; -1,
    'tax_query' =&gt; array(
        'taxonomy' =&gt; 'product-main-cats',
        'field'    =&gt; 'term_id',
        'terms'    =&gt; array(23),
        'operator' =&gt; 'NOT IN',
    ),
);
$prods = new WP_Query( $args );
</code></pre>

<p>I want to rewrite this query using the wpdb class so that I only fetch exactly what I need for my listing instead of the huge wp_query() object. The only columns I need from the wp_post table are, ID and post_title. I'm just not sure of the mySQL syntax, especially for excluding the posts related to the single taxonomy term. Can anyone help me rewrite this?</p>

<p>TIA!</p>

## Answers
### Answer ID: 43907510
<p>You can write this query via <code>$wpdb</code> , I have attached a sql query version below of your WP_Query.</p>

<pre><code>global $wpdb;
$results = $wpdb-&gt;get_results( "SELECT   wp_posts.* FROM wp_posts  WHERE 1=1  AND wp_posts.post_type = 'products' AND ((wp_posts.post_status = 'publish'))  ORDER BY wp_posts.post_title DESC", ARRAY_A );
</code></pre>

