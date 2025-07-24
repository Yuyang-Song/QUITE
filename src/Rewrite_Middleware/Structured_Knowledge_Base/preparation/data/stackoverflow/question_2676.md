# Optimize MYSQL in Extra :-Using where; Using temporary; Using filesort
[Link to question](https://stackoverflow.com/questions/46488411/optimize-mysql-in-extra-using-where-using-temporary-using-filesort)
**Creation Date:** 1506686507
**Score:** 0
**Tags:** mysql, sql, database-administration, query-performance
## Question Body
<p>What is the proper indexing ? i rewrite query and table for batter understanding.</p>

<p>I tried given different combinations of indexes for this query but it is still using from using tempory , using filesort etc.</p>

<pre><code>      CREATE TABLE IF NOT EXISTS `test_data` 
     (`table_id` int(11) NOT NULL AUTO_INCREMENT, 
    `id` int(11) NOT NULL,
    `store` varchar(255) NOT  NULL,  
    `brand` varchar(255) DEFAULT NULL,  
     `product` varchar(255)  NOT NULL, 
    `gender_id` int(11) NOT NULL,  
     `availability` int(11) NOT  NULL,  
     PRIMARY KEY (`table_id`),  
     UNIQUE KEY `table_id`  (`table_id`),  
     KEY `id` (`id`),  
     KEY `step_one`  (`product`,`availability`), 
      KEY `step_two`  (`product`,`availability`,`brand`,`store`), 
      KEY `step_three`  (`product`,`availability`,`brand`,`store`,`id`), 
      KEY `step_four`  (`brand`,`store`),   KEY `step_five` (`brand`,`store`,`id`) ) 
 ENGINE=InnoDB ;
</code></pre>

<p>Query :</p>

<pre><code>SELECT id ,store FROM `test_data` WHERE product='dresses' and availability=1
 group by brand order by store limit 10;
</code></pre>

<p>check live database <a href="http://sqlfiddle.com/#!9/5280b1/1" rel="nofollow noreferrer">http://sqlfiddle.com/#!9/5280b1/1</a></p>

