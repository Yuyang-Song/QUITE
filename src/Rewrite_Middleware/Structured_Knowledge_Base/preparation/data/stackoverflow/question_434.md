# Query optimization to reduce execution time
[Link to question](https://stackoverflow.com/questions/25975151/query-optimization-to-reduce-execution-time)
**Creation Date:** 1411391880
**Score:** 1
**Tags:** optimization, query-optimization, database-optimization
## Question Body
<p>Problem: the query shown below is slow, minimum execution time is 3.x sec and as the category id increase in "IN" clause execution of query taking more that a minute.</p>

<p>QUERY:</p>

<pre><code>explain SELECT a.* FROM
label a
INNER JOIN category_label c ON a.id = c.label_id
INNER JOIN product_label p ON a.id = p.label_id 
INNER JOIN product p2 ON p.product_id = p2.id
INNER JOIN category c2 ON p2.category_id = c2.id
INNER JOIN category c3 ON (c2.lft BETWEEN c3.lft AND c3.rgt) 
INNER JOIN user u ON ((u.id = p2.user_id AND u.is_active = 1))
INNER JOIN country c4 ON (p2.country_id = c4.id) 
WHERE (c.category_id IN ('843', '848', '849', '853', '856', '858') AND a.is_filterable = 1 AND a.type &lt;&gt; "textarea" AND c2.rgt = (c2.lft + 1) AND c3.id IN ('843', '848', '849', '853', '856', '858') AND c4.id IN ('190') AND p2.status = 1) 
GROUP BY a.id 
ORDER BY a.sort_order
</code></pre>

<p>Query explanation - </p>

<pre><code>*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: c4
         type: const
possible_keys: PRIMARY
          key: PRIMARY
      key_len: 4
          ref: const
         rows: 1
        Extra: Using index; Using temporary; Using filesort
*************************** 2. row ***************************
           id: 1
  select_type: SIMPLE
        table: c3
         type: range
possible_keys: PRIMARY,lft_rgt_inx
          key: PRIMARY
      key_len: 4
          ref: NULL
         rows: 6
        Extra: Using where
*************************** 3. row ***************************
           id: 1
  select_type: SIMPLE
        table: c
         type: range
possible_keys: PRIMARY,label_id,category_id
          key: PRIMARY
      key_len: 4
          ref: NULL
         rows: 197
        Extra: Using where; Using index; Using join buffer
*************************** 4. row ***************************
           id: 1
  select_type: SIMPLE
        table: a
         type: eq_ref
possible_keys: PRIMARY
          key: PRIMARY
      key_len: 4
          ref: c.label_id
         rows: 1
        Extra: Using where

*************************** 5. row ***************************
           id: 1
  select_type: SIMPLE
        table: p
         type: ref
possible_keys: product_id,label_id
          key: label_id
      key_len: 4
          ref: c.label_id
         rows: 3827
        Extra: 
*************************** 6. row ***************************
           id: 1
  select_type: SIMPLE
        table: p2
         type: eq_ref
possible_keys: PRIMARY,category_id,user_id,country_id
          key: PRIMARY
      key_len: 8
          ref: p.product_id
         rows: 1
        Extra: Using where
*************************** 7. row ***************************
           id: 1
  select_type: SIMPLE
        table: c2
         type: eq_ref
possible_keys: PRIMARY,lft_rgt_inx
          key: PRIMARY
      key_len: 4
          ref: p2.category_id
         rows: 1
        Extra: Using where
*************************** 8. row ***************************
           id: 1
  select_type: SIMPLE
        table: u
         type: eq_ref
possible_keys: PRIMARY
          key: PRIMARY
      key_len: 4
          ref: p2.user_id
         rows: 1
        Extra: Using where


Show create table - 

`labelMaster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(50) NOT NULL COMMENT 'textbox, checkbox, selectbox, textarea',
  `show_filter` tinyint(1) NOT NULL DEFAULT '1',
  `select_all_level` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB 


CREATE TABLE `categoryMaster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `lft` int(11) NOT NULL DEFAULT '0',
  `rgt` int(11) NOT NULL DEFAULT '0',
  `level` tinyint(4) NOT NULL DEFAULT '0',
  `product_count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `lft_rgt_inx` (`lft`,`rgt`),
  KEY `parent_id` (`parent_id`)
) ENGINE=InnoDB 


CREATE TABLE `productMaster` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `category_id` int(11) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '-1' ,
  `user_id` int(11) NOT NULL,
  `label_value_ids` varchar (255),
  `product_source_url` varchar(255) NOT NULL,
  `country_id` int(4) NOT NULL,
  `state_id` int(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `user_id` (`user_id`),
  KEY `x_area_id` (`x_area_id`),
  KEY `state_id` (`state_id`),
  KEY `country_id` (`country_id`),
  FULLTEXT KEY `name` (`name`),
  FULLTEXT KEY `label_value_ids` (`label_value_ids`)
) ENGINE=MyISAM


CREATE TABLE `product_label` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `product_id` bigint(20) NOT NULL,
  `label_id` int(11) NOT NULL,
  `label_value` varchar(1200) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `category_id` (`category_id`),
  KEY `label_id` (`label_id`)
) ENGINE=InnoDB

 CREATE TABLE `label_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label_id` int(11) NOT NULL,
  `value` varchar(255) NOT NULL,
  `sort_order` smallint(6) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `label_id` (`label_id`),
  CONSTRAINT `label_values_ibfk_1` FOREIGN KEY (`label_id`) REFERENCES `label` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB

 CREATE TABLE `category_label` (
  `category_id` int(11) NOT NULL,
  `label_id` int(11) NOT NULL,
  `is_listview` tinyint(1) NOT NULL,
  `sort_order` smallint(2) NOT NULL,
  PRIMARY KEY (`category_id`,`label_id`),
  KEY `label_id` (`label_id`),
  KEY `category_id` (`category_id`)
) ENGINE=MyISAM
</code></pre>

<p>Please suggest me how can i rewrite the query to reduce execution time and make website fast.</p>

<p>I have tried to change database engine.</p>

<p>Please note: The query already using cache.</p>

## Answers
### Answer ID: 25992708
<p>A few observations:you group by a.id ,isn<code>t a.id a primary key?in that case GROUP BY is unnecessary.
Rearrange your WHERE conditions with the most restrictive conditions first,leave the</code>IN<code>conditions last.Just for one value you don't need IN use =.
If the values are</code>INT`,you don't need quotes,mysql knows they are numbers but using quotes will give a slight overhead.</p>

<pre><code>WHERE  a.is_filterable = 1 AND a.type &lt;&gt; "textarea" 
AND c2.rgt = (c2.lft + 1) 
AND c4.id =190 AND p2.status = 1
AND c3.id IN (843, 848, 849, 853, 856, 858) 
AND c.category_id IN (843, 848, 849, 853, 856, 858) 
</code></pre>

<p>On table label(which you don`t have in your question) add </p>

<pre><code>ALTER TABLE `label` add KEY (is_filterable,type)
ALTER TABLE `label` add KEY (sort_order)
</code></pre>

<p>On table category(which you don`t have in your question) add these indexes</p>

<pre><code>ALTER TABLE `category` add KEY (rgt)
ALTER TABLE `category` add KEY (lft)
ALTER TABLE `category` add KEY (lft,rgt)
</code></pre>

<p>On table product(which you don`t have in your question) add an index</p>

<pre><code>ALTER TABLE `product` add KEY (status)
</code></pre>

<p>On user table(which you don`t have in your question) add</p>

<pre><code>ALTER TABLE `user` add KEY (id,is_active)
</code></pre>

<p>These indexes will be most useful with the structure of the above WHERE condition.Let me know how it goes.Make sure the indexes are not already there.</p>

