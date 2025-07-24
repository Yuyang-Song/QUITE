# Can this query be rewritten without UNION, and is it scaleable?
[Link to question](https://stackoverflow.com/questions/14060026/can-this-query-be-rewritten-without-union-and-is-it-scaleable)
**Creation Date:** 1356635916
**Score:** 2
**Tags:** mysql, sql, database-design, join
## Question Body
<p>I have a few tables:</p>

<ul>
<li>In the <code>product</code>-table, I have a list of products.</li>
<li>In the <code>user</code>-table, I have a list of users.</li>
<li>In the <code>group</code>-table, I have groups of users.</li>
<li>IN the <code>group_member</code>-table, I have linked <code>group</code> and <code>member</code> (many-to-many)</li>
<li>In the <code>user_product</code>-table, I have linked <code>user</code> and <code>product</code> (many-to-many)</li>
<li>In the <code>group_product</code>-table, I have linked <code>group</code> and <code>product</code> (many-to-many)</li>
</ul>

<p>So a user could have many products, a product could have many users. A user can be member of many groups, a group could have many members. A group could have many products, a product could have many groups. In other words, a product can have both groups and users.</p>

<p>What I want to ask the database is: "List all the products that a given <code>user</code> has access to, either through a direct relation in the <code>user_product</code>-table, or through the groups that the user is member of. I want the name of the product and the name of the user."</p>

<p>This is the query that I have come up with:</p>

<pre><code># First get all the products the user has access to via a group.
SELECT product.name,
       user.first_name
FROM product
       INNER JOIN group_product
               ON group_product.product_id = product.product_id
       INNER JOIN group
               ON group.group_id = group_product.group_id
       INNER JOIN group_member
               ON group_member.group_id = group.group_id
       INNER JOIN user
               ON user.user_id = group_member.user_id
WHERE user.user_id = 1

UNION 

# Now get all the products via direct access from user_product.
SELECT product.name,
       user.first_name
FROM product
       INNER JOIN user_product
               ON user_product.product_id = product.product_id
       INNER JOIN user
               ON user.user_id = user_product.user_id
WHERE user.user_id = 1
</code></pre>

<p>Is this a good query, or is it better/possible to rewrite this into a JOIN only query? Would this be a fast query if there were 100 000 users, 10 000 groups and 100 products?
Is this a good database design, or is it better to store this logic in another manner?</p>

<p>(This is my first more complex query.)</p>

## Answers
### Answer ID: 14060238
<p>Your query has the correct approach for your data model. The "correctness" of your data model really depends on volumes and frequency of change- you could opt to always store the explicit user-product relationship whenever a user is added to or removed from a group. This is a denormalizing tactic and moves the overhead from querying to updating - usually best not to consider these moves unless performance is tested and deficient.</p>

<p>A very tiny optimisation may be to avoid the join to user and product until after the union. At present you are only selecting the product name and user first_name, but if you were selecting many columns the sort/distinct would involve more work than strictly necessary, so something like:-</p>

<pre><code>select product.name, user.first_name
from
(
select 
group_product.product_id
from  
group_product
inner join group on group.group_id = group_product.group_id
inner join group_member on group_member.group_id = group.group_id
where group_member.user_id = 1
union
select product_id product.name,
from user_product
where user_product.user_id = 1
) as d
inner join product on product.product_id = d.product_id
inner join user on user.user_id = 1
</code></pre>

