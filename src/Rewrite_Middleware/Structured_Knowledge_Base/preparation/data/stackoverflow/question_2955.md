# Symfony queryBuilder, can`t rewrite sql to queryBuidler
[Link to question](https://stackoverflow.com/questions/60035077/symfony-querybuilder-cant-rewrite-sql-to-querybuidler)
**Creation Date:** 1580716157
**Score:** 0
**Tags:** php, sql, symfony, query-builder
## Question Body
<p>I can`t rewrite SQL query to queryBuilder, for my task need only queryBuilder object.
I have this SQL query, I need take from database per each user, orders which be last and have isPaid = 0. </p>

<pre><code> SELECT
        *
    FROM
        orders o
    JOIN
        (
        SELECT
            owner_id,
            MAX(created_at) max_date
        FROM
            orders
        GROUP BY
            owner_id
    ) max_dates
    ON
        o.owner_id = max_dates.owner_id AND o.created_at = max_dates.max_date
    WHERE
        is_paid = 0
</code></pre>

## Answers
### Answer ID: 60037061
<p>Since you join a subquery it might be a bit tricky to transfer this SQL query to DQL. Fortunately, you don't have to. Doctrine ORM allows you to perform a regular SQL query and then map the results back to an object, just like it would with DQL.</p>

<p>You can have a look at Native Queries and ResultSetMapping for this:
<a href="https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/native-sql.html" rel="nofollow noreferrer">https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/native-sql.html</a></p>

<p>In your case it could look something roughly like this in a repository find-method:</p>

<pre class="lang-php prettyprint-override"><code>public function findLatestUnpaidOrders()
{
    $sql = '...'; // Your query

    $rsm = new ResultSetMappingBuilder($this-&gt;em);
    $rsm-&gt;addRootEntityFromClassMetadata(Order::class, 'order');

    $query = $this-&gt;em-&gt;createNativeQuery($sql, $rsm);
    // $query-&gt;setParameter('owner_id', $user-&gt;getId()); // if you later want to pass parameters into your SQL query

    return $query-&gt;getResult();
}
</code></pre>

