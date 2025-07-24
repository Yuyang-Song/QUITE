# Laravel in docker container - can make migration but cannot migrate
[Link to question](https://stackoverflow.com/questions/59078971/laravel-in-docker-container-can-make-migration-but-cannot-migrate)
**Creation Date:** 1574891768
**Score:** 3
**Tags:** laravel, docker
## Question Body
<p>So I've searched this a good amount and everyone says either make the db host in .env file equal to mysql or the docker container ip but both have not worked for me?</p>

<p>I'm pretty sure it's a host issue but I do not know at this point?</p>

<p>Here's my docker-compose.yml file:</p>

<pre><code>version: "2"
services:

  web:
    container_name: algm
    build:
      context: .
      dockerfile: container-build/web/Dockerfile
    environment:
    - MYSQL_DATABASE=dbname
    - MYSQL_USER=dbuser
    - MYSQL_PASSWORD=654321
    - MYSQL_HOST=db
    ports:
    - "8080:80"
    volumes:
    - .:/var/www
    depends_on:
    - db

  db:
    image: mysql:5.7
    ports:
    - "6603:3306"
    environment:
    - MYSQL_ROOT_PASSWORD=654321
    - MYSQL_USER=dbuser
    - MYSQL_PASSWORD=654321
    - MYSQL_DATABASE=dbname
    volumes:
    - "mysql_data:/var/lib/mysql"
    - ./data/schema.sql:/docker-entrypoint-initdb.d/schema.sql

volumes:
  mysql_data: { driver: local }
</code></pre>

<p>Here's my connections in the .env file:</p>

<pre><code>DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=dbname
DB_USERNAME=dbuser
DB_PASSWORD=654321
</code></pre>

<p>so I get into my docker bash by the command:</p>

<pre><code>sudo docker-compose exec web /bin/bash
</code></pre>

<p>and there I can make models and migrations but cannot migrate?  I get the error:</p>

<pre><code> Illuminate\Database\QueryException  : SQLSTATE[HY000] [2002] php_network_getaddresses: getaddrinfo failed: Name or service not known (SQL: select * from information_schema.tables where table_schema = dbname and table_name = migrations and table_type = 'BASE TABLE')

  at /var/www/vendor/laravel/framework/src/Illuminate/Database/Connection.php:665
    661|         // If an exception occurs when attempting to run a query, we'll format the error
    662|         // message to include the bindings with SQL, which will make this exception a
    663|         // lot more helpful to the developer instead of just the database's errors.
    664|         catch (Exception $e) {
  &gt; 665|             throw new QueryException(
    666|                 $query, $this-&gt;prepareBindings($bindings), $e
    667|             );
    668|         }
    669| 

  Exception trace:

  1   PDOException::("PDO::__construct(): php_network_getaddresses: getaddrinfo failed: Name or service not known")
      /var/www/vendor/laravel/framework/src/Illuminate/Database/Connectors/Connector.php:70

  2   PDO::__construct("mysql:host=mysql;port=3306;dbname=dbname", "dbuser", "654321", [])
      /var/www/vendor/laravel/framework/src/Illuminate/Database/Connectors/Connector.php:70

  Please use the argument -v to see more details.
</code></pre>

<p>UPDATE, here's my Dockerfile in case it's needed:</p>

<pre><code>#
# Use this dockerfile to run the application.
#
# Start the server using docker-compose:
#
#   docker-compose build
#   docker-compose up
#
# NOTE: In future examples replace {{volume_name}} with your projects desired volume name
#
# You can install dependencies via the container:
#
#   docker-compose run {{volume_name}} composer install
#
# You can manipulate dev mode from the container:
#
#   docker-compose run {{volume_name}} composer development-enable
#   docker-compose run {{volume_name}} composer development-disable
#   docker-compose run {{volume_name}} composer development-status
#
# OR use plain old docker 
#
#   docker build -f Dockerfile-dev -t {{volume_name}} .
#   docker run -it -p "8080:80" -v $PWD:/var/www {{volume_name}}
#
FROM php:7.2-apache

RUN apt-get update \
 &amp;&amp; apt-get install -y vim git zlib1g-dev mariadb-client libzip-dev \
 &amp;&amp; docker-php-ext-install zip mysqli pdo_mysql \
 &amp;&amp; pecl install xdebug \
 &amp;&amp; docker-php-ext-enable xdebug \
 &amp;&amp; echo 'xdebug.remote_enable=on' &gt;&gt; /usr/local/etc/php/conf.d/xdebug.ini \
 &amp;&amp; echo 'xdebug.remote_host=host.docker.internal' &gt;&gt; /usr/local/etc/php/conf.d/xdebug.ini \
 &amp;&amp; echo 'xdebug.remote_port=9000' &gt;&gt;  /usr/local/etc/php/conf.d/xdebug.ini \
 &amp;&amp; a2enmod rewrite \
 &amp;&amp; sed -i 's!/var/www/html!/var/www/public!g' /etc/apache2/sites-available/000-default.conf \
 &amp;&amp; mv /var/www/html /var/www/public \
 &amp;&amp; curl -sS https://getcomposer.org/installer \
  | php -- --install-dir=/usr/local/bin --filename=composer \
 &amp;&amp; echo "AllowEncodedSlashes On" &gt;&gt; /etc/apache2/apache2.conf

WORKDIR /var/www
</code></pre>

## Answers
### Answer ID: 59079508
<p>I've tried your config and it's working. You just need to change <code>DB_HOST=mysql</code> to your container name <code>DB_HOST=db</code></p>

<pre><code>DB_CONNECTION=mysql
DB_HOST=db
DB_PORT=3306
DB_DATABASE=dbname
DB_USERNAME=dbuser
DB_PASSWORD=654321
</code></pre>

<p>Then go to your app folder inside the container and run <code>php artisan config:clear</code>, <code>php artisan cache:clear</code> and then execute migrations.</p>

