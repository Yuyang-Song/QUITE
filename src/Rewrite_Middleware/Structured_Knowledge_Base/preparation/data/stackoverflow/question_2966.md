# Can&#39;t log in to phpMyAdmin with root, but can access MySQL from command line
[Link to question](https://stackoverflow.com/questions/60517353/cant-log-in-to-phpmyadmin-with-root-but-can-access-mysql-from-command-line)
**Creation Date:** 1583280753
**Score:** 0
**Tags:** mysql, phpmyadmin
## Question Body
<p>I'm trying to set up phpMyAdmin on my server. I'm able to access it by going to mydomain.com/phpmyadmin, but when I try to log in, I get the error "Cannot log in to the MySQL server", even though I'm able to log in to MariaDB with the same credentials on the command line.</p>

<p><a href="https://i.sstatic.net/ln8Ke.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/ln8Ke.png" alt="enter image description here"></a></p>

<p>My nginx.conf:</p>

<pre><code>#startup file.
user nginx nginx;

#usually equal to number of CPUs you have. run command "grep processor /proc/cpuinfo | wc -l" to find it
worker_processes  auto;
worker_cpu_affinity auto;

error_log  /var/log/nginx/error.log;
pid        /var/run/nginx.pid;

# Keeps the logs free of messages about not being able to bind().
#daemon     off;

events {
    worker_connections  1024;
}

http {
#   rewrite_log on;

    include mime.types;
    default_type       application/octet-stream;
    access_log         /var/log/nginx/access.log;
    sendfile           on;
#   tcp_nopush         on;
    keepalive_timeout  3;
#   tcp_nodelay        on;
#   gzip               on;
        #php max upload limit cannot be larger than this       
    client_max_body_size 13m;
    index              index.php index.html index.htm;

    # Upstream to abstract backend connection(s) for PHP.
    upstream php {
                #this should match value of "listen" directive in php-fpm pool
        server 127.0.0.1:9000;
    }

    include sites-enabled/*;

    include snippets/phpMyAdmin.conf;

}
</code></pre>

<p>snippets/phpMyAdmin.conf: </p>

<pre><code>server {

server_name mydomain.com;

location /phpmyadmin {
    root /var/www/html;
    index index.php index.html index.htm;

    deny all;
    location ~ ^/phpmyadmin/(.+\.php)$ {
        try_files $uri =404;
        root /var/www/html;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include /etc/nginx/fastcgi_params;
    }

    location ~* ^/phpmyadmin/(.+\.(jpg|jpeg|gif|css|png|js|ico|html|xml|txt))$ {
        root /var/www/html;
    }

}
location /phpMyAdmin {
   rewrite ^/* /phpmyadmin last;
}

}
</code></pre>

<p>config.inc.php: </p>

<pre><code>&lt;?php
/**
 * phpMyAdmin configuration file, you can use it as base for the manual
 * configuration. For easier setup you can use "setup/".
 *
 * All directives are explained in Documentation.html and on phpMyAdmin
 * wiki &lt;http://wiki.phpmyadmin.net&gt;.
 */

/*
 * This is needed for cookie based authentication to encrypt password in
 * cookie
 */
$cfg['blowfish_secret'] = 'xxxxxxxxxxxxxxxxxxxx'; /* YOU MUST FILL IN THIS FOR COOKIE AUTH! */

/**
 * Server(s) configuration
 */
$i = 0;

// The $cfg['Servers'] array starts with $cfg['Servers'][1].  Do not use
// $cfg['Servers'][0]. You can disable a server config entry by setting host
// to ''. If you want more than one server, just copy following section
// (including $i incrementation) serveral times. There is no need to define
// full server array, just define values you need to change.
$i++;
$cfg['Servers'][$i]['host']          = 'localhost'; // MySQL hostname or IP address
$cfg['Servers'][$i]['port']          = '';          // MySQL port - leave blank for default port
$cfg['Servers'][$i]['socket']        = '';          // Path to the socket - leave blank for default socket
$cfg['Servers'][$i]['connect_type']  = 'tcp';       // How to connect to MySQL server ('tcp' or 'socket')
$cfg['Servers'][$i]['extension']     = 'mysqli';    // The php MySQL extension to use ('mysql' or 'mysqli')
$cfg['Servers'][$i]['compress']      = FALSE;       // Use compressed protocol for the MySQL connection
                                                    // (requires PHP &gt;= 4.3.0)
$cfg['Servers'][$i]['controluser']   = '';          // MySQL control user settings
                                                    // (this user must have read-only
$cfg['Servers'][$i]['controlpass']   = '';          // access to the "mysql/user"
                                                    // and "mysql/db" tables).
                                                    // The controluser is also
                                                    // used for all relational
                                                    // features (pmadb)
$cfg['Servers'][$i]['auth_type']     = 'cookie';    // Authentication method (config, http or cookie based)?
$cfg['Servers'][$i]['user']          = '';          // MySQL user
$cfg['Servers'][$i]['password']      = '';          // MySQL password (only needed
                                                    // with 'config' auth_type)
$cfg['Servers'][$i]['only_db']       = '';          // If set to a db-name, only
                                                    // this db is displayed in left frame
                                                    // It may also be an array of db-names, where sorting order is relevant.
$cfg['Servers'][$i]['hide_db']       = '';          // Database name to be hidden from listings
$cfg['Servers'][$i]['verbose']       = '';          // Verbose name for this host - leave blank to show the hostname

$cfg['Servers'][$i]['pmadb']         = '';          // Database used for Relation, Bookmark and PDF Features
                                                    // (see scripts/create_tables.sql)
                                                    //   - leave blank for no support
                                                    //     DEFAULT: 'phpmyadmin'
$cfg['Servers'][$i]['bookmarktable'] = '';          // Bookmark table
                                                    //   - leave blank for no bookmark support
                                                    //     DEFAULT: 'pma_bookmark'
$cfg['Servers'][$i]['relation']      = '';          // table to describe the relation between links (see doc)
                                                    //   - leave blank for no relation-links support
                                                    //     DEFAULT: 'pma_relation'
$cfg['Servers'][$i]['table_info']    = '';          // table to describe the display fields
                                                    //   - leave blank for no display fields support
                                                    //     DEFAULT: 'pma_table_info'
$cfg['Servers'][$i]['table_coords']  = '';          // table to describe the tables position for the PDF schema
                                                    //   - leave blank for no PDF schema support
                                                    //     DEFAULT: 'pma_table_coords'
$cfg['Servers'][$i]['pdf_pages']     = '';          // table to describe pages of relationpdf
                                                    //   - leave blank if you don't want to use this
                                                    //     DEFAULT: 'pma_pdf_pages'
$cfg['Servers'][$i]['column_info']   = '';          // table to store column information
                                                    //   - leave blank for no column comments/mime types
                                                    //     DEFAULT: 'pma_column_info'
$cfg['Servers'][$i]['history']       = '';          // table to store SQL history
                                                    //   - leave blank for no SQL query history
                                                    //     DEFAULT: 'pma_history'
$cfg['Servers'][$i]['verbose_check'] = TRUE;        // set to FALSE if you know that your pma_* tables
                                                    // are up to date. This prevents compatibility
                                                    // checks and thereby increases performance.
$cfg['Servers'][$i]['AllowRoot']     = TRUE;        // whether to allow root login
$cfg['Servers'][$i]['AllowDeny']['order']           // Host authentication order, leave blank to not use
                                     = '';
$cfg['Servers'][$i]['AllowDeny']['rules']           // Host authentication rules, leave blank for defaults
                                     = array();
$cfg['Servers'][$i]['AllowNoPassword']              // Allow logins without a password. Do not change the FALSE
                                     = FALSE;       // default unless you're running a passwordless MySQL server
$cfg['Servers'][$i]['designer_coords']              // Leave blank (default) for no Designer support, otherwise
                                     = '';          // set to suggested 'pma_designer_coords' if really needed
$cfg['Servers'][$i]['bs_garbage_threshold']         // Blobstreaming: Recommented default value from upstream
                                     = 50;          //   DEFAULT: '50'
$cfg['Servers'][$i]['bs_repository_threshold']      // Blobstreaming: Recommented default value from upstream
                                     = '32M';       //   DEFAULT: '32M'
$cfg['Servers'][$i]['bs_temp_blob_timeout']         // Blobstreaming: Recommented default value from upstream
                                     = 600;         //   DEFAULT: '600'
$cfg['Servers'][$i]['bs_temp_log_threshold']        // Blobstreaming: Recommented default value from upstream
                                     = '32M';       //   DEFAULT: '32M'
/*
 * End of servers configuration
 */

/*
 * Directories for saving/loading files from server
 */
$cfg['UploadDir'] = '/var/lib/phpMyAdmin/upload';
$cfg['SaveDir']   = '/var/lib/phpMyAdmin/save';

/*
 * Disable the default warning that is displayed on the DB Details Structure
 * page if any of the required Tables for the relation features is not found
 */
$cfg['PmaNoRelation_DisableWarning'] = TRUE;

/*
 * phpMyAdmin 4.4.x is no longer maintained by upstream, but security fixes
 * are still backported by downstream.
 */
$cfg['VersionCheck'] = FALSE;
?&gt;
</code></pre>

## Answers
### Answer ID: 60532849
<p>Figured it out, hoping this helps someone. Turns out MariaDB was not running. I had run <code>systemctl list-unit-files</code> which showed mariadb.service as "enabled", and I thought this meant the same thing as active.</p>

<p>However, running <code>systemctl mariadb status</code> showed the following:</p>

<pre><code>mysqld_safe Logging to '/var/log/mariadb/mariadb.log'.
mysqld_safe A mysqld process already exists
mariadb.service: main process exited, code=exited, status=1/FAILURE
mariadb.service entered failed state.
mariadb.service failed.
</code></pre>

<p>I ran <code>pkill mysqld</code>, <code>pkill mysqld_ssafe</code>, and <code>systemctl mariadb restart</code>, and voila, was able to log in to phpMyAdmin</p>

