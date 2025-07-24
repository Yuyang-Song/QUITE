# Output certain product page on homepage / WooCommerce shortcode not working properly
[Link to question](https://stackoverflow.com/questions/69527305/output-certain-product-page-on-homepage-woocommerce-shortcode-not-working-prop)
**Creation Date:** 1633960136
**Score:** 1
**Tags:** wordpress, woocommerce
## Question Body
<p>I need to output a certain product page on the homepage. <code>add_rewrite_rule</code> doesn't work for homepage for any reason (
there are actually no rewrite rules for the homepage in the database, WordPress seems to use some other functions to
query the homepage):</p>
<pre class="lang-php prettyprint-override"><code>//works fine
add_rewrite_rule( 'certainproductpage/?$',
    'index.php?post_type=product&amp;name=certainproduct',
    'top'
);
//does not work 
add_rewrite_rule( '', //tried everything like &quot;/&quot;, &quot;/?$&quot; etc
    'index.php?post_type=product&amp;name=certainproduct',
    'top'
);
</code></pre>
<p>After spending way too much time looking through wp / wc core code and stackoverflow I came across an alternative. I can
simply add a shortcode in the content of the page I need to be the homepage and a product page at the same
time: <code>[product_page id=815]</code>. Indeed it works great, but only if the shortcode is added in the admin editor or is
stored in the database (post_content). If I try to call the shortcode manually on the page template (
page-certainproductpage.php) then it outputs the product page without some necessary stuff (PayPal, PhotoSwipe and
Gallery js). Weirdly enough, if I keep the shortcode in the content (via Gutenberg / Code Editor) but don't
call <code>the_content</code> and only echo the shortcode then everything works fine:</p>
<pre class="lang-php prettyprint-override"><code>if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

get_header( 'shop' );

//works fine only if the same shortcode is within the certainproductpage's content
echo do_shortcode(&quot;[product_page id='815']&quot;);
//the_content();

get_footer( 'shop' );
</code></pre>
<p>Also when I try to add the shortcode via <code>the_content</code> filter hook before the do_shortcode function is applied in core's
default-filters.php ($priority &lt; 11), then I get only the error:</p>
<pre><code>NOTICE: PHP message: PHP Fatal error:  Maximum execution time of 30 seconds exceeded in /var/www/html/wp-includes/functions.php on line 5106
</code></pre>
<p>Unfortunately there is no stack trace logged. And the function around line 5107 is <code>wp_ob_end_flush_all</code> which is called on <code>shutdown</code> from <code>default-filters.php</code></p>
<p><code>echo do_shortcode(apply_filters('the_content', &quot;[product_page id=815]&quot;));</code> did not help either (same incomplete output as
with <code>echo do_shortcode(&quot;[product_page id=815]&quot;);</code>)</p>
<p>Also totally weird:
When I compare the string of the content from the editor and the string of the shortcode added programmatically it is
equal!:</p>
<pre class="lang-php prettyprint-override"><code>add_filter( &quot;the_content&quot;, function ( $content ){
            $wtf = &quot;&lt;!-- wp:paragraph --&gt;
&lt;p&gt;[product_page id=815]&lt;/p&gt;
&lt;!-- /wp:paragraph --&gt;&quot;;
            $result = $wtf === $content;
            ?&gt;&lt;pre&gt;&lt;?php var_dump($result)?&gt;&lt;/pre&gt;&lt;?php
            return $content;
}, 1 );
</code></pre>
<p>But if I replace <code>return $content</code> with <code>return $wtf</code> - I get the maximimum exucution time exceeded error.</p>
<p>So how can I properly output a product page on the homepage (&quot;/&quot;) or how can I get the same result with the shortcode
when applied within the <code>the_content</code> filter as when just adding the shortcode in the (Gutenberg) editor?</p>
<h3>Update</h3>
<p>Tested it with a simple custom shortcode outputting only a heading tag and it works fine with <code>the_content</code> filter. Also tried it on an absolutely clean site with only WooCommerce and PayPal installed - with the same results. Seems to be a bug on the WooCommerce side. Gonna run it through xDebug some day this week.</p>

## Answers
### Answer ID: 69529472
<p>I'd recommend one step at a time. First of all, does this work?</p>
<pre><code>add_filter( &quot;the_content&quot;, function ( $content ) {
   $content .= do_shortcode( '[product_page id=815]' );
   return $content;
}, 1 );
</code></pre>
<p>This should append a product page to every WordPress page/post.</p>
<p>If it works, then you need to limit it to the homepage only, by using is_front_page() conditional in case it's a static page:</p>
<pre><code>add_filter( &quot;the_content&quot;, function ( $content ) {
   if ( is_front_page() ) {
      $content .= do_shortcode( '[product_page id=815]' );
   }
   return $content;
}, 1 );
</code></pre>
<p>If this works too, then we'll see how to return a Gutenberg paragraph block, but not sure why you'd need that, so maybe give us more context</p>

### Answer ID: 69529469
<p>Ok, found a bit of a hacky solution. I just check on every page load whether the homepage is currently queried or not. Then I get the page content and check if it already contains the shortcode. If not then the page content gets updated in the database with the shortcode appended.</p>
<pre class="lang-php prettyprint-override"><code>//it has to be a hook which loads everything needed for the wp_update_post function 
//but at the same time has not global $post set yet
//if global $post is already set, the &quot;certainproductpage&quot;  will load content not modified by the following code
add_action( &quot;wp_loaded&quot;, function () {
    //check if homepage
    //there seems to be no other simple method to check which page is currently queried at this point
    if ( $_SERVER[&quot;REQUEST_URI&quot;] === &quot;/&quot; ) {
        $page    = get_post(get_option('page_on_front'));
        $product = get_page_by_path( &quot;certainproduct&quot;, OBJECT, &quot;product&quot; );

        if ( $page &amp;&amp; $product ) {
            $page_content       = $page-&gt;post_content;
            $product_id         = $product-&gt;ID;
            $shortcode          = &quot;[product_page id=$product_id]&quot;;
                    
            //add shortcode to the database's post_content if not already done
            $contains_shortcode = strpos( $page_content, $shortcode ) &gt; - 1;
            if ( ! $contains_shortcode ) {
                $shortcode_block = &lt;&lt;&lt;EOT
&lt;!-- wp:shortcode --&gt;
{$shortcode}
&lt;!-- /wp:shortcode --&gt;
EOT;
                $new_content     = $page_content . $shortcode_block;

                wp_update_post( array(
                    'ID'           =&gt; $page-&gt;ID,
                    'post_content' =&gt; $new_content,
                    'post_status'  =&gt; &quot;publish&quot;
                ) );
            }
        }
    }
} );

</code></pre>

