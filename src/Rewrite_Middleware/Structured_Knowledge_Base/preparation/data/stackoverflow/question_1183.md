# EntityFramework in .NetCore 3.1 and multiple DBContext
[Link to question](https://stackoverflow.com/questions/62436506/entityframework-in-netcore-3-1-and-multiple-dbcontext)
**Creation Date:** 1592420599
**Score:** 0
**Tags:** entity-framework, .net-core-3.1
## Question Body
<p>I have a .NetCore 2.2 app that is "working".  My customer has asked for some modifications and I decided to try migrating the app to .NetCore 3.1.  EntiryFramework is giving me fits.</p>

<p>My customer has a number of MS SQL "databases" like "Personnel", "Reservations", "Billing", etc.  It is very common for me to have to create queries that match people from Personnel with billing and or other records from other DBs.  I am doing this sort of thing in 2.2 now.</p>

<p>If I run a query similar to the following I get the exception:</p>

<pre><code>Cannot use multiple DbContext instances within a single query execution. Ensure the query uses a single context instance.
</code></pre>

<p>This query appears to use a single context but there is that <code>devicesInRoom</code> entity buried in there.  <code>devicesInRoom</code> is of type <code>IQueryable&lt;string&gt;</code> and comes from a "utility" query I ran earlier.  Basically I want ONLY the <code>reservations</code> where the <code>reservations.Device</code> is the same as one of the items in <code>devicesInRoom</code>.</p>

<pre><code>var reservations = (
    from reservation in reservationsContext.Reservations
    from reservationType in reservationsContext.Types.Where(
        reservationType =&gt; reservationType.Id.Equals(reservation.TypeId)
    ).DefaultIfEmpty()
    from roomMates in devicesInRoom
        .Where(
            roomMates =&gt; roomMates.Equals(reservation.Device)
        ).DefaultIfEmpty()
    where reservation.StartDate &lt; viewEnd
          &amp;&amp; reservation.EndDate &gt; viewStart
          &amp;&amp; reservation.Deleted.Equals(false)
    select reservation.Device
).ToList();
</code></pre>

<p>If I rewrite this query as:</p>

<pre><code>var reservations = (
    from reservation in reservationsContext.Reservations
    from reservationType in reservationsContext.Types.Where(
        reservationType =&gt; reservationType.Id.Equals(reservation.TypeId)
    ).DefaultIfEmpty()
    where reservation.StartDate &lt; viewEnd
          &amp;&amp; reservation.EndDate &gt; viewStart
          &amp;&amp; reservation.Deleted.Equals(false)
    select reservation.Device
).ToList();

var thing = (
    from res in reservations
    from roomMates in devicesInRoom
        .Where(
            roomMates =&gt; roomMates.Equals(res)
        ).DefaultIfEmpty()
    select res
).ToList();
</code></pre>

<p>I still get the error above.  I can't see why querying accross DBs is a bad thing.  </p>

<p>How do I fix this?</p>

## Answers
### Answer ID: 62436597
<blockquote>
  <p>I can't see why querying accross DBs is a bad thing.</p>
</blockquote>

<p>EF has never supported it.  EF Core 2x "solved" this and a number of other query translation limitations by simply evaluating the queries on the client.  EF 3 dropped this "feature" and you have to explicitly declare when you want client-side evaluation by switching from LINQ-to-Entities to LINQ-to-Objects, typically by introducing <code>.ToList()</code> or <code>.AsEnumerable()</code> to transition from server-side evaluation to client-side evaluation.</p>

<p>Something like:</p>

<pre><code>var reservations = (
    from reservation in reservationsContext.Reservations
    from reservationType in reservationsContext.Types.Where(
        reservationType =&gt; reservationType.Id.Equals(reservation.TypeId)
    ).DefaultIfEmpty().ToList()
    from roomMates in devicesInRoom.ToList()
        .Where(
            roomMates =&gt; roomMates.Equals(reservation.Device)
        ).DefaultIfEmpty()
    where reservation.StartDate &lt; viewEnd
          &amp;&amp; reservation.EndDate &gt; viewStart
          &amp;&amp; reservation.Deleted.Equals(false)
    select reservation.Device
).ToList();
</code></pre>

