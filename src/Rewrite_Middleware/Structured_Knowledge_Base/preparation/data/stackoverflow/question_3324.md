# GroupBy after SelectMany in EF Core
[Link to question](https://stackoverflow.com/questions/76385240/groupby-after-selectmany-in-ef-core)
**Creation Date:** 1685648843
**Score:** 1
**Tags:** c#, entity-framework-core
## Question Body
<p>Consider the following query, which lists the Schools, along with monthly statistics for the students that started that month at the school.</p>
<pre><code> _dbContext.Schools
  .Select(p =&gt; new MySchoolView
  {
    School= p,
    MonthlyStatistics = p.Teacher
      .SelectMany(d =&gt; d.Students)
      .GroupBy(d =&gt; new { d.StartDate.Month, d.StartDate.Year })
      .Select(g =&gt; new MonthlyStatisticsView
        {
          Year = g.Key.Year,
          Month = g.Key.Month,
          Count = g.Count(),
          Dollars = g.Sum(d =&gt; d.Tuition)
        }).ToList()
  })
</code></pre>
<p>EF Core chokes on this query:</p>
<blockquote>
<p>System.InvalidOperationException: Unable to translate a collection subquery in a projection since either parent or the subquery doesn't project necessary information required to uniquely identify it and correctly generate results on the client side. This can happen when trying to correlate on keyless entity type. This can also happen for some cases of projection before 'Distinct' or some shapes of grouping key in case of 'GroupBy'. These should either contain all key properties of the entity that the operation is applied on, or only contain simple property access expressions.</p>
</blockquote>
<p>However, it is able to handle a similar query, if we calculate the monthly statistics based on the Teacher table, instead of the student table:</p>
<pre><code> _dbContext.Schools
  .Select(p =&gt; new MySchoolView
  {
    School= p,
    MonthlyStatistics = p.Teacher
      .GroupBy(d =&gt; new { d.EmploymentDate.Month, d.EmploymentDate.Year })
      .Select(g =&gt; new MonthlyStatisticsView
        {
          Year = g.Key.Year,
          Month = g.Key.Month,
          Count = g.Count(),
          Dollars = g.Sum(d =&gt; d.Salary)
        }).ToList()
  })
</code></pre>
<p>I believe that this is due to EF Core not being able to handle the <code>.SelectMany</code> before the <code>.GroupBy</code>.  Is there a way that EF Core can handle a query like this, e.g. by directly navigating from the School to the Student or otherwise rewriting the SelectMany using other operations?</p>
<p>I already know about the following possibilities, which are not viable solutions for me:</p>
<ol>
<li>Using client side evaluation instead</li>
<li>Breaking the query into N queries</li>
<li>Restructuring the database</li>
</ol>

## Answers
### Answer ID: 76388310
<p>I would suggest another approach which is still performant but translatable. Preparing grouped data and then post process on the client side.</p>
<pre class="lang-cs prettyprint-override"><code>var query = 
    from s in _dbContext.Schools
    from t in s.Teacher
    from st in t.Students
    group st by new { s.Id, st.StartDate.Month, st.StartDate.Year } into g
    select new 
    {
        Id = g.Key.Id,
        Year = g.Key.Year,
        Month = g.Key.Month,
        Count = g.Count(),
        Dollars = g.Sum(d =&gt; d.Tuition)
    } into d
    join s in _dbContext.Schools on d.Id equals s.Id
    select new 
    {
        School = s,
        Details = d
    };

var rawData = query.ToList();

var result = rawData
    .GroupBy(r =&gt; r.School.Id)
    .Select(g =&gt; new MySchoolView
    {
        School = g.First().School,
        MonthlyStatistics = g.Select(s =&gt; new MonthlyStatisticsView
        {
            Year = s.Details.Year,
            Month = s.Details.Month,
            Count = s.Details.Count,
            Dollars = s.Details.Dollars
        }).ToList()
    });
</code></pre>

