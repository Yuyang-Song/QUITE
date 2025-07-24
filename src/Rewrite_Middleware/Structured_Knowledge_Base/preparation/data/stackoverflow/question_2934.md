# Error when doing mulitple ProjectTo layers with EfCore
[Link to question](https://stackoverflow.com/questions/59269836/error-when-doing-mulitple-projectto-layers-with-efcore)
**Creation Date:** 1575989241
**Score:** 1
**Tags:** c#, asp.net-core, automapper, ef-core-3.0
## Question Body
<p>I'm trying to create an "design guide" for building rest apis in my company and i wanted to have a 3 layers structure with automapper, asp.net core and ef core.</p>

<pre><code>Database Layer : DbSet Entities
Business Layer : Application Models
Api/Rest/External Layer : Dto Object
</code></pre>

<p>I've successfully manage to do that with the following gist : <a href="https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e" rel="nofollow noreferrer">https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e</a></p>

<p>but as you can see i need to use a hack to make this work... (<a href="https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e#file-automapper_bug_lambda_projection-cs-L23-L24" rel="nofollow noreferrer">https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e#file-automapper_bug_lambda_projection-cs-L23-L24</a>), (<a href="https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e#file-automapper_bug_lambda_projection-cs-L89" rel="nofollow noreferrer">https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e#file-automapper_bug_lambda_projection-cs-L89</a>) and (<a href="https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e#file-automapper_bug_lambda_projection-cs-L93" rel="nofollow noreferrer">https://gist.github.com/Angelinsky7/49c86333584e3f9cece44a88e7febd4e#file-automapper_bug_lambda_projection-cs-L93</a>)</p>

<pre><code>public IEnumerable&lt;SubLayer2&gt; _Subs { get; set; } = new HashSet&lt;SubLayer2&gt;();
public ICollection&lt;SubLayer2&gt; Subs =&gt; (ICollection&lt;SubLayer2&gt;)_Subs;

cfg.CreateMap&lt;Layer1, Layer2&gt;()
  .ForMember(p =&gt; p._Subs, opt =&gt; opt.MapFrom(src =&gt; src.Subs));
cfg.CreateMap&lt;Layer2, Layer3&gt;()
  .ForMember(p =&gt; p.Subs, opt =&gt; opt.MapFrom(src =&gt; src._Subs));
</code></pre>

<p>and i very don't like it (because even if this is working like that, in more complex senarii, it's not working anymore)</p>

<p>if i don't do the hack : <a href="https://gist.github.com/Angelinsky7/0e26507c07c066376d5a4de8726dd1f2" rel="nofollow noreferrer">https://gist.github.com/Angelinsky7/0e26507c07c066376d5a4de8726dd1f2</a></p>

<p>In the InMemory EfCore Case with Layer3 as IEnumerable: (i dind't have this one before creating the issue)
<code>Unhandled exception. System.InvalidOperationException: The LINQ expression 'dtoSubLayer2' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync()</code></p>

<p>In the SqlServer EfCore Case with Layer3 as IEnumerable: (what i would like to use)
<code>InvalidOperationException: When called from 'VisitLambda', rewriting a node of type 'System.Linq.Expressions.ParameterExpression' must return a non-null value of the same type. Alternatively, override 'VisitLambda' and change it to not visit children of this type.</code></p>

<p>In all EfCore with Layer3 as ICollection:
<code>Unhandled exception. System.NullReferenceException: Object reference not set to an instance of an object.</code></p>

<p>What am I doing wrong ? is this totally not possible to do ? Is there a way for me to find NullReferenceException or VisitLambda that pop up the exception and customize this behavior ? It would be perfect to have this kind of solution because i would have exactly what i would like to build my rest api...</p>

<h3>Source/destination types</h3>

<pre class="lang-cs prettyprint-override"><code>internal class Layer1 {
  public Int64 Id { get; set; }
  public ICollection&lt;SubLayer1&gt; Subs { get; set; } = new HashSet&lt;SubLayer1&gt;();
}

internal class SubLayer1 {
  public Int64 Id { get; set; }
  public Int64 LayerId { get; set; }
}

internal class Layer2 {
  public Int64 Id { get; set; }
  public ICollection&lt;SubLayer2&gt; Subs { get; set; } = new HashSet&lt;SubLayer2&gt;();
}

internal class SubLayer2 {
  public Int64 Id { get; set; }
}

internal class Layer3 {
  public Int64 Id { get; set; }
  public IEnumerable&lt;SubLayer3&gt; Subs { get; set; } = new HashSet&lt;SubLayer3&gt;();
}

internal class SubLayer3 {
  public Int64 Id { get; set; }
}
</code></pre>

<h3>Mapping configuration</h3>

<pre class="lang-cs prettyprint-override"><code>cfg.CreateMap&lt;Layer1, Layer2&gt;();
cfg.CreateMap&lt;SubLayer1, SubLayer2&gt;();

cfg.CreateMap&lt;Layer2, Layer3&gt;();
cfg.CreateMap&lt;SubLayer2, SubLayer3&gt;();
</code></pre>

<h3>Version: x.y.z</h3>

<pre><code>&lt;PackageReference Include="AutoMapper" Version="9.0.0" /&gt;
&lt;PackageReference Include="Microsoft.EntityFrameworkCore.InMemory" Version="3.1.0" /&gt;
&lt;PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="3.1.0" /&gt;
</code></pre>

<h3>Expected behavior</h3>

<p>I should be able to use ProjectTo Multiple time to change layers without having to use a trick to do it. And i should be able to choose between ICollection and IEnumerable when i would like</p>

<h3>Actual behavior</h3>

<p>Depending on the implementation one the 3 exceptions rises (most of the time it's the 'VisitLambda' lambda one</p>

<h3>Steps to reproduce</h3>

<p><a href="https://gist.github.com/Angelinsky7/0e26507c07c066376d5a4de8726dd1f2" rel="nofollow noreferrer">https://gist.github.com/Angelinsky7/0e26507c07c066376d5a4de8726dd1f2</a></p>

<p>thanks for all the help and thanks for taking the time !!!
(and sorry if this is a efcore issue but i was thinking : "because i can create a "hack" in automapper it's maybe here")</p>

<p>i came here because the automapper team decided that it wasn't a bug on their part (<a href="https://github.com/AutoMapper/AutoMapper/issues/3280" rel="nofollow noreferrer">https://github.com/AutoMapper/AutoMapper/issues/3280</a>)</p>

## Answers
### Answer ID: 59270816
<p>it seems that automapper cannot do what i would like to have.
My mistake.
Thanks for the community to help me.</p>

