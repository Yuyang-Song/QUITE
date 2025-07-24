# Resolving Poor Execution Plan in SQL Server with CLR Scalar Function
[Link to question](https://stackoverflow.com/questions/79324597/resolving-poor-execution-plan-in-sql-server-with-clr-scalar-function)
**Creation Date:** 1735841140
**Score:** 2
**Tags:** sql-server, t-sql, query-optimization, sqlclr, query-planner
## Question Body
<p>Essentially, my question boils down to observing these two query plans (from SQL Server 2019):</p>
<ol>
<li>Plan using a SQL-defined scalar function.
<ul>
<li><a href="https://www.brentozar.com/pastetheplan/?id=ByIIIdEIJx" rel="nofollow noreferrer">Link to plan</a></li>
</ul>
</li>
</ol>
<p><a href="https://i.sstatic.net/ZLMqbzEm.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/ZLMqbzEm.png" alt="SQL scalar function query plan" /></a></p>
<ol start="2">
<li>Plan using a CLR-defined scalar function.
<ul>
<li><a href="https://www.brentozar.com/pastetheplan/?id=B1nKUO48ke" rel="nofollow noreferrer">Link to plan</a></li>
</ul>
</li>
</ol>
<p><a href="https://i.sstatic.net/GsWXoX1Q.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/GsWXoX1Q.png" alt="CLR scalar function query plan" /></a></p>
<p>I defined a scalar function to parse out a string representation of an IP address into the <code>binary(16)</code> value of the IPv6 address (mapping IPv4 addresses over to IPv6). I first implemented it in SQL, but then I also implemented it in C# using the built-in <code>IPAddress</code> class to parse the value. I'm attempting to use this function to join a table containing IP address strings to a table with a list of parsed out CIDR blocks (clustered index on <code>[Start]</code> and <code>[End]</code> <code>binary(16)</code> values).</p>
<p>There were two ways that I wrote the SQL query:</p>
<ol>
<li>Use the scalar function directly in the <code>JOIN</code> criteria.</li>
</ol>
<pre class="lang-sql prettyprint-override"><code>SELECT
    *
FROM
    [dbo].[values]
    val
LEFT JOIN
    [dbo].[cidr]
    cidr
        ON [dbo].[fn_ParseIP](val.[IpAddress]) BETWEEN cidr.[Start] AND cidr.[End]
;
</code></pre>
<ol start="2">
<li>Compute the scalar function in an <code>APPLY</code> clause before referencing it in the <code>JOIN</code>.</li>
</ol>
<pre class="lang-sql prettyprint-override"><code>SELECT
    val.*, cidr.*
FROM
    [dbo].[values]
    val
CROSS APPLY
    (
        SELECT [ParsedIpAddress] = [dbo].[fn_ParseIP](val.[IpAddress])
    )
    calc
LEFT JOIN
    [dbo].[cidr]
    cidr
        ON calc.[ParsedIpAddress] BETWEEN cidr.[Start] AND cidr.[End]
;
</code></pre>
<p><em>In my testing, <code>[dbo].[values]</code> contained 17 rows (and was defined using <code>VALUES</code> rather than being an actual table) and <code>[dbo].[cidr]</code> contained 986,320 rows.</em></p>
<p>When using a scalar function defined in SQL, query 1 takes about 7.5 minutes to run and query 2 takes under 1 second.</p>
<p>When using a CLR scalar function, both queries take about 2.5 minutes to run, but query 2 has an extra node in the query plan to compute the scalar function after the join.</p>
<p>The difference is ultimately that when referencing the scalar function that was defined in SQL, I'm able to get it to generate the first plan where it computes the results of the scalar function first and then uses those as the seek predicate into the <code>[dbo].[cidr]</code> clustered index when performing the join. But when using the CLR function, it always performs the calculation as part of the clustered index seek (and filter), so it is running the function significantly more often to get the results.</p>
<p>My assumption is that this behavior could be due to the query planner believing the function to be nondeterministic, but I have the CLR function implemented with the following attributes:</p>
<pre class="lang-cs prettyprint-override"><code>    [SqlFunction(
        DataAccess = DataAccessKind.None,
        IsDeterministic = true,
        IsPrecise = true
    )]
    [return: SqlFacet(IsFixedLength = true, IsNullable = true, MaxSize = 16)]
    public static SqlBinary fn_CLR_ParseIP([SqlFacet(MaxSize = 50)] SqlString ipAddress)
    { }
</code></pre>
<p>My hope was that I could rely on the .NET standard library to deal with the IP address parsing for me in SQL. Currently, we have some processes that work with IPv4 addresses only, and I need to update them to work with IPv6 as well. In some of our large databases, this processing is very slow, so I was hoping that the parsing logic in .NET would be more efficient. It seems like the CLR function itself is faster than my SQL implementation, but the effect on the query plan is significantly worse.</p>
<p>I can likely rewrite the query to use temporary tables to parse the IP addresses out first, and that should resolve this issue. I can also get decent results when defining an equivalent CLR table-valued function that returns just a single row.</p>
<p>However, I'd like to know if there is something that I'm missing that would make it easier to use a CLR scalar function as part of a filter predicate. Is it just a bad idea and I should proceed with some of these alternatives, or is there something I that I could do that would make it easier to work with the CLR function as a drop-in replacement for the SQL function?</p>
<hr />
<p>For anybody that is interested, here is the final query that is performing well using the concept given in T N's answer.</p>
<pre class="lang-sql prettyprint-override"><code>SELECT
    *
FROM
    [dbo].[values]
    val
CROSS APPLY
    (
        SELECT [IpAddress] = [dbo].[fn_CLR_ParseIP](val.[IpAddress])
    )
    parsed
OUTER APPLY
    (
        SELECT TOP (1)
            *
        FROM
            [dbo].[cidr]
            _cidr
        WHERE
                _cidr.[range_start] &lt;= parsed.[IpAddress]
            AND _cidr.[range_end]   &gt;= parsed.[IpAddress]
        ORDER BY
            _cidr.[range_start] DESC
    )
    cidr
;
</code></pre>

## Answers
### Answer ID: 79324913
<p>If your <code>cidr</code> table has rows with <em>no</em> overlapping <code>Start/End</code> ranges, so that for any given IP address there will be <em>at most</em> one matching row, you can:</p>
<ol>
<li>Use <code>SELECT TOP 1 ... ORDER BY ...</code> logic to efficiently identify a single candidate row based on the <code>Start</code> column.</li>
<li>Confirm a match by checking the <code>End</code> column value.</li>
<li>Wrap this all up in an <code>OUTER APPLY</code>, with the <code>TOP 1</code> further wrapped up inside a nested subselect.</li>
<li>The <code>WHERE [End] ...</code> test must be performed <em>after</em> the <code>TOP 1</code> operation to prevent scanning of additional rows for the case where the (first) candidate row does not match.</li>
</ol>
<pre><code>OUTER APPLY (
    SELECT candidate.*
    FROM (
        SELECT TOP 1
        FROM cidr
        WHERE cidr.Start &lt;= calc.ParsedIpAddress
        ORDER BY cidr.Start DESC
    ) candidate
    WHERE candidate.[End] &gt;= calc.ParsedIpAddress
) match
</code></pre>
<p>An index on either <code>cidr(Start)</code>, <code>cidr(Start, [End])</code>, or <code>cidr(Start) INCLUDE([End])</code> would be needed for efficient operation.</p>
<p>If your source <code>cidr</code> table can have arbitrarily overlapping ranges such that a given IP can potentially have multiple matches, then I know of no <em>simple</em> &amp; <em>efficient</em> lookup method that avoids a range scan. An index on <code>cidr(Start, [End])</code> would at least perform the range scan on a limited-width (more compact) index rather than to the presumable wider table (clustered index). That might provide some performance improvement.</p>
<p>A more involved solution might involve segregating/partitioning the <code>cidr</code> table based on the number of fixed octets (like the original/obsolete class A, B, C, D subnets) or the number of fixed bits (/16, /24, etc) - up to 16 octets or 128 bits for IPV6. You would then optimize the lookups into each partition and UNION the results. This would almost simulate the way SQL server implements <a href="https://learn.microsoft.com/en-us/sql/relational-databases/spatial/spatial-indexes-overview" rel="nofollow noreferrer"><em>spacial indexes</em></a>.</p>

