# Razor-Pages - Searching by a Date
[Link to question](https://stackoverflow.com/questions/67094978/razor-pages-searching-by-a-date)
**Creation Date:** 1618415297
**Score:** 1
**Tags:** c#, asp.net-core, .net-core, entity-framework-core, razor-pages
## Question Body
<p>I am creating an in-house Razor Pages application which connects to a SQL database using Entity Framework. I have a page with a search form and I want to be able to search for records based on an entered date.</p>
<p>Here is what I have so far:</p>
<pre><code>public async Task OnGetAsync(string searchString)
{
    // provide an IQueryable list of web registrants that can be parsed.
    // IQueryable&lt;Models.WebPestMSTR&gt; webRegistrationIQ = (from a in _context.WebPestMSTR
    //                                                     select a);

    // If the Search string is empty than only show the unprocessed web registration.  Otherwise parse the table for matching records.
    if (!String.IsNullOrEmpty(searchString))
    {
        // There is a search parameter. Parse the query for matching records.
        // Parse the search parameter to see if it is a date (bool isCertNo = BigInteger.TryParse(searchString, out numOut);)
        if (DateTime.TryParse(searchString, out DateTime dateTime))
        {
            WebPestMSTR = await _context.WebPestMSTR
                    .Where(a =&gt; a.DateAdded.ToShortDateString() == dateTime.ToShortDateString())
                    .Include(w =&gt; w.Course)
                    .Include(w =&gt; w.MiraInfo)
                    .ToListAsync();

            // webRegistrationIQ = webRegistrationIQ.Where(a =&gt; a.DateAdded.ToShortDateString() == dateTime.ToShortDateString());
        }
        else
        {
            IQueryable&lt;Models.WebPestMSTR&gt; webRegistrationIQ = (from a in _context.WebPestMSTR
                                                                select a);

            webRegistrationIQ = webRegistrationIQ.Where(a =&gt; a.LastName.Contains(searchString));

            WebPestMSTR = await webRegistrationIQ
                    .Include(w =&gt; w.Course)
                    .Include(w =&gt; w.MiraInfo)
                    .ToListAsync();
        }
    }
    else
    {
        // No search parameters so only show unprocessed records.
        WebPestMSTR = await _context.WebPestMSTR
            .Include(w =&gt; w.Course)
            .Include(w =&gt; w.MiraInfo)
            .Where(w =&gt; w.IsProcessed == false)
            .ToListAsync();
    }
}
</code></pre>
<p>I am able to successfully parse the searchString if it is a date, but errors out on the where. The error is:</p>
<blockquote>
<p>InvalidOperationException: The LINQ expression 'DbSet
.Where(w =&gt; w.DateAdded.ToShortDateString() == __ToShortDateString_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>
<p>The search works when searching by a Last Name just fine.</p>
<p>Any ideas?</p>

## Answers
### Answer ID: 67096044
<p>If you need  to compare only  dates (without time) and you using ms sql server you can try</p>
<pre><code> WebPestMSTR = await _context.WebPestMSTR
           .Where(a =&gt; EF.Functions.DateDiffDay(a.DateAdded, dateTime)==0)
           .Include(w =&gt; w.Course)
            .Include(w =&gt; w.MiraInfo)
            .ToListAsync();
</code></pre>
<p>if you need more presize comparison you can use EF.Functions.DateDiffMinute or EF.Functions.DateDiffSecond instead. This functions are included in a Microsoft.EntityFrameworkCore.SqlServer nuget package.</p>

