# Select and join relation with more than one result without mapping to one property
[Link to question](https://stackoverflow.com/questions/76972681/select-and-join-relation-with-more-than-one-result-without-mapping-to-one-proper)
**Creation Date:** 1692908257
**Score:** 0
**Tags:** javascript, mysql, node.js, typescript, typeorm
## Question Body
<p>I am trying to perform a SELECT query on a MySQL database using TypeORM. Basically I have the product entity which is related to the medic entity with a many to many relationship. If I were to execute the raw select query from the product table and left or inner join on medic table, for a product that has more than one medic, that product in the results would repeat itself with each medic separately. TypeORM groups and maps the relation to one property. I was not able to find anything about disabling this functionality for a query.</p>
<p>The example seems simple and a raw query would be fit for this specific case but in reality the endpoint accepts many different query parameters, more relations and properties to select and a mix of optional ORDER BY clauses so I'm curious if there is a solution to this before I rewrite the whole method, or if it's obvious and I'm not seeing it.</p>
<p>Raw results example:</p>
<pre><code>{
  &quot;products&quot;: [
    {
      &quot;id&quot;: 1,
      &quot;medic_id&quot;: 1
    },
    {
      &quot;id&quot;: 1,
      &quot;medic_id&quot;: 2
    },
    {
      &quot;id&quot;: 1,
      &quot;medic_id&quot;: 3
    }
  ]
}
</code></pre>
<p>TypeORM results example:</p>
<pre><code>{
  &quot;products&quot;: [
    {
      &quot;id&quot;: 1,
      &quot;medics&quot;: [
        {
          &quot;id&quot;: 1
        },
        {
          &quot;id&quot;: 2
        },
        {
          &quot;id&quot;: 3
        }
      ]
    }
  ]
}

</code></pre>
<p>Desired result example:</p>
<pre><code>{
  &quot;products&quot;: [
    {
      &quot;id&quot;: 1,
      &quot;medic&quot;: {
        &quot;id&quot;: 1
      }
    },
    {
      &quot;id&quot;: 1,
      &quot;medic&quot;: {
        &quot;id&quot;: 2
      }
    },
    {
      &quot;id&quot;: 1,
      &quot;medic&quot;: {
        &quot;id&quot;: 3
      }
    }
  ]
}
</code></pre>
<p>I tried <code>leftJoinAndMapOne</code> and <code>innerJoinAndMapOne</code> but it only brings the first relation.</p>

