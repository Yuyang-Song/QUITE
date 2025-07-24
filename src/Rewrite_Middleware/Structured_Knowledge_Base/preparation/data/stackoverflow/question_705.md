# Architecture of a write-intensive feature
[Link to question](https://stackoverflow.com/questions/38012666/architecture-of-a-write-intensive-feature)
**Creation Date:** 1466768688
**Score:** 8
**Tags:** ruby, oracle-database, ruby-on-rails-3, caching, memcached
## Question Body
<p>I use Ruby on Rails backed by Oracle database and memcached for my current project.</p>

<p>There is a pretty heavily used feature, which relies on a single database views as a datasource, and this data source internally has other database views and tables inside. </p>

<p>It's a virtual db view, to be able to access everything from one place, not a materialized db view.</p>

<p>Users most of the times if they are in the feature they are looking to update, so having data up to date is important.</p>

<p>When obtaining data from this view, I inner join security table to the view (security table is not part of the view itself) which contains some fields that we use to control data access on more granular level. For example security table has <code>user_id, prop_1, prop_2</code> columns, where <code>prop_1, prop_2</code> are columns available on a db view and the <code>user_id</code> is a logged in user. Some users have same props in the security table say <code>prop_1 = 1 and prop_2 = 1</code>, but also can have <code>prop_1</code> like the other user but have different <code>prop_2</code> like <code>prop_1 = 2 and prop_2 = 1</code>. There are many different combination of prop_1 and prop_2, think about them as a FK to another table, so possible to have many entries.</p>

<p>By now the time to retrieve the records on the app is almost 10 seconds, it's pretty slow. I'm considering alternative approach.</p>

<p>First thing I though of was the materialized view, but since the user do frequent updates, it might not be the best choice, as refreshing the view might take time.</p>

<p>Second thing I thought about was the cache, to use <code>prop_1</code> and <code>prop_2</code> combination as a composite key to the underlying data, as many users have the same combination and whoever has the same combination can access the same data.</p>

<p>However this approach might require more code rewrites and logic to save and retrieve data in fragments, rather from one location with one query like in the database view.</p>

<p><strong>In your experience, how did you address same/similar issue? Or is there a better approach that I could try?</strong> </p>

## Answers
### Answer ID: 38202646
<p>If you are enduring some latencies probably cause to your db, you may migrate some of your views to a <a href="http://redis.io/" rel="nofollow">REDIS database</a> (in-memory data structure store) which is probably one of the most efficient in "read/write" intensive.</p>

<p>Concerning the update problematic, you may implement a <a href="https://en.wikipedia.org/wiki/WebSocket" rel="nofollow">websocket</a> to diffuse/push precise update directly to those who need it.</p>

<p>I underline that this possibility required some modifications on both client &amp; server sides, but I assume that it is the best approach to keep final user view updated with low latency.</p>

<p>Best regards</p>

### Answer ID: 38197338
<blockquote>
  <p>"relies on a single database views as a datasource, and this data source internally has other database views and tables inside."</p>
</blockquote>

<p>If this were an object we would call it <a href="https://en.wikipedia.org/wiki/God_object" rel="nofollow">a God Object</a>, which is a bad thing. It's just as much of an anti-pattern in the database realm. Without knowing the details it's hard to be sure but probably you have a mess of inner joins, outer joins and cross joins, leading to de-normalization, data duplication and (perhaps) integrity issues. </p>

<p>Certainly you have performance problems, which is inevitable because such a thing is un-tunable. Whether you want want one row or ten thousand rows it's the same query. You're not giving the optimizer the chance to make sensible decisions. </p>

<p>So the first thing you need to do is break up this view into meaningful data objects (views or tables) which map to focused business domains. You're already using Rails, it shouldn't be that hard to manage a better Data Access Layer. </p>

<p>As for security, Oracle does have a built-in Virtual Private Database implementation. If you have Enterprise Edition you should definitely use DBMS_RLS to control row level (and column level) access. The main advantage of RLS is that it's invisible: set a policy on a table or view, and it is automatically applied to all SQL executed on the object.</p>

<p>If you're on Standard Edition then you're stuck with using explicit joins to your security table (but see below).</p>

<p>As for the use of <code>memcached</code>, in my experience application developers tend to build external caches because they don't understand how Oracle databases work and so implement poor data access strategies - such as routing everything through a single monstrous view... </p>

<p>Breaking your DAL into discrete meaningful objects will give you better performance because the database optimizer will be able to select the most efficient path for extracting the precise set of information needed. Also the retrieval paths will be better because the hot (most frequently queried) blocks will be help in the database buffer cache, whereas at the moment I suspect that's being utterly trashed by a surfeit of full table scans. You can leverage Server Result caching, which could help with "users have the same combination and [who] can access the same data"  <a href="http://docs.oracle.com/cd/E11882_01/server.112/e41573/memory.htm#PFGRF987" rel="nofollow">Find out more</a>.</p>

<p>So you may find you don't need an external cache at all. Certainly by letting the database manage its data properly - using technology appropriately - you should find you need a lot less data held externally. You describe your application as "write intensive" so you must be spending a lot of cycles keeping the cache and the database in synch. Obviously if you're dealing with Facebook quantities of data you need to use Facebook style approaches to data management. But generally, <a href="http://c2.com/cgi/wiki?DoTheSimplestThingThatCouldPossiblyWork" rel="nofollow">Do The Simplest Thing That Could Possibly Work</a> remains the best starting point.   </p>

### Answer ID: 38148471
<p>It is hard to give a good answer without more information about your view, but I'll give it a try.</p>

<p>First of all I question the use of a single very complex view. That is hard to tune and can often cause performance problems, so if it is possible to split it up in the application that would be my first bet.</p>

<p>Second, have you looked at the execution plan (explain plan) for the query with the security filters included? Is it using sensible indexes? If not, create them. Perhaps the security properties are not indexed, for example?</p>

<p>A third option may be to use PL/SQL and call a stored procedure that acts like the view. That gives you more control in the database, making it possible to control the query and split it into multiple steps, but to get the same result as Today.</p>

<p>Finally you may be able to rewrite the view for better performance. One often overlooked feature is the WITH clause, which makes it possible to run a query before the main query and use the result as a table. It has helped me improve performance for complex views dramatically.</p>

<p>DBMS_RLS is cool but can be expensive, it requires the Enterprise Edition and it wouldn't surprise me if you need a separate license too. I would go for a programmatic solution first.</p>

### Answer ID: 38086523
<p>Many times joining to a complex view presents performance problems.</p>

<p>Are <code>prop_1</code> and <code>prop_2</code> values that you want to limit to?  That is, are you joining your view to the security table on those columns, like</p>

<pre><code>WHERE  my_view.prop_1 = security_table.prop_1
AND    my_view.prop_2 = security_table.prop_2
AND    security_table.user_id = :current_user_id
</code></pre>

<p>?</p>

<p>Next question: do <code>prop_1</code> and <code>prop_2</code> map to columns in the underlying tables of the view?  If so, can they be used to access rows from the underlying tables <em>quickly</em> (outside of your view)?</p>

<p>If so, I would try to use <code>DBMS_RLS.ADD_POLICY</code> add security policies on the underlying tables to enforce your security (i.e., limit values of <code>prop_1</code> and <code>prop_2</code> based on current user) and not join the security table to the view at all.</p>

<p>If you add security policies to the underlying tables, Oracle will add those predicates when accessing the tables, <em>before</em> the complexity of your query starts.  That might give Oracle's optimizer the extra help it needs to make the process faster.</p>

<p>Without seeing your code, it's hard to say more.</p>

