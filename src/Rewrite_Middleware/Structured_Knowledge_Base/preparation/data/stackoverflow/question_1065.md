# Wordpress add rewrite rule doesn&#39;t work for me
[Link to question](https://stackoverflow.com/questions/57361061/wordpress-add-rewrite-rule-doesnt-work-for-me)
**Creation Date:** 1565016663
**Score:** 1
**Tags:** wordpress, plugins, url-rewriting, permalinks
## Question Body
<p>I'm developing a plugin that creates 2 pages: one listing page and one details page.</p>

<p>I don't use custom types. I have created a table into the database where I save the company details and also a slug for the details page.</p>

<p>It's working properly but I have a problem with the URLs. They are not pretty.</p>

<p>On the listing page I use this code to create the link:</p>

<pre><code>    &lt;a href="https://www.website.com/company/details/?companyname=&lt;?php echo $value-&gt;company_slug; ?&gt;"&gt;&lt;?php echo stripslashes($value-&gt;company_name); ?&gt;&lt;/a&gt;
</code></pre>

<p>The generated link looks like this:</p>

<pre><code>    https://www.website.com/company/details/?companyname=new-company-name
</code></pre>

<p>I use the query because I need it on the details page, where I use this code:</p>

<pre><code>    $company_slug = $_GET['companyname'];
    $company_details = $wpdb-&gt;get_row("SELECT * FROM $table_company WHERE company_slug = '$company_slug'");
</code></pre>

<p>This is how I retrieve the company details from sql and it also works just fine.</p>

<p>I have created manually in Wordpress the details page.</p>

<p>The problem is that I want the details URL to look pretty, like this:</p>

<pre><code>    https://www.website.com/company/details/new-company-name/
</code></pre>

<p>Generating it like this it's easy but when I click, I get a 404, since the query from URL is missing. </p>

<p>I was thinking it's easy to create directly the pretty URL and on the details page to parse the URL and get the company slug. It didn't work. I get a 404 maybe because the page doesn't physically exist.</p>

<p>So, I've done some research about URL rewrite and I have found some examples but none worked.</p>

<p>I have found tried this code also:</p>

<pre><code>    add_filter('query_vars', function($vars) {
        $vars[] = "companyname";
        return $vars;
    });

    function custom_rewrite_rule() {
        add_rewrite_rule('^companyname/?([^/]*)/?','company/details/?companyname=$matches[1]','top');
    }
    add_action('init', 'custom_rewrite_rule', 10, 0);
</code></pre>

<p>I've read that I shouldn't use matches if I use a custom URL instead of index.php, so I have also tried without matches:</p>

<pre><code>    add_rewrite_rule('^companyname/?([^/]*)/?','company/details/?companyname=$1','top');
</code></pre>

<p>No results. If course, after every change I have saved again the permalinks. </p>

<p>This should be an easy task but somehow it doesn't work. </p>

<pre><code>    https://developer.wordpress.org/reference/functions/add_rewrite_rule/
</code></pre>

<p>Does anyone of you know how can I make this work?</p>

<p>Thank you.</p>

<p>Regards,
AG</p>

## Answers
### Answer ID: 57372685
<p>Thank you very much for your fast reply. It worked. </p>

<p>Of course, I had to change the link on the listing page to:</p>

<pre><code>    &lt;a href="https://www.website.com/company/details/&lt;?php echo $value-&gt;company_slug; ?&gt;"&gt;&lt;?php echo stripslashes($value-&gt;company_name); ?&gt;&lt;/a&gt;
</code></pre>

<p>I have removed the query from the link and it looks like this now:</p>

<pre><code>    https://www.website.com/company/details/new-company-name/ 
</code></pre>

<p>What I don't understand, is how does WP know which is the query, since I removed it from the link.</p>

<p>I can see the same data if I access</p>

<pre><code>    https://www.website.com/company/details/?companyname=new-company-name
</code></pre>

<p>or </p>

<pre><code>    https://www.website.com/company/details/new-company-name/
</code></pre>

<p>But, basically, this part (?companyname=) doesn't exist anymore in the link, since I changed it. </p>

<p>I have no query now in my plugin, but somehow everything works properly. :)</p>

<p>I did not declare it somewhere. It's completely gone and it works. </p>

<p>How does this code know that the query exists and it's retrieving the slug from the database?</p>

<pre><code>    $companyname = get_query_var( 'companyname' );
</code></pre>

<p>I only have this code now:</p>

<pre><code>    &lt;a href="https://www.website.com/company/details/&lt;?php echo $value-&gt;company_slug; ?&gt;"&gt;&lt;?php echo stripslashes($value-&gt;company_name); ?&gt;&lt;/a&gt;
</code></pre>

<p>So, no query in URL.</p>

<p>Thank you for your time.</p>

<p>Regards,
AG</p>

### Answer ID: 57363817
<p>I am assuming that the details page you created has the slug <code>company/details</code>. Here's what you need to do to make it work-</p>

<p><strong>1. Add the custom rewrite rules in functions.php file:</strong></p>

<pre><code>function theme_custom_rewrites() {
    add_rewrite_tag("%companyname%", "([a-z0-9\-_]+)");
  add_rewrite_rule('^company/details/([a-z0-9\-_]+)/?$', 'index.php?pagename=company/details&amp;companyname=$matches[1]', 'top');
}

add_action('init', 'theme_custom_rewrites'); 
</code></pre>

<p>It registers a new rewrite tag/query var named <code>companyname</code> to be used later and registers a custom rewrite rule for the specific URL structure you want (<code>/company/details/company_name</code>). </p>

<p><strong>2. Get the company name on the template file and use it:</strong> After you have added the above code and saved the permalinks, you can get the companyname just by using the <code>get_query_var()</code> function.</p>

<p><code>$companyname = get_query_var( 'companyname' );</code></p>

<p>Hope it helps. Thanks.</p>

