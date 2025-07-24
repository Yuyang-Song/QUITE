# Extremely slow query times in Entity Framework compared to SSMS
[Link to question](https://stackoverflow.com/questions/69243743/extremely-slow-query-times-in-entity-framework-compared-to-ssms)
**Creation Date:** 1632058379
**Score:** 5
**Tags:** c#, sql-server, entity-framework-core
## Question Body
<p>I've inherited a codebase and I'm having a weird issue with Entity Framework Core v3.1.19.</p>
<p>Entity Framework is generating the following query (as found in SQL Server Profiler) and it's taking nearly 30 seconds to run, when running the same code (again taken from profiler) takes 1 second  in SSMS (this is one example but the entire site runs extremely slow when getting data from the database).</p>
<pre><code>exec sp_executesql N'SELECT [t].[Id], [t].[AccrualLink], [t].[BidId], [t].[BidId1], [t].[Cancelled], [t].[ClientId], [t].[CreatedUtc], [t].[CreatorUserId], [t].[Date], [t].[DeletedUtc], [t].[DeleterUserId], [t].[EmergencyContact], [t].[EmergencyName], [t].[EmergencyPhone], [t].[EndDate], [t].[FinalizerId], [t].[Guid], [t].[Invoiced], [t].[IsDeleted], [t].[Notes], [t].[OfficeId], [t].[PONumber], [t].[PlannerId], [t].[PortAgencyAgentEmail], [t].[PortAgencyAgentName], [t].[PortAgencyAgentPhone], [t].[PortAgencyId], [t].[PortAgentId], [t].[PortId], [t].[PortType], [t].[PositionNote], [t].[ProposalLink], [t].[ServiceId], [t].[ShipId], [t].[ShorexAssistantEmail], [t].[ShorexAssistantName], [t].[ShorexAssistantPhone], [t].[ShorexManagerEmail], [t].[ShorexManagerName], [t].[ShorexManagerPhone], [t].[ShuttleBus], [t].[ShuttleBusEmail], [t].[ShuttleBusName], [t].[ShuttleBusPhone], [t].[ShuttleBusServiceProvided], [t].[TouristInformationBus], [t].[TouristInformationEmail], [t].[TouristInformationName], [t].[TouristInformationPhone], [t].[TouristInformationServiceProvided], [t].[UpdatedUtc], [t].[UpdaterUserId], [t].[Water], [t].[WaterDetails], [t0].[Id], [t0].[CreatedUtc], [t0].[CreatorUserId], [t0].[DeletedUtc], [t0].[DeleterUserId], [t0].[Guid], [t0].[IsDeleted], [t0].[LanguageId], [t0].[Logo], [t0].[Name], [t0].[Notes], [t0].[OldId], [t0].[PaymentTerms], [t0].[Pricing], [t0].[Services], [t0].[Status], [t0].[UpdatedUtc], [t0].[UpdaterUserId], [t1].[Id], [t1].[CreatedUtc], [t1].[CreatorUserId], [t1].[DeletedUtc], [t1].[DeleterUserId], [t1].[Guid], [t1].[IsDeleted], [t1].[Name], [t1].[OldId], [t1].[UpdatedUtc], [t1].[UpdaterUserId], [s].[Id], [s].[CreatedUtc], [s].[CreatorUserId], [s].[DeletedUtc], [s].[DeleterUserId], [s].[Guid], [s].[IsDeleted], [s].[Name], [s].[Pax], [s].[UpdatedUtc], [s].[UpdaterUserId]
FROM (
    SELECT [o].[Id], [o].[AccrualLink], [o].[BidId], [o].[BidId1], [o].[Cancelled], [o].[ClientId], [o].[CreatedUtc], [o].[CreatorUserId], [o].[Date], [o].[DeletedUtc], [o].[DeleterUserId], [o].[EmergencyContact], [o].[EmergencyName], [o].[EmergencyPhone], [o].[EndDate], [o].[FinalizerId], [o].[Guid], [o].[Invoiced], [o].[IsDeleted], [o].[Notes], [o].[OfficeId], [o].[PONumber], [o].[PlannerId], [o].[PortAgencyAgentEmail], [o].[PortAgencyAgentName], [o].[PortAgencyAgentPhone], [o].[PortAgencyId], [o].[PortAgentId], [o].[PortId], [o].[PortType], [o].[PositionNote], [o].[ProposalLink], [o].[ServiceId], [o].[ShipId], [o].[ShorexAssistantEmail], [o].[ShorexAssistantName], [o].[ShorexAssistantPhone], [o].[ShorexManagerEmail], [o].[ShorexManagerName], [o].[ShorexManagerPhone], [o].[ShuttleBus], [o].[ShuttleBusEmail], [o].[ShuttleBusName], [o].[ShuttleBusPhone], [o].[ShuttleBusServiceProvided], [o].[TouristInformationBus], [o].[TouristInformationEmail], [o].[TouristInformationName], [o].[TouristInformationPhone], [o].[TouristInformationServiceProvided], [o].[UpdatedUtc], [o].[UpdaterUserId], [o].[Water], [o].[WaterDetails]
    FROM [OpsDocuments] AS [o]
    WHERE ([o].[IsDeleted] &lt;&gt; CAST(1 AS bit)) AND ((CASE
        WHEN [o].[Cancelled] = CAST(0 AS bit) THEN CAST(1 AS bit)
        ELSE CAST(0 AS bit)
    END &amp; CASE
        WHEN [o].[Invoiced] = CAST(0 AS bit) THEN CAST(1 AS bit)
        ELSE CAST(0 AS bit)
    END) = CAST(1 AS bit))
    ORDER BY [o].[Date]
    OFFSET @__p_0 ROWS FETCH NEXT @__p_1 ROWS ONLY
) AS [t]
LEFT JOIN [TourClients] AS [t0] ON [t].[ClientId] = [t0].[Id]
LEFT JOIN [TourLanguages] AS [t1] ON [t0].[LanguageId] = [t1].[Id]
LEFT JOIN [Ships] AS [s] ON [t].[ShipId] = [s].[Id]
ORDER BY [t].[Date]',N'@__p_0 int,@__p_1 int',@__p_0=0,@__p_1=10
</code></pre>
<p>This query is returning 10 rows from a possible 55 so were not talking big numbers or anything.</p>
<p>At first I thought it might be data type issues on conversion but checking all the data types they are all correct and since the issue is showing in profiler I'm assuming this is a SQL issue not specifically Entity Framework. However I cant find any difference between the two when running in profiler except the one from EF just takes 30 times longer.</p>
<p>Hoping someone might have a suggestion of where to look.</p>
<p>Edit: Thanks for all the suggestions in the comments. As to the Linq and reproducible example it's going to be tricky as the code base for this project is some odd home-baked auto-generating system. You give it a ViewModel with tonnes of custom attributes and it tries to do everything for you (so many layers of abstraction) so its difficult to find anything.
It sounds like I'm going to have to start rewriting these into more finite controllers.</p>

## Answers
### Answer ID: 74653062
<p>I know this is a very late answer, but based on a similar situation recently encountered - this looks very much like an EntityFramework LINQ-to-SQL clause in the codebase is using bitwise operators ('&amp;', '|') instead of logical operators ('&amp;&amp;', '||'). That would explain the odd 'CAST 1 as bit' and '&amp;' and '|' occurrences in the generated SQL above.</p>
<p>CASTs in the WHERE absolutely kill performance. In our case, a 30sec query immediately went subsecond once this was identified.*</p>
<p>Check LINQ along the lines of: <code>&quot;.Where(x =&gt; x.Prop1==true &amp; x.Prop2==false) | (x.Prop3==true))...&quot;</code> and ensure the operators are '&amp;&amp;' instead of '&amp;', etc. It's easy to be already thinking ahead to SQL when writing this code, but it's still C#!</p>
<ul>
<li>I need to be a little more specific on how CASTing in WHEREs killed performance in our case, without actually CASTing the db fields themselves. Here's an example of generated SQL, from using bitwise ops in the EF Core <code>.Where()</code> C#:</li>
</ul>
<p><code>WHERE CASE WHEN cid = 1234 THEN CAST(1 as bit) ELSE CAST (0 as bit) END &amp; (CASE WHEN (date1 IS NULL OR date1 IN ('2000-1-1', '1999-1-1')) THEN CAST (1 as bit) ELSE CAST(0 as bit) END | CASE WHEN (isverified IS NOT NULL AND isverified = CAST(1 as bit)) THEN CAST (1 AS bit) ELSE CAST(0 as bit) END)</code></p>
<p>This can be rewritten with logical ops as:</p>
<p><code>WHERE ci=1234 AND ((date1 IS NULL OR date1 IN ('2000-1-1', '1999-1-1')) OR (isverified IS NOT NULL AND isverified=1))</code></p>
<p>First query (EF-generated thanks to bitwise ops mistakenly in the EF code Where clause) took 30secs on our 45-million-row table. The second was &lt;1s. The explanation for this that I can see is - and I'm open to correction - that the first query essentially generates a bitwise expression per row that must be evaluated, thus being non-sargable and requiring a table scan.</p>

### Answer ID: 69253956
<p>The main issue here is that you have stated that this &quot;query&quot; is taking more than 30 seconds in EF and less than 1 second in SSMS, but what you haven't provided is the SQL that EF has compiled for execution</p>
<blockquote>
<p>You're asking us to compare <em>apples</em> with the <em>idea</em> of an orange...<br />
We really need to see the compiled SQL as a minimum but the C# / Linq code will also be helpful. It doesn't have to compile, but it will demonstrate some of the context that you are operating within.</p>
</blockquote>
<h2>tldr</h2>
<p>This is less likely to be about EF itself and more about the patterns in the code you are executing and <strong>your specific query</strong>.<br />
For such a small and simple query lazy loading should not be used at all, after that the usual suspects that we talk about with EF performance should not be significantly measurable for this tiny dataset either. <em>All we can say from the little information provided is that your EF query does not match your expected SQL</em>, so we should start there and make sure your EF query is compiling a reasonable approximation of the query that you are expecting.</p>
<h2>If all else fails, simply use <a href="https://learn.microsoft.com/en-us/ef/core/querying/raw-sql" rel="nofollow noreferrer">Raw SQL Queries</a> and move on.</h2>
<p>While it is true that there are some overheads inherent by using an ORM like EF, with a simple query like this we should be talking about a few <em>milliseconds</em>, anything else indicates that your EF Linq query is either wrong or written very poorly.</p>
<p>If you are using Lazy Loading, then be mindfull of which lines of code will cause a new query from the server instead of using the in-memory data. Lazy Loading can be powerful but there are relatively few situations where it makes sense. Using projections is a good alternative, but you should consider disabling lazy loading altogether and switching over to eager loading <em>always</em>. If you are unsure, try disabling the lazy loading feature of your data context, you'll find out very quickly if your code was depending on the lazy feature as it will likely fail at runtime.</p>
<p>If there is a single execution point then you should be able capture the raw SQL <em>and</em> time the round trip.<br />
<em>Post the code you used to time the execution, the raw SQL and the time please.</em></p>
<blockquote>
<p>If a single execution point takes 30 seconds to load then there might be a <em>cold start</em> issue, that is you might have some processes executing before your query, wihtout knowing more about your framework, an easy example to debug with is to initiate the database connection first with a simple call to return the count of all the <code>OpsDocuments</code> records, then execute your query.</p>
</blockquote>
<p>The other performance concerns like having too many columns or strange data type comparisons don't really apply here. You could optimise this query for sure, but with 10 rows and less than 50 columns, even a very slow PC should be able to read this result into an EF graph in a few milliseconds.</p>
<p>If you have already eliminated Lazy-Loading, and your captured SQL query generated by EF is <em>lightning fast</em> when executed in SSMS but awfully slow from your application runtime, then Locking &quot;might&quot; be a concern.</p>
<p>A simple way to verify if locking is an issue is to query the database for the current executing queries while your application is waiting for the response, if the wait time is truely 30 seconds, then you'll have plenty of time to execute the following in SSMS while you are waiting.</p>
<blockquote>
<p>As a bonus, this will prove if the query is running at all</p>
</blockquote>
<pre><code>Declare @Identifier Char(1) = '~'
SELECT r.session_id, r.status,
       st.TEXT AS batch_text,
       qp.query_plan AS 'XML Plan',
       r.start_time,
       r.status,
       r.total_elapsed_time, r.blocking_session_id, r.wait_type, r.wait_time, r.open_transaction_count, r.open_resultset_count
FROM sys.dm_exec_requests AS r
     CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS st
     CROSS APPLY sys.dm_exec_query_plan(r.plan_handle) AS qp
WHERE st.TEXT NOT LIKE 'Declare @Identifier Char(1) = ''~''%'
ORDER BY cpu_time DESC;
</code></pre>

### Answer ID: 69248005
<p>EF will always take longer than a raw SQL because EF has to materialize tracked entities for every entity returned in the query.</p>
<p>Looking at the SQL this is an eager-loading query across 4 tables, OPSDocuments, TourClients, TourLanguages, and Ships.</p>
<p>Reasons this could suddenly take much longer after some seemingly unrelated changes: new relationships being lazy loaded.
An example of this would be where this data is being serialized and a new relationship has been added to one or more entities which are now being tripped by lazy load hits. (Usually evidenced by seeing extra queries coming up after this one runs before the page loads)</p>
<p>Other causes for this to be taking longer than it should:</p>
<ol>
<li>The DbContext is tracking too many entities. The more entities a DbContext is tracking, the more references it has to go through when piecing together results from a Linq query. Some teams expect that EF caches instances similar to NHibernate and this would improve performance. Typically it is the opposite, the more entities it is tracking the longer it can take to get results.</li>
<li>Concurrent reads &amp; locks. If tables are not efficiently indexed this can be a bit of a killer when a system is run in production compared to testing/debugging. Typically though this would affect systems that have very large row and/or user counts.</li>
</ol>
<p>The best general advice I can offer when it comes to tackling performance issues with EF is to leverage projection as much as possible. This helps you optimized queries and identify useful indexes that reflect the highest-volume scenarios you are pulling data, as well as avoid future pitfalls from changing relationships which can result in Select n+1 lazy load hits creeping into systems.</p>
<p>For example, instead of:</p>
<pre><code>var results = context.OpsDocuments
    .Include(x =&gt; x.TourClient)
    .ThenInclude(x =&gt; x.TourLanguage)
    .Include(x =&gt; x.Ship)
    .OrderBy(x =&gt; x.Date)
    .ToList();
</code></pre>
<p>use:</p>
<pre><code>var results = context.OpsDocuments
    .Select(x =&gt; new TourSummaryViewModel
    {
        DocumentId = x.DocumentId,
        ClientId = x.Client.Id,
        ClientName = x.Client.Name,
        Language = x.Client.Language.Name,
        ShipName = x.Ship.Name,
        Date = x.Date
    }).OrderBy(x =&gt; x.Date)
    .ToList();
</code></pre>
<p>... Where the view model reflects just the details you need from the entity graph. This protects you from introduced relationships that the view/consumer doesn't need (unless you add them to the <code>Select</code>) and the resulting query can help identify useful indexes to boost performance if this is something that gets run a fair bit. (Tuning indexing based on actual DB use rather than guesswork)</p>
<p>I would also recommend that all queries like this implement a limiter for the maximum rows returned. (using <code>Take</code>) to help avoid surprises as systems age where row counts grow over time leading to performance degradation over time.</p>

