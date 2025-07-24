# Custom lithium routing scenario
[Link to question](https://stackoverflow.com/questions/8717119/custom-lithium-routing-scenario)
**Creation Date:** 1325616450
**Score:** 3
**Tags:** php, url-routing, lithium
## Question Body
<p>I've been tasked with rewriting an existing website with large pre-existing link catalog. For argument's sake, let's assume we can't do anything that would change the link catalog. Here's a few examples of the link structure we're working with:</p>

<ol>
<li><p><strong>An item page would be:</strong></p>

<pre><code>www.domain.com/widgets/some-totally-awesome-large-purple-widget
</code></pre></li>
<li><p><strong>A category sub page page would be:</strong></p>

<pre><code>www.domain.com/widgets/purple-widgets
</code></pre></li>
<li><p><strong>A category parent page page would be:</strong></p>

<pre><code>www.domain.com/widgets/
</code></pre></li>
<li><p><strong>A custom page may be:</strong></p>

<pre><code>www.domain.com/some-random-page
</code></pre></li>
</ol>

<p>The various page types are too numerous to write individual Routers for.</p>

<p>Using Router::connect I can easily account for the first and second scenarios using something like:</p>

<pre><code>Router::connect('/{:pageroot}/{:pagekey}', 'Pages::index');
</code></pre>

<p>In turn, the Pages::index method looks for entries in our database with the "key" of '/widgets/purple-widgets'.</p>

<p>However, the framework defaults to the '/{:controller}/{:action}/{:args}' route for pages like the third and fourth. I know that this is the correct behavior for the framework. Also, best practice would state that I should write the site to match this behavior. But, that isn't an option here.</p>

<p>What I need is a Router that would allow the third and fourth examples to function the same as the first. All examples should be sent to the Pages::index controller, which in turn queries a database using the URL path as a key.</p>

## Answers
### Answer ID: 8724622
<p>If you don't have any convention in the URL for what is what, between page, item and category. I'd go with a very generic router.</p>

<pre><code>Router::connect('/{:category}/{:page}/{:item}', 'Pages::any');
Router::connect('/{:category}/{:page}', array('Pages::any', 'item' =&gt; null));
Router::connect('/{:category}', array('Pages::any', 'page' =&gt; null, 'item' =&gt; null));
</code></pre>

<p>And in <code>Pages::any()</code> to search for the correct stuff. Is that <code>category</code> a <code>page</code> after all (example 4)? Is that <code>page</code> an <code>item</code> (example 1)?</p>

<p><strong>or</strong></p>

<p>You store the URL somewhere (e.g. a mapping table in the database) and use the <code>pattern</code> version of a <a href="http://lithify.me/docs/lithium/net/http/Route" rel="nofollow">lithium Route</a>.</p>

<pre><code>Router::connect(new Route(array(
    'pattern' =&gt; '@^/(?&lt;path&gt;.+)$@',
    'params' =&gt; array('controller' =&gt; 'pages', 'action' =&gt; 'any'),
    'keys' =&gt; array('path' =&gt; 'path'),
    // extra stuff, if the path is `tata`, it skips this route and uses
    // any of the following ones that matches.
    'handler' =&gt; function($request) {
        if ($request-&gt;params['path'] == 'tata') {
            return false;
        } else {
            return $request;
        }
    }
)));
</code></pre>

<p>From that point, you'll get the full URL.</p>

### Answer ID: 8724994
<p>You probably should write a smart Router Helper which is maybe able to process your request based on your db defined routes.</p>

<p>Take a look into: <a href="https://github.com/UnionOfRAD/lithium/blob/master/net/http/Router.php" rel="nofollow">net/http/Router.php</a></p>

<p>especially connect(), parse() and match()</p>

<p>I would start to write some kind of anonymous function and progress it to a testable Class which is located in /extension.. ?</p>

