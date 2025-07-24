# Creating SEO and human freindly/readable URLs using PHP and IIS7
[Link to question](https://stackoverflow.com/questions/6878144/creating-seo-and-human-freindly-readable-urls-using-php-and-iis7)
**Creation Date:** 1311968147
**Score:** 1
**Tags:** php, iis, iis-7
## Question Body
<p>I am running PHP5.3.6 and IIS7. I am currently working on a product centric site where I have one php page that dynamically generates a page based on a query string such as <code>/product.php?id=12345</code>.</p>

<p>The volume of products that I have in the database varies, but measures in the hundreds. They have unique IDs and names.</p>

<p>I want for each page to be addresses by their name instead of by the query string.</p>

<p>For example, instead of:</p>

<pre><code>/product.php?id=12345
</code></pre>

<p>I would prefer:</p>

<pre><code>/acme-super-widget-in-blue-with-cool-groovy-gadget-attachment
</code></pre>

<p>I have the <code>URL Rewrite</code> component in IIS7, but I don't want to enter values manually. I would rather have a dynamic process in place. I believe the needed functionailty here is to add an URL Rewrite rule to the <code>web.config</code> file, but I'm not sure if that is true or the best approach.</p>

<p>Thank you.</p>

## Answers
### Answer ID: 6881220
<p>I would recommend using the ID along with the name so that you can support products with the same name (future proofing), or products with non-ascii characters... should you have international names. I would also recommend using only ascii characters in the URL's for now as I've noticed some sites and browser tend to expand non-ascii characters in to ugly percent encoding. </p>

<p>IIS 7 is a bit trickier than Apache, but I think this might work for you <a href="http://blogs.iis.net/bills/archive/2008/05/31/urlrewrite-module-for-iis7.aspx" rel="nofollow">http://blogs.iis.net/bills/archive/2008/05/31/urlrewrite-module-for-iis7.aspx</a></p>

<p>Here is an example rewrite rule which will strip the name off the id and pass just the id to the script.</p>

<p><strong>IIS 7 Using the module in the link above</strong></p>

<p>Match URL</p>

<pre><code>^([0-9]+)[^/]*/?$
</code></pre>

<p>Action</p>

<pre><code>index.php?id={R:1} [QSA,L]
</code></pre>

<p><strong>Apache just for good messure ;)</strong></p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^([0-9]+)[^/]*/?$ index.php?id=$1 [QSA,L]
</code></pre>

<p>Here is a PHP function that will generate the id name portion of your friendly URLs.</p>

<pre><code>function friendlyURL($id, $title) {

    $string = $title;
    $paramcount = func_num_args();
    for ($i = 2; $i &lt; $paramcount; $i++) {
        $string .= "-" . func_get_arg($i);
    }
    $string = preg_replace('`&amp;(amp;)?#?[a-z0-9]+;`i', '-', $string);
    $string = htmlentities($string, ENT_COMPAT, "utf-8");
    $string = preg_replace("`&amp;([a-z]+);`i", "", $string);
    $string = preg_replace("`['\[\]]`", "", $string);

    $tmp = $string;
    $string = preg_replace(array("/[^A-Za-z0-9]/", "`[-]+`"), "-", $string);

    $string = trim($string, '-');
    return trim($id . "-" . $string, '-');
}
</code></pre>

<p>This would give you URL's like</p>

<p>Product ID = 12345, Name = "acme super widget"</p>

<pre><code>/12345-acme-super-widget/
</code></pre>

<p>Product ID = 12345, Name = "Japanese product ギター"</p>

<pre><code>/12345-japanese-product/
</code></pre>

### Answer ID: 6879456
<p>It looks like this: <a href="http://www.iis.net/download/URLRewrite" rel="nofollow">http://www.iis.net/download/URLRewrite</a> is exactly what you need.</p>

