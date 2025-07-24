# Laravel: connecting to the database in the docker/ docker-compose throwing error, &quot;No such file or directory &quot;
[Link to question](https://stackoverflow.com/questions/66295711/laravel-connecting-to-the-database-in-the-docker-docker-compose-throwing-error)
**Creation Date:** 1613849332
**Score:** 0
**Tags:** laravel, docker, docker-compose
## Question Body
<p>I am working on a Laravel 6 application. I am using Docker as my development environment. I am trying to connecting to the database in the docker-compose configuring the variables in the .env file. But it is not working.</p>
<p>This is my docker-compose.yaml file.</p>
<pre><code>version: '3'
services:
  app:
    container_name: coup_app
    build:
      context: .
      dockerfile: .docker/Dockerfile
    image: 'laravelapp'
    ports:
      - 8081:80
    networks:
      - coup-network
    volumes:
      - ./:/var/www/html
      - ./:/var/www/
      - ./ci:/var/www/ci:cached
      - ./vendor:/var/www/vendor:delegated
      - ./storage:/var/www/storage:delegated
      - ./node_modules:/var/www/node_modules:cached
      - ~/.ssh:/root/.ssh:cached
      - ./composer.json:/var/www/composer.json
      - ~/.composer/cache:/root/.composer/cache:delegated
  db:
    container_name: coup_db
    image: library/mariadb:10.4.11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: coup
      MYSQL_USER: coup
      MYSQL_PASSWORD: secret
    volumes:
      - coup-data:/var/lib/mysql
    networks:
      - coup-network
    ports:
      - &quot;33060:3306&quot;
networks:
  coup-network:
    driver: &quot;bridge&quot;
volumes:
  coup-data:
    driver: &quot;local&quot;
</code></pre>
<p>This is my Dockerfile.</p>
<pre><code>FROM php:7.4.1-apache
USER root
WORKDIR /var/www/html
RUN apt-get update &amp;&amp; apt-get install -y \
libpng-dev \
zlib1g-dev \
libxml2-dev \
libzip-dev \
libonig-dev \
zip \
curl \
unzip \
&amp;&amp; docker-php-ext-configure gd \
&amp;&amp; docker-php-ext-install -j$(nproc) gd \
&amp;&amp; docker-php-ext-install pdo_mysql \
&amp;&amp; docker-php-ext-install mysqli \
&amp;&amp; docker-php-ext-install zip \
&amp;&amp; docker-php-source delete
COPY .docker/vhost.conf /etc/apache2/sites-available/000-default.conf
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN chown -R www-data:www-data /var/www/html \
&amp;&amp; a2enmod rewrite
</code></pre>
<p>The followings are the DB credentials in my .env file.</p>
<pre><code>DB_CONNECTION=mysql
DB_HOST=db
DB_PORT=3306
DB_DATABASE=coup
DB_USERNAME=coup
DB_PASSWORD=secret
</code></pre>
<p>When I run the migration, I am getting the following error.</p>
<pre><code>  Illuminate\Database\QueryException  : SQLSTATE[HY000] [2002] No such file or directory (SQL: SHOW FULL TABLES WHERE table_type = 'BASE TABLE')

  at /var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connection.php:669
    665|         // If an exception occurs when attempting to run a query, we'll format the error
    666|         // message to include the bindings with SQL, which will make this exception a
    667|         // lot more helpful to the developer instead of just the database's errors.
    668|         catch (Exception $e) {
  &gt; 669|             throw new QueryException(
    670|                 $query, $this-&gt;prepareBindings($bindings), $e
    671|             );
    672|         }
    673| 

  Exception trace:

  1   PDOException::(&quot;SQLSTATE[HY000] [2002] No such file or directory&quot;)
      /var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connectors/Connector.php:70

  2   PDO::__construct(&quot;mysql:host=localhost;port=3306;dbname=coup&quot;, &quot;coup&quot;, &quot;secret&quot;, [])
      /var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connectors/Connector.php:70
</code></pre>
<p>What is wrong with my configuration and how can I fix it?</p>

## Answers
### Answer ID: 66308924
<p>The problem here is that Laravel is not using the value of <code>DB_HOST</code>: in your <code>.env</code> it is set to <code>DB_HOST=db</code> but the stack trace shows</p>
<blockquote>
<p>2   PDO::__construct(&quot;mysql:host=<strong>localhost</strong>;port=3306;dbname=coup&quot;, &quot;coup&quot;, &quot;secret&quot;, [])
/var/www/html/vendor/laravel/framework/src/Illuminate/Database/Connectors/Connector.php:70</p>
</blockquote>
<p>i.e. Laravel is effectively using <code>localhost</code> instead of <code>db</code> as the host.</p>
<hr />
<h2>Background on the error message</h2>
<p>In case you're wondering why the error message says <em>SQLSTATE[HY000] [2002] <strong>No such file or directory</strong></em>,
from the <a href="https://dev.mysql.com/doc/refman/8.0/en/connecting.html" rel="nofollow noreferrer"><code>mysql</code> docs</a>:</p>
<blockquote>
<ul>
<li><p>If the host is not specified or is <code>localhost</code>, a connection to the local host occurs:</p>
<ul>
<li>On Unix, MySQL programs treat the host name localhost specially, in a way that is likely different from what you expect compared to other network-based programs: the client connects using a Unix socket file. The <code>--socket</code> option or the <code>MYSQL_UNIX_PORT</code> environment variable may be used to specify the socket name.</li>
</ul>
</li>
</ul>
</blockquote>
<p>i.e. instead of trying to establish a <em>network</em> connection to <code>localhost</code> PHP will try to establish a connection via a <em>unix socket</em> by opening its file path (e.g. <code>/var/run/mysqld/mysqld.sock</code>).</p>
<p>Since in your case the database is running in a separate container this local path to the unix socket of the database is not available inside the Laravel container which is why the error message is <em>No such file or directory</em>.</p>

