# Why is AsSplitQuery doing separate roundtrip to DB for each query?
[Link to question](https://stackoverflow.com/questions/75580890/why-is-assplitquery-doing-separate-roundtrip-to-db-for-each-query)
**Creation Date:** 1677503294
**Score:** 2
**Tags:** .net, entity-framework-core, ef-core-7.0
## Question Body
<p>I have finally been able to upgrade a very old codebase from EF6 to EF Core 7 and I'm playing with some &quot;new&quot; features.</p>
<p>I have been super hyped about Split query option for eager loading but when reading the  <a href="https://learn.microsoft.com/en-us/ef/core/querying/single-split-queries#characteristics-of-split-queries" rel="nofollow noreferrer">documentation</a> I was taken back by this:</p>
<blockquote>
<p>Each query currently implies an additional network roundtrip to your database. Multiple network roundtrips can degrade performance, especially where latency to the database is high (for example, cloud services).</p>
</blockquote>
<p>Why? Why is it not multiple queries in a single roundtrip? <code>SqlDataReader</code> can process queries with multiple result sets. This stopped me from rewriting existing code using stored procedure to EF.</p>
<p>Unless, these split queries are executed concurrently when MARS is enabled on connection to SQL server. Are they? I know that <code>DbContext</code> does not support parallel processing but does it execute these queries concurrently and only process results in sequence?</p>
<p>Additional question - if there is this limitation for executing each query in separate roundtrip, is it possible to define SplitQuery behaviour only for certain includes in a query instead of defining it for all includes in a query?</p>

## Answers
### Answer ID: 75581016
<p>Based on some discussion on the github if MARS is enabled EF Core can use it for split queries (see <a href="https://github.com/dotnet/efcore/issues/21420" rel="nofollow noreferrer">this</a> and <a href="https://github.com/dotnet/efcore/pull/21456" rel="nofollow noreferrer">this</a>), but in general case (since EF Core can be used with different databases) the <a href="https://learn.microsoft.com/en-us/ef/core/querying/single-split-queries" rel="nofollow noreferrer">next quote</a> from the docs I would argue explains the general case behavior/wording:</p>
<blockquote>
<p>While some databases allow consuming the results of multiple queries at the same time (SQL Server with MARS, Sqlite), most allow only a single query to be active at any given point. So all results from earlier queries must be buffered in your application's memory before executing later queries, which leads to increased memory requirements.</p>
</blockquote>
<p>Also the following <a href="https://github.com/dotnet/efcore/issues/30299#issuecomment-1435529785" rel="nofollow noreferrer">comment by Shay Rojansky</a> (one of the EF team members) can be useful:</p>
<blockquote>
<p>MARS support in SqlClient is known to have various performance issues (as well as other bugs), some of them severe. It's recommended to avoid it.</p>
</blockquote>

