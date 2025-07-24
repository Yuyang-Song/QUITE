# Entity Framework - loading entities by multiple navigation properties in one request
[Link to question](https://stackoverflow.com/questions/34854349/entity-framework-loading-entities-by-multiple-navigation-properties-in-one-req)
**Creation Date:** 1453118632
**Score:** 1
**Tags:** c#, sql, entity-framework, linq
## Question Body
<p>Good afternoon, everyone! I've got a new  question: assume that I have the following entity in my database:</p>

<pre><code>public class Entity1
{
public virtual Entity2 Navigation1 {get;set;}
public virtual Entity3 Navigation2 {get; set;}
......
}
</code></pre>

<p>And I need is to execute the following query:</p>

<pre><code>SELECT * FROM Entity1 ent1
join Entity2 as ent2 on ent2.Id = ent1.Entity2Id
join Entity3 as ent3 on ent3.Id = ent1.Entity3Id
</code></pre>

<p>If I code this way:</p>

<pre><code>context.Entry(ent1).Reference(rep=&gt;rep.Navigation1).Load();
context.Entry(ent1).Reference(rep=&gt;rep.Navigation2).Load();
</code></pre>

<p>Entity Framework will execute 2 queries. How am I supposed to rewrite the code so that the framework performs only one call to the database?</p>

## Answers
### Answer ID: 34854579
<p>You want to utilize the navigation properties.</p>

<p>For example:</p>

<pre><code>IQueryable&lt;Entity1&gt; query = DBContext.Set&lt;Entity1&gt;()
    .Include(x =&gt; x.Navigation1)
    .Include(x =&gt; x.Navigation2);

IList&lt;Entity1&gt; mylist = query.ToList();
</code></pre>

<p>mylist would then contain your entity with properties set matching your associated entities.</p>

