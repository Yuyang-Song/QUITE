# How bad is $wp_rewrite-&gt;flush_rules() on &#39;init&#39; action hook?
[Link to question](https://stackoverflow.com/questions/28321875/how-bad-is-wp-rewrite-flush-rules-on-init-action-hook)
**Creation Date:** 1423054241
**Score:** 1
**Tags:** wordpress, performance, url-rewriting
## Question Body
<p>According to <a href="http://codex.wordpress.org/Rewrite_API/flush_rules" rel="nofollow" title="Rewrite API/flush rules">the Codex</a>:</p>

<blockquote>
  <p>[...] This function can be extremely costly in terms of performance. It should be used as sparingly as possible - such as during activation or deactivation of plugins or themes. Every attempt should be made to avoid using it in hooks that execute on each page load, such as <a href="http://codex.wordpress.org/Plugin_API/Action_Reference/init" rel="nofollow">init</a>.</p>
</blockquote>

<p>Ok, so, I know it shouldn't be used in every page load and I'm not, but I still need a very conditional rewrite rule on this project. 
I have these 2 url structures:</p>

<pre><code> - example.com/products/tables/fancy-computer-table //This is a product url, here I expect the normal behavior from wp.

 - example.com/products/tables/office //This should be some kind of a filter, where the site gets all the tables related to the office department. Note how both URL structure matches.
</code></pre>

<p>To make it work, I narrowed it down to these very specific URLs, using some regex. If matched, I'll run 2 queries to verify if the url I'm in is for the filter I want that rule to apply, or if it's a product url. In the latter, I want wordpress to behave normally. But I have to flush the rules either way, whether it's a product or it's the category and the filter, so that both pages work properly and dinamically.</p>

<p>I do all this to narrow down the use of this function to the least possible, but the Codex doesn't really tell me how bad it does affect the performance, or why.
I'm passing the parameter on that function as <strong>false</strong> by the way, so it doesn't rewrite my htaccess file, but I'm not sure where that <em>rewrite rule option</em> is stored, if it's on the memory somewhere, or on the database, wish they would provide some clarification on that.</p>

<p>Thanks in advance for reading this question. Any pointers are appreciated here, even if you want to point me to some other way of doing this. :)</p>

<hr>

<p><strong>EDIT</strong>: Posting some code here so you guys can actually understand what I mean and let me know if this maybe this could be bad practice... maybe a suggestion on how to do it better.</p>

<pre><code>&lt;?php function custom_rewrite_products()
{   
// regex to match either "products/tables/fancy-computer-table" or "products/tables/office"
preg_match('#products\/([^\/]+)\/([^\/]+)\/?#', $_SERVER['REQUEST_URI'], $url_matches);
if(is_array($url_matches)) {
    $query_category = new WP_Query('category_name='.$url_matches[1]);
    $query_category-&gt;get_posts();

    $args = array(
        'post_type' =&gt; 'filters',
        'name' =&gt; $url_matches[2]
    );
    $query_post = new WP_Query($args);
    $query_post-&gt;get_posts();

    if($query_category-&gt;have_posts() &amp;&amp; $query_post-&gt;have_posts()) {
        $category_ID = '';
        $filter = '';

        $category_ID = '' . $query_category-&gt;query_vars['cat'] . '';
        $filter = '' . $query_post-&gt;query_vars['name'] . '';
        $string = "index.php?cat={$category_ID}&amp;filter={$filter}";
        add_rewrite_rule('products/([^/]+)/([^/]+)/?$', $string, 'top');
    }

    global $wp_rewrite;
    //Call flush_rules() as a method of the $wp_rewrite object
    $wp_rewrite-&gt;flush_rules(false);
    }
 }
 add_action('init', 'custom_rewrite_products');
</code></pre>

<p>I still don't understand why, but the flush is needed here, so the <code>$category_ID</code> and <code>$filter</code> variables actually get passed to the rewrite rules. If I take it out, the rewrite just goes to the index page, the place where the values should be are empty.
In case you're wondering, I created the filters on a custom post type and they are related to each post by using a custom field, since they're like four or five and they're present on every category on this project. As you can see, I already have a category/subcategory structure and I didn't find it smart to create these filters once again by hand inside each main category.</p>

## Answers
### Answer ID: 28323570
<p>There is a 'rewrite_rules' record in the 'wp_options' table that includes all the rewrite rules. When calling flush_rules(), WordPress will clear this record and regenerate all the new rules, including the ones you're not changing.</p>

