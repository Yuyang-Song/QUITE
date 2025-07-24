# How to query multiple tables using LINQ syntax in .NET core 3
[Link to question](https://stackoverflow.com/questions/62426880/how-to-query-multiple-tables-using-linq-syntax-in-net-core-3)
**Creation Date:** 1592389736
**Score:** 2
**Tags:** c#, linq, entity-framework-core, .net-core-3.1
## Question Body
<p>I need to query two database tables for a search term and return the results. The following was working in EF Core 2:</p>

<pre><code>var SearchTerm = "hello";
IQueryable&lt;TableA&gt; q;
q = (from a in context.TableA
     join b in context.TableB on a equals b.A into leftjoin
     from c in leftjoin.DefaultIfEmpty()                     
     where c.Column1.Contains(SearchTerm)
        || a.Column1.Contains(SearchTerm)
        || a.Column2.Contains(SearchTerm)
     select a);

return q.Include(a =&gt; a.TableD)
        .GroupBy(a =&gt; a.Id)
        .Select(group =&gt; group.First())
        .ToList();
</code></pre>

<p>The idea of the above is to take a SearchTerm and query two columns from TableA, join to TableB and also query a column in this one then select distinct values from TableA.</p>

<p>In .NET 3 the above throws an error saying it can't be translated to SQL. I tried to rewrite this, the best I can do is the below:</p>

<pre><code>var SearchTerm = "hello";
var q = (from a in context.TableA
         join b in context.TableB on a equals b.A into leftjoin
         from c in leftjoin.DefaultIfEmpty()                     
         where c.Column1.Contains(SearchTerm)
             || a.Column1.Contains(SearchTerm)
             || a.Column2.Contains(SearchTerm)                    
         select a.Id).Distinct().ToList();  

return context.TableA
    .Where(a =&gt; q.Contains(a.Id))
    .Include(c =&gt; c.TableD)
    .ToList();
</code></pre>

<p>Which works ok but involves two database queries, since I already have the list of TableA from the first query it would be great to be able to just use this without having to extract the Ids and performing the second query. Also making sure the database continues to handle the distinct part rather than C# would be preferable too.</p>

<p>The definitions of A and B are:</p>

<pre><code>public class TableA
{
    public int Id { get; set; }

    public string Column1 { get; set; }

    public string Column2 { get; set; }

    public int TableDId { get; set; }

    public TableD TableD { get; set; }
}

public class TableB
{
    public int Id { get; set; }

    public string Column1 { get; set; }

    public int TableAId { get; set; }

    public TableA TableA { get; set; }
}
</code></pre>

## Answers
### Answer ID: 62428099
<p>If I understood you correctly you have one-to-many relation between <code>TableA</code> and <code>TableB</code>, so it should be possible to add collection navigation property to <code>TableA</code> like in <a href="https://www.learnentityframeworkcore.com/configuration/one-to-many-relationship-configuration" rel="nofollow noreferrer">this tutorial</a> for example:</p>

<pre><code>public class TableA
{
    public int Id { get; set; }
    ...
    public ICollection&lt;TableB&gt; TableBs { get; set; } 
}
</code></pre>

<p>So you can try to do something like this:</p>

<pre><code>context.TableA
    .Where(ta =&gt; ta.TableBs.Any(tb =&gt; tb.Column1.Contains(SearchTerm)) 
        || ta.Column1.Contains(SearchTerm) 
        || ta.Column2.Contains(SearchTerm))
    .Include(c =&gt; c.TableD)
    .ToList();
</code></pre>

<p>Another option is to try subquery:</p>

<pre><code>var q = (from a in context.TableA
         join b in context.TableB on a.Id equals b.TableAId  into leftjoin
         from c in leftjoin.DefaultIfEmpty()                     
         where c.Column1.Contains(SearchTerm)
             || a.Column1.Contains(SearchTerm)
             || a.Column2.Contains(SearchTerm)                    
         select a.Id);  // remove Distinct and ToList

return context.TableA
    .Where(a =&gt; q.Contains(a.Id))
    .Include(c =&gt; c.TableD)
    .ToList();
</code></pre>

