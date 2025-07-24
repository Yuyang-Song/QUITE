# Running Wordpress on Docker, NGinx, php &amp; sql - Error establishing a database connection
[Link to question](https://stackoverflow.com/questions/70468090/running-wordpress-on-docker-nginx-php-sql-error-establishing-a-database-co)
**Creation Date:** 1640299772
**Score:** 0
**Tags:** mysql, wordpress, docker
## Question Body
<p>this is a follow up on this question: Running wordpress on docker-compose,nginx, mysql and php</p>
<p>I'll put my configuration down bellow so if anyone needs it feel free to use it.</p>
<p>After I made the connection I still have issue with loading the project. Now I get this error I get: DB error from wordpress</p>
<p>This is the line in that error:</p>
<pre><code>mysqli_real_connect( $this-&gt;dbh, $host, $this-&gt;dbuser, $this-&gt;dbpassword, null, $port, $socket, $client_flags );
</code></pre>
<p>My guess something in that wp-config file is set to a wrong value.</p>
<p>I checked all the wp-config files I could.</p>
<p>I made a new database called &quot;wordpress&quot; and imported data to it via terminal.</p>
<p>I connected to my SQL with username and password so I think that also ok.</p>
<p>The part I think it's wrong is the port and I don't know how to check if its ok.</p>
<p>I can't change the port to 3306 because I can't run docker-compose with it (it will fail because 3306 is taken, so I'm using 3307). I tried to change it into &quot;3306&quot;, &quot;3307&quot; and localhost but it didn't work.</p>
<p>This are the files: docker-compose.yml</p>
<pre><code>version: &quot;3&quot;

services:
  nginx:
    image: nginx
    ports:
      - 8080:80
    volumes:
      - ./src:/src
      - ./site.conf:/etc/nginx/conf.d/default.conf
      - ./wp-config.php:/src/wp-config.php

    links:
      - php
  db:
    image: mysql
    ports:
      - 3307:3306
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: toor
    volumes:
      - db-data:/var/lib/mysql
  php:
    build:
      context: .
      dockerfile: ./php/Dockerfile
    image: php:7-fpm
    volumes:
      - ./src:/src
      - ./wp-config.php:/src/wp-config.php

volumes:
  db-data:
</code></pre>
<p>This is my wp-config:</p>
<pre><code>&lt;?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to &quot;wp-config.php&quot;
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'root' );

/** MySQL database password */
define( 'DB_PASSWORD', 'toor' );

/** MySQL hostname */
define( 'DB_HOST', 'mysql:3307' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'put your unique phrase here' );
define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );
define( 'LOGGED_IN_KEY',    'put your unique phrase here' );
define( 'NONCE_KEY',        'put your unique phrase here' );
define( 'AUTH_SALT',        'put your unique phrase here' );
define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );
define( 'LOGGED_IN_SALT',   'put your unique phrase here' );
define( 'NONCE_SALT',       'put your unique phrase here' );

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', true );

/* Add any custom values between this line and the &quot;stop editing&quot; line. */



/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
</code></pre>
<p>And this is my site.conf file:</p>
<pre><code>server {
    index index.php index.html;
    server_name _;
    error_log  /var/log/nginx/error.log;
    access_log /var/log/nginx/access.log;
    root /src;
    location / {
        # This is cool because no php is touched for static content.
        # include the &quot;?$args&quot; part so non-default permalinks doesn't break when using query string
        try_files $uri $uri/ /index.php?$args;
    }
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }

    #stolen from the nginx.conf
    # BEGIN W3TC Minify cache
    location ~ /wp-content/cache/minify/.*js_gzip$ {
        gzip off;
        types {}
        default_type application/x-javascript;
        add_header Content-Encoding gzip;
        expires 31536000s;
        etag on;
        if_modified_since exact;
        add_header Referrer-Policy &quot;no-referrer-when-downgrade&quot;;
        add_header Vary &quot;Accept-Encoding&quot;;
    }
    location ~ /wp-content/cache/minify/.*css_gzip$ {
        gzip off;
        types {}
        default_type text/css;
        add_header Content-Encoding gzip;
        expires 31536000s;
        etag on;
        if_modified_since exact;
        add_header Referrer-Policy &quot;no-referrer-when-downgrade&quot;;
        add_header Vary &quot;Accept-Encoding&quot;;
    }
    # END W3TC Minify cache
    # BEGIN W3TC Page Cache cache
    location ~ /wp-content/cache/page_enhanced.*gzip$ {
        gzip off;
        types {}
        default_type text/html;
        add_header Content-Encoding gzip;
        etag on;
        if_modified_since exact;
        add_header Referrer-Policy &quot;no-referrer-when-downgrade&quot;;
    }
    # END W3TC Page Cache cache
    # BEGIN W3TC Browser Cache
    gzip on;
    gzip_types text/css text/x-component application/x-javascript application/javascript text/javascript text/x-js text/richtext text/plain text/xsd text/xsl text/xml image/bmp application/java application/msword application/vnd.ms-fontobject application/x-msdownload image/x-icon application/json application/vnd.ms-access video/webm application/vnd.ms-project application/x-font-otf application/vnd.ms-opentype application/vnd.oasis.opendocument.database application/vnd.oasis.opendocument.chart application/vnd.oasis.opendocument.formula application/vnd.oasis.opendocument.graphics application/vnd.oasis.opendocument.spreadsheet application/vnd.oasis.opendocument.text audio/ogg application/pdf application/vnd.ms-powerpoint image/svg+xml application/x-shockwave-flash image/tiff application/x-font-ttf audio/wav application/vnd.ms-write application/font-woff application/font-woff2 application/vnd.ms-excel;
    location ~ \.(css|htc|less|js|js2|js3|js4)$ {
        expires 31536000s;
        etag on;
        if_modified_since exact;
        try_files $uri $uri/ /index.php?$args;
    }
    location ~ \.(html|htm|rtf|rtx|txt|xsd|xsl|xml)$ {
        etag on;
        if_modified_since exact;
        try_files $uri $uri/ /index.php?$args;
    }
    location ~ \.(asf|asx|wax|wmv|wmx|avi|avif|avifs|bmp|class|divx|doc|docx|exe|gif|gz|gzip|ico|jpg|jpeg|jpe|webp|json|mdb|mid|midi|mov|qt|mp3|m4a|mp4|m4v|mpeg|mpg|mpe|webm|mpp|_otf|odb|odc|odf|odg|odp|ods|odt|ogg|ogv|pdf|png|pot|pps|ppt|pptx|ra|ram|svg|svgz|swf|tar|tif|tiff|_ttf|wav|wma|wri|xla|xls|xlsx|xlt|xlw|zip)$ {
        expires 31536000s;
        etag on;
        if_modified_since exact;
        try_files $uri $uri/ /index.php?$args;
    }
    add_header Referrer-Policy &quot;no-referrer-when-downgrade&quot;;
    # END W3TC Browser Cache
    # BEGIN W3TC Minify core
    set $w3tc_enc &quot;&quot;;
    if ($http_accept_encoding ~ gzip) {
        set $w3tc_enc _gzip;
    }
    if (-f $request_filename$w3tc_enc) {
        rewrite (.*) $1$w3tc_enc break;
    }
    rewrite ^/wp-content/cache/minify/ /index.php last;
    # END W3TC Minify core
    # BEGIN W3TC Page Cache core
    set $w3tc_rewrite 1;
    if ($request_method = POST) {
        set $w3tc_rewrite 0;
    }
    if ($query_string != &quot;&quot;) {
        set $w3tc_rewrite 0;
    }
    if ($request_uri !~ \/$) {
        set $w3tc_rewrite 0;
    }
    if ($http_cookie ~* &quot;(comment_author|wp\-postpass|w3tc_logged_out|wordpress_logged_in|wptouch_switch_toggle)&quot;) {
        set $w3tc_rewrite 0;
    }
    set $w3tc_preview &quot;&quot;;
    if ($http_cookie ~* &quot;(w3tc_preview)&quot;) {
        set $w3tc_preview _preview;
    }
    set $w3tc_ssl &quot;&quot;;
    if ($scheme = https) {
        set $w3tc_ssl _ssl;
    }
    if ($http_x_forwarded_proto = 'https') {
        set $w3tc_ssl _ssl;
    }
    set $w3tc_enc &quot;&quot;;
    if ($http_accept_encoding ~ gzip) {
        set $w3tc_enc _gzip;
    }
    if (!-f &quot;$document_root/wp-content/cache/page_enhanced/$http_host/$request_uri/_index$w3tc_ssl$w3tc_preview.html$w3tc_enc&quot;) {
      set $w3tc_rewrite 0;
    }
    if ($w3tc_rewrite = 1) {
        rewrite .* &quot;/wp-content/cache/page_enhanced/$http_host/$request_uri/_index$w3tc_ssl$w3tc_preview.html$w3tc_enc&quot; last;
    }
    # END W3TC Page Cache core

    #end stolen
}
</code></pre>

## Answers
### Answer ID: 70469181
<p>As you guessed the problem comes from the wordpress config file. You're using <code>mysql</code> (image name) as your <code>DB_HOST</code>. You should use the service name instead:</p>
<pre><code>/** MySQL hostname */
define( 'DB_HOST', 'db:3306' );
</code></pre>
<p>I don't think that the port is the problem. You need to use <code>3306</code> since this is port that is configured in <a href="https://github.com/docker-library/mysql/blob/bdf0905b75bc9f7d91cedd859476af8d7629e539/5.7/Dockerfile.debian" rel="nofollow noreferrer">MySQL official image</a>.</p>
<hr />
<h4>A security advice</h4>
<p>Also don't expose your SQL port unless you need to access it from the host.</p>
<pre><code>ports:
  - 3307:3306
</code></pre>
<p>This will create an iptables rule for <code>3307</code> and make it accessible from the outside world. You can expose to the linked services such as your <code>nginx</code> one using :</p>
<pre><code>expose:
  - &quot;3306&quot;
</code></pre>
<p>Or restrict it to localhost:</p>
<pre><code>ports:
  - &quot;127.0.0.1:3307:3306&quot;
</code></pre>

