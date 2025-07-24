# The LINQ Expression &#39;DbSet&lt;&gt; Could not be translated method &#39;System.DateTime.ToString&#39; failed, After Migrated from ASP.NET Core 2.1 to .NET6
[Link to question](https://stackoverflow.com/questions/74687301/the-linq-expression-dbset-could-not-be-translated-method-system-datetime-tos)
**Creation Date:** 1670239035
**Score:** 0
**Tags:** c#, linq, .net-6.0, asp.net-core-2.1
## Question Body
<p>I have migrated my project ASP.NET Core 2.1 to .NET6, but some of my LINQ Query do not work properly and give the below error:</p>
<blockquote>
<p>System.InvalidOperationException
Message=The LINQ expression 'DbSet()
.Where(p =&gt; p.PaymentDate.ToString(&quot;MMM-yyyy&quot;).Equals(__ToString_0) &amp;&amp; p.PaymentType == &quot;Treatment Fee&quot;)'
could not be translated. Additional information: Translation of method 'System.DateTime.ToString' failed.
If this method can be mapped to your custom function,
Either rewrite the query in a form that can be translated,
or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>Here is my Home Controller Code in ASP.NET Core 2.1 which returns data from Database As a Monthly and Daily report and displays them in a Line chart and ViewBag. This Code is working fine with asp.net core 2.1, but after I migrated to .NET6 it gives an error for each line of LINQ Query Code that I used Date String Formatting
for Example: <code>a.RegisterDate.Value.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;)</code></p>
<p>Here Is my Home Controller code in ASP.NET Core 2.1  That Need to be modified in .NET6 LINQ Query Format, please help me to modify all this code from asp.net core 2.1 to .NET6 LINQ Query, Thank You.</p>
<pre><code>public class HomeController : BaseController
{
    private readonly IMvcControllerDiscovery _mvcControllerDiscovery;
    private readonly IWebHostEnvironment _hostingEnvironment;
    public HomeController(HoshmandDBContext context, IWebHostEnvironment hostingEnvironment, IMvcControllerDiscovery mvcControllerDiscovery) : base(context)
    {
        _hostingEnvironment = hostingEnvironment;
        _mvcControllerDiscovery = mvcControllerDiscovery;
    }
    public IActionResult Index(DateTime? date = null)
    {
        date = date ?? GetLocalDateTime();
        ViewBag.date = date;
        // MonthlyTransectionList(date);
        ViewBag.CompletedPatients = _context.PatientTbs.Where(a =&gt; a.PatientStatus == &quot;Completed&quot; &amp;&amp; !a.IsDeleted &amp;&amp; a.RegisterDate.Value.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Count();

        string[] monthName = { &quot;Jan&quot;, &quot;Feb&quot;, &quot;Mar&quot;, &quot;Apr&quot;, &quot;May&quot;, &quot;Jun&quot;, &quot;Jul&quot;, &quot;Aug&quot;, &quot;Sep&quot;, &quot;Oct&quot;, &quot;Nov&quot;, &quot;Dec&quot; };
        // patient chart registration
        ViewBag.PatientRegistrationStatisticsInCurrentYear = GetNumberOfPatientsPerMonthInCurrentYear(monthName);

        // transaction chart
        List&lt;IncomeAndOutcome&gt; incomeAndOutcomes = new List&lt;IncomeAndOutcome&gt;();
        var IncomePerMonthInCurrentYear = GetIncomePerMonthInCurrentYear(monthName);
        var OutcomePerMonthInCurrentYear = GetOutcomePerMonthInCurrentYear(monthName);
        foreach (var item in IncomePerMonthInCurrentYear)
        {
            incomeAndOutcomes.Add(new IncomeAndOutcome
            {
                month = item.Key,
                Income = item.Value,
                Outcome = OutcomePerMonthInCurrentYear.FirstOrDefault(a =&gt; a.Key == item.Key).Value
            });
        }
        ViewBag.IncomeAndOutcomeStatisticsInCurrentYear = incomeAndOutcomes;
        var _todayAppointments = _context.AppointmentTbs
            .Where(a =&gt; !a.IsDeleted &amp;&amp; a.AppointmentDate.Value.ToString(&quot;MMM-yyyy&quot;) == date.Value.ToString(&quot;MMM-yyyy&quot;))
            .GroupBy(a =&gt; a.SesstionGroup);

        List&lt;TodayAppointment&gt; todayAppointments = new List&lt;TodayAppointment&gt;();
        if (_todayAppointments.Any(a =&gt; a.FirstOrDefault().AppointmentStatus == 4))
        {
            todayAppointments.Add(new TodayAppointment
            {
                status = &quot;Pending&quot;,
                count = _todayAppointments.Where(a =&gt; a.FirstOrDefault().AppointmentStatus == 4).Count()
            });
        }
        else
        {
            todayAppointments.Add(new TodayAppointment
            {
                status = &quot;Pending&quot;,
                count = 0
            });
        }
        if (_todayAppointments.Any(a =&gt; a.FirstOrDefault().AppointmentStatus == 1))
        {
            todayAppointments.Add(new TodayAppointment
            {
                status = &quot;Completed&quot;,
                count = _todayAppointments.Where(a =&gt; a.FirstOrDefault().AppointmentStatus == 1).Count()
            });
        }
        else
        {
            todayAppointments.Add(new TodayAppointment
            {
                status = &quot;Completed&quot;,
                count = 0
            });
        }
        if (_todayAppointments.Any(a =&gt; a.FirstOrDefault().AppointmentStatus == 3))
        {
            todayAppointments.Add(new TodayAppointment
            {
                status = &quot;Canceled&quot;,
                count = _todayAppointments.Where(a =&gt; a.FirstOrDefault().AppointmentStatus == 3).Count()
            });
        }
        else
        {
            todayAppointments.Add(new TodayAppointment
            {
                status = &quot;Canceled&quot;,
                count = 0
            });
        }
        ViewBag.TodayAppointments = todayAppointments;

        return View();
    }
    private IActionResult MonthlyTransectionList(DateTime? date = null)
    {
        ViewBag.MonthlyPatientIcomeTreatmentFee = _context.PatientPaymentHistories.Where(a =&gt; a.PaymentDate.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;)) &amp;&amp; a.PaymentType == &quot;Treatment Fee&quot;).Sum(a =&gt; a.PaidAmount);
        ViewBag.MonthlyPatientIcomeVisitFee = _context.PatientPaymentHistories.Where(a =&gt; a.PaymentDate.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;)) &amp;&amp; a.PaymentType == &quot;Checkup Fee&quot;).Sum(a =&gt; a.PaidAmount);
        ViewBag.MonthlyExpenseOut = _context.Expenses.Where(a =&gt; !a.IsDelete &amp;&amp; a.ExpenseDate.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Sum(a =&gt; a.ExpenseAmount);
        ViewBag.MonthlyStockOut = _context.StockTransectionTbs.Where(a =&gt; a.TransectionDate.Value.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Sum(a =&gt; a.TransectionAmount);
        ViewBag.MonthlyPatientRefunded = _context.PatientPaymentHistories.Where(a =&gt; a.PaymentDate.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;)) &amp;&amp; a.PaymentType == &quot;Refund&quot;).Sum(a =&gt; a.PaidAmount);
        ViewBag.MonthlyLabOut = _context.labsPayments.Where(a =&gt; a.PaymentDate.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Sum(a =&gt; a.TotalPaid);
        ViewBag.MonthlySalaryOut = _context.EmployeeTransectionTbs.Where(a =&gt; !a.IsDeleted &amp;&amp; a.TransectionDate.Value.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Sum(a =&gt; a.TransectionAmount);
        ViewBag.MonthlyDebitedTransectionOut = _context.OtherTransectionTbs.Where(a =&gt; !a.IsDeleted &amp;&amp; a.TransectionType == &quot;Debited&quot; &amp;&amp; a.TransectionDate.Value.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Sum(a =&gt; a.TransectionAmount);
        ViewBag.MonthlyCreditedTransectionOut = _context.OtherTransectionTbs.Where(a =&gt; !a.IsDeleted &amp;&amp; a.TransectionType == &quot;Credited&quot; &amp;&amp; a.TransectionDate.Value.Date.ToString(&quot;MMM-yyyy&quot;).Equals(date.Value.ToString(&quot;MMM-yyyy&quot;))).Sum(a =&gt; a.TransectionAmount);
        return View();
    }
    private PatientRegistrationStatisticsInCurrentYear GetNumberOfPatientsPerMonthInCurrentYear(string[] monthName)
    {
        var PatientsInCurrentYear = _context.PatientTbs.Where(a =&gt; !a.IsDeleted &amp;&amp; a.IsActive.Value &amp;&amp; a.RegisterDate.Value &gt;= new DateTime(GetLocalDateTime().Year, 1, 1).Date);
        PatientRegistrationStatisticsInCurrentYear patientRegistrationStatisticsInCurrentYear = new PatientRegistrationStatisticsInCurrentYear
        {
            totalPatient = PatientsInCurrentYear.Count(),
            year = new DateTime(GetLocalDateTime().Year, 1, 1).Year,
            PatientPerMonth = new Dictionary&lt;string, int&gt;()
        };
        foreach (var item in monthName)
        {
            patientRegistrationStatisticsInCurrentYear.PatientPerMonth[item] = PatientsInCurrentYear.Where(a =&gt; a.RegisterDate.Value.ToString(&quot;MMM&quot;) == item).Count();
        }
        return patientRegistrationStatisticsInCurrentYear;
    }
    private Dictionary&lt;string, decimal&gt; GetIncomePerMonthInCurrentYear(string[] monthName)
    {
        Dictionary&lt;string, decimal&gt; Income = new Dictionary&lt;string, decimal&gt;();
        foreach (var month in monthName)
        {
            var income = _context.PatientPaymentHistories
                .Where(a =&gt; a.PaymentDate.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; !a.IsDeleted &amp;&amp;
                 !string.Equals(a.PaymentType, &quot;Refund&quot;, StringComparison.CurrentCultureIgnoreCase)
                 &amp;&amp; a.PaymentDate.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.PaidAmount)
                + _context.OtherTransectionTbs.Where(a =&gt; a.TransectionDate.Value.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1)
                 &amp;&amp; !a.IsDeleted &amp;&amp; string.Equals(a.TransectionType, &quot;Credited&quot;, StringComparison.CurrentCultureIgnoreCase)
                 &amp;&amp; a.TransectionDate.Value.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.TransectionAmount);
            Income.Add(month, income.Value);
        }
        return Income;
    }
    private Dictionary&lt;string, decimal&gt; GetOutcomePerMonthInCurrentYear(string[] monthName)
    {
        Dictionary&lt;string, decimal&gt; outcome = new Dictionary&lt;string, decimal&gt;();
        foreach (var month in monthName)
        {
            var og = _context.Expenses.Where(a =&gt; !a.IsDelete &amp;&amp; a.ExpenseDate.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; a.ExpenseDate.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.ExpenseAmount)
             + _context.StockTransectionTbs.Where(a =&gt; a.TransectionDate.Value.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; a.TransectionDate.Value.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.TransectionAmount)
             + _context.PatientPaymentHistories.Where(a =&gt; a.PaymentDate.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; a.PaymentDate.ToString(&quot;MMM&quot;) == month &amp;&amp; a.PaymentType == &quot;Refund&quot;).Sum(a =&gt; a.PaidAmount)
             + _context.labsPayments.Where(a =&gt; a.PaymentDate.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; a.PaymentDate.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.TotalPaid)
             + _context.EmployeeTransectionTbs.Where(a =&gt; !a.IsDeleted &amp;&amp; a.TransectionDate.Value.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; a.TransectionDate.Value.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.TransectionAmount)
             + _context.OtherTransectionTbs.Where(a =&gt; !a.IsDeleted &amp;&amp; a.TransectionType == &quot;Debited&quot; &amp;&amp; a.TransectionDate.Value.Date &gt;= new DateTime(GetLocalDateTime().Year, 1, 1) &amp;&amp; a.TransectionDate.Value.ToString(&quot;MMM&quot;) == month).Sum(a =&gt; a.TransectionAmount);
            outcome.Add(month, og.Value);
        }
        return outcome;
    }
}
public class PatientRegistrationStatisticsInCurrentYear
{
    public int year { get; set; }
    public int totalPatient { get; set; }
    public Dictionary&lt;string, int&gt; PatientPerMonth { get; set; }
}

public class IncomeAndOutcome
{
    public string month { get; set; }
    public decimal Income { get; set; }
    public decimal Outcome { get; set; }
}
public class TodayAppointment
{
    public string status { get; set; }
    public int count { get; set; }
}
</code></pre>

## Answers
### Answer ID: 74689716
<p>Your approach to filter by month is not translatable by EF Core. I would suggest to introduce extension method which will generate correct filter by month. And another benefit, if your tables has indexes on date - they will be used by Database server.</p>
<p>Sample of usage:</p>
<pre class="lang-cs prettyprint-override"><code>ViewBag.CompletedPatients = _context.PatientTbs.Where(a =&gt; a.PatientStatus == &quot;Completed&quot; &amp;&amp; !a.IsDeleted)
   .FilterByMonth(date.Value, a =&gt; a.RegisterDate).Count();
ViewBag.CheckupPatients = _context.PatientTbs.Where(a =&gt; a.PatientStatus == &quot;Checkup&quot; &amp;&amp; !a.IsDeleted)
   .FilterByMonth(date.Value, a =&gt; a.RegisterDate).Count();
</code></pre>
<p>Extension implemenation, it contains <code>FilterByDay</code>, <code>FilterByMonth</code>, <code>FilterByYear</code> and generic <code>FilterByDateRange</code>:</p>
<pre class="lang-cs prettyprint-override"><code>public static class QueryableExtensions
{
    public static IQueryable&lt;T&gt; FilterByDay&lt;T&gt;(this IQueryable&lt;T&gt; query, DateTime date, Expression&lt;Func&lt;T, DateTime?&gt;&gt; dateField)
    {
        var start = date.Date;
        var end   = start.AddDays(1);

        return query.FilterByDateRange(start, end, dateField);
    }

    public static IQueryable&lt;T&gt; FilterByMonth&lt;T&gt;(this IQueryable&lt;T&gt; query, DateTime date, Expression&lt;Func&lt;T, DateTime?&gt;&gt; dateField)
    {
        var start = new DateTime(date.Year, date.Month, 1);
        var end   = start.AddMonths(1);

        return query.FilterByDateRange(start, end, dateField);
    }

    public static IQueryable&lt;T&gt; FilterByYear&lt;T&gt;(this IQueryable&lt;T&gt; query, DateTime date, Expression&lt;Func&lt;T, DateTime?&gt;&gt; dateField)
    {
        var start = new DateTime(date.Year, 1, 1);
        var end   = start.AddYears(1);

        return query.FilterByDateRange(start, end, dateField);
    }

    public static IQueryable&lt;T&gt; FilterByDateRange&lt;T&gt;(this IQueryable&lt;T&gt; query, DateTime startInclusive,
        DateTime endExclusive, Expression&lt;Func&lt;T, DateTime?&gt;&gt; dateField)
    {
        var entityParam = dateField.Parameters[0];
        var fieldExpr   = dateField.Body;

        // e.DateField &gt;= startInclusive &amp;&amp; e.DateField &lt; endExclusive 
        var filterExpression = Expression.AndAlso(
            Expression.GreaterThanOrEqual(fieldExpr, Expression.Constant(startInclusive, fieldExpr.Type)),
            Expression.LessThan(fieldExpr, Expression.Constant(endExclusive, fieldExpr.Type)));

        // e =&gt; e.DateField &gt;= startInclusive &amp;&amp; e.DateField &lt; endExclusive 
        var filterLambda = Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(filterExpression, entityParam);
        return query.Where(filterLambda);
    }
}
</code></pre>
<p>Also I have noticed that you have used EF Core extremely ineffective. Access to the same table can be simplified:</p>
<pre class="lang-cs prettyprint-override"><code>var statistic = _context.PatientTbs
    .Where(a =&gt; !a.IsDeleted)
    .FilterByMonth(date.Value, a =&gt; a.RegisterDate)
    .GroupBy(a =&gt; 1) // by constant
    .Select(g =&gt; new
    {
        Completed = g.Count(x =&gt; x.PatientStatus == &quot;Completed&quot;),
        Checkup = g.Count(x =&gt; x.PatientStatus == &quot;Checkup&quot;),
        Working = g.Count(x =&gt; x.PatientStatus == &quot;Working&quot;),
        Closed = g.Count(x =&gt; x.PatientStatus == &quot;Closed&quot;)
    })
    .FirstOrDefault();

ViewBag.CompletedPatients = statistic?.Completed ?? 0;
ViewBag.CheckupPatients = statistic?.Checkup ?? 0;
ViewBag.WorkingPatients = statistic?.Working ?? 0;
ViewBag.ClosedPatients = statistic?.Closed ?? 0;
</code></pre>
<p>Also for month statistic query can be executed once:</p>
<pre class="lang-cs prettyprint-override"><code>string[] monthName = { &quot;Jan&quot;, &quot;Feb&quot;, &quot;Mar&quot;, &quot;Apr&quot;, &quot;May&quot;, &quot;Jun&quot;, &quot;Jul&quot;, &quot;Aug&quot;, &quot;Sep&quot;, &quot;Oct&quot;, &quot;Nov&quot;, &quot;Dec&quot; }; 

var patientsInCurrentYear = _context.PatientTbs.FilterByYear(date.Value, a =&gt; a.RegisterDate);

var statisticByMonth = patientsInCurrentYear
    .GroupBy(a =&gt; a.RegisterDate.Value.Month)
    .Select(g =&gt; new 
    {
        Month = g.Key,
        Count = g.Count();
    })
    .ToDictionary(x =&gt; x.Month);

for (var i = 0; i &lt; monthName.Length; i++) 
{ 
    item = monthName[i];
    var count = 0;
    if (statisticByMonth.TryGetValue(i + 1, out var statistic))
        count = statistic.Count;

    patientRegistrationStatisticsInCurrentYear.PatientPerMonth[item] = count; 
}
</code></pre>

### Answer ID: 74687646
<p>EF Core 2 had automatic silent client side evaluation enabled, which was disabled for later versions - see the corresponding <a href="https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client" rel="nofollow noreferrer">breaking change</a>:</p>
<blockquote>
<p><strong>Old behavior</strong></p>
<p>Before 3.0, when EF Core couldn't convert an expression that was part of a query to either SQL or a parameter, it automatically evaluated the expression on the client. By default, client evaluation of potentially expensive expressions only triggered a warning.</p>
</blockquote>
<blockquote>
<p><strong>New behavior</strong></p>
<p>Starting with 3.0, EF Core only allows expressions in the top-level projection (the last Select() call in the query) to be evaluated on the client. When expressions in any other part of the query can't be converted to either SQL or a parameter, an exception is thrown.</p>
</blockquote>
<p>As a quick fix  you <a href="https://learn.microsoft.com/en-us/ef/core/querying/client-eval#explicit-client-evaluation" rel="nofollow noreferrer">explicitly evaluate</a> on client side (via <code>AsEnumerable</code> or <code>ToList</code> and their async counterparts), but in general I would argue that you should consider rewriting queries so they are translated into SQL (based on your database you should look into supported function mappings, like <a href="https://learn.microsoft.com/en-us/ef/core/providers/sql-server/functions#date-and-time-functions" rel="nofollow noreferrer">here for SQL Server</a>, based on exception message you should look into using correct datetime functions, which compare dateparts).</p>

