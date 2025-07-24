# PostgreSQL &amp; JPA - &quot;Mixing of ? parameters and other forms is not supported&quot; error
[Link to question](https://stackoverflow.com/questions/76991067/postgresql-jpa-mixing-of-parameters-and-other-forms-is-not-supported-err)
**Creation Date:** 1693210542
**Score:** 0
**Tags:** spring, postgresql, spring-data-jpa, jsonb
## Question Body
<p>I have a jsonb data column with this sample data:</p>
<pre><code>[
  {
    &quot;eventId&quot;: &quot;5&quot;,
    &quot;events&quot;: [
      &quot;a&quot;,
      &quot;b&quot;
    ]
    &quot;customerId&quot;:&quot;123&quot;
  }
]
</code></pre>
<p>And I'm trying to filter this data by events with the spring application. I managed to construct a working SQL query in my PostgreSQL database:</p>
<p><code>SELECT DISTINCT jsonb_path_query(jsonb_column, '$[*] ? (@.events[*] like_regex &quot;a&quot; flag &quot;i&quot;)') FROM my_table</code></p>
<p>However, when constructing a similar @Query in JPA, and using the <code>?1</code> parameter:</p>
<pre><code>@Query(nativeQuery=true,
        value=&quot;SELECT DISTINCT jsonb_path_query(jsonb_column, '$[*] ? (@.events[*] like_regex \&quot;?1\&quot; flag \&quot;i\&quot;)') \n +&quot;
        &quot;FROM my_table\n&quot;
)
</code></pre>
<p>I'm getting this error:
<code>Mixing of ? parameters and other forms like ?1 is not supported</code></p>
<p>Is there a way to rewrite the original query without the use of the <code>?</code> operator? It's nested arrays, so <code>jsonb_path_query</code> comes in really handy, and I have no clue how to replace it.</p>
<p>Any advice would be appreciated.</p>
<p>Tried making a new operator in Postgre, but it doesn't work with this query for some reason.</p>

## Answers
### Answer ID: 78768717
<p>instead of using a spring-data-jpa @Query on a repository if you are using hibernate you can define a</p>
<pre><code>@org.hibernate.annotations.NamedNativeQuery(name=&quot;MyTable.findByFoo&quot;,query=&quot;SELECT DISTINCT jsonb_path_query(jsonb_column, '$[*] \\?\\? (@.events[*] like_regex &quot;a&quot; flag &quot;i&quot;)') FROM my_table&quot;)
</code></pre>
<p>(note that <code>FindByFoo</code> must match the repository function name)</p>

