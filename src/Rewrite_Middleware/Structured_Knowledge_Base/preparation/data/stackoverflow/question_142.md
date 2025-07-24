# MySQL: Comparing dates in where clause with joins
[Link to question](https://stackoverflow.com/questions/14328607/mysql-comparing-dates-in-where-clause-with-joins)
**Creation Date:** 1358205585
**Score:** 1
**Tags:** mysql, join, indexing
## Question Body
<p>I'm having a hard time figuring how to query/index a database.</p>

<p>The situation is pretty simple. Each time a user visits a category, his/her visit date is stored. My goal is to list the categories in which elements have been added after the user's latest visit.</p>

<p>Here are the two tables:</p>

<pre><code>CREATE TABLE `elements` (
  `category_id` int(11) NOT NULL,
  `element_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `added_date` datetime NOT NULL,
  PRIMARY KEY (`category_id`,`element_id`),
  KEY `index_element_id` (`element_id`)
)

CREATE TABLE `categories_views` (
  `member_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `view_date` datetime NOT NULL,
  PRIMARY KEY (`member_id`,`category_id`),
  KEY `index_element_id` (`category_id`)
)
</code></pre>

<p>Query:</p>

<pre><code>SELECT
    categories_views.*,
    elements.category_id
FROM
    elements
    INNER JOIN categories_views ON (categories_views.category_id = elements.category_id)
WHERE
    categories_views.member_id = 1
    AND elements.added_date &gt; categories_views.view_date
GROUP BY elements.category_id
</code></pre>

<p>Explained:</p>

<pre><code>*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: elements
         type: ALL
possible_keys: PRIMARY
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 89057
        Extra: Using temporary; Using filesort
*************************** 2. row ***************************
           id: 1
  select_type: SIMPLE
        table: categories_views
         type: eq_ref
possible_keys: PRIMARY,index_element_id
          key: PRIMARY
      key_len: 8
          ref: const,convert.elements.category_id
         rows: 1
        Extra: Using where
</code></pre>

<p>With about 100k rows in each table, the query is taking around 0.3s, which is too long for something that should be executed for every user action in a web context.</p>

<p>If possible, what indexes should I add, or how should I rewrite this query in order to avoid using filesorts and temporary tables?</p>

## Answers
### Answer ID: 14328852
<p>If each member has a relatively low number of category_views, I suggest testing a different query:</p>

<pre><code>SELECT v.*
  FROM categories_views v
 WHERE v.member_id = 1
   AND EXISTS 
       ( SELECT 1
           FROM elements e
          WHERE e.category_id = v.category_id
            AND e.added_date &gt; v.view_date
       )
</code></pre>

<p>For optimum performance of that query, you'd want to ensure you had indexes:</p>

<pre><code>... ON elements (category_id, added_date)

... ON categories_views (member_id, category_id) 
</code></pre>

<p>NOTE: It looks like the primary key on the <code>categories_views</code> table may be <code>(member_id, category_id)</code>, which means an appropriate index already exists.</p>

<p>I'm assuming (as best as I can figure out from the original query) is that the <code>categories_views</code> table contains only the "latest" view of the category for a user, that is, <code>member_id, category_id</code> is unique. It looks like that has to be the case, if the original query is returning a correct result set (if its only returning categories that have "new" elements added since the "last view" of that category by the user; otherwise, the existence of any "older" <code>view_date</code> values in the <code>categories_views</code> table would trigger the inclusion of the category, even if there were a newer <code>view_date</code> that was later than the latest (max <code>added_date</code>) element in a category.</p>

<p>If that's not the case, i.e. <code>(member_id,category_id)</code> is not unique, then the query would need to be changed.</p>

<hr>

<p>The query in the original question is a bit puzzling, it references <code>element_views</code> as a table name or table alias, but that doesn't appear in the EXPLAIN output. I'm going under the assumption that <code>element_views</code> is meant to be a synonym for <code>categories_views</code>.</p>

<hr>

<p>For the original query, add a covering index on the <code>elements</code> table:</p>

<pre><code> ... ON elements (category_id, added_date)
</code></pre>

<p>The goal there is to get the explain output to show "Using index"</p>

<p>You might also try adding an index:</p>

<pre><code> ... ON categories_views (member_id, category_id, added_date)
</code></pre>

<p>To get all the columns from the categories_view table (for the select list), the query is going to have to visit the pages in the table (unless there's an index that contains all of those columns. The goal would be reduce the number of rows that need to be visited on data pages to find the row, by having all (or most) of the predicates satisfied from the index.</p>

<hr>

<p>Is it necessary to return the <code>category_id</code> column from the <code>elements</code> table? Don't we already know that this is the same value as in the <code>category_id</code> column from the <code>categories_views</code> table, due to the inner join predicate?</p>

<hr>

