# Linq join with exists
[Link to question](https://stackoverflow.com/questions/11964743/linq-join-with-exists)
**Creation Date:** 1345010561
**Score:** 0
**Tags:** linq, join, contains
## Question Body
<p>I'm busy rewriting a system and are using Linq queries to extract data from the database. I am used to plain old TSQL and stored procedures so my Linq skills are not the best.
I have a sql query that I try to rewrite in Linq that contains a join, where clause and IN statements. I do get it right but when I run the sql query I get a different value as from the Linq query. Somewhere I'm missing something and can't find the reason.</p>

<p>Here is the SQL:</p>

<pre><code>select 
    isnull(Sum(QtyCC) + Sum(QtyEmployee), 0) *
    isnull(Sum(UnitPrice), 0)[TotalRValue]             
from 
    tbl_app_KGCWIssueLines a
        inner join tbl_app_KGCWIssue b on b.IssueNrLnk = a.IssueNrLnk
where   
    b.CreationDate &gt;= '2011-02-01' and 
    a.IssueNrLnk IN (
        select 
            IssueNrLnk
        from 
            tbl_app_KGCWIssue
        where   
            CustomerCode = 'PRO002' and   
            ISNULL(Tier1,'') = 'PRO002' and   
            ISNULL(Tier2,'') = 'HAMD01' and   
            ISNULL(Tier3,'') = '02' and   
            ISNULL(Tier4,'') = '02001' and  
            ISNULL(Tier5,'') = 'PTAHQ001' and   
            ISNULL(Tier6,'') = '035' and   
            ISNULL(Tier7,'') = '' and   
            ISNULL(Tier8,'') = '' and   
            ISNULL(Tier9,'') = '' and   
            ISNULL(Tier10,'') = ''
)
</code></pre>

<p>And here is the Linq:</p>

<pre><code>ctx.ObjectContext.tbl_app_KGCWIssue
    .Join(ctx.ObjectContext.tbl_app_KGCWIssueLines, 
        i =&gt; i.IssueNrLnk, l =&gt; l.IssueNrLnk, (i, l) =&gt; new { i, l })
    .Where(o =&gt; o.i.CreationDate &gt;= IntervalStartDate)
    .Where(p =&gt; ctx.ObjectContext.tbl_app_KGCWIssue
        .Where(a =&gt; 
            a.CustomerCode == CustomerCode &amp;&amp; 
            a.Tier1 == employee.Tier1 &amp;&amp; 
            a.Tier2 == employee.Tier2 &amp;&amp; 
            a.Tier3 == employee.Tier3 &amp;&amp; 
            a.Tier4 == employee.Tier4 &amp;&amp; 
            a.Tier5 == employee.Tier5 &amp;&amp; 
            a.Tier6 == employee.Tier6 &amp;&amp; 
            a.Tier7 == employee.Tier7 &amp;&amp; 
            a.Tier8 == employee.Tier8 &amp;&amp; 
            a.Tier9 == employee.Tier9 &amp;&amp; 
            a.Tier10 == employee.Tier10)
        .Select(i =&gt; i.IssueNrLnk)
        .Contains(p.l.IssueNrLnk))
    .Sum(p =&gt; p.l.UnitPrice * (p.l.QtyEmployee + p.l.QtyCC));
</code></pre>

