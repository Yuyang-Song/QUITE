# DRY in C# code documentation on two interface variants
[Link to question](https://stackoverflow.com/questions/9891391/dry-in-c-code-documentation-on-two-interface-variants)
**Creation Date:** 1332857904
**Score:** 1
**Tags:** c#, documentation, dry, fluent-interface
## Question Body
<p>I am currently rewriting a SDK to access a webservice.</p>

<p>Since the model for a database query consists of many classes (actually one class for each of about twenty possible filters), I decided to provide a fluent interface additonally.</p>

<p>So instead of</p>

<pre><code>new Query(
 Age = new AgeFilter() { From = 18, To = 65 },
 Location = new PostalCodeFilter() { Zip = 12345, new RadiusDefinition() { ... } }
);
</code></pre>

<p>the user can now write:</p>

<pre><code>Query.Create()
  .WithAge(18, 65)
  .WithLocation(12345, 50, "miles");
</code></pre>

<p>Now I found out that the traditional way has to be included as well (I cannot hide the actual objects as internal).</p>

<p>How can I avoid having to document both the parameters of the fluent interface and the fields of the data classes? The descriptions are the same. I thought about see/seealso but this wouldn't show up in Visual Studio's Code Assistant.</p>

## Answers
### Answer ID: 9892516
<p>If you use Sandcastle you can use the <a href="http://www.ewoodruff.us/shfbdocs/html/79897974-ffc9-4b84-91a5-e50c66a0221d.htm" rel="nofollow"><code>&lt;inheritdoc /&gt;</code></a> tag just like this:</p>

<pre><code>///&lt;param name="from"&gt;
///&lt;inheritdoc cref="AgeFilter.From" select="/summary/node()" /&gt;
///&lt;/param&gt;
</code></pre>

<p>or</p>

<pre><code>///&lt;summary&gt;
///&lt;inheritdoc cref="QueryFilters.WithAge" select="/param[@name='from']/node()"/&gt;
///&lt;/summary&gt;
</code></pre>

### Answer ID: 9891674
<p>I don't think you can. An xml-doc comment is applied to a very specific thing and isn't easily "shared". But, you can "link" between elements using the <code>&lt;see&gt;</code> tag. Have a look at <a href="http://msdn.microsoft.com/en-us/library/acd0tfbe.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/acd0tfbe.aspx</a> and see if it's of use to you.</p>

<p>Understand that DRY really applies mainly to code; writing the same line of code twice means that if a change to the logic inherent in that code has to be made, it has to be made twice. What you're trying to avoid repeating is markup, which while it can have the same inherent problem of having to make changes in multiple places, markup usually has fewer tools available to avoid restating similar things. If you look at other libraries which have multiple ways to accomplish a similar goal, you'll find that a lot of the documentation appears copy-pasted.</p>

