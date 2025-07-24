# How to reference SQL snippet multiple times in a query?
[Link to question](https://stackoverflow.com/questions/30775047/how-to-reference-sql-snippet-multiple-times-in-a-query)
**Creation Date:** 1434009917
**Score:** 0
**Tags:** sql-server, t-sql, sql-server-2012
## Question Body
<p>I need to convert some stored procs to views and the stored procs have a lot of <code>DECLARE</code> statements which create constants that get referenced later in the query. For example</p>

<p><code>SELECT @FIRSTDAYLASTYEAR = DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01')</code></p>

<p>I need to refer to <code>@FIRSTDAYLASTYEAR</code> in a single query multiple times, what's the best way to do this without having to declare variables?</p>

<p>For example consider:</p>

<pre><code>DECLARE @FIRSTDAYLASTYEAR datetime = DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01')
select
    @FIRSTDAYLASTYEAR as FirstDayLastYear,
    Case when orderDate &gt; @FIRSTDAYLASTYEAR then 'CurrentOrders' else 'ArchiveOrders' end as State
from
    orders
</code></pre>

<p>I don't want to rewrite as</p>

<pre><code>select
    DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01') as FirstDayLastYear,
    Case when orderDate &gt; DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01') then 'CurrentOrders' else 'ArchiveOrders' end as State
from
    orders
</code></pre>

<p>I want to be able to alias <code>@FIRSTDAYLASTYEAR</code> somehow in the query.</p>

<p><strong>EDIT</strong></p>

<p>Thanks for the replies, do you think this would perform the same:</p>

<pre><code>select
    constants.FirstDayLastYear,
    Case when orderDate &gt; constants.FirstDayLastYear then 'CurrentOrders' else 'ArchiveOrders' end as State
from
    orders o
cross join 
    (select 
        DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01') as FirstDayLastYear
        ) as constants
</code></pre>

<p>Reason I ask is that this code may get ported to another database platform at a future date that doesn't support CTEs. </p>

## Answers
### Answer ID: 30775661
<p>You can also use <code>APPLY VALUES</code>:</p>

<pre><code>SELECT   
  FirstDateLastYear as FirstDayLastYear,
  CASE WHEN orderDate &gt; FirstDateLastYear THEN 'CurrentOrders' ELSE 'ArchiveOrders' END AS State
FROM orders
CROSS APPLY (VALUES(DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01'))) AS date(FirstDateLastYear);
</code></pre>

### Answer ID: 30775165
<p>You should consider 'common table expressions' like</p>

<pre><code>WITH vars AS (
  SELECT DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, getdate())), '1901-01-01') as FirstDayLastYear) 
)
SELECT Case when orderDate &gt; FirstDayLastYear) then 'CurrentOrders' else 'ArchiveOrders' end as State
... --- your actual select statement for the view ...
FROM orders, vars
...
</code></pre>

### Answer ID: 30775160
<p>You can construct a CTE that contains a single row with all of your variables, and then reference that in the query:</p>

<pre><code>WITH Consts as (
    SELECT DATEADD(YEAR, DATEDIFF(YEAR, '19010101', getdate()), '19000101')
           as FirstDayLastYear,
           DATEADD(YEAR, DATEDIFF(YEAR, '19010101', getdate()), '19001231')
           as LastDayLastYear
)
select
    c.FirstDayLastYear,
    Case when orderDate &gt; c.FirstDayLastYear then 'CurrentOrders' else 'ArchiveOrders' end as State
from
    orders
       cross join
    Consts c
</code></pre>

<p>If you have variables that build on top of other variables, you might need to have multiple levels of CTEs.</p>

### Answer ID: 30775189
<p>You can create a scalar function:</p>

<pre><code>CREATE FUNCTION fnPrevYear ( )
RETURNS date
AS
    BEGIN
        RETURN DATEADD(YEAR, DATEDIFF(YEAR, '1901-01-01', DATEADD(YEAR, -1, GETDATE())), '1901-01-01')
    END
</code></pre>

<p>and just call it where needed:</p>

<pre><code>SELECT dbo.fnPrevYear()  
</code></pre>

<p>But it will be slow for large data. You can use common table expressions as a better alternative to this.</p>

### Answer ID: 30775168
<p>Local variables are not allowed in views in SQL Server.<br>
In the case you described, I would probably create a view to encapsulate the value of the variable used in the stored procedure, and then query that view as a sub query or derived table (depending on your needs) inside the bigger view.</p>

<p>However, this may not be possible for converting all the local variables in your stored procedure. for the cases where it's impossible, you can create a user defined function to encapsulate the value of the local variable and use it in the same way I've descried using the view.</p>

<p>you could create a <code>cte</code> instead of a view, however if you will need the same logic to apply to more then one view, you will have to write the <code>cte</code> for each procedure you convert to view.</p>

