# How to change my URL structure on old php site using database values?
[Link to question](https://stackoverflow.com/questions/13689405/how-to-change-my-url-structure-on-old-php-site-using-database-values)
**Creation Date:** 1354559271
**Score:** 0
**Tags:** php, .htaccess, url-rewriting, url-routing
## Question Body
<p>I've been tasked with making the URLs for an old website "pretty"</p>

<p>It's a real estate website with a few dozen buildings and maybe 100ish total apartment listings.</p>

<p>Current urls are like: (i was able to remove <code>.php</code> extension easily with <code>.htaccess</code>)</p>

<pre><code>example.com/about?building-id=65
example.com/about?apartment-id=35
</code></pre>

<p>It gets considerably more complicated than that, with some search pages, different listings views, a contact form page that gets sent a building or apt id to prefil the form with some info, etc...</p>

<p>But for this example...</p>

<p>Ideally the URLs should be</p>

<pre><code>example.com/about/building-name/
example.com/about/building-name/apartment-name
</code></pre>

<p>The building name and apartment name are both values stored in the database, with the id#s as the primary keys.</p>

<p>After researching this issue a bit, I've determined a couple different approaches</p>

<p>1) <strong>Dynamically Generate the <code>.htaccess</code> file upon changes in admin</strong>  </p>

<ul>
<li>I think I can do this right? </li>
<li>It would explicitly rewrite just about every possible valid query string possibility ( up to couple hundred probably)</li>
<li>I imagine this will cause some performance issues, and is probably not best practice.</li>
<li>If its the easiest option, I'm ok with it being sloppy and bad practice as long as it works.</li>
</ul>

<p>2) <strong>Create a <em>controller</em> and rewite all queries to <code>index.php</code> which would put together all the views from here.</strong></p>

<ul>
<li>This is a bit more out of my comfort zone, but probably considered the best practice?</li>
</ul>

<p><em>The site is seriously old, and poorly put together (1000s of lines of custom (non OOP) php with lots of code duplication) For that matter, its really 2 different sites sharing the one database, and most of the code base (2nd was created some time ago with a copy-paste of original code base and has since grown apart)</em></p>

<hr>

<p><strong>My Question(s)</strong></p>

<ul>
<li><p>Are these viable options and did I miss any alternative?</p></li>
<li><p>Which approach should I take?</p></li>
</ul>

## Answers
### Answer ID: 13690755
<p>The actual generation of the .htaccess file wouldn't be an issue. I mean, writing 500 or 1000 lines of text to a file isn't such a big deal at all. However, the multitude of rules may actually very well give a performance hit, as the engine would check the requested URL against each for every HTTP request. It's probably not a very big performance hit, but it seems wasteful to me. Note that Apache, AFAIK, does no optimization on .htaccess rewrite rules or redirects, i.e. it doesn't build a big regex out of the small regexes, etc.</p>

<p>Option 2, parsing the request in PHP, is actually less work, I think, especially with a huge non-OOP site.</p>

<p>Consider a snippet like this:</p>

<pre><code>$uri = explode('/', $_SERVER['REQUEST_URI']);
if($uri[0] == 'about') {
    $id_aray = lookup_building_and_apartment_by_name( $uri[1], $uri[2] );
    $_GET['building_id'] = $id_array['building'];
    $_GET['apartment_id'] = $id_array['apartment'];
    include('about.php');
} 
else if($uri[0] == 'something_else') {
    // something else.
}
else {
    // 404
}
</code></pre>

<p>Such a logic would serve perfectly well as a controller, and it isn't such a big work. </p>

<p>Alternarively, you could put a URI-parser snippet at the top of every entry point. Like, at the top of about.php:</p>

<pre><code>$uri = explode('/', $_SERVER['REQUEST_URI']);
$id_aray = lookup_building_and_apartment_by_name( $uri[1], $uri[2] );
$_GET['building_id'] = $id_array['building'];
$_GET['apartment_id'] = $id_array['apartment'];
</code></pre>

<p>This would enable you to work incrementally, one subpage at a time, and the old links would continue to work as well.</p>

<hr>

<p>Mostly for the record: there's an option 3, you can use <a href="http://www.regular-expressions.info/brackets.html" rel="nofollow">capture groups</a> in mod_rewrite rules, like so:</p>

<pre><code>RewriteRule ^/about/([^/]+)/([^/]+)$ about.php?building_name=$1&amp;apt_name=$2 [NC,L]
RewriteRule ^/about/([^/]+)$ about.php?building_name=$1 [NC,L]
</code></pre>

<p>(This can be done with a single rule, but it's considerably easier to read &amp; write like this.) This still requires you to have a php-based translation in about.php, but has the advantage that you can put these rules in your httpd.conf.</p>

<p>There's also an option 4: <a href="http://httpd.apache.org/docs/current/rewrite/rewritemap.html" rel="nofollow">RewriteMap</a>. It's an awesome and powerful tool, and it may be just the thing for you, if you're able to cope with the terseness of the Apache manual. Learning to use it would probably take a lot more time than using the PHP-based solution, but it's a good thing to know, it's an efficient solution, and it's very elegant. </p>

<p>You could easily generate a <a href="http://httpd.apache.org/docs/current/rewrite/rewritemap.html#txt" rel="nofollow">text-based mapping</a>, then use the mapping in the RewriteRule, like so:</p>

<pre><code>RewriteMap building_map txt:/etc/apache2/buildings.txt
RewriteRule ^/about/([^/]+)$ about.php?building-id=${building_map:$1|0} [NC,L]
</code></pre>

