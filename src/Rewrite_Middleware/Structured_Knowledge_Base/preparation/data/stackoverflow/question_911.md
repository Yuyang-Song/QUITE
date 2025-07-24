# Add extra SELECT expression result to the existing entity
[Link to question](https://stackoverflow.com/questions/49543031/add-extra-select-expression-result-to-the-existing-entity)
**Creation Date:** 1522266751
**Score:** 1
**Tags:** php, mysql, symfony, doctrine-orm
## Question Body
<p>I have the project that allows to rate a company in many aspects. The following diagram could help you to understand the relations in my database. Of course, I have deleted from the scheme the fields, that are not important in the context of my problem.
<a href="https://i.sstatic.net/RpHYN.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/RpHYN.png" alt="EER diagram"></a>
Currently, in my repository class of the <code>Company</code> entity, I am searching for companies using <code>QueryBuilder</code> and returning an instance of <code>\Doctrine\ORM\Tools\Pagination\Paginator</code>.</p>

<p>The below code is responsible for fetching companies:</p>

<pre><code>public function search(CompanySearchQuery $command): Paginator
{
    $qb = $this-&gt;createQueryBuilder('c')
        -&gt;setFirstResult($command-&gt;getOffset())
        -&gt;setMaxResults($command-&gt;getMaxResults())
        -&gt;orderBy('c.name', 'ASC');

    ... plus extra "where" conditions

    return new Paginator($qb, true);
}
</code></pre>

<p>I wonder how I can attach the average score to each company using <code>QueryBuilder</code> and <code>Paginator</code>.</p>

<p>Here is the native SQL that allows me to get data I need:</p>

<pre><code>SELECT
  c.id,
  c.name,
  AVG(o2.score) as score
FROM
  company c
LEFT JOIN
  opinion o ON c.id = o.company_id
LEFT JOIN
  opinion_scope o2 ON o.id = o2.opinion_id
GROUP BY
  c.id
</code></pre>

<p><strong>My question is:</strong> Is it possible to add <code>averageScore</code> property to the <code>Company</code> class and map it from <code>QueryBuilder</code> result?</p>

<p>I tried to rewrite my SQL query to use with the existing code:</p>

<pre><code>$qb = $this-&gt;createQueryBuilder('c')
    -&gt;select('c', 'AVG(s.score)')
    -&gt;leftJoin('c.opinions', 'o')
    -&gt;leftJoin('o.scopes', 's')
    -&gt;groupBy('c.id')
    -&gt;setFirstResult($command-&gt;getOffset())
    -&gt;setMaxResults($command-&gt;getMaxResults())
    -&gt;orderBy('c.name', 'ASC')
;
</code></pre>

<p>With the above code I get database exception as following:</p>

<pre><code>SQLSTATE[42000]: Syntax error or access violation: 1055 Expression #14 of 
SELECT list is not in GROUP BY clause and contains nonaggregated column 
'database.o1_.score' which is not functionally dependent on columns in GROUP BY
clause; this is incompatible with sql_mode=only_full_group_by").
</code></pre>

<p>The SQL query that is executed for the above QueryBuilder is:</p>

<pre><code>SELECT 
  DISTINCT id_8 
FROM 
  (
    SELECT 
      DISTINCT id_8, 
      name_9 
    FROM 
      (
        SELECT 
          c0_.updated_at AS updated_at_0, 
          c0_.description AS description_1, 
          c0_.website AS website_2, 
          c0_.email AS email_3, 
          c0_.phone AS phone_4, 
          c0_.street AS street_5, 
          c0_.postal_code AS postal_code_6, 
          c0_.city AS city_7, 
          c0_.id AS id_8, 
          c0_.name AS name_9, 
          c0_.slug AS slug_10, 
          c0_.created_at AS created_at_11, 
          AVG(o1_.score) AS sclr_12, 
          o1_.score AS score_13, 
          o1_.opinion_id AS opinion_id_14, 
          o1_.type_id AS type_id_15 
        FROM 
          company c0_ 
          LEFT JOIN opinion o2_ ON c0_.id = o2_.company_id 
          LEFT JOIN opinion_scope o1_ ON o2_.id = o1_.opinion_id 
        GROUP BY 
          c0_.id
      ) dctrn_result_inner 
    ORDER BY 
      name_9 ASC
  ) dctrn_result 
LIMIT 
  2 OFFSET 0
</code></pre>

<p>I do not understand why Doctrine adds the following fragment:</p>

<pre><code>o1_.score AS score_13, 
o1_.opinion_id AS opinion_id_14, 
o1_.type_id AS type_id_15 
</code></pre>

## Answers
### Answer ID: 49543358
<p>The issue seems to be that you're trying to select every column from 'c', which is your resulting table from performing two LEFT JOINs. Instead, you need to be specifying a from clause for the company table:</p>

<pre><code>$qb = $this-&gt;createQueryBuilder()
    -&gt;select('c', 'AVG(s.score)')
    -&gt;from('company', 'c')
    -&gt;leftJoin('c.opinions', 'o')
    -&gt;leftJoin('o.scopes', 's')
    -&gt;groupBy('c.id')
    -&gt;setFirstResult($command-&gt;getOffset())
    -&gt;setMaxResults($command-&gt;getMaxResults())
    -&gt;orderBy('c.name', 'ASC')
;
</code></pre>

<p>This will avoid including o1.score is your returned columns, which is what that error is referencing </p>

