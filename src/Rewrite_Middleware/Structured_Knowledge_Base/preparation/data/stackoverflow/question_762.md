# Can I efficiently query generic fields without resorting to HQL?
[Link to question](https://stackoverflow.com/questions/41281399/can-i-efficiently-query-generic-fields-without-resorting-to-hql)
**Creation Date:** 1482403800
**Score:** 7
**Tags:** orchardcms, orchardcms-1.9
## Question Body
<p>I find myself doing a lot of queries to fetch just the first couple of items of a big set, e.g. to show the three most recent news articles or blog posts on the homepage of a website.</p>

<p>As long as this query only involves predefined or custom Parts, I can do something like this:</p>

<pre class="lang-cs prettyprint-override"><code>public IEnumerable&lt;ContentItem&gt; GetTopArticles(int amount)
{
    var cultureRecord = _cultureManager.GetCultureByName(_orchardServices.WorkContext.CurrentCulture);

    var articles = _orchardServices.ContentManager.Query().ForType("Article")
        .Where&lt;LocalizationPartRecord&gt;(lpr =&gt; lpr.CultureId == cultureRecord.Id)
        .OrderBy&lt;CommonPartRecord&gt;(cpr =&gt; cpr.PublishedUtc)
        .Slice(0, amount);

    return articles;
}
</code></pre>

<p>I'm assuming this will more or less be the same as a <code>SELECT TOP [amount] ...</code> in SQL and will have good performance on a large number of records.</p>

<p>However, sometimes I use Migrations or Import to create Content Types from an external source and want to conditionally check a field from the generic Part. In this case I don't have a Part or PartRecord class that I can pass as a parameter to the ContentQuery methods and if I want to do a conditional check on any of the fields I currently do something like this:</p>

<pre class="lang-cs prettyprint-override"><code>public IEnumerable&lt;ContentItem&gt; GetTopArticles(int amount)
{
    var articles = _orchardServices.ContentManager.Query().ForType("Article")
        .OrderBy&lt;CommonPartRecord&gt;(cpr =&gt; cpr.PublishedUtc)
        .List()
        .Where(a =&gt; a.Content.Article.IsFeatured.Value == true)
        .Take(amount);

    return articles;
}
</code></pre>

<p>This is really wasteful and causes large overhead on big sets but I really, <strong>REALLY</strong>, do not want to delve into the database to figure out Orchard's inner workings and construct long and complex HQL queries every time I want to do something like this.</p>

<h2>Is there any way to rewrite the second query with IContentQuery methods without incurring a large performance hit?</h2>

## Answers
### Answer ID: 41284557
<p>I'm working on something similar (being able to query model data with a dynamic name). Sadly, I haven't found anything that makes it easy.</p>

<p>The method I've found that works is to do plain SQL queries against the database. Check out <a href="https://bitbucket.org/bleroy/orchardpo/src/87045c32cbffc7d731e0c1fd3db2a73827c54d47/Services/LocalizationService.cs?at=default&amp;fileviewer=file-view-default" rel="nofollow noreferrer">this module</a> for syntax on that if you do later find yourself willing to delve into the database.</p>

