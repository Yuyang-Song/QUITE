# Doctrine DQL query with SQL functions
[Link to question](https://stackoverflow.com/questions/9126669/doctrine-dql-query-with-sql-functions)
**Creation Date:** 1328262629
**Score:** 6
**Tags:** php, sql, symfony, doctrine-orm, dql
## Question Body
<p>I'm porting simple web application written in CodeIgniter to Symfony2 bundle. I'm new into Symfony2 and Doctrine and I've a problem with one SQL query, that I want to rewrite in DQL. I've all ready to go in my bundle, I've created Entity class and I'm able to insert data to database and do simple queries in Object-Oriented-Programming way that Symfony2 provides. Unfortunately, I have no idea how to implement this SQL query in DQL:</p>

<pre><code>$sql = "SELECT * FROM t WHERE 
UNIX_TIMESTAMP(t.date) &gt; ".(time()-300)." AND
ROUND(t.x,3) = ".round($x, 3);
</code></pre>

<p>As you can see there are some SQL function calls, that needs to be executed on database server. Doctrine can't understand this calls. For sure, I have an option to quit using Doctrine and do this query using basic PDO inside my Symfony2 bundle, but I would like to take full advantages of using Symfony2 and Doctrine. So I would like to have this done in OOP way or using clever DQL query that understands something like:</p>

<pre><code>$em-&gt;createQuery("SELECT t FROM MyTestBundle:MyEntity t WHERE t.x = :x")
-&gt;setParameter("x", round($x,3));
</code></pre>

<p>but being able to rewrite my SQL query from old application to my new bundle is a must. Please, help me finding right solution.</p>

## Answers
### Answer ID: 33121109
<p>I know I meets a little late but if this allows the other to find an alternative solution : </p>

<p>use bundle : <a href="https://github.com/beberlei/DoctrineExtensions" rel="noreferrer">Doctrine Extensions</a></p>

<p>after configure your config.yml : </p>

<pre><code>doctrine:
    orm:
        dql:
            string_functions:
                UNIX_TIMESTAMP: DoctrineExtensions\Query\Mysql\UnixTimestamp
</code></pre>

### Answer ID: 17591192
<p>Unfortunately you can't use SQL functions in DQL query. So you have 2 options:</p>

<ol>
<li><p>You can create a User Defined Function in DQL. Here is the official documentation of Doctrine on how to do this <a href="http://docs.doctrine-project.org/en/latest/cookbook/dql-user-defined-functions.html" rel="nofollow">http://docs.doctrine-project.org/en/latest/cookbook/dql-user-defined-functions.html</a></p></li>
<li><p>Or you can execute an SQL query directly in doctrine. Here is official documentation for using Native SQL in Doctrine <a href="http://docs.doctrine-project.org/en/latest/reference/native-sql.html" rel="nofollow">http://docs.doctrine-project.org/en/latest/reference/native-sql.html</a></p></li>
</ol>

<p>Judging by the date on the question I don't think this can help you now but I hope it can help others that have the same problem</p>

