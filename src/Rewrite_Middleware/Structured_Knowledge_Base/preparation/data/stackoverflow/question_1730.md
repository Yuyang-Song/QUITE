# How do I rewrite query expressions to replace enumerations with ints?
[Link to question](https://stackoverflow.com/questions/5362468/how-do-i-rewrite-query-expressions-to-replace-enumerations-with-ints)
**Creation Date:** 1300542472
**Score:** 17
**Tags:** c#, entity-framework, reflection, expression-trees, entity-framework-4.1
## Question Body
<p>Inspired by a desire to be able to use enumerations in EF queries, I'm considering adding an ExpressionVisitor to my repositories that will take incoming criteria/specifications criteria and rewrite them to use the corresponding persisted int property.</p>

<p>I'm consistently using the following Value-suffix pattern in my (code-first) entities:</p>

<pre><code>public class User : IEntity
{
    public long ID { get; set; }

    internal int MemberStatusValue { get; set; }

    public MemberStatus MemberStatus 
    {
        get { return (MemberStatus) MemberStatusValue; }
        set { MemberStatusValue = (int) value; }
    }
}
</code></pre>

<p>And map this to the database using the following:</p>

<pre><code>internal class UserMapping : AbstractMappingProvider&lt;User&gt;
{
    public override void DefineModel( DbModelBuilder modelBuilder )
    {
        // adds ToTable and other general mappings
        base.DefineModel( modelBuilder );

        Map.Property( e =&gt; e.MemberStatusValue ).HasColumnName( "MemberStatus" );
    }
}
</code></pre>

<p>In my repositories I have the following method:</p>

<pre><code>public IQueryable&lt;T&gt; Query( Expression&lt;Func&lt;T, bool&gt;&gt; filter, params string[] children )
{
    if( children == null || children.Length == 0 )
    {
        return Objects.Where( filter );
    }
    DbQuery&lt;T&gt; query = children.Aggregate&lt;string, DbQuery&lt;T&gt;&gt;( Objects, ( current, child ) =&gt; current.Include( child ) );
    return filter != null ? query.Where( filter ) : query;
}
</code></pre>

<p>I'd like to add a method call inside this method to rewrite the filter expression, replacing all references to the MemberStatus property with references to MemberStatusValue.</p>

<p>I suppose it will be a solution involving something like seen <a href="https://stackoverflow.com/questions/5361957/how-to-build-a-lambdaexpression-from-an-existing-lambdaexpression-without-compili">in this SO post</a>, but I'm not sure exactly how to get from idea to implementation.</p>

<p>If you can give any advice on the potential performance impact of adding this feature, that would also be appreciated.</p>

## Answers
### Answer ID: 10949350
<p>I'm not sure whether this is quite what you're after, but I've found it simpler to handle enums in a similar but slightly different way. To wit, I have two properties, as you do, but my int property is public and is what the database persists; I then have another public "wrapper" property that gets/sets the int property value via casts from/to the desired enumerated type, which is what's actually used by the rest of the application.</p>

<p>As a result, I don't have to mess around with the model; EF understands and persists the int property just fine while the rest of the application gets nice interactions with the enum type. The only thing I don't like about my approach is that I have to write my LINQ statements with a bunch of casts on any enum value I'm trying to query to turn it into an int to match against the field that's actually persisted. It's a small price, however, and I'd like to suggest it to you because it appears to me that you're using a string to generate your query which gives up all the type safety, Intellisense, etc. that LINQ provides.</p>

<p>Finally, if you're interested in a walkthrough of how to use the new enum features in EF 5 (which is available in beta for download now if you'd like to try it out), check this out:</p>

<p><a href="http://msdn.microsoft.com/en-us/hh859576" rel="nofollow">http://msdn.microsoft.com/en-us/hh859576</a></p>

