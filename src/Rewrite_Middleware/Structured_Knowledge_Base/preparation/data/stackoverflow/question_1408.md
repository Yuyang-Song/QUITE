# How to get DateTime From Database in Solar Date Fromat (Shamsi Date)?
[Link to question](https://stackoverflow.com/questions/75199855/how-to-get-datetime-from-database-in-solar-date-fromat-shamsi-date)
**Creation Date:** 1674385217
**Score:** 0
**Tags:** c#, entity-framework-core, desktop-application, datetime-format
## Question Body
<p>I am trying to get DataTime from database in Persian Date Fromat,
For this task i made an extinsion method,
and my App Culture is FA-fa, So the DateTime.Now returning Persian Date.</p>
<p>Here is cultureInfo</p>
<pre class="lang-cs prettyprint-override"><code>System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo(&quot;fa-AF&quot;);
System.Threading.Thread.CurrentThread.CurrentUICulture = new System.Globalization.CultureInfo(&quot;fa-AF&quot;);
</code></pre>
<p>Here is My Code in ViewModel Which makes error:</p>
<pre class="lang-cs prettyprint-override"><code>long mntRevenue = (long)db.StudentFees
   .Where(f =&gt; DateConverter.ToPersianDate(f.Date).Month == DateTime.Now.Month).Sum(s =&gt; s.Pay);
</code></pre>
<p>Error is:</p>
<blockquote>
<p>System.InvalidOperationException: 'The LINQ expression 'DbSet()
.Where(s =&gt; (DateTime?)s.Date
.ToPersianDate().Month == DateTime.Now.Month)' could not be translated. Additional information: Translation of method 'SchoolViewModel.ViewModels.DateConverter.ToPersianDate' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information.
Translation of method 'SchoolViewModel.ViewModels.DateConverter.ToPersianDate' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.'</p>
</blockquote>
<p>My Extinsion Method is:</p>
<pre class="lang-cs prettyprint-override"><code>public static class DateConverter
{
    #region Static Methods
    public static DateTime ToPersianDate(this DateTime? dt)
    {
        try
        {
            DateTime dateTime = dt ?? DateTime.Now;
            PersianCalendar persianCalendar = new PersianCalendar();
            string year = persianCalendar.GetYear(dateTime).ToString();
            string month = persianCalendar.GetMonth(dateTime).ToString()
                            .PadLeft(2, '0');
            string day = persianCalendar.GetDayOfMonth(dateTime).ToString()
                            .PadLeft(2, '0');
            string hour = dateTime.Hour.ToString().PadLeft(2, '0');
            string minute = dateTime.Minute.ToString().PadLeft(2, '0');
            string second = dateTime.Second.ToString().PadLeft(2, '0');
            return DateTime.Parse(String.Format(&quot;{0}/{1}/{2} {3}:{4}:{5}&quot;, year, month, day, hour, minute, second));

        }
        catch { return DateTime.Now; }
    }
    #endregion
}
</code></pre>
<p>I want to get date from database and compare it with Current Month and give the compare result to linq expression. The DateTime should be in the Persian Format (Shamsi Date).</p>

## Answers
### Answer ID: 75203725
<p>Thanks for all who leaves comments, Specially @lets do it.
I found the solution,
I just Remove the ToPersianDate Extinsion Method and Add DateAndPay class,</p>
<p>DateAndPay Class:</p>
<pre><code>  public class DateAndPay
    {
        public DateTime Date { get; set; }
        public int Pay { get; set; }
    }
</code></pre>
<p>Here it is:</p>
<pre><code>PersianCalendar persianCalendar = new PersianCalendar();
int month = persianCalendar.GetMonth(DateTime.Now); 

using AppDbContext db = new();
List&lt;DateAndPay&gt; studentFee = await db.StudentFees.Select(f =&gt; new DateAndPay { Date= f.Date,Pay= f.Pay }).ToListAsync();

long mntRevenue = (long)studentFee.Where(f =&gt; persianCalendar.GetMonth(f.Date) == month).Sum(f=&gt; f.Pay);
</code></pre>

