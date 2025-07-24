# How to rewrite correlated join from SQL to LINQ
[Link to question](https://stackoverflow.com/questions/68200461/how-to-rewrite-correlated-join-from-sql-to-linq)
**Creation Date:** 1625080315
**Score:** 0
**Tags:** c#, mysql, sql, linq
## Question Body
<p>I'm trying to rewrite following SQL query into LINQ:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT `i`.`symbol`, `i`.`id`, `t0`.`close`, `t`.`close`, `t`.`close` - `t0`.`close`, (`t`.`close` - `t0`.`close`) / `t0`.`close`
FROM `investment` AS `i`
LEFT JOIN `investment_record` AS `t0` ON `t0`.id = (
    SELECT `i0`.id
    FROM `investment_record` AS `i0`
    WHERE (`i0`.`date` &lt;= @dateFrom) AND i.id = i0.investment_id
    ORDER BY `i0`.`date` DESC
    LIMIT 1
)
LEFT JOIN `investment_record` AS `t` ON `t`.id =(
    SELECT `i0`.id
    FROM `investment_record` AS `i0`
    WHERE (`i0`.`date` &lt;= @dateTo) AND i.id = i0.investment_id
    ORDER BY `i0`.`date` DESC
    LIMIT 1
) 

WHERE `i`.`id` IN (@id0, @id1, ....)
</code></pre>
<p>My main issues are the <code>AND i.id = i0.investment_id</code> and <code>LIMIT 1</code> parts of JOINs.</p>
<p>Currently the best I could achieve is this:</p>
<pre class="lang-cs prettyprint-override"><code>from inv in _context.Investment
join recTo in _context.InvestmentRecord on inv.Id equals recTo.InvestmentId into recToColl
from recToNullable in recToColl.Where(x =&gt; x.Date &lt;= dateTo).OrderByDescending(x =&gt; x.Date).Take(1).DefaultIfEmpty()
join recFrom in _context.InvestmentRecord on inv.Id equals recFrom.InvestmentId into recFromColl
from recFromNullable in recFromColl.Where(x =&gt; x.Date &lt;= dateFrom).OrderByDescending(x =&gt; x.Date).Take(1).DefaultIfEmpty()
where investmentIds.Contains(inv.Id)
let amountFrom = recFromNullable.Close
let amountTo = recToNullable.Close
select new InvestmentPerformance(
  inv.Symbol,
  inv.Id,
  amountFrom,
  amountTo,
  amountTo - amountFrom,
  (amountTo - amountFrom) / amountFrom
);
</code></pre>
<p>but the problem is it doesn't work.</p>
<p>It gives the expression cannot be translated exception:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression
'DbSet()
.GroupJoin(
inner: DbSet(),
outerKeySelector: inv =&gt; inv.Id,
innerKeySelector: recTo =&gt; recTo.InvestmentId,
resultSelector: (inv, recToColl) =&gt; new {
inv = inv,
recToColl = recToColl
})' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly
by inserting a call to 'A sEnumerable', 'AsAsyncEnumerable', 'ToList',
or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a>
for more information.</p>
</blockquote>
<p>Point of this ugly SQL (and LINQ) is to calculate performance of investment for given time interval. User is able to specify from-to dates. Problem is sometimes user could specify date without any records (bank holiday for example). So for given date, I want to use the closest previous record (that is the reason for <code>&lt;= @dateFrom</code> conditions and <code>ORDER BY date DESC LIMIT 1</code> parts of the SQL.</p>
<p>I tried many variations of the LINQ with different forms of joins, but none of them worked as I need :(</p>
<p>I'm using EF.Core 5 and MySQL database.</p>

## Answers
### Answer ID: 68200700
<p>The original SQL query seems complex to me. I would already rewrite it using a <code>OUTER APPLY</code> instead of sub-join queries.</p>
<pre class="lang-sql prettyprint-override"><code>SELECT `i`.`symbol`, `i`.`id`, `t0`.`close`, `t`.`close`, `t`.`close` - `t0`.`close`, (`t`.`close` - `t0`.`close`) / `t0`.`close`
FROM `investment` AS `i`
OUTER APPLY (
  SELECT `i0`.id
  FROM `investment_record` AS `i0`
  WHERE (`i0`.`date` &lt;= @dateFrom) AND i.id = i0.investment_id
  ORDER BY `i0`.`date` DESC
  LIMIT 1
) AS t0
OUTER APPLY (
  SELECT `i0`.id
  FROM `investment_record` AS `i0`
  WHERE (`i0`.`date` &lt;= @dateTo) AND i.id = i0.investment_id
  ORDER BY `i0`.`date` DESC
  LIMIT 1
) AS t

WHERE `i`.`id` IN (@id0, @id1, ....)
</code></pre>
<p>Then I would translate this using EF's way to write <code>OUTER APPLY</code>. This <a href="https://stackoverflow.com/questions/16501002/entity-framework-and-cross-outer-apply">SO post</a> might be of help.</p>
<p>It would look something like this:</p>
<pre class="lang-cs prettyprint-override"><code>from inv in _context.Investments
from rec1 in _context.InvestmentsRecords.Where(ir =&gt; ir.InvestmentId = inv.InvestmentId).Where(ir =&gt; ir.Date &lt;= DateFrom).OrderByDescending().Take(1)
from rec1 in _context.InvestmentsRecords.Where(ir =&gt; ir.InvestmentId = inv.InvestmentId).Where(ir =&gt; ir.Date &lt;= DateTo).OrderByDescending().Take(1)
...
</code></pre>

