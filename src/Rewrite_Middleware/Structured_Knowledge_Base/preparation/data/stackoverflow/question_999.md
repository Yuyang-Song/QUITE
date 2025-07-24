# laravel php artisan migrate issue
[Link to question](https://stackoverflow.com/questions/53924237/laravel-php-artisan-migrate-issue)
**Creation Date:** 1545757945
**Score:** 2
**Tags:** mysql, laravel, ubuntu, pdo, vagrant
## Question Body
<p>When I run this command: <code>php artisan migrate</code> I have got an error:</p>

<blockquote>
  <p>Illuminate\Database\QueryException  : could not find driver (SQL:
  select * from information_schema.tables where table_schema = loag and
  table_name = migrations)</p>
</blockquote>

<p>I have set up a vagrant environment with <strong>ubuntu 18.04</strong> and PHP, MySQL with versions 7.2. i edited the <strong>php.ini</strong> file and did all of the 1000 things on 100 sites on the web. i'm getting confused that it still don't work to migrate</p>

<pre><code>composer create-project laravel/laravel projectname
</code></pre>

<p><strong>config/database.php</strong></p>

<pre><code>'mysql' =&gt; [
            'driver' =&gt; 'mysql',
            'host' =&gt; '127.0.0.1',//env('DB_HOST', '127.0.0.1'),
            'port' =&gt; '3306',//env('DB_PORT', '3306'),
            'database' =&gt; 'loag',//env('DB_DATABASE', 'forge'),
            'username' =&gt; 'root',//env('DB_USERNAME', 'forge'),
            'password' =&gt; 'root',//env('DB_PASSWORD', ''),
            'unix_socket' =&gt; '/etc/mysql/mysql.sock',//env('DB_SOCKET', ''),
            'charset' =&gt; 'utf8mb4',
            'collation' =&gt; 'utf8mb4_unicode_ci',
            'prefix' =&gt; '',
            'prefix_indexes' =&gt; true,
            'strict' =&gt; true,
            'engine' =&gt; null,
        ],
</code></pre>

<p><strong>.env</strong></p>

<pre><code>APP_NAME="Laendliche Ostbahnen AG"
APP_ENV=local
APP_KEY=base64:SKuPKct0ug16L4DTEvcFD59YuHKf8znDmQrqG973L6w=
APP_DEBUG=true
APP_URL=http://localhost

LOG_CHANNEL=stack

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=loag
DB_USERNAME=root
DB_PASSWORD=root`
</code></pre>

<p><strong>composer.json</strong></p>

<pre><code>{
    "name": "laravel/laravel",
    "type": "project",
    "description": "The Laravel Framework.",
    "keywords": [
        "framework",
        "laravel"
    ],
    "license": "MIT",
    "require": {
        "php": "^7.1.3",
        "fideloper/proxy": "^4.0",
        "laravel/framework": "5.7.*",
        "laravel/tinker": "^1.0"
    },
    "require-dev": {
        "beyondcode/laravel-dump-server": "^1.0",
        "filp/whoops": "^2.0",
        "fzaninotto/faker": "^1.4",
        "mockery/mockery": "^1.0",
        "nunomaduro/collision": "^2.0",
        "phpunit/phpunit": "^7.0"
    },
...
</code></pre>

<p><strong>installation on ubuntu:enter code here</strong></p>

<pre><code># Set environment variable
DEBIAN_FRONTEND=noninteractive

# Update Packages
apt-get update

# Upgrade Packages
apt-get dist-upgrade

# Apache
apt-get install -y apache2

# Enable Apache Mods
a2enmod rewrite

# Install PHP
apt-get install -y php7.2

# PHP Apache Mod
apt-get install -y libapache2-mod-php7.2

# Restart Apache
service apache2 restart

# PHP Mods
apt-get install -y php7.2-xml
apt-get install -y php7.2-common
apt-get install -y php7.2-zip

# PHP-MYSQL lib
apt-get install -y php7.2-mysql
apt-get install -y mysql-server

# Disable old apache vhosts config and enable the new one
#a2dissite 000-default.conf

# Restart Apache
sudo systemctl restart apache2.service
</code></pre>

<p>DBs in phpmyadmin: (the affected db should be loag(loag and laravel are empty)
information_schema
laravel
loag
mysql
performance_schema
phpmyadmin
sys</p>

<p>need more?</p>

<p>when i do:<code>php artisan migrate</code> the following output is generated:</p>

<pre><code>Illuminate\Database\QueryException  : could not find driver (SQL: select * from information_schema.tables where table_schema = loag and table_name = migrations)

  at C:\Users\Marco Ris\Desktop\Webdevelopment\loag\vendor\laravel\framework\src\Illuminate\Database\Connection.php:664
    660|         // If an exception occurs when attempting to run a query, we'll format the error
    661|         // message to include the bindings with SQL, which will make this exception a
    662|         // lot more helpful to the developer instead of just the database's errors.
    663|         catch (Exception $e) {  &gt; 664|             throw new QueryException(
    665|                 $query, $this-&gt;prepareBindings($bindings), $e
    666|             );
    667|         }
    668|

  Exception trace:

  1   PDOException::("could not find driver")
      C:\Users\Marco Ris\Desktop\Webdevelopment\loag\vendor\laravel\framework\src\Illuminate\Database\Connectors\Connector.php:70

  2   PDO::__construct("mysql:unix_socket=/etc/mysql/mysql.sock;dbname=loag", "root", "root", [])      C:\Users\Marco Ris\Desktop\Webdevelopment\loag\vendor\laravel\framework\src\Illuminate\Database\Connectors\Connector.php:70

  Please use the argument -v to see more details
</code></pre>

## Answers
### Answer ID: 53924277
<p>May be this will solve your problem,</p>

<pre><code>sudo apt-get install php7-mysql
</code></pre>

<p>or</p>

<pre><code>sudo apt-get install php5-mysql
</code></pre>

<p>or</p>

<pre><code>sudo apt-get install php-mysql
</code></pre>

