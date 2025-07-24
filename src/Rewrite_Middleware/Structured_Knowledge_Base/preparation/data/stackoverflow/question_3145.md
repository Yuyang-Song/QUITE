# Linq Error: Average could not be translated
[Link to question](https://stackoverflow.com/questions/68649355/linq-error-average-could-not-be-translated)
**Creation Date:** 1628071744
**Score:** 0
**Tags:** c#, asp.net, linq
## Question Body
<pre><code>        public List&lt;Stats&gt; subjects = _context.Gradebooks
            .Include(s =&gt; s.Student)
            .Include(s=&gt;s.Subject)
            .Where(s =&gt; s.LessonDate &gt;= startDate &amp;&amp; s.LessonDate &lt;= endDate &amp;&amp; s.Student.GradeId == gradeId &amp;&amp; s.Mark !=&quot;0&quot;)
            .GroupBy(s=&gt;s.Subject.Name)
            .Select(g=&gt; new Stats
            {
                Name = g.Key,
                Avg = g.Average(s=&gt;int.Parse(s.Mark)) //error
                //Avg = g.Average(s =&gt; s.StudentId) //works
            }).ToList();
</code></pre>
<blockquote>
<p>An unhandled exception occurred while processing the request.
InvalidOperationException: The LINQ expression
'GroupByShaperExpression: KeySelector: s.Name,
ElementSelector:EntityShaperExpression: EntityType: Gradebook
ValueBufferExpression: ProjectionBindingExpression:
EmptyProjectionMember IsNullable: False</p>
<p>.Average(s =&gt; int.Parse(s.Mark))' could not be translated. Either
rewrite the query in a form that can be translated, or switch to
client evaluation explicitly by inserting a call to 'AsEnumerable',
'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>I'm building an asp.net website with Entity Framework Core. Can anyone tell me what's wrong in this linq query? I'm getting error about Average function. When I try other stupid value for Average function like StudentId, everything  works. Should I make my nvarchar field in database to int if everything fails?</p>
<p>My entities:<br/>
Gradebook<br/>
Id int<br/>
LessonDate datetime2(7)<br/>
Mark nvarchar(20)<br/>
StudentId int<br/>
SubjectId int<br/>
TeacherId int<br/>
<br/>
Subject<br/>
Id int<br/>
Name nvarchar (50)<br/>
<br/>
Student<br/>
GradeId int<br/>
(other non relevant properties)<br/>
<br/>
Stats class:<br/></p>
<pre><code>    public class Stats
    {
        public string Name;
        public double Avg;
    }


</code></pre>

## Answers
### Answer ID: 68650023
<p>Using Covert.ToInt32() instead of int.Parse() gets rid of the error. Thank you Random12b3 and Svyatoslav Danyliv.</p>

### Answer ID: 68649846
<p>What you are trying to achieve is only possible if you move the ToList() call before the Select call. The reason for this is because you are trying to convert mark from string to an int before it is actually retrieved from the DB. The following code will most probably work:</p>
<pre class="lang-cs prettyprint-override"><code>public List&lt;Stats&gt; subjects = _context.Gradebooks
    .Include(s =&gt; s.Student)
    .Include(s =&gt; s.Subject)
    .Where(s =&gt; s.LessonDate &gt;= startDate &amp;&amp; s.LessonDate &lt;= endDate &amp;&amp; s.Student.GradeId == gradeId &amp;&amp; s.Mark !=&quot;0&quot;)
    .GroupBy(s =&gt; s.Subject.Name)
    .ToList()
    .Select(g =&gt; new Stats
    {
        Name = g.Key,
        Avg = g.Average(s =&gt; int.Parse(s.Mark))
    });
</code></pre>

