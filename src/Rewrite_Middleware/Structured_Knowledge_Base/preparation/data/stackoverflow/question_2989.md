# LINQ Multiple &quot;||&quot; with &quot;&amp;&quot; operator
[Link to question](https://stackoverflow.com/questions/61344718/linq-multiple-with-operator)
**Creation Date:** 1587475635
**Score:** 1
**Tags:** c#, sql-server, entity-framework, linq, asp.net-core-3.1
## Question Body
<p>I have the following Linq query trying to filter a collection of results that meet certain conditions as follows:</p>

<pre><code>public async Task&lt;BillListResponse&gt; GetStudentCurrentBillsAsync(Student student)
    {
        var studentEvents = student.StudentEvents;
        var studentServices = student.StudentServices;
        var studentGroups = student.StudentGroups;

List&lt;Bill&gt; currentBills = await _context.Bills
            .Include(b =&gt; b.Category)
            .Where(b =&gt; ((b.ClassBills.Any(c =&gt; c.StudentClassId == student.ClassId)) || studentGroups.Any(sg =&gt; sg.SpecialGroupId == b.GroupId) || studentServices.Any(ss =&gt; ss.SpecialServiceId == b.ServiceId) || b.CareerPathBills.Any(cpb =&gt; cpb.CareerPathId == student.CareerPathId)) &amp;&amp; b.SessionId == currentSession.Id
                ).ToListAsync();
......
</code></pre>

<p>But I keep getting the following error </p>

<blockquote>
  <p>InvalidOperationException: The LINQ expression 'DbSet
  .Where(b => DbSet
  .Where(c => EF.Property>(b, "Id") != null &amp;&amp; EF.Property>(b, "Id") == EF.Property>(c, "BillId"))
  .Any(c => c.StudentClassId == __student_ClassId_0) || __student_StudentEvents_1
  .Any(se => (Nullable)se.EventId == b.EventId) || __student_StudentGroups_2
  .Any(sg => (Nullable)sg.SpecialGroupId == b.GroupId) || __student_StudentServices_3
  .Any(ss => (Nullable)ss.SpecialServiceId == b.ServiceId) || DbSet
  .Where(c0 => EF.Property>(b, "Id") != null &amp;&amp; EF.Property>(b, "Id") == EF.Property>(c0, "BillId"))
  .Any(c0 => (Nullable)c0.CareerPathId == __student_CareerPathId_4) &amp;&amp; b.SessionId == __currentSession_Id_5)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>

<p>which I have not been able to resolve.
However, I realized that if remove the "||" clauses in the expression, as follows:</p>

<pre><code>List&lt;Bill&gt; currentBills = await _context.Bills
            .Include(b =&gt; b.Category)
            .Where(b =&gt; b.ClassBills.Any(c =&gt; c.StudentClassId == student.ClassId) &amp;&amp; b.SessionId == currentSession.Id
                ).ToListAsync();
</code></pre>

<p>it works but I need more conditions as expressed in the full expression. </p>

<p>I am running on ASP.NET-Core 3.1 on Windows with SQL Server Database.</p>

<p>I seems I am getting something wrong with the "||" operator. </p>

<p>Please guide me to resolve this. I will appreciate.</p>

<p>Thank you</p>

<p><strong>UPDATE</strong></p>

<hr>

<p>The entity relationships are as follows:</p>

<p>The student entity has the following</p>

<pre><code>public virtual ICollection&lt;StudentGroup&gt; StudentGroups { get; set; }
public virtual ICollection&lt;StudentService&gt; StudentServices { get; set; }

public virtual ICollection&lt;StudentEvent&gt; StudentEvents { get; set; }
</code></pre>

<p>And the following DbSets exist too </p>

<pre><code>public DbSet&lt;StudentGroup&gt; StudentGroups { get; set; }
public DbSet&lt;StudentEvent&gt; StudentEvents { get; set; }
public DbSet&lt;SpecialService&gt; Services { get; set; }
</code></pre>

<p>And the many-to-many intermediate tables are as follows</p>

<pre><code>public class StudentEvent
{
    public string StudentId { get; set; }
    public int EventId { get; set; }

    [ForeignKey("StudentId")]
    public Student Student { get; set; }
    [ForeignKey("EventId")]
    public SchoolEvent Event { get; set; }
}

public class StudentService
{
    public int SpecialServiceId { get; set; }
    public virtual SpecialService Service { get; set; }
    public string StudentId { get; set; }
    public virtual Student Student { get; set; }
}

public class StudentGroup
{
    public int SpecialGroupId { get; set; }
    public virtual SpecialGroup SpecialGroup { get; set; }
    public string StudentId { get; set; }
    public virtual Student Student { get; set; }
}
</code></pre>

<hr>

<p>UPDATE</p>

<p>I have modified the query as follows and it seems to be working now.</p>

<pre><code>var studentEvents = student.StudentEvents.ToList();
var studentServices = student.StudentServices.ToList();
var studentGroups = student.StudentGroups.ToList();

List&lt;Bill&gt; bills = await (from b in _context.Bills where b.ClassBills.Any(c =&gt; c.StudentClassId == student.ClassId) || (studentEvents.Any() &amp;&amp; studentEvents.Any(se =&gt; se.EventId == b.EventId)) || (studentGroups.Any() &amp;&amp; studentGroups.Any(sg =&gt; sg.SpecialGroupId == b.GroupId)) || (studentServices.Any() &amp;&amp; studentServices.Any(ss =&gt; ss.SpecialServiceId == b.ServiceId)) || b.CareerPathBills.Any(cpb =&gt; cpb.CareerPathId == student.CareerPathId) select b).ToListAsync();
</code></pre>

<hr>

<p>Another way that seems to work as expected is the following</p>

<pre><code>var studentEvents = student.StudentEvents.ToList();
var studentServices = student.StudentServices.ToList();
var studentGroups = student.StudentGroups.ToList();

var currentBills = _context.Bills
            ?.Include(b =&gt; b.Category)
            ?.Include(b =&gt; b.ClassBills)
            ?.Include(b=&gt;b.CareerPathBills)
            ?.Where(b =&gt; b.SessionId == currentSession.Id);

        if (student.StudentEvents.Any())
        {
            currentBills = currentBills.Where(b =&gt; student.StudentEvents.Any(se =&gt; se.EventId == b.EventId));
        }

        if (student.StudentServices.Any())
        {
            currentBills = currentBills.Where(b =&gt; student.StudentServices.Any(se =&gt; se.SpecialServiceId == b.ServiceId));
        }

        if (student.StudentGroups.Any())
        {
            currentBills = currentBills.Where(b =&gt; student.StudentGroups.Any(se =&gt; se.SpecialGroupId == b.GroupId));
        }

        var currentBillsList = await currentBills.ToListAsync();
</code></pre>

<p>And </p>

<pre><code>currentBillsList
</code></pre>

<p>is the expected result to return </p>

<p>I am not sure whether or not this is the right approach.</p>

## Answers
### Answer ID: 61344939
<p>The reason why it is failing is that the <code>students</code> collection might not be part of SQL query for database tables, i.e. when calling <code>ToList</code> or <code>ToListAsync</code> it is becoming C# entities collection and will not work with LINQ to Entities collections.</p>
<p><strong>Hint</strong>: make sure that your <code>students</code> are collections of <code>IQueryable</code>.</p>
<p>However, as an alternative suggestion here, you can use <code>Join</code> Students and Bills, instead of using filtering in the <code>Where</code> clause.</p>

