# LINQ Exclude records using 2 different database contexts
[Link to question](https://stackoverflow.com/questions/64009733/linq-exclude-records-using-2-different-database-contexts)
**Creation Date:** 1600777697
**Score:** 1
**Tags:** c#, .net, asp.net-core, entity-framework-core
## Question Body
<p>I had some code that was working fine when looking at a single database context but when I split the models into 2 different contexts the query now fails.</p>
<p>So I get that I can't use 2 different contexts in a single query so I tried extracting one set into a list and then excluded entries in the list from the query</p>
<pre><code>var exclude = _traceContext.TraceDetails.Where(w =&gt; w.Trace.CreatedBy == userName).ToList();

var data = from s in _billingContext.log
                   where s.FormattedMessage.Contains(userName)
                   where !(
                           from l in exclude
                           select l.LogTime
                           ).Contains(s.Timestamp)
                   select s;
</code></pre>
<p>This gets a conversion error:</p>
<p><strong>SqlException: Conversion failed when converting date and/or time from character string.</strong></p>
<p>Both columns are <code>DateTime</code></p>
<p>If I try and generate data as:</p>
<pre><code>var data = _billingContext.log.Where(l =&gt; !exclude.Any(e =&gt; e.LogTime == l.Timestamp)).OrderBy(o =&gt; o.objID);
</code></pre>
<p>I get:</p>
<p><strong>InvalidOperationException: The LINQ expression 'DbSet
.Where(y =&gt; !(__exclude_0
.Any(e =&gt; e.LogTime == y.Timestamp)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</strong></p>
<p>I'm not sure what I'm doing wrong here. What I need is the contents of <code>log</code> where none of the LogTimes are in the Timestamps in <code>exclude</code></p>
<p><strong>Edit After using Contains as the comment from Mong Zhu</strong></p>
<p>So I still got the conversion error when using Contains so tried splitting the operation and making sure I'm comparing 2 of the same types</p>
<pre><code>var exclude = _traceContext.TraceDetails.Where(w =&gt; w.Trace.CreatedBy == userName).Select(f =&gt; f.LogTime.ToString(&quot;yyyy-MM-dd HH:mm:ss.fff&quot;)).ToList();

            var data = _billingContext.YWAF_log.Where(s =&gt; s.FormattedMessage.Contains(userName));

            var data2 = from d in data where !exclude.Contains(d.Timestamp.ToString(&quot;yyyy-MM-dd HH:mm:ss.fff&quot;)) select d;
</code></pre>
<p>This gets me the <strong>'your query could not be translated...'</strong></p>
<p><strong>Edit - Models as requested</strong></p>
<pre><code>    public class Trace
{
    [Key]
    public int ObjID { get; set; }
    public string Name { get; set; }
    public string CreatedBy { get; set; }
    public DateTime CreatedOn { get; set; }
    public string ServerName { get; set; }

    public ICollection&lt;TraceDetail&gt; TraceDetails { get; set; }
}

    public class TraceDetail
{
    [Key]
    public int ObjID { get; set; }

    [DataType(DataType.DateTime)]
    [DisplayFormat(DataFormatString = &quot;{0:yyyy-MM-dd HH:mm:ss.fff}&quot;)]
    public DateTime LogTime { get; set; }
    public string ServiceName { get; set; }
    public int Duration { get; set; }
    public int? Threshold { get; set; }

    public Trace Trace{ get; set; }
}

public class YWAF_log
{
    [Key]
    public int objID { get; set; }
    [DataType(DataType.DateTime)]
    [DisplayFormat(DataFormatString = &quot;{0:yyyy-MM-dd HH:mm.ss.fff}&quot;)]
    public DateTime Timestamp { get; set; }
    public string FormattedMessage { get; set; }
}
</code></pre>
<p>Please note I can't match on objID as they are sequences and as the database is restored frequently they aren't re-sequenced.</p>
<p>Trace and TraceDetail are in one context and YWAF_Log in a different context - both DBs are SQL Server 2008 R2</p>

## Answers
### Answer ID: 64009940
<p>change your code to this :</p>
<pre><code>var exclude = _traceContext.TraceDetails.Where(w =&gt; w.Trace.CreatedBy == userName).select(c =&gt; c.LogTime).ToList();

var data = from s in _billingContext.log
                   where s.FormattedMessage.Contains(userName)
                   and
                     !exclude.Contains(s.Timestamp)
                   select s;
</code></pre>

