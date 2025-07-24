# Creating dynamic URLs in htaccess
[Link to question](https://stackoverflow.com/questions/5845609/creating-dynamic-urls-in-htaccess)
**Creation Date:** 1304211090
**Score:** 4
**Tags:** php, .htaccess
## Question Body
<p>I'm trying to write an .htaccess file that will make my URLs more attractive to search engines. I know basically how to do this, but I'm wondering how I could do this dynamically.</p>

<p>My URL generally looks like:</p>

<pre><code>view.php?mode=prod&amp;id=1234
</code></pre>

<p>What I'd like to do is take the id from the url, do a database query, then put the title returned from the DB into the url. something like:</p>

<pre><code>/products/This-is-the-product-title
</code></pre>

<p>I know that some people have accomplished this with phpbb forum URLs and topics, and i've tried to track the code down to where it replaces the actual URL with the new title string URL, but no luck.</p>

<p>I know I can rewrite the URL with just the id like:</p>

<pre><code>RewriteRule ^view\.php?mode=prod&amp;id=([0-9]+) /products/$1/
</code></pre>

<p>Is there a way in PHP to overwrite the URL displayed?</p>

## Answers
### Answer ID: 5847426
<p>One way to do it, would be just like most mvc frameworks. You can redirect all your pages to the same index.php file, and you use your script to determine which page to load. </p>

<p>.htaccess</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . index.php [L]
&lt;/IfModule&gt;
</code></pre>

<p>and your php file will have a script like this one:</p>

<pre><code>  // get the url
  $uri = (isset($_SERVER['REQUEST_URI']))?$_SERVER['REQUEST_URI']: false;
  $query = (isset($_SERVER['QUERY_STRING']))?$_SERVER['QUERY_STRING']: '';
  $url = str_replace($query,'',$uri); // you can edit this part to do something with the query
  $arr = explode('/',$url);
  array_shift($arr);

  // get the correct page to display
  $controller =!empty($arr[0])?$arr[0]:'home'; // $arr[0] could be product/ 
  $action = isset($arr[1]) &amp;&amp; !empty($arr[1])?$arr[1]:'index'; // $arr[1] can be product-title
    }
</code></pre>

<p>of course you will have to work this code to fashion your application</p>

<p>I hope this helps</p>

### Answer ID: 5845662
<p>At the moment you're wondering how to convert your ugly URL (e.g. <code>/view.php?mode=prod&amp;id=1234</code>) into a pretty URL (e.g. <code>/products/product-title</code>). Start looking at this the other way around.</p>

<p>What you want is someone typing <code>/products/product-title</code> to actually take them to the page that can be accessed by <code>/view.php?mode=prod&amp;id=1234</code>.</p>

<p>i.e. your rule could be as follows:</p>

<pre><code>RewriteRule ^products/([A-Za-z0-9-])/?$ /view.php?mode=prod&amp;title=$1
</code></pre>

<p>Then in view.php do a lookup based on the <code>title</code> to find the <code>id</code>. Then carry on as normal. </p>

### Answer ID: 5845621
<p>One way would be to output a Location: header to force a redirect to the chosen URL.</p>

