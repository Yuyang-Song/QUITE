# WordPress ReWrite Rule And Matches Processing
[Link to question](https://stackoverflow.com/questions/33657378/wordpress-rewrite-rule-and-matches-processing)
**Creation Date:** 1447266552
**Score:** 1
**Tags:** php, regex, wordpress
## Question Body
<p>Its a WordPress Query and another add_rewrite_rule one for that matter.</p>

<p>What i want is to have a user enter the url and two custome marameters as such "<strong>foods/food</strong>".... so the url is <a href="http://wordpress_home/" rel="nofollow">http://wordpress_home/</a><strong>foods/food</strong>. 
Thing is that 'foods' is a redirect rule and i want to process 'food' further.</p>

<blockquote>
<pre><code>    add_rewrite_rule(
        "^foods/([0-9]+)",
        "index.php?page_id=\$matches[1]",
        "top"
    );
</code></pre>
</blockquote>

<p>In the above example, the 'foods' bit works. i'm currently checking for numbers but I now want to use 'food' by sending it to another function, processing it by getting relevant data from the 'food' function and then using the returned data to complete the url. 'Food' might return the correct 'page_id' but a database call is necessary using 'food' to get the 'page_id' to complete the url so the correct page for the correct user(s) will display.</p>

<p>I can't inject a function in to the rewrite rule above. Can any one help?
<br>I've tried <code>checkfood( $matches[1] )</code> but that just fails.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 53765219
<p>Add another parameter &amp;foods=1 so you can identify in the template_redirect if it should do anything.</p>

<pre><code>add_rewrite_rule(
        "^foods/([0-9]+)",
        "index.php?page_id=\$matches[1]&amp;foods=1",
        "top"
    );

add_action('template_redirect', 'fww_template_pretty_permalink_handler');
function fww_template_pretty_permalink_handler() {
    $foodspage = get_query_var('foods');
    if ($foodspage == 1) {
      //do whatever - load a specific template, or set up objects or whatever
      //depends how your code works
    }
}
add_filter( 'query_vars', 'fww_rewrite_add_var' );
function fww_rewrite_add_var( $vars )
{
   $vars[] = 'foods';
   return $vars;
}
</code></pre>

<p><strong>Note:</strong> If you are using hooks and actions, you won't need to add a template handler as you can just ensure you pass along a URL parameter to identify when your code should run.</p>

<p>You can check the query_var for existence in your hooks and actions, and these query vars are not visible since they're hidden by the rewrite.</p>

