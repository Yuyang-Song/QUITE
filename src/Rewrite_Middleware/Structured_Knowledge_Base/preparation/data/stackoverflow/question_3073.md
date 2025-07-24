# Wordpress multi-language no plugin
[Link to question](https://stackoverflow.com/questions/65263014/wordpress-multi-language-no-plugin)
**Creation Date:** 1607761960
**Score:** 1
**Tags:** php, wordpress, url-rewriting
## Question Body
<p>I am working on a wordpress site and I need to implement multiple-languages function (i don't want to use any plugin, just pure programming). I created 2 folders (en/de) and put index.php in each one of them. The problem I am confrunting now is that I want to shows pages in specific language. Example:
For en:</p>
<pre><code>www.domain.com/en/example
</code></pre>
<p>For de:</p>
<pre><code>www.domain.com/de/beispiel
</code></pre>
<p>Where Beispiel = example . I did the rewrite rules needed for this using <code>add_rewrite_rule()</code> function, but how can I get the page from the database only if the language coresponds to a column where the language is set for every post?
PS: I added one more column for pages table,in order to tell for what language are written.
My intention is to write a custom query inside index.php , which will get specified page from the table by <code>pagename</code> and <code>current language</code>. How can I do this?</p>
<p>UPDATE 1:
I found a solution , but I do not know if it is recommended. In my theme's index.php I chnaged</p>
<pre><code>global $post;
    $i = 0;
    while ( have_posts() &amp;&amp; $post-&gt;language == 'en') {
        
        $i++;
        if ( $i &gt; 1 ) {
                echo '&lt;hr class=&quot;post-separator styled-separator is-style-wide section-inner&quot; aria-hidden=&quot;true&quot; /&gt;';
        }
         the_post();
        
        get_template_part( 'template-parts/content', get_post_type() );

    }
</code></pre>
<p>Where <code>$post-&gt;language</code> is the field from mysql table where the language is stored.</p>

