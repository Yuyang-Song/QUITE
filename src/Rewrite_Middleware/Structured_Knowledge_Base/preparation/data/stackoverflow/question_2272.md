# EF 5.0 Oracle Code First set Precision to number types
[Link to question](https://stackoverflow.com/questions/27013910/ef-5-0-oracle-code-first-set-precision-to-number-types)
**Creation Date:** 1416391313
**Score:** 1
**Tags:** c#, oracle-database, entity-framework, ef-code-first
## Question Body
<p>with Entity Framework 5.0 and ODP.NET I am trying to build a <em>code first</em> DbContext for my existing Oracle database.
I know this approach is not supported officially by ODP, but maybe there is a workaround for the <em>only</em> problem I still need to solve.</p>

<p>All my tables have keys which are of type <code>NUMBER(18,0)</code>. This is a simple example:</p>

<ul>
<li><p>Table</p>

<pre><code>&gt; DESCRIBE T_USER  
KUSER  NOT NULL NUMBER(18,0)
</code></pre></li>
<li><p>Domain Object</p>

<pre><code>public class User
{  
    public long Id { get; set; }  
    /* ... */  
}
</code></pre></li>
<li><p>Mapping configuration</p>

<pre><code>modelBuilder.Entity&lt;User&gt;()
    .ToTable("T_USER");
modelBuilder.Entity&lt;User&gt;()
    .Property&lt;long&gt;(x =&gt; x.Id)
    .IsRequired()
    .HasColumnType("number")
    .HasColumnName("KUSER");
</code></pre></li>
</ul>

<p>I cannot specify the Precision attribute though, because only the <code>DecimalPropertyConfiguration</code> class (.Property()) exposes Precision and Scale properties.</p>

<p>The result is that all translated queries contain a CAST AS number with 19 digits precision (default mapping for Int64), like:
    SELECT 
      CAST( "Extent1"."KUSER" AS number(19,0)) AS "C1",
    /* ... */</p>

<p>The same casts are done in JOIN and WHERE clauses with heavy performance impacts on each query.</p>

<p>In the EDMX XML file - which I have deprecated since I hope to not have to use it ever in the future -
I had this line:</p>

<pre><code>&lt;Property Name="KUSER" Type="number" Nullable="false" Precision="18" /&gt;
</code></pre>

<p><strong>Is it possible to manually set the Precision of a property after EF model creation?</strong></p>

<p>Or maybe there is a way to extend EF configuration classes and add a custom <code>NumberPropertyConfiguration</code>
which exposes the Precision property.
The fact that the Edm namespace is internal has stopped me from pursuing this latter path.</p>

<h3>Notes</h3>

<ul>
<li>I can not represent those properties with C# <code>decimal</code> type because I would have to rewrite pretty much all the domain layer.  </li>
<li>I can not add a fake <code>long</code> property to wrap an hidden <code>decimal</code> one, because the <code>long</code> field needs to be used in LINQ-to-SQL queries joins and select</li>
</ul>

<h3>Updates</h3>

<ul>
<li>Added call to <code>.HasColumnType("number")</code> in the <code>PrimitivePropertyConfiguration</code>, but the result is the same.</li>
<li><p>Is it feasible to alter property facets by traversing the <code>MetadataWorkspace</code>?</p>

<pre><code>(this as IObjectContextAdapter).ObjectContext.MetadataWorkspace
</code></pre>

<p><del>I will try this myself as soon as possible and update with results.</del><br>
<strong>No</strong>, <code>MetadataWorkspace</code> is read only.</p></li>
</ul>

## Answers
### Answer ID: 27014263
<p>No you cannot do that. If you're using Code First the model is defined by your code. If your code says that a property is <code>long</code>, it won't be mapped as a <code>NUMBER()</code> column in the database.</p>

<p>The only direct workarounds I can think of are the ones that you mention, but you want to avoid.</p>

<p>You can still use a mapper, like <a href="http://automapper.org/" rel="nofollow">AutoMapper</a> (<a href="https://automapper.codeplex.com/" rel="nofollow">more info here</a>), which allows you to map from your EF entities to your domain entities. Depending on how your code is implemented this could work, but, if you leak EF LINQ functionalities to your domain logic, then this wouldn't work. You could try using <a href="https://github.com/AutoMapper/AutoMapper/wiki/Queryable-Extensions" rel="nofollow">AutoMapper IQueryable Extensions</a> but I'm not sure if they would work for your use case.</p>

