# Improving query speed by removing sub queries
[Link to question](https://stackoverflow.com/questions/16987993/improving-query-speed-by-removing-sub-queries)
**Creation Date:** 1370619732
**Score:** 0
**Tags:** sql, performance, sqlperformance
## Question Body
<p>I'm looking to speed up this query. At the moment it takes just over 20 seconds to execute which is terrible.</p>

<p>I can't find a way to remove the sub queries by using and JOIN functions.</p>

<p><strong>SQL:</strong></p>

<pre><code>(

    SELECT
        `manual`.`id`,
        `fname`,
        `lname`,
        `email`,
        '' AS `company`,
        '' AS `level`,
        `completed_tests`.`assessment`,
        '' AS `st_ref`,
        '1' AS `manual`,
        `completed_tests`.`percentage`,
        '' AS `last_visit`,
        '' AS `joined`

    FROM
        `manual`

    LEFT JOIN `used_codes` ON `manual`.`id` = `used_codes`.`user` AND `used_codes`.`id` = (SELECT MAX(`id`) FROM `used_codes` WHERE `user` = `manual`.`id` AND `manual` = 1)
    LEFT JOIN `vcode` ON `manual`.`vcode` = `vcode`.`id`
    LEFT JOIN `groups` ON `vcode`.`group` = `groups`.`id`
    LEFT JOIN `completed_tests` ON `manual`.`id` = `completed_tests`.`user` AND `completed_tests`.`id` = (SELECT MAX(`id`) FROM `completed_tests` WHERE `user` = `manual`.`id` AND `manual` = 1)

)
UNION ALL
(

    SELECT
        `users`.`id`,
        `fname`,
        `lname`,
        `email`,
        `company`,
        `users`.`level`,
        `completed_tests`.`assessment`,
        `orders`.`st_ref`,
        '0' AS `manual`,
        `completed_tests`.`percentage`,
        `last_visit`,
        `joined`

    FROM
        `users`

    LEFT JOIN `orders` ON `users`.`id` = `orders`.`user` AND `orders`.`id` = (SELECT MAX(`id`) FROM `orders` WHERE `status` = 3 AND `user` = `users`.`id`)
    LEFT JOIN `used_codes` ON `users`.`id` = `used_codes`.`user` AND `used_codes`.`id` = (SELECT MAX(`id`) FROM `used_codes` WHERE `user` = `users`.`id` AND `manual` = 1)
    LEFT JOIN `vcode` ON `used_codes`.`vcode` = `vcode`.`id`
    LEFT JOIN `groups` ON `vcode`.`group` = `groups`.`id`
    LEFT JOIN `completed_tests` ON `users`.`id` = `completed_tests`.`user` AND `completed_tests`.`id` = (SELECT MAX(`id`) FROM `completed_tests` WHERE `user` = `users`.`id` AND `manual` = 0)

)

ORDER BY `lname` ASC, `fname` ASC;
</code></pre>

<p>To give you an idea of the database structure, there are two main tables, one for <code>users</code> and another for <code>manual</code>.  The other tables hold additional data and are linked with the users's ID and another field called <code>manual</code> to see which database they belong in.</p>

<p>The problem I'm having is that I need the data of that user to show whether they have any additional data in the other tables or not.  When I tested this using JOIN functions, the record would be removed from the results completely.</p>

<p>I think the main part of the query that need rewriting is the <code>LEFT JOIN</code>s.  I can't work out a way that does the same as this: <code>LEFT JOIN orders ON users.id = orders.user AND orders.id = (SELECT MAX(id) FROM orders WHERE status = 3 AND user = users.id)</code></p>

## Answers
### Answer ID: 16989506
<p>What if you take out the sub queries like:</p>

<p><code>
SELECT MAX(<code>id</code>) FROM <code>orders</code> WHERE <code>status</code> = 3 AND <code>user</code> = <code>users</code>.<code>id</code>
</code></p>

<p>Put them into temp tables and index the id. You can definitely index temp tables and I've seen it make a huge difference in performance when I'm trying to optimize sub queries.</p>

<p>Of course you'll have to remove the user = user.id part, but you can keep the status = 3 part.</p>

<p>You pay the price once for a big query (storing all users with that status and indexing the temp table), but then all subsequent calls are very fast.</p>

