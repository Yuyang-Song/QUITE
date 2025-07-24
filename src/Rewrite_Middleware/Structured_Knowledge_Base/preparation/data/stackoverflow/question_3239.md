# Entity Framework to EF Core 6 migration query not working
[Link to question](https://stackoverflow.com/questions/73118058/entity-framework-to-ef-core-6-migration-query-not-working)
**Creation Date:** 1658812896
**Score:** -1
**Tags:** .net, entity-framework, linq, entity-framework-core, linq-to-entities
## Question Body
<p>We are migrating our ASP.NET Framework Web Api project to .NET 6 and after fixing all build errors while running the project it starts giving errors in EF queries related to EF Core 3.0+ does not support client evaluation anywhere in the query. We have so many queries written in this way and it's very difficult to find and tell what part of query is causing the issue, like its left join using DefaultIfEmpty() or something else.</p>
<p>Is there some way or tool which can convert these queries to EF Core 3.0+ or at least tell exactly what part of query is causing the problem so that we can apply the change ASAP? Any help/idea will be appreciated, below is such query and I am getting client evaluation error but no clue what part is causing the error. I have all foreign keys constraints in database and I don't like to rewrite the queries again and test it.</p>
<pre><code>var employees = (from e in context.Employees
     join c in context.CompanyEmployees on e.UserId equals c.EmployeeId into ec
     from ce in ec.DefaultIfEmpty()
     join cp in context.CompanyPositions
     on ce.Employee.UserId equals cp.UserId into cpgrp
     from cp1 in cpgrp.DefaultIfEmpty()
     join ctp in context.CategoryPositions on cp1.PositionId equals ctp.PositionId into catpgrp
     from catp in catpgrp.DefaultIfEmpty()
     where e.OrganizationId == organizationId &amp;&amp; (companyId == null || ce.CompanyId == companyId)
     &amp;&amp; (categoryId == null || catp.CategoryId == categoryId)
    
     select new { e, ce }).GroupBy(e =&gt; e.e.UserId).Select(g =&gt; g.FirstOrDefault());
</code></pre>

## Answers
### Answer ID: 73120739
<p>This is workaround query which should return desired result. It emulates what EF Core should do to correctly execute query from question.</p>
<pre class="lang-cs prettyprint-override"><code>var dataQuery = 
    from e in context.Employees
    join c in context.CompanyEmployees on e.UserId equals c.EmployeeId into ec
    from ce in ec.DefaultIfEmpty()
    join cp in context.CompanyPositions on ce.Employee.UserId equals cp.UserId into cpgrp
    from cp1 in cpgrp.DefaultIfEmpty()
    join ctp in context.CategoryPositions on cp1.PositionId equals ctp.PositionId into catpgrp
    from catp in catpgrp.DefaultIfEmpty()
    where e.OrganizationId == organizationId &amp;&amp; (companyId == null || ce.CompanyId == companyId)
        &amp;&amp; (categoryId == null || catp.CategoryId == categoryId) 
    select new { e, ce };

var query = 
    from d in dataQuery.Select(d =&gt; new { d.e.UserId }).Distinct()
    from q in dataQuery.Where(q =&gt; q.e.UserId == d.UserId)
        .Take(1)
    select q;
</code></pre>
<p>Note that usually joins are not needed because of navigation properties and such GroupBy query is a sign that something wrong with joins and query duplicates result.</p>

