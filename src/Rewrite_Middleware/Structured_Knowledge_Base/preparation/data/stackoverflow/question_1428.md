# Custom query_var rewrite rule being interrupted by &#39;page&#39; rewrite rule
[Link to question](https://stackoverflow.com/questions/75836442/custom-query-var-rewrite-rule-being-interrupted-by-page-rewrite-rule)
**Creation Date:** 1679677434
**Score:** 0
**Tags:** php, sql, wordpress, routes
## Question Body
<p>I have a custom rewrite rule that appears to be getting interrupted.</p>
<p><strong>The Code:</strong></p>
<pre><code>class drinks {

    public function drink_rewrite_rule() {
        add_rewrite_rule(
            'drinks/([a-z]+)[/]?$',
            'index.php?pagename=drinks&amp;drink=$matches[1]',
            'top'
        );
    }

    public function query_drink($urlslug) {
        global $wpdb;
        $table_name = $wpdb-&gt;prefix . 'drink_data'; // Replace 'custom_pages' with your actual table name
        $slug = $wpdb-&gt;get_var( $wpdb-&gt;prepare( &quot;SELECT slug FROM $table_name WHERE slug = %s&quot;, $urlslug ) );
        return $slug;
    }
}

$init = new drinks();

add_action('init', [$init, 'drink_rewrite_rule']);

add_filter('query_vars', function ( $query_vars ){
    $query_vars[] = 'drink';
    return $query_vars;
} );

function test() {
    $slug = get_query_var( 'drink' );
    $clean_slug = sanitize_title($slug);
    $class = new drinks();
    
    if ( get_query_var( 'drink' ) ==  false || get_query_var( 'drink' ) == '' ) {
        return $template;
    }
    
    if ( !$class-&gt;query_drink($clean_slug)) {
        global $wp_query;
        $wp_query-&gt;set_404();
        status_header( 404 );
    }

    return get_template_directory() . '/resources/page-templates/' . 'drink.php';
}
add_action( 'template_include', 'test');
</code></pre>
<p><strong>The Problem</strong></p>
<p>If I use the url <code>/drinks/coca-cola</code> the desired outcome occurs:</p>
<p><em>Matched Rule</em>
drinks/([a-z]+)[/]?$</p>
<p><em>Matched Query</em>
pagename=drink
&amp;drink=coca-cola</p>
<p><em>Query String</em>
pagename=drinks
&amp;drink=coca-cola</p>
<p>I then get the template page desired and can utilize the database query to dynamically populate data.</p>
<p>However, if I use the url <code>/drinks/gg4</code> the result is:</p>
<p><em>Matched Rule</em>
(.?.+?)(?:/([0-9]+))?/?$</p>
<p><em>Matched Query</em>
pagename=drinks%2Fgg4
&amp;page=</p>
<p><em>Query String</em>
pagename=drinks%2Fgg4</p>
<p>The query doesn't even get passed, as Query Monitor shows</p>
<pre><code>SELECT slug
FROM wp_drink_data
WHERE slug = ''
</code></pre>
<p>It is as though, for what appears to be a random reason, something is interrupting this query for some drink slugs and not others. I can enter a random name that isn't even in the database as the slug, and it will at least query the DB.</p>
<p>What am I getting wrong here? What am I missing?</p>

## Answers
### Answer ID: 75836819
<p><strong>SOLVED</strong>
As always with programming, sometimes it is the most ridiculous thing that was overlooked.</p>
<p>The issue lied in my rewrite rule.</p>
<p><code>'drinks/([a-z]+)[/]?$'</code> didn't allow for numeric characters nor dashes, which was why <code>gg4</code> wasn't catching.</p>
<p>Changing the rule to the following solves the issue.
<code>drinks/([a-zA-Z0-9\-]+)/?$</code></p>

