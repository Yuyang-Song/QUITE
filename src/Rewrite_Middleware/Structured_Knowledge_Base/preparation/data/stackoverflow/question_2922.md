# Using multiple DbContext getting error Cannot use multiple DbContext instances within a single query execution
[Link to question](https://stackoverflow.com/questions/58530568/using-multiple-dbcontext-getting-error-cannot-use-multiple-dbcontext-instances-w)
**Creation Date:** 1571862623
**Score:** 6
**Tags:** c#, asp.net-core-mvc, entity-framework-core
## Question Body
<p>I started a new MVC app using .NET Core 3.  I have three DbContext files that use three different databases: ComplaintDbContext for my main application, IdentityCoreDbContext for Identity users, and EmployeeDbContext for my employee database.  </p>

<p>In my app I have a repository class called ComplaintRepository and the constructor looks like this:</p>

<pre><code>public ComplaintRepository(ComplaintDbContext context, 
        EmployeeDbContext employeeContext)
    {
        _context = context;
        _employeeContext = employeeContext;
    }
</code></pre>

<p>In my ComplaintController I need to get data from both databases.  I can get my data from my Complaint database, but once I call my Action that gets data from my Employee database I get the error:</p>

<p>Cannot use multiple DbContext instances within a single query execution. Ensure the query uses a single context instance.</p>

<p>I tried something like this:</p>

<pre><code>public class FrameworkContext : DbContext
{
    public DbSet&lt;Customer&gt; Customers { get; set; }
}

public class ExtendedContext : FrameworkContext
{
    public DbSet&lt;Order&gt; Orders { get; set; }
}
</code></pre>

<p>I cannot get it working.  Any help would be appreciated.  Thanks!</p>

<p>Edit:</p>

<p>I started a new repository called EmployeeRepository to separate concerns.  Here is my Action that is giving me problems:</p>

<pre><code>    public IEnumerable&lt;ApplicationUser&gt; GetWorkerList()
    {
        var employees = _employeeRepository.GetEmployeesByUnit(22);

        //Get ApplicationUsers where user exists in Employees list
        IEnumerable&lt;ApplicationUser&gt; userList = _userManager.Users
            .Where(emp =&gt; employees.Any(e =&gt; emp.EmployeeID == e.EmployeeId)).OrderBy(e =&gt; e.LastName);

        return userList;            
    }
</code></pre>

<p>My Employee database and my Identity database both share a column called EmployeeId.</p>

<p>When I tried changing it to use ToList() I started getting a different error:</p>

<p>InvalidOperationException: The LINQ expression 'Where( source: DbSet, predicate: (a) => Any( source: (Unhandled parameter: __employees_0), predicate: (e) => a.EmployeeID == e.EmployeeId))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>

<p>Edit:</p>

<p>I used Tao Zhou's recommendation of using ToList() and I was able to get it working.  I replaced IEnumerable in my repository to use this:</p>

<pre><code>    public List&lt;TblEmployee&gt; GetEmployeesByUnit(int unitId)
    {
        var emp = _context.TblEmployee.Where(e =&gt; e.UnitId == unitId &amp;&amp;
                e.TermDate == null)
            .OrderBy(e =&gt; e.LastName).ToList();

        return emp;
    }
</code></pre>

<p>In my controller I basically did the same and I now have this:</p>

<pre><code>    public List&lt;ApplicationUser&gt; GetWorkerList()
    {
        var employees = _employeeRepository.GetEmployeesByUnit(22);

        List&lt;ApplicationUser&gt; userList = new List&lt;ApplicationUser&gt;();

        //Get ApplicationUsers where user exists in Employees list
        foreach (TblEmployee emp in employees)
        {
            ApplicationUser user = _userManager.Users
                .Where(e =&gt; e.EmployeeID == emp.EmployeeId).FirstOrDefault();

            userList.Add(user);
        }

        return userList;            
    }
</code></pre>

<p>I would like to use LINQ instead of the foreach loop.</p>

## Answers
### Answer ID: 75092391
<p>Since you are only using the <code>EmployeeId</code> in the <code>Any</code> method comparison, you could use <code>Contains</code></p>
<pre class="lang-cs prettyprint-override"><code>var employees = _employeeRepository.GetEmployeesByUnit(22);
var employeeIds = employees.Select(x =&gt; x.EmployeeId).ToHashSet();

//Get ApplicationUsers where user exists in Employees list
IEnumerable&lt;ApplicationUser&gt; userList = _userManager.Users
            .Where(emp =&gt; employeeIds.Contains(emp.EmployeeID)).OrderBy(e =&gt; e.LastName);

return userList;
// or return userList.ToList();
</code></pre>

### Answer ID: 72317884
<p>I have also faced the same problem, from what I could tell, you cannot use different DbContext for same query. Just make sure you used same DbContext object for same query.</p>

