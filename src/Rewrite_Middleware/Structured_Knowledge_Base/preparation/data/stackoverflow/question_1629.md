# mysql query, better way to write this?
[Link to question](https://stackoverflow.com/questions/1923318/mysql-query-better-way-to-write-this)
**Creation Date:** 1261070981
**Score:** 0
**Tags:** sql, mysql, database
## Question Body
<p><strong>EDIT</strong>
I'm understand the table is a mess. I took over this project and am rewriting the PHP and making serious changes to the database. I am not asking how I should layout the database. I need to make a quick, temporary fix and am looking for a better way to write the query below.
<strong>END EDIT</strong></p>

<p>Hi there! </p>

<p>So I have this query(below) this is not finished and is getting long. I was wondering if there was a way to shorten it at all, or if there was a better way to go about it..?</p>

<pre><code>SELECT user.*,
cat1id.CategoryName as cat1,
cat2id.CategoryName as cat2,
cat3id.CategoryName as cat3,
cat4id.CategoryName as cat4,
cat5id.CategoryName as cat5,
cat6id.CategoryName as cat6,
cat7id.CategoryName as cat7,
cat8id.CategoryName as cat8,
cat9id.CategoryName as cat9,
cat10id.CategoryName as cat10
FROM users AS user
LEFT JOIN Category cat1id ON user.categoryid = cat1id.id
LEFT JOIN Category cat2id ON user.categoryid_2 = cat2id.id
LEFT JOIN Category cat3id ON user.categoryid_3 = cat3id.id
LEFT JOIN Category cat4id ON user.categoryid_4 = cat4id.id
LEFT JOIN Category cat5id ON user.categoryid_5 = cat5id.id
LEFT JOIN Category cat6id ON user.categoryid_6 = cat6id.id
LEFT JOIN Category cat7id ON user.categoryid_7 = cat7id.id
LEFT JOIN Category cat8id ON user.categoryid_8 = cat8id.id
LEFT JOIN Category cat9id ON user.categoryid_9 = cat9id.id
LEFT JOIN Category cat10id ON user.categoryid_10 = cat10id.id
WHERE user.id = 65447
</code></pre>

<p>Thanks!</p>

## Answers
### Answer ID: 1923460
<p>If you can't change the database, then you're on the right lines. If you're going to have to work with this, then maybe a table or view that converts your mess into something more normalized would be a good idea.</p>

<p>EDIT: if you want to convert this into a view that is (almost) normalized, you could do something like:</p>

<pre><code>CREATE VIEW user_category AS
SELECT users.id as user_id, Category.id as category_id
FROM users INNER JOIN Category ON users.categoryid = Category.id
UNION
SELECT users.id, Category.id
FROM users INNER JOIN Category ON users.categoryid_2 = Category.id
UNION
SELECT users.id, Category.id
FROM users INNER JOIN Category ON users.categoryid_3 = Category.id
....
</code></pre>

<p>etc. This code is untested, but I'm sure you get the idea. You'd have to test the performance and see if it is acceptable, but there aren't any outer joins in there.</p>

### Answer ID: 1925050
<p>Assuming you're stuck with this schema, and knowing that you have PHP available, you could always use PHP to make life a little easier for you. Something like...</p>

<pre><code>$tables = 10;
$query = "SELECT user.*;

for ( $i = 0; $i &lt;= $tables; $i++) {
    $query += ", cat{$i}id.CategoryName as cat{$i} ";
}

$query += " FROM users AS user";

for ( $i = 0; $i &lt;= $tables; $i++) {
    $query += " LEFT JOIN Category cat{$i}id ON user.categoryid = cat{$i}id.id ";
}

$query += "WHERE user.id = 65447";
</code></pre>

<p>(Please excuse my PHP, I'm not familiar with it, but hopefully it's enough to give you an idea)</p>

<p><a href="https://stackoverflow.com/questions/60174/best-way-to-stop-sql-injection-in-php">Also, don't forget to parametize your inputs!</a> </p>

### Answer ID: 1923329
<p>Pick up a book on database design and read about relations...</p>

<p>Edit: generalized to "relations".</p>

### Answer ID: 1923578
<p>I don't envy you this project.  It looks like it's bursting with antipatterns.</p>

<p>Here's a suggestion:  lots of outer joins in a query can be costly.  And getting all those categories in separate columns is awkward.  Try this instead:</p>

<pre><code>SELECT u.*, c.CategoryName
FROM users AS u
LEFT JOIN Category AS c
 ON (c.id IN (u.categoryid,   u.categoryid_2, u.categoryid_3, u.categoryid_4, 
              u.categoryid_5, u.categoryid_6, u.categoryid_7, u.categoryid_8,
              u.categoryid_9, u.categoryid_10))
WHERE u.id = 65447;
</code></pre>

<p>Another trick you can do (given that you tagged this question with <code>mysql</code>):</p>

<pre><code>SELECT u.*, GROUP_CONCAT(c.CategoryName) AS CatList
FROM users AS u
LEFT JOIN Category AS c
 ON (c.id IN (u.categoryid,   u.categoryid_2, u.categoryid_3, u.categoryid_4, 
              u.categoryid_5, u.categoryid_6, u.categoryid_7, u.categoryid_8,
              u.categoryid_9, u.categoryid_10))
WHERE u.id = 65447
GROUP BY u.id;
</code></pre>

<p>This reduces the output to a single row, and all the <code>CategoryName</code> strings are concatenated together, separated by commas.  See <a href="http://dev.mysql.com/doc/refman/5.1/en/group-by-functions.html#function_group-concat" rel="nofollow noreferrer"><code>GROUP_CONCAT()</code></a>.</p>

### Answer ID: 1923501
<p>If you're using Mysql5 you could try writing a view.</p>

<p>so </p>

<pre><code>CREATE VIEW big_damn_query AS 
SELECT user.*,
cat1id.CategoryName as cat1,
cat2id.CategoryName as cat2,
cat3id.CategoryName as cat3,
cat4id.CategoryName as cat4,
cat5id.CategoryName as cat5,
cat6id.CategoryName as cat6,
cat7id.CategoryName as cat7,
cat8id.CategoryName as cat8,
cat9id.CategoryName as cat9,
cat10id.CategoryName as cat10
FROM users AS user
LEFT JOIN Category cat1id ON user.categoryid = cat1id.id
LEFT JOIN Category cat2id ON user.categoryid_2 = cat2id.id
LEFT JOIN Category cat3id ON user.categoryid_3 = cat3id.id
LEFT JOIN Category cat4id ON user.categoryid_4 = cat4id.id
LEFT JOIN Category cat5id ON user.categoryid_5 = cat5id.id
LEFT JOIN Category cat6id ON user.categoryid_6 = cat6id.id
LEFT JOIN Category cat7id ON user.categoryid_7 = cat7id.id
LEFT JOIN Category cat8id ON user.categoryid_8 = cat8id.id
LEFT JOIN Category cat9id ON user.categoryid_9 = cat9id.id
LEFT JOIN Category cat10id ON user.categoryid_10 = cat10id.id;
</code></pre>

<p>then your query will be </p>

<pre><code>SELECT * FROM big_damn_query bdq WHERE bdq.id = 65447
</code></pre>

### Answer ID: 1923489
<p>If you are stuck with this Data Model, I don't know if you can really optimize this SQL very much. However, here are some things you can do to help with the performance of what you have:</p>

<ul>
<li>ensure that all the fields you are using in your Joins are Indexed</li>
<li>save this query as a View in the database.</li>
</ul>

### Answer ID: 1923448
<p>Rather than having a categoryid_x column, your table structure should look something like this: (My syntax may be off a bit, and this is very trimmed down, but it should get you started)</p>

<pre><code>CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE category (
    category_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE user_category (
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
</code></pre>

<p>What this sets up is a "one-to-many" relationship. You will be able to assign any number of categories to any given user.</p>

<p>To retrieve the categories for a given user:</p>

<pre><code>SELECT *
FROM category
WHERE user = 65447;
</code></pre>

### Answer ID: 1923326
<p>Looks like you need to normalise your database schema - the repeated categoryid_<em>n</em> columns in your user table should be taken out into a separate table ideally.</p>

