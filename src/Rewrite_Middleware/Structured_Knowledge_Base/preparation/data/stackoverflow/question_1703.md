# Two level group by in sql server
[Link to question](https://stackoverflow.com/questions/4472985/two-level-group-by-in-sql-server)
**Creation Date:** 1292605894
**Score:** 0
**Tags:** sql-server, sql-server-2005, group-by
## Question Body
<p>I have a query that retrieves a list of received part shipments from plants. The receipt column is stored as total receipts for the day but there are multiple imports through out the day. This is causing our current query to report some shipments several times. (I can't change how the data is stored in the database without causing major issues with other reports)</p>

<p>Current query:</p>

<pre><code>    select ppl.plant_id, ppl.part_id, sum(pol.receipt) reciept
        from purchase_order_levels pol
    join plant_part_levels ppl
        on ppl.id = pol.plant_part_level_id
    join imports im
        on im.id = ppl.import_id
    where im.active = 1 and im.level_date &lt;= '12-17-2010 10:26'
    group by ppl.plant_id, ppl.part_id
</code></pre>

<p>My attempt to retrieve only receipt levels from the end of the day</p>

<pre><code>    select ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0) as level_date, max(pol.receipt) reciept
        from mc_cup_purchase_order_levels pol
    join mc_cup_plant_part_levels ppl
        on ppl.id = pol.plant_part_level_id
    join mc_cup_imports im
        on im.id = ppl.import_id
    where im.active = 1 and im.level_date &lt;= '12-17-2010 10:26'
    group by ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0)
</code></pre>

<p>The above query works but I need to add an additional level of grouping to sum up the receipts when I tried doing that I got a syntax error. It didn't seem to like treating a subquery like a table.</p>

<pre><code>select plant_id, part_id, sum(pol.receipt) from
(
        select ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0) as level_date, max(pol.receipt) reciept
            from mc_cup_purchase_order_levels pol
        join mc_cup_plant_part_levels ppl
            on ppl.id = pol.plant_part_level_id
        join mc_cup_imports im
            on im.id = ppl.import_id
        where im.active = 1 and im.level_date &lt;= '12-17-2010 10:26'
        group by ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0)
)
group by ppl.plant_id, ppl.part_id
</code></pre>

<p>What is the proper way to add a second level of grouping on my data? I'm trying to keep this logic in the database so I don't have to rewrite the application to sum the data in memory.</p>

## Answers
### Answer ID: 51101107
<p>I'm not sure if this works on SqlServer 2005, but at leas in newer versions it should work. You just have to set an alias for the sub-query to be referred as a table.</p>

<pre><code>select plant_id, part_id, sum(pol.receipt) from
(
        select ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0) as level_date, max(pol.receipt) reciept
            from mc_cup_purchase_order_levels pol
        join mc_cup_plant_part_levels ppl
            on ppl.id = pol.plant_part_level_id
        join mc_cup_imports im
            on im.id = ppl.import_id
        where im.active = 1 and im.level_date &lt;= '12-17-2010 10:26'
        group by ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0)
) as tbl
group by tbl.plant_id, tbl.part_id
</code></pre>

### Answer ID: 4473039
<p>Use a Common Table Expression (CTE):</p>

<pre><code>;WITH My_CTE (plant_id, part_id, level_date, receipt) AS
(
select ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0) as level_date, max(pol.receipt) reciept
                from mc_cup_purchase_order_levels pol
            join mc_cup_plant_part_levels ppl
                on ppl.id = pol.plant_part_level_id
            join mc_cup_imports im
                on im.id = ppl.import_id
            where im.active = 1 and im.level_date &lt;= '12-17-2010 10:26'
            group by ppl.plant_id, ppl.part_id, DATEADD(dd, DATEDIFF(dd,0,ppl.level_date), 0)
    )
select plant_id, part_id, sum(receipt) from My_CTE
group by plant_id, part_id
</code></pre>

