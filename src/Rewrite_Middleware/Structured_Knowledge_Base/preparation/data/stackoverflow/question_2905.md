# Merge a linq expression from both db and in memory data
[Link to question](https://stackoverflow.com/questions/58095323/merge-a-linq-expression-from-both-db-and-in-memory-data)
**Creation Date:** 1569403752
**Score:** 0
**Tags:** entity-framework, linq
## Question Body
<p>I am using Entity Framework for querying data and I need to merge data already  in memory (including new record) with the ones in db.</p>

<p>For example:</p>

<blockquote>
<pre><code>var linqdb = from d in context.Set&lt;DEPARTMENT&gt;()
             join i in context.Set&lt;INSTALLATION&gt;() 
             on d.INSTID equals i.INSTID
             select new { d.DEPTNAME, i.INSTNAME };

var linqm = from d in context.Set&lt;DEPARTMENT&gt;().Local
            join i in context.Set&lt;INSTALLATION&gt;().Local 
            on d.INSTID equals i.INSTID
            select new { d.DEPTNAME, i.INSTNAME };

var linqunion = linqm.Union(linqdb.AsEnumerable());
</code></pre>
</blockquote>

<p>The difference is only the source where to execute the query: 
the first is database the second is in memory.
How I could achieve a result without having to rewrite the LINQ query 2 times?</p>

<p>Regards
Luigi</p>

