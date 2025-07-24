# How common is web farming/gardens? Should i design my website for it?
[Link to question](https://stackoverflow.com/questions/6832410/how-common-is-web-farming-gardens-should-i-design-my-website-for-it)
**Creation Date:** 1311693582
**Score:** 2
**Tags:** asp.net, iis, caching, web-farm
## Question Body
<p>I'm running a ASP.NET website, the server both reads and writes data to a database but also stores some frequently accessed data directly in the process memory as a cache. When new requests come in they are processed depending on data in the cache before it's written to the DB.</p>

<p>My hosting provider suddenly decided to put their servers under a load balancer. This means that my caching system will go bananas as several servers randomly processes the requests. So i have to rewrite a big chunk of my application only to get worse performance since i now have to query the database instead of a lightning fast in memory variable check.</p>

<p>First i don't really see the point of distributing the load on the iis server as in my experience DB queries are most often the bottleneck, now the DB has to take even more banging. Second, it seems like these things would require careful planning, not just something a hosting provider would set up for all their clients and expect all applications to be written to suit them. </p>

<p>Are these sort of things common or was i stupid using the process memory as cache in the first place? </p>

<p>Should i start looking for a new hosting provider or can i expect web farming to arrive sooner or later anywhere? Should I keep transitions like this in consideration for all future apps i write and avoid in process caching and similar designs completely?</p>

<p>(Please don't want to make this into a farming vs not farming battle, i'm just wondering if it's so common that i have to keep it in mind when developing.)</p>

## Answers
### Answer ID: 6833137
<p>I am definitely more of a developer than a network/deployment guru.  So while I have a reasonably good overall understanding of these concepts (and some firsthand experience with pitfalls/limitations), I'll rely on other SO'ers to more thoroughly vet my input.  With that caveat...</p>

<p>First thing to be aware of: a "web farm" is different from a "web garden".  A web farm is usually a series of (physical or virtual) machines, usually each with a unique IP address, behind some sort of load-balancer.  Most load balancers support session-affinity, meaning a given user will get a random machine on their first hit to the site, but will get that same machine on every subsequent hit.  Thus, your in-memory state-management should still work fine, and session affinity will make it very likely that a given session will use the same application cache throughout its lifespan.</p>

<p>My understanding is a "web garden" is specific to IIS, and is essentially "multiple instances" of the webserver running in parallel on the same machine.  It serves the same primary purpose as a web farm (supporting a greater number of concurrent connections).  However, to the best of my knowledge it does not support any sort of session affinity.  That means each request could end up in a different logical application, and thus each could be working with a different application cache.  It also means that you cannot use in-process session handling - you must go to an ASP Session State Service, or SQL-backed session configuration.  Those were the big things that bit me when my client moved to a web-garden model.</p>

<p>"<em>First i don't really see the point of distributing the load on the iis server as in my experience DB queries are most often the bottleneck</em>".  IIS has a finite number of worker threads available (configurable, but still finite), and can therefore only serve a finite number of simultaneous connections.  Even if each request is a fairly quick operation, on busy websites, that finite ceiling can cause slow user experience.  Web farms/gardens increases that number of simultaneous requests, even if it doesn't perfectly address leveling of CPU load.</p>

<p>"<em>Are these sort of things common or was i stupid using the process memory as cache in the first place?</em> "  This isn't really an "or" question.  Yes, in my experience, web farms are very common (web gardens less so, but that might just be the clients I've worked with).  Regardless, there is nothing wrong with using memory caches - they're an integral part of ASP.NET.  Of course, there's numerous ways to use them incorrectly and cause yourself problems - but that's a much larger discussion, and isn't really specific to whether or not your system will be deployed on a web farm.</p>

<p>IN MY OPINION, you should design your systems assuming:</p>

<ul>
<li>they will have to run on a web farm/garden</li>
<li>you will have session-affinity</li>
<li>you will NOT have application-level-cache-affinity</li>
</ul>

<p>This is certainly not an exhaustive guide to distributed deployment.  But I hope it gets you a little closer to understanding some of the farm/garden landscape.</p>

