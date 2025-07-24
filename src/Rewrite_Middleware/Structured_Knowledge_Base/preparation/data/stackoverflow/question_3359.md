# How to rewrite Sort.Order parameters for Spring JPA?
[Link to question](https://stackoverflow.com/questions/77147683/how-to-rewrite-sort-order-parameters-for-spring-jpa)
**Creation Date:** 1695277848
**Score:** 0
**Tags:** java, spring, spring-boot, spring-data-jpa
## Question Body
<p>I want to rewrite a sort query:</p>
<p>So far the query was: <code>?sort=lastname&amp;sort=...</code></p>
<pre><code>@GetMapping
public void getPersons(..., Pageable pageable) {
   pageable.getSort().getOrderFor(&quot;lastname&quot;); //TODO replace with 'surname'
}

@Entity
class PersonEntity {
     String lastname;
     //String surname;
}
</code></pre>
<p>Now database fields changed from <code>lastname</code> to <code>surname</code>. Thus I have to rewrite the sort query, but without having API users to change their bookmarks. So that <code>?sort=lastname</code> acts the same as <code>?sort=surname</code>.</p>
<p>How could I achieve that, because neither <code>Pageable</code> nor <code>Sort</code> has <em>setters</em>?</p>
<p>Of course, as suggested by @M. Deinum, I could rewrite the entire Pageable.Sort as follows. But is this really the solution?</p>
<pre><code>    if (pageable != null
            &amp;&amp; pageable.getSort() != null
            &amp;&amp; pageable.getSort().isSorted()
            &amp;&amp; pageable.getSort().getOrderFor(&quot;lastname&quot;) != null) {
        List&lt;Sort.Order&gt; orders = pageable.getSort().stream()
                .map(order -&gt; {
                    String property = order.getProperty();
                    if (StringUtils.equals(property, &quot;lastname&quot;)) 
                           property = &quot;surname&quot;;
                    return new Sort.Order(order.getDirection(), property, order.getNullHandling());
                })
                .collect(Collectors.toList());
        PageRequest.of(pageable.getPageNumber(), pageable.getPageSize(), Sort.by(orders));
   }
</code></pre>

