# MySQL find and update based on results from 2 tables
[Link to question](https://stackoverflow.com/questions/60240959/mysql-find-and-update-based-on-results-from-2-tables)
**Creation Date:** 1581785505
**Score:** 0
**Tags:** mysql, regex
## Question Body
<p>First off, please note that this is not answered in the question here:
<a href="https://stackoverflow.com/questions/12394506/mysql-update-table-based-on-another-tables-value">MySQL update table based on another tables value</a>
or indeed any other Stack question or answer that I could find!</p>

<p>I converted a forum on a website and now just need to repair the internal URL links on a few hundred of the posts. </p>

<p>Posts are found in the column <strong>post_content</strong> within the table <strong>xyz_posts</strong>  </p>

<pre><code>ID     post_content  

1467  This is great https://example.com/index.php?topic=1234 I really like it
1468  Hello world
1469  Take a look https://example.com/index.php?topic=5678.0
</code></pre>

<p>You can see the URLs are mostly buried in the post text.
Note that the example above can sometimes be written with <strong>topic=1234.0</strong> at the end, although it is actually stored in the database as a value of 1234. I don't want to rewrite the url and accidentally keep the .0</p>

<p>Here's an example of how I need that table to look:</p>

<pre><code>ID     post_content  

1467  This is great https://example.com/finished-page/ I really like it
1468  Hello world
1469  Take a look https://example.com/another-page/
</code></pre>

<p>So, the table <strong>xyz_converter</strong> maps the old topic number to the new post ID like this:</p>

<pre><code>meta_key             meta_value     value_id  

_bbp_old_topic_id    1234           15675
_bbp_old_reply_id    1234           17439

</code></pre>

<p>Caveat here, the number 1234 also exists in this table for forum replies which we don't want, but the meta_key and value_id are different for those as shown. This SQL query works to get to the right one:  </p>

<pre><code>SELECT * FROM `xyz_converter` WHERE meta_key LIKE '_bbp_old_topic_id' AND `meta_value` LIKE '1234'
</code></pre>

<p>Also in table <strong>xyz_posts</strong> we map the value_id mentioned above to the post's URL suffix like this:  </p>

<pre><code>ID        post_name

15675     finished-page 
15676     another-page 
</code></pre>

<p>How do I construct a SQL query that will detect the meta_value in one table and then replace it with the correct final URL as mentioned? </p>

<p><strong>PROCESS SUMMARY</strong></p>

<ol>
<li>Detect the URL in <strong>xyz_posts</strong> post_content</li>
<li>Extract the topic number from the URL (eg 1234). If it's 1234.0 then take just 1234</li>
<li>Convert it to a post number in found in <strong>xyz_converter</strong> value_id (eg 15675) ensuring it is found alongside _bbp_old_topic_id</li>
<li>Take the suffix of the URL in <strong>xyz_posts</strong> post_name (eg 'finished-page')</li>
<li>Rewrite the original URL to include the suffix (not forgetting the trailing slashes).</li>
</ol>

<p>I'm using <strong>MySQL 5.7.29</strong> and <strong>PHPMyAdmin</strong>.
I'm fairly new to SQL queries and a Regex noob, but willing to learn more!</p>

## Answers
### Answer ID: 60241336
<p>A solution that uses only MySQL commands and works in MySQL 5.7 could be like this.</p>

<p>If <code>.0</code> is present only in the urls you could use a query like this to remove all occurences of <code>.0</code> from <code>post_content</code> in <code>xyz_posts</code>.</p>

<pre><code>UPDATE `xyz_posts` SET post_content=REPLACE(post_content,'.0 ',' ') WHERE post_content LIKE '%topic=%.0 %';
</code></pre>

<p>Then you can use</p>

<pre><code>CREATE TABLE temp_tbl
SELECT CONCAT('index.php?topic=',c.meta_value) as `find_value` ,p.post_name as `replace_value`
FROM `xyz_converter` c
INNER JOIN `xyz_posts` p ON c.value_id=p.id AND `meta_key`='_bbp_old_topic_id'
ORDER BY meta_value DESC;

UPDATE `xyz_posts` p 
INNER JOIN  `temp_tbl` t ON p.post_content LIKE CONCAT('%',t.find_value,'%')
SET p.`post_content`=REPLACE(p.`post_content`,t.find_value,t.replace_value);
</code></pre>

<p>The first command will create a temporary table where the first column will be the value that you want to find and replace like <code>index.php?topic=1234</code> and the second column will be the value you want to be replace with like <code>finished-page</code></p>

<p>The second command will replace <code>posts_content</code> in <code>xyz_posts</code> taking the first column from <code>temp_tbl</code> and replacing it with the second column.</p>

<p>Below an sql fiddle where you can see the solution in action</p>

<p><a href="http://sqlfiddle.com/#!9/651f00/3" rel="nofollow noreferrer">http://sqlfiddle.com/#!9/7bce8c</a></p>

<p>Of course you should first create a copy of your database and try these commands to ensure everything works fine before trying it in your production database.</p>

