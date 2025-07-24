# Filtering thousands of composite keys in EF Core 3
[Link to question](https://stackoverflow.com/questions/70570232/filtering-thousands-of-composite-keys-in-ef-core-3)
**Creation Date:** 1641236206
**Score:** 0
**Tags:** performance, entity-framework-core, fetch, composite-key
## Question Body
<p>I have the following entity class (I am using Pomelo for MySql provider and EF Core 3.1):</p>
<pre><code>public class MyEntity
{
     public int AAA { get; set; }
     public string BBB { get; set; }
     public decimal CCC { get; set; }
}
</code></pre>
<p>The corresponding MySQL table MyEntity has a composite primary key composed of the two properties AAA and BBB.</p>
<p>Given a list of thousands filter entities of type MyEntity, I must retrieve from the database only the records whose corresponding primary key fetch the filter list.</p>
<p><strong>My first solution was to try using a predicate</strong> as mentioned in a former thread, and i<strong>t works if the list of filters does not contains too many filter entities, otherwise I get a Stackoverflow exception if the list of filters contains for instance 1 million entities:</strong></p>
<pre><code>// Variable 'filters' contains several thousands of MyEntity objects.
var results = myContext.Set&lt;MyEntity&gt;()
                       .Where(PredicateHelper.FilterEntity(filters))
                       .ToList();
</code></pre>
<p>Here is the implementation of the predicate methods:</p>
<pre><code> public static class PredicateHelper
 {
     public static Expression&lt;Func&lt;MyEntity, bool&gt;&gt; False&lt;MyEntity&gt;()
     {
        return f =&gt; false;
     }

     public static Expression&lt;Func&lt;MyEntity, bool&gt;&gt; FilterEntity(List&lt;MyEntity&gt; keys)
     {
         var predicate = PredicateHelper.False&lt;MyEntity&gt;();

         foreach (MyEntity key in keys)
         {
             predicate = predicate.Or(ent =&gt; ent.AAA == key.AAA &amp;&amp; ent.BBB == key.BBB);
         }

         return predicate;
    }
  }
</code></pre>
<p><strong>So I tried another solution using a Where clause with a Contain query inside</strong>, but I get an exception telling me that there is no MySql translation for the query, and <strong>I must evaluate it client-side</strong>. But if I insert a ToList() before the Where clause, it means that the entire set of records will be stored in-memory right?, and I do not want it, how can I solve the issue, thanks in advance for any suggestions?</p>
<pre><code>var results = myContext.Set&lt;MyEntity&gt;()
.Where(ent =&gt; filters.Contains(new MyEntity()
 {
      AAA = ent.AAA,
      BBB = ent.BBB
 }))
 .ToList();
</code></pre>
<p>But I get the following exception: The LINQ expression DbSet.Where(c =&gt;__list_0.Contains(new M{ AAA = c.AAA, BBB = c.BBB }))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>

