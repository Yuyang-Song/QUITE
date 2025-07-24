# Key fallback in NHibernate LINQ query
[Link to question](https://stackoverflow.com/questions/12208016/key-fallback-in-nhibernate-linq-query)
**Creation Date:** 1346378723
**Score:** 2
**Tags:** c#, linq, nhibernate
## Question Body
<p>H!</p>

<p>I'm coding a message store with locale fallback for a web application which uses NHibernate over a SQL database. For example, the result of <code>store.Get("Greet", "fr-ca-on")</code> would be the best-match value from this data (<code>fr-ca</code>):</p>

<pre><code>Key    Locale    Message
-----  ------    --------
Greet            Hello
Greet  fr        Bonjour!
Greet  fr-ca     Âllo!
Greet  fr-ca-qc  Âllo toi!
</code></pre>

<p>I've tried various queries like this to implement the fallback:</p>

<pre class="lang-c# prettyprint-override"><code>string[] locales = new[] { "fr-ca-on", "fr-ca", "fr", "" }; 
return (
   from Translation translation in reader.Get&lt;Translation&gt;()
   where locales.Contains(translation.Locale)
   group translation by translation.Key into translationGroup
   select translationGroup.OrderByDescending(p =&gt; p.Locale.Length).First()
   //or: select translationGroup.MaxBy(p =&gt; p.Locale.Length)
);
</code></pre>

<p>These work very well in memory, but NHibernate can't translate the group select into SQL. (It only seems to support simple aggregate methods like <code>.Count()</code>, not selects.)</p>

<p>How can I rewrite this query so NHibernate can translate it to SQL? I can't think of a way that doesn't involve undeferring the query into memory early, which would really hurt the application's performance.</p>

<p>(I'd rather not use resource files, because I have other entities which relate to the translations.)</p>

## Answers
### Answer ID: 12250698
<p>if you really just want to implement the mentionend Get method</p>

<p>how about that?</p>

<pre><code>private string Get(string key, string locale)
{
    return (from Translation t in reader
       where t.Key == key &amp;&amp; (t.Locale == null || t.Locale == "" || locale.StartsWith(t.Locale))
       orderby t.Locale descending
       select t.Value).First();
}
</code></pre>

<p>PS: the change to 'StartsWith' makes sense depending on the locale keys you have and what you request 
exotic but the only example i can think of right now :) 'fr-ch' may give you french when requesting 'ch' (suisse german)</p>

### Answer ID: 12254056
<p>I was able to rewrite it as a LINQ subquery:</p>

<pre class="lang-c# prettyprint-override"><code>string[] locales = new[] { "fr-ca-on", "fr-ca", "fr", "" }; 
return (
    from Translation translation in reader.Get&lt;Translation&gt;()
    where
        locales.Contains(translation.Locale)
        &amp;&amp; (translation.Locale.Length == reader
            .Get&lt;Translation&gt;()
            .Where(p =&gt; locales.Contains(p.Locale) &amp;&amp; p.Key == translation.Key)
            .Max(p =&gt; p.Locale.Length)
        )
    select translation
);
</code></pre>

<p>NHibernate handles the subquery nicely and turns it into this (prettified) SQL:</p>

<pre class="lang-sql prettyprint-override"><code>SELECT *
FROM [translation] translation
WHERE
    [locale] IN ('fr-ca-on', 'fr-ca', 'fr', '')
    AND LEN([locale]) = (
        SELECT CAST(MAX(LEN(sub.[locale])) AS INT)
        FROM [translation] sub
        WHERE
           sub.[locale] IN ('fr-ca-on', 'fr-ca', 'fr', '')
           AND sub.[key] = translation.[key]
)
</code></pre>

