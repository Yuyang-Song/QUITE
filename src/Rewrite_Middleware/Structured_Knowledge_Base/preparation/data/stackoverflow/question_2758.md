# standard_init_linux.go:195: exec user process caused &quot;no such file or directory&quot;
[Link to question](https://stackoverflow.com/questions/51085604/standard-init-linux-go195-exec-user-process-caused-no-such-file-or-directory)
**Creation Date:** 1530196574
**Score:** 0
**Tags:** docker, docker-compose, dockerfile, docker-machine, aws-codebuild
## Question Body
<p>I pulled up wordpress Dockerfile and Docker entry from Docker hub (<a href="https://github.com/docker-library/wordpress/tree/c919246e5ce9a94cb0ad275072d34563ef2ecc46/php7.2/apache" rel="nofollow noreferrer">https://github.com/docker-library/wordpress/tree/c919246e5ce9a94cb0ad275072d34563ef2ecc46/php7.2/apache</a>) and built the image using AWS code build. It pushes the image to AWS ECR and it does the deployment on ECS. Deployment fails with below code 
standard_init_linux.go:195: exec user process caused "no such file or directory"</p>

<p>I tried few of the fixes but none of them are working and throwing the same issue
1. I changed #!/bin/bash to #!/bin/sh 
When I am doing the docker build locally on Ec2, deployment works fine. </p>

<p>Any help will be highly appreciated </p>

<p>Dockerfile</p>

<pre><code>FROM php:7.2-apache

# install the PHP extensions we need
RUN set -ex; \
    \
    savedAptMark="$(apt-mark showmanual)"; \
    \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        libjpeg-dev \
        libpng-dev \
    ; \
    \
    docker-php-ext-configure gd --with-png-dir=/usr --with-jpeg-dir=/usr; \
    docker-php-ext-install gd mysqli opcache zip; \
    \
# reset apt-mark's "manual" list so that "purge --auto-remove" will remove all build dependencies
    apt-mark auto '.*' &gt; /dev/null; \
    apt-mark manual $savedAptMark; \
    ldd "$(php -r 'echo ini_get("extension_dir");')"/*.so \
        | awk '/=&gt;/ { print $3 }' \
        | sort -u \
        | xargs -r dpkg-query -S \
        | cut -d: -f1 \
        | sort -u \
        | xargs -rt apt-mark manual; \
    \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
    rm -rf /var/lib/apt/lists/*

# set recommended PHP.ini settings
# see https://secure.php.net/manual/en/opcache.installation.php
RUN { \
        echo 'opcache.memory_consumption=128'; \
        echo 'opcache.interned_strings_buffer=8'; \
        echo 'opcache.max_accelerated_files=4000'; \
        echo 'opcache.revalidate_freq=2'; \
        echo 'opcache.fast_shutdown=1'; \
        echo 'opcache.enable_cli=1'; \
    } &gt; /usr/local/etc/php/conf.d/opcache-recommended.ini

RUN a2enmod rewrite expires

VOLUME /var/www/html

ENV WORDPRESS_VERSION 4.9.6
ENV WORDPRESS_SHA1 40616b40d120c97205e5852c03096115c2fca537

RUN set -ex; \
    curl -o wordpress.tar.gz -fSL "https://wordpress.org/wordpress-${WORDPRESS_VERSION}.tar.gz"; \
    echo "$WORDPRESS_SHA1 *wordpress.tar.gz" | sha1sum -c -; \
# upstream tarballs include ./wordpress/ so this gives us /usr/src/wordpress
    tar -xzf wordpress.tar.gz -C /usr/src/; \
    rm wordpress.tar.gz; \
    chown -R www-data:www-data /usr/src/wordpress

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["apache2-foreground"]
</code></pre>

<p>Docker-entrypoint.sh</p>

<pre><code>#!/bin/sh
set -euo pipefail

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
    local var="$1"
    local fileVar="${var}_FILE"
    local def="${2:-}"
    if [ "${!var:-}" ] &amp;&amp; [ "${!fileVar:-}" ]; then
        echo &gt;&amp;2 "error: both $var and $fileVar are set (but are exclusive)"
        exit 1
    fi
    local val="$def"
    if [ "${!var:-}" ]; then
        val="${!var}"
    elif [ "${!fileVar:-}" ]; then
        val="$(&lt; "${!fileVar}")"
    fi
    export "$var"="$val"
    unset "$fileVar"
}

if [[ "$1" == apache2* ]] || [ "$1" == php-fpm ]; then
    if [ "$(id -u)" = '0' ]; then
        case "$1" in
            apache2*)
                user="${APACHE_RUN_USER:-www-data}"
                group="${APACHE_RUN_GROUP:-www-data}"
                ;;
            *) # php-fpm
                user='www-data'
                group='www-data'
                ;;
        esac
    else
        user="$(id -u)"
        group="$(id -g)"
    fi

    if ! [ -e index.php -a -e wp-includes/version.php ]; then
        echo &gt;&amp;2 "WordPress not found in $PWD - copying now..."
        if [ "$(ls -A)" ]; then
            echo &gt;&amp;2 "WARNING: $PWD is not empty - press Ctrl+C now if this is an error!"
            ( set -x; ls -A; sleep 10 )
        fi
        tar --create \
            --file - \
            --one-file-system \
            --directory /usr/src/wordpress \
            --owner "$user" --group "$group" \
            . | tar --extract --file -
        echo &gt;&amp;2 "Complete! WordPress has been successfully copied to $PWD"
        if [ ! -e .htaccess ]; then
            # NOTE: The "Indexes" option is disabled in the php:apache base image
            cat &gt; .htaccess &lt;&lt;-'EOF'
                # BEGIN WordPress
                &lt;IfModule mod_rewrite.c&gt;
                RewriteEngine On
                RewriteBase /
                RewriteRule ^index\.php$ - [L]
                RewriteCond %{REQUEST_FILENAME} !-f
                RewriteCond %{REQUEST_FILENAME} !-d
                RewriteRule . /index.php [L]
                &lt;/IfModule&gt;
                # END WordPress
            EOF
            chown "$user:$group" .htaccess
        fi
    fi

    # TODO handle WordPress upgrades magically in the same way, but only if wp-includes/version.php's $wp_version is less than /usr/src/wordpress/wp-includes/version.php's $wp_version

    # allow any of these "Authentication Unique Keys and Salts." to be specified via
    # environment variables with a "WORDPRESS_" prefix (ie, "WORDPRESS_AUTH_KEY")
    uniqueEnvs=(
        AUTH_KEY
        SECURE_AUTH_KEY
        LOGGED_IN_KEY
        NONCE_KEY
        AUTH_SALT
        SECURE_AUTH_SALT
        LOGGED_IN_SALT
        NONCE_SALT
    )
    envs=(
        WORDPRESS_DB_HOST
        WORDPRESS_DB_USER
        WORDPRESS_DB_PASSWORD
        WORDPRESS_DB_NAME
        "${uniqueEnvs[@]/#/WORDPRESS_}"
        WORDPRESS_TABLE_PREFIX
        WORDPRESS_DEBUG
    )
    haveConfig=
    for e in "${envs[@]}"; do
        file_env "$e"
        if [ -z "$haveConfig" ] &amp;&amp; [ -n "${!e}" ]; then
            haveConfig=1
        fi
    done

    # linking backwards-compatibility
    if [ -n "${!MYSQL_ENV_MYSQL_*}" ]; then
        haveConfig=1
        # host defaults to "mysql" below if unspecified
        : "${WORDPRESS_DB_USER:=${MYSQL_ENV_MYSQL_USER:-root}}"
        if [ "$WORDPRESS_DB_USER" = 'root' ]; then
            : "${WORDPRESS_DB_PASSWORD:=${MYSQL_ENV_MYSQL_ROOT_PASSWORD:-}}"
        else
            : "${WORDPRESS_DB_PASSWORD:=${MYSQL_ENV_MYSQL_PASSWORD:-}}"
        fi
        : "${WORDPRESS_DB_NAME:=${MYSQL_ENV_MYSQL_DATABASE:-}}"
    fi

    # only touch "wp-config.php" if we have environment-supplied configuration values
    if [ "$haveConfig" ]; then
        : "${WORDPRESS_DB_HOST:=mysql}"
        : "${WORDPRESS_DB_USER:=root}"
        : "${WORDPRESS_DB_PASSWORD:=}"
        : "${WORDPRESS_DB_NAME:=wordpress}"

        # version 4.4.1 decided to switch to windows line endings, that breaks our seds and awks
        # https://github.com/docker-library/wordpress/issues/116
        # https://github.com/WordPress/WordPress/commit/1acedc542fba2482bab88ec70d4bea4b997a92e4
        sed -ri -e 's/\r$//' wp-config*

        if [ ! -e wp-config.php ]; then
            awk '/^\/\*.*stop editing.*\*\/$/ &amp;&amp; c == 0 { c = 1; system("cat") } { print }' wp-config-sample.php &gt; wp-config.php &lt;&lt;'EOPHP'
// If we're behind a proxy server and using HTTPS, we need to alert Wordpress of that fact
// see also http://codex.wordpress.org/Administration_Over_SSL#Using_a_Reverse_Proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) &amp;&amp; $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
EOPHP
            chown "$user:$group" wp-config.php
        fi

        # see http://stackoverflow.com/a/2705678/433558
        sed_escape_lhs() {
            echo "$@" | sed -e 's/[]\/$*.^|[]/\\&amp;/g'
        }
        sed_escape_rhs() {
            echo "$@" | sed -e 's/[\/&amp;]/\\&amp;/g'
        }
        php_escape() {
            local escaped="$(php -r 'var_export(('"$2"') $argv[1]);' -- "$1")"
            if [ "$2" = 'string' ] &amp;&amp; [ "${escaped:0:1}" = "'" ]; then
                escaped="${escaped//$'\n'/"' + \"\\n\" + '"}"
            fi
            echo "$escaped"
        }
        set_config() {
            key="$1"
            value="$2"
            var_type="${3:-string}"
            start="(['\"])$(sed_escape_lhs "$key")\2\s*,"
            end="\);"
            if [ "${key:0:1}" = '$' ]; then
                start="^(\s*)$(sed_escape_lhs "$key")\s*="
                end=";"
            fi
            sed -ri -e "s/($start\s*).*($end)$/\1$(sed_escape_rhs "$(php_escape "$value" "$var_type")")\3/" wp-config.php
        }

        set_config 'DB_HOST' "$WORDPRESS_DB_HOST"
        set_config 'DB_USER' "$WORDPRESS_DB_USER"
        set_config 'DB_PASSWORD' "$WORDPRESS_DB_PASSWORD"
        set_config 'DB_NAME' "$WORDPRESS_DB_NAME"

        for unique in "${uniqueEnvs[@]}"; do
            uniqVar="WORDPRESS_$unique"
            if [ -n "${!uniqVar}" ]; then
                set_config "$unique" "${!uniqVar}"
            else
                # if not specified, let's generate a random value
                currentVal="$(sed -rn -e "s/define\((([\'\"])$unique\2\s*,\s*)(['\"])(.*)\3\);/\4/p" wp-config.php)"
                if [ "$currentVal" = 'put your unique phrase here' ]; then
                    set_config "$unique" "$(head -c1m /dev/urandom | sha1sum | cut -d' ' -f1)"
                fi
            fi
        done

        if [ "$WORDPRESS_TABLE_PREFIX" ]; then
            set_config '$table_prefix' "$WORDPRESS_TABLE_PREFIX"
        fi

        if [ "$WORDPRESS_DEBUG" ]; then
            set_config 'WP_DEBUG' 1 boolean
        fi

        TERM=dumb php -- &lt;&lt;'EOPHP'
&lt;?php
// database might not exist, so let's try creating it (just to be safe)
$stderr = fopen('php://stderr', 'w');
// https://codex.wordpress.org/Editing_wp-config.php#MySQL_Alternate_Port
//   "hostname:port"
// https://codex.wordpress.org/Editing_wp-config.php#MySQL_Sockets_or_Pipes
//   "hostname:unix-socket-path"
list($host, $socket) = explode(':', getenv('WORDPRESS_DB_HOST'), 2);
$port = 0;
if (is_numeric($socket)) {
    $port = (int) $socket;
    $socket = null;
}
$user = getenv('WORDPRESS_DB_USER');
$pass = getenv('WORDPRESS_DB_PASSWORD');
$dbName = getenv('WORDPRESS_DB_NAME');
$maxTries = 10;
do {
    $mysql = new mysqli($host, $user, $pass, '', $port, $socket);
    if ($mysql-&gt;connect_error) {
        fwrite($stderr, "\n" . 'MySQL Connection Error: (' . $mysql-&gt;connect_errno . ') ' . $mysql-&gt;connect_error . "\n");
        --$maxTries;
        if ($maxTries &lt;= 0) {
            exit(1);
        }
        sleep(3);
    }
} while ($mysql-&gt;connect_error);
if (!$mysql-&gt;query('CREATE DATABASE IF NOT EXISTS `' . $mysql-&gt;real_escape_string($dbName) . '`')) {
    fwrite($stderr, "\n" . 'MySQL "CREATE DATABASE" Error: ' . $mysql-&gt;error . "\n");
    $mysql-&gt;close();
    exit(1);
}
$mysql-&gt;close();
EOPHP
    fi

    # now that we're definitely done writing configuration, let's clear out the relevant envrionment variables (so that stray "phpinfo()" calls don't leak secrets from our code)
    for e in "${envs[@]}"; do
        unset "$e"
    done
fi

exec "$@"
</code></pre>

## Answers
### Answer ID: 55794525
<p>Have you tried using the explicit path as follows?
<code>ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]</code></p>

