# Is there a problem with ADO.NET DataSets in a load balanced environment?
[Link to question](https://stackoverflow.com/questions/1058618/is-there-a-problem-with-ado-net-datasets-in-a-load-balanced-environment)
**Creation Date:** 1246285526
**Score:** 1
**Tags:** asp.net, ado.net, asp.net-3.5, load-balancing
## Question Body
<p>For the last few months we've had a wierd problem with our website.  Once in a while various queries to the database, using ADO.NET DataSets, will throw an error... the most common of which is "Failed to enable constraints.  One or more rows contain values violating non-null, unique, or foreign-key constraints."</p>

<p>The data is actually valid though, as without changing anything the error will be intermittent.  Further, the "fix" for it is to recycle the app pool on both web servers... so the problem can't be bad data being returned.  Once this is done it can run fine for weeks at a time, or break 3 times in one day.  There's no consistency to it...</p>

<p>It also <em>seems</em> like newer means of data access, such as Linq 2 SQL, work just fine... though it's hard to tell since the site is using both at the moment.  (Working on getting everything over to L2S, but don't have a lot of time to rewrite old components unfortunately...)</p>

<p>So has anyone had anything like this before?  Is it something with the load balancing?  Maybe something wrong with the servers?  (I've forced all connections to each server in turn and experienced the error on both of them.)  Could it be something wrong with running in a VM?</p>

<p>Err... ok, so the overall question is: What's causing this and how do I fix it?</p>

<p>Oh, and the website is in .NET 3.5...</p>

## Answers
### Answer ID: 1058711
<p>Based off of what you've said, I would guess that this is related to the load experienced on the servers at the time of the error.</p>

<p>If you can, set up a staging environment that is load balanced like your production servers are.  Then start load testing the app.  </p>

<p>Also, make sure you have all the latest service packs / updates applied on your production servers.  MS has a tendency to not tell us everything they are fixing.  Finally, look on MS connect to see if a hotfix corrects the problem you are talking about.</p>

<p><strong>UPDATE:</strong></p>

<p>Load testing can be as simple or complicated as you can afford.  What it should do is run through a sequence of pages that perform standard operations on your site in a repeatable way.  You usually want to simulate "think" times between each page load / operation that are in line with expected user behavior.</p>

<p>Then, you execute the test as a certain number of simulataneous users.  While the test is executing, you need to record any errors and the servers performance counters to get an idea of how the app really performs.</p>

<p><a href="http://www.opensourcetesting.org/performance.php" rel="nofollow noreferrer">Some links to load testing tools are here</a>.  <a href="http://adamesterline.com/2007/04/23/watin-watir-and-selenium-reviewed/" rel="nofollow noreferrer">Another list is here</a>.</p>

<p>As a side note, I've seen apps start exhibiting strange behavior under a load of only 5 simultaneous users.  It really depends on how the site is built.  </p>

