# How to access a property from a base class in a LINQ query with two levels of inheritance in EF Core
[Link to question](https://stackoverflow.com/questions/77791052/how-to-access-a-property-from-a-base-class-in-a-linq-query-with-two-levels-of-in)
**Creation Date:** 1704863622
**Score:** 2
**Tags:** c#, entity-framework, linq, inheritance, tph
## Question Body
<p>We use SQL Server and EF Core to map our C# objects to the database. The object model has two levels of abstraction as follows:</p>
<pre class="lang-cs prettyprint-override"><code>public abstract class Animal
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public class Parrot : Animal
{
    public bool CanSpeak { get; set; }
}

public abstract class Mammal : Animal
{
    public bool HasPouch { get; set; }
}

public class Dog : Mammal
{
    public bool HasTail { get; set; }
}

public class Cat : Mammal
{
    public double MaxHeight { get; set; }
}

public class Horse : Mammal
{
    public string Breed { get; set; }
    public int RacingSpeed { get; set; }
}
</code></pre>
<p>Main parts of the <code>DbContext</code> inherited class:</p>
<pre class="lang-cs prettyprint-override"><code>public DbSet&lt;Animal&gt; Animals { get; set; }

protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity&lt;Animal&gt;()
        .ToTable(&quot;Animals&quot;)
        .HasDiscriminator&lt;string&gt;(&quot;AnimalType&quot;)
        .HasValue&lt;Parrot&gt;(&quot;Parrot&quot;)
        .HasValue&lt;Dog&gt;(&quot;Dog&quot;)
        .HasValue&lt;Cat&gt;(&quot;Cat&quot;)
        .HasValue&lt;Horse&gt;(&quot;Horse&quot;);

    // Additional configurations if needed
}
</code></pre>
<p>Now I'm going to show 3 types of LINQ queries out of which the first two work but the last one causes a runtime error (<code>IvalidOperationException</code> - something like: The LINQ expression 'DbSet&lt;<code>Animal</code>&gt;().OfType&lt;<code>Mammal</code>&gt;()' could not be translated).</p>
<p>This one queries a property from the very base <em>abstract</em> class of the hierarchy which is used in EF configuration for the <code>Animals</code> table:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;Animal&gt; list = context.Animals
    .Where(x =&gt; x.Name == &quot;Max&quot;)
    .ToList();
</code></pre>
<p>No problem with it.</p>
<p>This one needs to query a property from a concrete class and works fine as well:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;Animal&gt; catsUnder50cm = context.Animals
    .Where(x =&gt; x is Cat &amp;&amp; (x as Cat).MaxHeight &lt;= 50)
    .ToList();
</code></pre>
<p>However, with this one, although it compiles OK, I get the runtime error mentioned above:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;Animal&gt; marsupials = context.Animals
    .Where(x =&gt; x is Mammal &amp;&amp; (x as Mammal).HasPouch)
    .ToList();
</code></pre>
<p>I think this is due to the fact <code>Mammal</code> is an abstract class. I could rewrite it this way:</p>
<pre class="lang-cs prettyprint-override"><code>List&lt;Animal&gt; marsupials2 = context.Animals
    .Where(x =&gt; (x is Dog &amp;&amp; (x as Dog).HasPouch) || (x is Cat &amp;&amp; (x as Cat).HasPouch) || (x is Horse &amp;&amp; (x as Horse).HasPouch) )
    .ToList();
</code></pre>
<p>But as you can see, the query gets quite complex and ugly at the same time. And the more classes inherit from <code>Mammal</code> the more complex the query is. Which is exactly our case.</p>
<p>The question is:</p>
<p>Is it possible to use a property of the &quot;middle&quot; abstract class which is not part of the model in LINQ queries?</p>
<p>If not, can we somehow &quot;add&quot; that abstract class to the EF data model?</p>
<p>The <code>Mammal</code> data type should map to the same table of <code>Animals</code>. Is that possible?</p>

## Answers
### Answer ID: 77791196
<p>εὕρηκᾰ</p>
<p>I think I found a solution. I don't like it that much though.</p>
<p>As a workaround, I need to map the &quot;middle&quot; abstract class to the same table. And map its new property (<code>HasPouch</code>) to the same column.</p>
<p>Basically, you shall do something like this in your <code>DbContext</code> configuration:</p>
<pre class="lang-cs prettyprint-override"><code>EntityTypeBuilder&lt;Mammal&gt; mammalBuilder = modelBuilder.Entity&lt;Mammal&gt;();
mammalBuilder.ToTable(&quot;Animals&quot;);
mammalBuilder.Property(x =&gt; x.HasPouch).HasColumnName(&quot;HasPouch&quot;);
</code></pre>

