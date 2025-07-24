# How to use HAVING condition in CodeIgniter mySQL query that is grouping data from three tables with specific values
[Link to question](https://stackoverflow.com/questions/78644692/how-to-use-having-condition-in-codeigniter-mysql-query-that-is-grouping-data-fro)
**Creation Date:** 1718832087
**Score:** 0
**Tags:** mysql, codeigniter-4, codeigniter-query-builder
## Question Body
<p>I've been using CodeIgniter v4 query builder for most of my database needs and all is fine as it's a very readable way to structure queries, but I've come across a query that is quite complex to write, even directly. I'm trying to familiarise myself with subqueries but I'm struggling at the moment.</p>
<p>This is my code so far which produces a result but needs the HAVING elements at the bottom to be refined and working as they have been omitted so far, so those conditions don't feature in the query as it currently stands.</p>
<p>I am selecting specific values from 'members' where a mem_id has more than 3 photos (where a photo has a specifc attribute related to a column in photos) AND where mem_id has more than 3 posts (where a post has a specific attribute related to a column in posts) and then grouping the results in order of 'mem_id'.</p>
<pre><code>$builder = $this-&gt;db-&gt;table('members');
$builder-&gt;select('value1.mem_id, members.value2, members.value3);
$builder-&gt;join('photos', 'photos.mem_id = members.mem_id')
$builder-&gt;join('posts', 'posts.mem_id = members.mem_id');
$builder-&gt;where('posts.accepted', '1');
$builder-&gt;where('posts.status', '1');
$builder-&gt;where('members.regdate &lt;=', '2018-09-09');
$builder-&gt;where('members.lastdate &gt;=', '2019-01-01');
$builder-&gt;where('members.essentials', '1');
$builder-&gt;where('members.smile', '1');
$builder-&gt;groupBy('posts.mem_id');
$builder-&gt;groupBy('photos.mem_id');
$builder-&gt;orderBy('mem_id', 'DESC');
$builder-&gt;having([condition - mem_id has more than 3 posts in posts table]);
$builder-&gt;having([condition - mem_id has more than 3 photos in photos table]);
$query = $builder-&gt;get();
</code></pre>
<p>Table 1, 'members', has various columns. Each row is indexed with a column called 'mem_id', essentially an id of a specific member. Each mem_id is unique and there is only only row per 'mem_id'.</p>
<p>Table 2, 'photos', has data related to photos that are specific to each mem_id. So one mem_id could have multiple rows in this table.</p>
<p>Table 3, 'posts' has data related to posts that are specific to each mem_id. So one mem_id could have multiple post in this table.</p>
<p>Can anyone help with the HAVING element of the query? It probably needs rewriting as a direct query rather than using query builder but I've been struggling to do it that way.</p>
<p>Thanks in advance.</p>
<p>The query returns results but only because there is no HAVING conditions as mentioned. I can't figure out how to integrate those conditions in the query.</p>

