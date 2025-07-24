# aggregation count in linq query returns null
[Link to question](https://stackoverflow.com/questions/63117185/aggregation-count-in-linq-query-returns-null)
**Creation Date:** 1595859138
**Score:** 0
**Tags:** c#, linq, asp.net-core
## Question Body
<p>I'm implementing asp.net core 3.1 project. In my controller I have a linq query like the following and without defining inprocessapicount and pendingcount which claculates counts of related amounts, it works fine but after adding them to applicants query in select part, applicants returns null and the error is: .Count(a =&gt; a.requestStatus == &quot;bb&quot;) could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync() . I appreciate if anyone suggests me a solution.</p>
<pre><code> var applicants = (from t1 in _context.VwDesk
                              
                              let tg = new {
     
                                   itemID = t1.ItemId,
                                   applicantID = t1.ApplicantId,
                                   applicantName = t1.ApplicantName,
                                 
                                   gateName =t1.GateName,

                                   requestStatus = t1.LastReqStatus
                               }
                               group tg by new { tg.requestStatus,tg.itemID ,tg.applicantID, tg.applicantName} into ApiAppGp
                               select new
                               {
                                   applicantName = ApiAppGp.Key.applicantName,

                                   itemname = ApiAppGp.Key.itemID,
 
                                   itemcount =ApiAppGp.Count(),

                                   inprocessapicount = ApiAppGp.Where(a =&gt; a.requestStatus == &quot;bb&quot;).Count(),
                                   pendingapicount = ApiAppGp.Where(a =&gt; a.requestStatus == &quot;aa&quot;).Count()


                               }).ToList();
</code></pre>
<p>What I want is: There are some applicants in Database and each applicant may have multiple or zero requests. (Each applicant orders multiple or zero itemID) each one of those applicants needs to get some item (itemID) and each of those item has requeststatus ==&quot;aa&quot; or requeststatus ==&quot;bb&quot; or none of them which the status in that case is &quot;general&quot;. Now I want to understand, how many each applicant's itemID has requeststatus==&quot;aa&quot; and how many each applicant's itemID has requeststatus==&quot;bb&quot; according to all ItemId they have ordered.</p>

## Answers
### Answer ID: 63119661
<p>Try combining <code>Where</code> and <code>Count</code> methods, because <code>Count</code> has also Lambda version:</p>
<pre class="lang-cs prettyprint-override"><code>inprocessapicount = ApiAppGp.Count(a =&gt; a.requestStatus == &quot;bb&quot;),
pendingapicount = ApiAppGp.Count(a =&gt; a.requestStatus == &quot;aa&quot;)
</code></pre>
<p>Otherwise, I don't see any problem in your code, unless the <code>GroupBy</code> statement actually can find any element to Group(empty collection).<br />
Try also running the same result without the initial <code>select</code> statement(before <code>group by</code>).</p>

