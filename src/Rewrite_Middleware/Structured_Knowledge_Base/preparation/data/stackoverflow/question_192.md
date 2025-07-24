# Can I compile my PHP script to a faster executing format?
[Link to question](https://stackoverflow.com/questions/1647826/can-i-compile-my-php-script-to-a-faster-executing-format)
**Creation Date:** 1256872721
**Score:** 4
**Tags:** php, optimization, compilation, fastcgi
## Question Body
<p>I have a PHP script that acts as a JSON API to my backend database.</p>

<p>Meaning, you send it an HTTP request like: <a href="http://example.com/json/?a=1&amp;b=2&amp;c=3" rel="nofollow noreferrer">http://example.com/json/?a=1&amp;b=2&amp;c=3</a>...  it will return a json object with the result set from my database.</p>

<p>PHP works great for this because it's literally about 10 lines of code. </p>

<p>But I also know that PHP is slow and this is an API that's being called about 40x per second at times and PHP is struggling to keep up.</p>

<p>Is there a way that I can compile my PHP script to a faster executing format?  I'm already using PHP-APC which is a bytecode optimization for PHP as well as FastCGI.</p>

<p>Or, does anyone recommend a language I rewrite the script in so that Apache can still process the example.com/json/ requests?</p>

<p>Thanks</p>

<p><strong>UPDATE</strong>: I just ran some benchmarks:</p>

<ul>
<li>PHP script takes 0.6 second to
complete</li>
<li>If I use the generated SQL from the PHP script above and run the query from the same web server but directly from within the MySQL command, meaning, network latency is still in play - the fetched result set takes only 0.09 seconds to complete.</li>
</ul>

<p>As you notice, PHP is literally 1 order of magnitude slower in generating the results. Network does not appear to be the major bottleneck in this case, though I agree it typically is the root cause.</p>

## Answers
### Answer ID: 2473705
<p>From your benchmark it looks like the php code is indeed the problem. Can you post the code?</p>

<p>What happens when you remove the MySQL code and just put in a hard-coded string representing what you'll get back from the db?</p>

<p>Since it takes .60 seconds from php and only .09 seconds from a MySQL CLI I will guess that the connection creation is taking too much time. PHP creates a new connection per request by default and that can be slow sometimes.</p>

<p>Think about it, depending on your env and your code you will:</p>

<ol>
<li>Resolve the hostname of the MySQL server to an IP</li>
<li>Open a connection to the server</li>
<li>Authenticate to the server</li>
<li>Finally run your query</li>
</ol>

<p>Have you considered using <a href="http://php.net/manual/en/features.persistent-connections.php" rel="nofollow noreferrer">persistent MySQL connections</a> or <a href="http://sqlrelay.sourceforge.net/" rel="nofollow noreferrer">connection pooling</a>?
It effectively allows you to jump right to query step from above.</p>

<p>Caching is great for performance as well. I think others have covered this pretty well already.</p>

### Answer ID: 1650201
<p>Since you already have APC installed, it can be used (similar to the memcached recommendations) to store objects.  If you can cache your database results, do it!
<a href="https://www.php.net/manual/en/function.apc-store.php" rel="nofollow noreferrer">https://www.php.net/manual/en/function.apc-store.php</a>
<a href="https://www.php.net/manual/en/function.apc-fetch.php" rel="nofollow noreferrer">https://www.php.net/manual/en/function.apc-fetch.php</a></p>

### Answer ID: 1650166
<p>Please see <a href="https://stackoverflow.com/questions/621502/php-compilers-do-you-know-of-any">this question</a>. You have several options. Yes, PHP can be compiled to native ELF (and possibly even FatELF) format. The problem is all of the Zend creature comforts. </p>

### Answer ID: 1650150
<p>I've had a lot of luck with using PHP, memcached and nginx's memcache module together for very fast results. The easiest way is to just use the full URL as the cache key </p>

<p>I'll assume this URL:</p>

<pre><code>/widgets.json?a=1&amp;b=2&amp;c=3
</code></pre>

<p>Example PHP code:</p>

<pre><code>&lt;?
$widgets_cache_key = $_SERVER['REQUEST_URI'];

// connect to memcache (requires memcache pecl module)
$m = new Memcache;
$m-&gt;connect('127.0.0.1', 11211);

// try to get data from cache
$data = $m-&gt;get($widgets_cache_key);
if(empty($data)){
    // data is not in cache. grab it.
    $r = mysql_query("SELECT * FROM widgets WHERE ...;");
    while($row = mysql_fetch_assoc($r)){
        $data[] = $row;
    }
    // now store data for next time.
    $m-&gt;set($widgets_cache_key, $data);
}

var_dump(json_encode($data));
?&gt;
</code></pre>

<p>That in itself provides a huge performance boost. If you were to then use nginx as a front-end for Apache (put Apache on 8080 and nginx on 80), you could do this in your nginx config:</p>

<pre><code>worker_processes  2;

events {
    worker_connections  1024;
}

http {
    include  mime.types;
    default_type  application/octet-stream;

    access_log  off;
    sendfile  on;
    keepalive_timeout  5;
    tcp_nodelay  on;
    gzip  on;

    upstream apache {
        server  127.0.0.1:8080;
    }

    server {
        listen  80;
        server_name  _;

        location / {
            if ($request_method = POST) {
                proxy_pass  http://apache;
                break;
            }
            set  $memcached_key $uri;
            memcached_pass  127.0.0.1:11211;
            default_type  text/html;
            proxy_intercept_errors  on;
            error_page  404 502 = /fallback;
        }

        location /fallback {
            internal;
            proxy_pass  http://apache;
            break;
        }
    }
}
</code></pre>

<p>Notice the <code>set  $memcached_key $uri;</code> line. This sets the <code>memcached</code> cache key to use <code>REQUEST_URI</code> just like the PHP script. So if nginx discovers a cache entry with that key it will serve it directly from memory, and you never have to touch PHP or Apache. Very fast.</p>

<p>There is an unofficial <a href="http://code.google.com/p/modmemcachecache/" rel="nofollow noreferrer">Apache memcache module</a> as well. Haven't tried it but if you don't want to mess with nginx this may help you as well.</p>

### Answer ID: 1650045
<p>If your database is very read-heavy (I'm guessing it is) then a basic caching implementation would help, and <code>memcached</code> would make it very fast.</p>

<p>Let me change your URL structure for this example:</p>

<pre><code>/widgets.json?a=1&amp;b=2&amp;c=3
</code></pre>

<p>For each call to your web service, you'd be able to parse the GET arguments and use those to create a key to use in your cache. Let's assume you're querying for <code>widgets</code>. Example code:</p>

<pre><code>&lt;?
// a function to provide a consistent cache key for your resource
function cache_key($type, $params = array()){
 if(empty($type)){
  return false;
 }
 // order your parameters alphabetically by key.
 ksort($params);
 return sha1($type . serialize($params));
}

// you get the same cache key no matter the order of parameters
var_dump(cache_key('widgets', array('a' =&gt; 3, 'b' =&gt; 7, 'c' =&gt; 5)));
var_dump(cache_key('widgets', array('b' =&gt; 7, 'a' =&gt; 3, 'c' =&gt; 5)));


// now let's use some GET parameters.
// you'd probably want to sanitize your $_GET array, however you want.
$_GET = sanitize($_GET);

// assuming URL of /widgets.json?a=1&amp;b=2&amp;c=3 results in the following func call:
$widgets_cache_key = cache_key('widgets', $_GET);

// connect to memcache (requires memcache pecl module)
$m = new Memcache;
$m-&gt;connect('127.0.0.1', 11211);

// try to get data from cache
$data = $m-&gt;get($widgets_cache_key);
if(empty($data)){
 // data is not in cache. grab it.
 $r = mysql_query("SELECT * FROM widgets WHERE ...;");
 while($row = mysql_fetch_assoc($r)){
  $data[] = $row;
 }
 // now store data for next time.
 $m-&gt;set($widgets_cache_key, $data);
}

var_dump(json_encode($data));
?&gt;
</code></pre>

### Answer ID: 1648150
<p>Consider that if you're handling database updates, your MySQL performance is what, IMO, needs attention. I would expand the test harness like so:</p>

<ul>
<li>run mytop on the dbserver</li>
<li>run ab (apache bench) from a client, like your desktop</li>
<li>run top or vmstat on the webserver</li>
</ul>

<p>And watch for these things:</p>

<ul>
<li>updates to the table forcing reads to wait (MyISAM engine)</li>
<li>high load on the webserver (could indicate low memory conditions on webserver)</li>
<li>high disk activity on webserver, possibly from logging or other web requests causing random seeking of uncached files</li>
<li>memory growth of your apache processes. If your result sets are getting transformed into large associative arrays, or getting serialized/deserialized, these can become expensive memory allocation operations. Your code might need to avoid calls like mysql_fetch_assoc() and start fetching one row at a time.</li>
</ul>

<p>I often wrap my db queries with a little profiler adapter that I can toggle to log unusually query times, like so:</p>

<pre><code>function query( $sql, $dbcon, $thresh ) {
    $delta['begin'] = microtime( true );
    $result = $dbcon-&gt;query( $sql );
    $delta['finish'] = microtime( true );
    $delta['t'] = $delta['finish'] - $delta['begin'];
    if( $delta['t'] &gt; $thresh )
        error_log( "query took {$delta['t']} seconds; query: $sql" );
    return $result;
}
</code></pre>

<p>Personally, I prefer using xcache to APC, because I like the diagnostics page it comes with.</p>

<p>Chart your performance over time. Track the number of concurrent connections and see if that correlates to performance issues. You can grep the number of http connections from netstat from a cronjob and log that for analysis later. </p>

<p>Consider enabling your mysql query cache, too.</p>

### Answer ID: 1647867
<p>The first rule of optimization is to make sure you actually have a performance problem. The second rule is to figure out where the performance problem is by <em>measuring</em> your code. Don't guess. Get hard measurements.</p>

<p>PHP is not going to be your bottleneck. I can pretty much guarantee that. Network bandwidth and latency will dwarf the small overhead of using PHP vs. a compiled C program. And if not network speed, then it will be disk I/O, or database access, or a really bad algorithm, or a host of other more likely culprits than the language itself.</p>

### Answer ID: 1647836
<p>You're already using APC opcode caching which is good. If you find you're still not getting the performance you need, here are some other things you could try:</p>

<p>1) Put a <a href="http://www.squid-cache.org/" rel="nofollow noreferrer">Squid caching proxy</a> in front of your web server. If your requests are highly cacheable, this might make good sense.</p>

<p>2) Use <a href="http://www.danga.com/memcached/" rel="nofollow noreferrer">memcached</a> to cache expensive database lookups.</p>

### Answer ID: 1647835
<p>Before you go optimizing something, first figure out if it's a problem. Considering it's only 10 lines of code (according to you) I very much suspect you don't have a problem. Time how long the script takes to execute. Bear in mind that network latency will typically dwarf trivial script execution times.</p>

<p>In other words: don't solve a problem until you <em>have</em> a problem.</p>

<p>You're already using an opcode cache (APC). It doesn't get much faster than that. More to the point, it rarely <strong>needs</strong> to get any faster than that.</p>

<p>If anything you'll have problems with your database. Too many connections (unlikely at 20x per second), too slow to connect or the big one: query is too slow. If you find yourself in this situation 9 times out of 10 effective indexing and database tuning is sufficient.</p>

<p>In the cases where it isn't is where you go for some kind of caching: memcached, beanstalkd and the like.</p>

<p>But honestly 20x per second means that these solutions are almost certainly overengineering for something that isn't a problem.</p>

