# Forcing client side evaluation on a predicate builder expression in .net core 3.1
[Link to question](https://stackoverflow.com/questions/61675579/forcing-client-side-evaluation-on-a-predicate-builder-expression-in-net-core-3)
**Creation Date:** 1588928407
**Score:** 1
**Tags:** c#, .net-core, asp.net-core-3.1, ef-core-3.0, linqkit
## Question Body
<p>I am using LinqKit's predicate builder expressions for search functions. I build a dynamic expression which is then applied on the entity.</p>

<p>Had this working before, but after migrating to .net core 3.1, I am getting errors due to the restriction on client side valuations.</p>

<p>I understand this can be overcome by forcing <code>AsEnumerable()</code> casting.</p>

<p>However I don't understand exactly how to do this on predicate expressions.</p>

<p>Predicate builder function:</p>

<pre><code>private Expression&lt;Func&lt;A, bool&gt;&gt; BuildDynamicWhereClauseForA(string searchValue)
{
    var predicate = PredicateBuilder.New&lt;A&gt;(true);

    if (!string.IsNullOrWhiteSpace(searchValue))
    {
        var searchTerms = searchValue.Split(' ').ToList().ConvertAll(x =&gt; x.ToLower());

        foreach (var item in searchTerms)
        {
            predicate = predicate.Or(x =&gt; x.col1.ToLower().Contains(item));
            predicate = predicate.Or(x =&gt; x.col2.ToLower().Contains(item));
            predicate = predicate.Or(x =&gt; x.col3.ToString().ToLower().Contains(item));
        }
    }

    return predicate;
}
</code></pre>

<p>Function which performs actual database call:</p>

<pre><code>private List&lt;AD&gt; GetDataFromDBForA(string searchBy ...)
{
    var whereClause = BuildDynamicWhereClauseForA(searchBy);

    List&lt;AD&gt; result;

    result =  db.A.AsExpandable()
                  .Where(whereClause)
                  .OrderBy(sortBy)
                  .Select(m =&gt; new AD
                                   {
                                      ...
                                      ...
                                   })
                  .Skip(skip)
                  .Take(take)
                  .ToList()

    return result;
}
</code></pre>

<p>This is the error I get:</p>

<blockquote>
  <p>The LINQ expression 'DbSet
      .Where(e => e.col1.ToLower().Contains(__item_0) || e.col2.ToLower().Contains(__item_0) ||
  e.Col3.ToString().ToLower().Contains(__item_0))' could not be
  translated. Either rewrite the query in a form that can be translated,
  or switch to client evaluation explicitly by inserting a call to
  either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
  ToListAsync().</p>
</blockquote>

<p>I understand why this is happening.</p>

<p>But I don't understand predicates as well and can't seem to cast the result to enumerable or list to force client side evaluation.</p>

<p>What I have tried:</p>

<pre><code> result =  db.A.AsEnumerable()
               .AsQueryable()
               .Where(whereClause)
               .OrderBy(sortBy)
</code></pre>

