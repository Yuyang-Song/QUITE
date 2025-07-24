# &quot;Connection refused&quot;, when trying to connect to DB from inside the Docker container
[Link to question](https://stackoverflow.com/questions/47928791/connection-refused-when-trying-to-connect-to-db-from-inside-the-docker-contai)
**Creation Date:** 1513872881
**Score:** 1
**Tags:** php, mysql, database, docker, pdo
## Question Body
<p>I'm having some problems with the following Dockerfile:</p>

<pre><code>FROM php:7.0-apache

RUN a2enmod rewrite

RUN docker-php-ext-install pdo pdo_mysql

COPY php.ini /usr/local/etc/php/
COPY . /var/www/html/
</code></pre>

<p>I'm using the Slim PHP framework and trying to connect to the database, but is returning the following error:</p>

<pre><code>HTTP/1.1 500 Internal Server Error Content-Type: text/html {"error": {"text": SQLSTATE[HY000] [2002] Connection refused}
</code></pre>

<p>Here's the code where the exception is raised:</p>

<pre><code>// Instantiate a database connection
$container['db'] = function ($c) {
    try {
        $db = $c['settings']['db'];

        $pdo = new PDO("mysql:host=" . $db['host'], $db['user'], $db['pass']);  

        $pdo-&gt;setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo-&gt;setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        //Create database if not exists
        $dbname = "`".str_replace("`","``",$db['dbname'])."`";
        $pdo-&gt;query("CREATE DATABASE IF NOT EXISTS $dbname");
        $pdo-&gt;query("use $dbname");

        //Create tables if not exists
        $pdo-&gt;query(
            "CREATE TABLE IF NOT EXISTS `Assets` (
                `id` INT AUTO_INCREMENT NOT NULL,
                `first_property` varchar(50),
                `second_property` varchar(50),
                PRIMARY KEY (`id`))"
        );   

        return $pdo;
    } catch (PDOException $e) {
        return $c['response']
            -&gt;withStatus(500)
            -&gt;withHeader('Content-Type', 'text/html')
            -&gt;write('{"error": {"text": ' . $e-&gt;getMessage() . '}');
    }
};
</code></pre>

<p>Does anyone know where the problem could be?</p>

<p>Thank you in advance!</p>

## Answers
### Answer ID: 47929124
<p>You can create a docker container for MySQL using something like...</p>

<pre><code>docker run --name MySQLDB -v /var/lib/mysql -e MYSQL_ROOT_PASSWORD=rootpwd -d mysql:5.7
</code></pre>

<p>then (assuming linux)</p>

<pre><code>docker inspect MySQLDB | grep IPA
</code></pre>

<p>to get the IP address to use for the connection.</p>

