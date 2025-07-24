# Alternative to setting variables in SELECT for MySQL 8
[Link to question](https://stackoverflow.com/questions/73935896/alternative-to-setting-variables-in-select-for-mysql-8)
**Creation Date:** 1664802245
**Score:** 0
**Tags:** mysql
## Question Body
<p>I have a context where I need to be able to run the same query under MySQL 5 and 8. When running the following SQL query:</p>
<pre class="lang-sql prettyprint-override"><code>SET
    @item_row := 0,
    @var_row := 0;
SELECT
    *
FROM
    (
        SELECT
            @item_row := @item_row + 1 AS `row_nr`,
            `id` AS `order_item_id`
        FROM
            `order_items`
        WHERE
            `order_id` = ?
    ) `items`
    INNER JOIN (
        SELECT
            @var_row := @var_row + 1 AS `row_nr`,
            `index_number`
        FROM
            `recipe_variables`
        WHERE
            `recipe_variables`.`order_id` = ?
            AND `recipe_variables`.`index_number` = 1
    ) `vars` USING (`row_nr`)
    INNER JOIN `order_items`
    ON `order_items`.`id` = `items`.`order_item_id`
WHERE
    `items`.`order_item_id` = ?
</code></pre>
<p>I get the following warning:</p>
<pre><code>setting user variables within expressions is deprecated and will be removed in a future release
</code></pre>
<p>And the results are incorrect. However only under one environment running MySQL 8. On another server running MySQL 8 it works fine, and on yet another running MySQL 5, it too works correctly without warnings.</p>
<p>I know I can rewrite the query to not use variables by using <code>ROW_NUMBER() OVER ()</code> instead, but this is not supported on the old MySQL 5 server that I am not allowed the update for the moment.</p>
<p>I checked their full versions and both MySQL 8 databases return <code>8.0.25</code> (using <code>SELECT VERSION()</code>). What can cause this difference? And how can I change my query such that is still backwards compatible with MySQL 5, but does run without warnings under MySQL 8?</p>

## Answers
### Answer ID: 73938021
<p>The key mistake was using <code>WHERE</code> instead of <code>HAVING</code> in the presence of counter variables, which caused the <code>row_nr</code> to always resolve to 1, due the filter always resulting in at most 1 record (unique identifier). Apparently the semantics of MySQL 5 and 8 differs in this regard, as version 5 behaves the same whether you use <code>WHERE</code> or <code>HAVING</code>.</p>
<p>Using <code>HAVING</code> it now works consistently across environments, except for the warnings only still showing up in the one, but that suffices for my needs. The best solution is to just upgrade that old MySQL 5 server and rewriting the query to use <code>ROW_NUMBER() OVER ()</code>, which will happen in a few months, so I can live with a few warnings for now.</p>
<p>I did add <code>ORDER BY</code> clauses as suggested by @Barmar, as though it returns the records in insertion order in practice, I don't actually have this guarantee according to the semantics of MySQL, so better to just add them to be sure (<code>ORDER BY id ASC</code>). I also added a <code>LIMIT</code> as otherwise the <code>ORDER BY</code> does not need to be adhered to according to the semantics, as I have run into when wanting to <a href="https://mariadb.com/kb/en/mariadb/why-is-order-by-in-a-from-subquery-ignored/" rel="nofollow noreferrer">group by an ordered subquery in MariaDB</a>.</p>

