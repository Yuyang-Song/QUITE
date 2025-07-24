# LINQ could not be translated. Call to &#39;AsEnumerable&#39;, &#39;AsAsyncEnumerable&#39;, &#39;ToList&#39;, or &#39;ToListAsync&#39;
[Link to question](https://stackoverflow.com/questions/78112131/linq-could-not-be-translated-call-to-asenumerable-asasyncenumerable-toli)
**Creation Date:** 1709705153
**Score:** 0
**Tags:** linq, asp.net-core, asp.net-web-api, entity-framework-core
## Question Body
<p>How can I compare a list sent to me for filtering with a list in my database?</p>
<p>I have a List called CandidateLanguage in my candidate entity.</p>
<p>And I get a list called LanguageSkills from outside to filter. Then, when I fetch my candidates, I want to make this comparison, but I get an error.</p>
<p>My code :</p>
<pre><code>var entities = _context.Candidates
    .Include(p =&gt; p.CandidateLanguages)
    .Where(m =&gt; m.CandidateLanguages
        .Any(l =&gt; languageSkills
            .Any(c =&gt;
                c.LanguageId == l.LanguageId &amp;&amp;
                c.Writing &lt;= l.Writing &amp;&amp;
                c.Reading &lt;= l.Reading &amp;&amp;
                c.Speaking &lt;= l.Speaking
            )
        )
    )
    .AsNoTracking();
</code></pre>
<p>The error I received:</p>
<blockquote>
<p>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'</p>
</blockquote>

## Answers
### Answer ID: 78117997
<p>As mentioned in the comments, EF cannot translate a list of objects (languageSkills) to be used like that in a filter. You can only use collections of simple types. More complex comparisons against in-memory objects need to be done in memory.</p>
<p>We can do an initial filter based on the language IDs requested:</p>
<pre><code>var languageIds = languageSkills.Select(x =&gt; x.LanguageId).Distinct().ToList();

var entities = _context.Candidates
    .Include(p =&gt; p.CandidateLanguages)
    .Where(m =&gt; m.CandidateLanguages
        .Any(l =&gt; laungageIds.Contains(l.LanguageId)))
    .AsNoTracking()
    .ToList();

entities = entities
    .Where(l =&gt; languageSkills.Any(c =&gt;
            c.LanguageId == l.LanguageId &amp;&amp;
            c.Writing &lt;= l.Writing &amp;&amp;
            c.Reading &lt;= l.Reading &amp;&amp;
            c.Speaking &lt;= l.Speaking))
    .ToList();
</code></pre>
<p>The first query runs against SQL and retrieves all candidates for the selected languages. From there we filter it down in memory to the exact matches. The caveat of this approach is that this could end up loading a significant amount of data.</p>
<p>A more complete approach if you are dealing with a lot of candidates to filter down and a relatively reasonable number of skill criteria would be to use a dynamic expression builder to build a <code>Where</code> expression based on the criteria. This will be used to compose an (AND-AND-AND) OR (AND-AND-AND) OR (AND-AND-AND) ... expression from your list of languageSkills. This can be done with <code>PredicateBuilder</code>, or manually composing an expression in a loop, or something like the DynamicWhere Nuget package.</p>

