# Why does query hang sometimes but not others
[Link to question](https://stackoverflow.com/questions/17385621/why-does-query-hang-sometimes-but-not-others)
**Creation Date:** 1372548318
**Score:** 3
**Tags:** mysql
## Question Body
<p>There is, in a legacy product I support, a PHP query to mysql which works sometimes and at other times hangs (is perhaps finite, but if so an unreasonably long duration).  My SQL skills are pretty limited, but I was able to run the query manually on mysql and here's what I've found out so far.</p>

<p>Given tables 'orders', 'lineItems', and 'lineItemDefns', </p>

<p>where each order is one-to-many lineItems and
lineItems are one-to-one with lineItemDefinitions</p>

<p>and table OrderReports which maps each report (reportId) to a group of orders and their lineItem data and the following SQl query:</p>

<pre><code>SELECT SEC_TO_TIME(SUM(orders.itemCount*lineItems.itemCount*lineItemDefns.estimatedDuration)) as estimatedTotalDuration
FROM orders, lineItems, lineItemDefns
WHERE orders.id=lineItems.parentOrder
  AND lineItemDefns.id=lineItems.definitionId
  AND orders.id in 
      (SELECT DISTINCT orderId 
       FROM OrderReports
       WHERE OrderReports.reportId=98619);
</code></pre>

<p>(This was dumped from the query string immediately before call to DBI getAll in PHP.)</p>

<p>When I run the second select by itself it returns almost instantaneously with a single row.  When I run the first select substituting that orderId for the second select, it returns in less than a second with a NULL estimatedTotalDuration.  There are only two rows for this reportId, which corresponds to the two lineItem rows for this order.  The estimatedDurations for the lineItems (in lineItemDefns) are both NULL.</p>

<p>All the ids in the query, primary and foreign, are indexed.</p>

<p>All numbers are integers, duration time is in seconds (int(11)). The itemCounts in this case are 1.</p>

<p>But when I run it as above, it works in my test database (slow at 30 seconds) but it won't complete when left for an unreasonable amount of time (over 50 minutes) for an equivalent  report on the production data.</p>

<p>No tables seem to be locked up as I can run the first two partial query tests while the report is hung.</p>

<p>Can someone point out any obvious causes (e.g. handling null estimatedDurations?).
Likewise, any hints on what to look at next?  It's a production database, so I don't want to do anything that could cause delays to other users.</p>

<p>Any suggestions for rewriting the query would be appreciated as well.</p>

<p>mysql 5.0.37 on Fedora 7 (test db is mysql 5.0.45 on Fedora 8)</p>

<p>Like, Penny in The Big Bang Theory, that's all I know. Oh, Fig Newton is named after Newton, MA. ;)</p>

## Answers
### Answer ID: 17385686
<p>The problem is that old versions of MySQL did not optimize <code>in</code> with a subquery very well.  In particular, it is running the subquery for every possible row of output . . . doing the <code>select distinct</code> over and over again.</p>

<p>You can move this subquery to the <code>from</code> clause to fix the problem:</p>

<pre><code>SELECT SEC_TO_TIME(SUM(orders.itemCount*lineItems.itemCount*lineItemDefns.estimatedDuration)) as estimatedTotalDuration
FROM orders join
     lineItems
     on orders.id=lineItems.parentOrder join
     lineItemDefns
     on lineItemDefns.id=lineItems.definitionId join
     (SELECT DISTINCT orderId 
      FROM OrderReports
      WHERE OrderReports.reportId=98619
     ) orep
     on orders.id = orep.id
</code></pre>

<p>I also moved all your joins into the <code>from</code> clause to use standard ANSI join syntax.</p>

