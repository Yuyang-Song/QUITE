# CakePHP 2.0 Routing and Pagination Issue
[Link to question](https://stackoverflow.com/questions/11207622/cakephp-2-0-routing-and-pagination-issue)
**Creation Date:** 1340714722
**Score:** 2
**Tags:** cakephp, routes
## Question Body
<p>In my routes configuratoin, I only use custom routes. Now I have a problem with pagination, before it worked well.</p>

<p>Routes:</p>

<pre><code>// view all posts by year and month
Router::connect('/blog/:year/:month/*', array(
 'controller' =&gt; 'posts',
 'action' =&gt; 'index',
 'month' =&gt; null
), array(
  'pass' =&gt; array(
    'year',
    'month'
  ),
  'year' =&gt; '[12][0-9]{3}',
  'month' =&gt; '0[1-9]|1[012]'
));
</code></pre>

<p>This should do the following: /blog/2012/ should list all posts from 2012, while month is not relevant. /blog/2012/05/ should list all posts from May 2012, month being relevant. I added the /* at the end to use /blog/2012/05/page:2, which works fine now. HOWEVER, /blog/2012/page:2 does not work, page:2 is assumed to be a month, and because of the non-matching regex, transforms to '', so the database query looks for a month ''. </p>

<p>I probably somehow did not fully grasp routing, and how to declare variables that can be passed and can't be passed, but how could I rewrite this configuration to make it work, without changing it fundamentally? I really think it's a configuration issue.
Thanks.</p>

## Answers
### Answer ID: 11220903
<p>In order to solve this in a pragmatic and maybe not that elegant way, I came up with the following. First I connected the page named parameter:</p>

<pre><code>Router::connectNamed(array('page' =&gt; '[\d]+'), array(
 'default' =&gt; false,
 'greedy' =&gt; false
));
</code></pre>

<p><a href="http://book.cakephp.org/2.0/en/development/routing.html#controlling-named-parameters" rel="nofollow">according to the cookbook</a>, this will only enable the page named parameter and disable all others, and it will only accept numerical values.</p>

<p>I am not sure whether this was particularly connected to my specific issue though.</p>

<p>Secondly, I reread the cookbook and saw <a href="http://book.cakephp.org/2.0/en/development/routing.html#routes-configuration" rel="nofollow">here</a> that the order of connections in routes.php really matters. I.e., when an url has to be routed, connections at the top of the file have higher priority over connections at the bottom. Thus, I came up with this configuration order:</p>

<pre><code> // view all posts by year and month
 Router::connect('/blog/:year/:month/*', array(
    'controller' =&gt; 'posts',
    'action' =&gt; 'index'
  ), array(
    'year' =&gt; '[12][0-9]{3}',
    'month' =&gt; '0[1-9]|1[012]'
  ));

  // view all posts by year
 Router::connect('/blog/:year/*', array(
    'controller' =&gt; 'posts',
    'action' =&gt; 'index'
 ), array('year' =&gt; '[12][0-9]{3}'));

  // view all posts
  Router::connect('/blog/*', array(
     'controller' =&gt; 'posts',
     'action' =&gt; 'index'
  ));
</code></pre>

<p>Before, it was reversed, i.e. /blog/* was connected first. Because of the greedy star, this "swallowed" everything, also stuff like /blog/2012/, where 2012 was just passed as an argument. Whereas now, I can come up with /blog/2012/page:2, /blog/2012/05/page:2, and "fake" urls like /blog/2012/5ssfd/page:2 will map to /blog/2012/page:2, i.e. in this case, the first connection wasn't matched, so it jumps to the second connection. The reason I did it this way is that I wasn't able to do stuff like /blog/:year/:month/page:page and thus avoid the greedy star (maybe somebody knows how to do this).</p>

### Answer ID: 11211063
<p>If you disabled all the default Cake routes, it will stop the pagination working, you can get the routes used for pagination only by adding:</p>

<p><code>Router::connectNamed(false, array('default' =&gt; true));</code></p>

<p><a href="http://book.cakephp.org/2.0/en/development/routing.html#controlling-named-parameters" rel="nofollow">http://book.cakephp.org/2.0/en/development/routing.html#controlling-named-parameters</a></p>

