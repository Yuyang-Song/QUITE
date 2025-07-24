# Adjusting Windows Hosts File and .htaccess for local development
[Link to question](https://stackoverflow.com/questions/60794764/adjusting-windows-hosts-file-and-htaccess-for-local-development)
**Creation Date:** 1584837223
**Score:** 0
**Tags:** php, .htaccess, codeigniter, xampp, localhost
## Question Body
<p>I used XAMPP for local development. Normally I would just create different folders in htdocs and I would get all my expected results as needed by adding the right locations in the hosts file.</p>

<p>For example in my htdocs file I would put:</p>

<p>127.0.0.1 website1.com
127.0.0.1 website2.com
127.0.0.2 website3.com</p>

<p>All my projects would call as needed whenever I would use the address in the browser. </p>

<p>I have inherited a project that uses a hacked up version of codeigniter as will as a jacked up .htaccess file. The only way I can get this to work is to put all the project files in the root of htdocs. This is making my htdocs folder very messy. </p>

<p>Can someone please explain how I can fix this? I would like to keep my current structure the way it is. I know it has to do with the way the .htaccess file is written. </p>

<p>here are the files that config:
.htaccess</p>

<pre><code>#RewriteEngine On
#RewriteCond %{REQUEST_FILENAME} !-f
#RewriteCond %{REQUEST_FILENAME} !-d
#RewriteRule ^(.*)$ index.php/$1 [L]

&lt;IfModule mod_rewrite.c&gt;
   RewriteEngine On
   RewriteBase /

RewriteCond %{SERVER_PORT} 80

   #Removes access to the system folder by users.
   #Additionally this will allow you to create a System.php controller,
   #previously this would not have been possible.
   #'system' can be replaced if you have renamed your system folder.
   RewriteCond %{REQUEST_URI} ^system.*
   RewriteRule ^(.*)$ t2v.com/index.php?/$1 [L]

   #When your application folder isn't in the system folder
   #This snippet prevents user access to the application folder
   #Submitted by: Fabdrol
   #Rename 'application' to your applications folder name.
   RewriteCond %{REQUEST_URI} ^application.*
   RewriteRule ^(.*)$ t2v.com/index.php?/$1 [L]

   #Checks to see if the user is attempting to access a valid file,
   #such as an image or css document, if this isn't true it sends the
   #request to index.php
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   RewriteRule ^(.*)$ t2v.com/index.php?/$1 [L]
&lt;/IfModule&gt;

&lt;IfModule !mod_rewrite.c&gt;
   # If we don't have mod_rewrite installed, all 404's
   # can be sent to index.php, and everything works as normal.
   # Submitted by: ElliotHaughin

   ErrorDocument 404 /index.php
&lt;/IfModule&gt;
</code></pre>

<p>.env.development</p>

<pre><code>BASE_URL=http://localname.com
DB_USER=root
DB_PASS=
DB_DATABASE=localdatabase_devdb
</code></pre>

<p>config.php</p>

<pre><code>&lt;?php
defined('BASEPATH') or exit('No direct script access allowed');

/*
|--------------------------------------------------------------------------
| Base Site URL
|--------------------------------------------------------------------------
|
| URL to your CodeIgniter root. Typically this will be your base URL,
| WITH a trailing slash:
|
|   http://example.com/
|
| WARNING: You MUST set this value!
|
| If it is not set, then CodeIgniter will try guess the protocol and path
| your installation, but due to security concerns the hostname will be set
| to $_SERVER['SERVER_ADDR'] if available, or localhost otherwise.
| The auto-detection mechanism exists only for convenience during
| development and MUST NOT be used in production!
|
| If you need to allow multiple domains, remember that this file is still
| a PHP script and you can easily do that on your own.
|
*/
//$config['base_url'] = 'http://inifaresworkshops.com/t3/';
// $config['base_url'] = 'http://dev.time2visit.com'
$config['base_url'] = getenv('BASE_URL');


/*
|--------------------------------------------------------------------------
| Index File
|--------------------------------------------------------------------------
|
| Typically this will be your index.php file, unless you've renamed it to
| something else. If you are using mod_rewrite to remove the page set this
| variable so that it is blank.
|
*/
$config['index_page'] = ''; //index.php

/*
|--------------------------------------------------------------------------
| URI PROTOCOL
|--------------------------------------------------------------------------
|
| This item determines which server global should be used to retrieve the
| URI string.  The default setting of 'REQUEST_URI' works for most servers.
| If your links do not seem to work, try one of the other delicious flavors:
|
| 'REQUEST_URI'    Uses $_SERVER['REQUEST_URI']
| 'QUERY_STRING'   Uses $_SERVER['QUERY_STRING']
| 'PATH_INFO'      Uses $_SERVER['PATH_INFO']
|
| WARNING: If you set this to 'PATH_INFO', URIs will always be URL-decoded!
*/
$config['uri_protocol']    = 'REQUEST_URI';

/*
|--------------------------------------------------------------------------
| URL suffix
|--------------------------------------------------------------------------
|
| This option allows you to add a suffix to all URLs generated by CodeIgniter.
| For more information please see the user guide:
|
| https://codeigniter.com/user_guide/general/urls.html
*/
$config['url_suffix'] = '';

/*
|--------------------------------------------------------------------------
| Default Language
|--------------------------------------------------------------------------
|
| This determines which set of language files should be used. Make sure
| there is an available translation if you intend to use something other
| than english.
|
*/
$config['language']    = 'english';

/*
|--------------------------------------------------------------------------
| Default Character Set
|--------------------------------------------------------------------------
|
| This determines which character set is used by default in various methods
| that require a character set to be provided.
|
| See http://php.net/htmlspecialchars for a list of supported charsets.
|
*/
$config['charset'] = 'UTF-8';

/*
|--------------------------------------------------------------------------
| Enable/Disable System Hooks
|--------------------------------------------------------------------------
|
| If you would like to use the 'hooks' feature you must enable it by
| setting this variable to TRUE (boolean).  See the user guide for details.
|
*/
$config['enable_hooks'] = false;

/*
|--------------------------------------------------------------------------
| Class Extension Prefix
|--------------------------------------------------------------------------
|
| This item allows you to set the filename/classname prefix when extending
| native libraries.  For more information please see the user guide:
|
| https://codeigniter.com/user_guide/general/core_classes.html
| https://codeigniter.com/user_guide/general/creating_libraries.html
|
*/
$config['subclass_prefix'] = 'MY_';

/*
|--------------------------------------------------------------------------
| Composer auto-loading
|--------------------------------------------------------------------------
|
| Enabling this setting will tell CodeIgniter to look for a Composer
| package auto-loader script in application/vendor/autoload.php.
|
|   $config['composer_autoload'] = TRUE;
|
| Or if you have your vendor/ directory located somewhere else, you
| can opt to set a specific path as well:
|
|   $config['composer_autoload'] = '/path/to/vendor/autoload.php';
|
| For more information about Composer, please visit http://getcomposer.org/
|
| Note: This will NOT disable or override the CodeIgniter-specific
|   autoloading (application/config/autoload.php)
*/
$config['composer_autoload'] = 'vendor/autoload.php';

/*
|--------------------------------------------------------------------------
| Allowed URL Characters
|--------------------------------------------------------------------------
|
| This lets you specify which characters are permitted within your URLs.
| When someone tries to submit a URL with disallowed characters they will
| get a warning message.
|
| As a security measure you are STRONGLY encouraged to restrict URLs to
| as few characters as possible.  By default only these are allowed: a-z 0-9~%.:_-
|
| Leave blank to allow all characters -- but only if you are insane.
|
| The configured value is actually a regular expression character group
| and it will be executed as: ! preg_match('/^[&lt;permitted_uri_chars&gt;]+$/i
|
| DO NOT CHANGE THIS UNLESS YOU FULLY UNDERSTAND THE REPERCUSSIONS!!
|
*/
$config['permitted_uri_chars'] = 'a-z 0-9~%.:_\- &amp;';

/*
|--------------------------------------------------------------------------
| Enable Query Strings
|--------------------------------------------------------------------------
|
| By default CodeIgniter uses search-engine friendly segment based URLs:
| example.com/who/what/where/
|
| You can optionally enable standard query string based URLs:
| example.com?who=me&amp;what=something&amp;where=here
|
| Options are: TRUE or FALSE (boolean)
|
| The other items let you set the query string 'words' that will
| invoke your controllers and its functions:
| example.com/index.php?c=controller&amp;m=function
|
| Please note that some of the helpers won't work as expected when
| this feature is enabled, since CodeIgniter is designed primarily to
| use segment based URLs.
|
*/
$config['enable_query_strings'] = FALSE;
$config['controller_trigger'] = 'c';
$config['function_trigger'] = 'm';
$config['directory_trigger'] = 'd';

/*
|--------------------------------------------------------------------------
| Allow $_GET array
|--------------------------------------------------------------------------
|
| By default CodeIgniter enables access to the $_GET array.  If for some
| reason you would like to disable it, set 'allow_get_array' to FALSE.
|
| WARNING: This feature is DEPRECATED and currently available only
|          for backwards compatibility purposes!
|
*/
$config['allow_get_array'] = TRUE;

/*
|--------------------------------------------------------------------------
| Error Logging Threshold
|--------------------------------------------------------------------------
|
| You can enable error logging by setting a threshold over zero. The
| threshold determines what gets logged. Threshold options are:
|
|   0 = Disables logging, Error logging TURNED OFF
|   1 = Error Messages (including PHP errors)
|   2 = Debug Messages
|   3 = Informational Messages
|   4 = All Messages
|
| You can also pass an array with threshold levels to show individual error types
|
|   array(2) = Debug Messages, without Error Messages
|
| For a live site you'll usually only enable Errors (1) to be logged otherwise
| your log files will fill up very fast.
|
*/
$config['log_threshold'] = 0;

/*
|--------------------------------------------------------------------------
| Error Logging Directory Path
|--------------------------------------------------------------------------
|
| Leave this BLANK unless you would like to set something other than the default
| application/logs/ directory. Use a full server path with trailing slash.
|
*/
$config['log_path'] = '';

/*
|--------------------------------------------------------------------------
| Log File Extension
|--------------------------------------------------------------------------
|
| The default filename extension for log files. The default 'php' allows for
| protecting the log files via basic scripting, when they are to be stored
| under a publicly accessible directory.
|
| Note: Leaving it blank will default to 'php'.
|
*/
$config['log_file_extension'] = '';

/*
|--------------------------------------------------------------------------
| Log File Permissions
|--------------------------------------------------------------------------
|
| The file system permissions to be applied on newly created log files.
|
| IMPORTANT: This MUST be an integer (no quotes) and you MUST use octal
|            integer notation (i.e. 0700, 0644, etc.)
*/
$config['log_file_permissions'] = 0644;

/*
|--------------------------------------------------------------------------
| Date Format for Logs
|--------------------------------------------------------------------------
|
| Each item that is logged has an associated date. You can use PHP date
| codes to set your own date formatting
|
*/
$config['log_date_format'] = 'Y-m-d H:i:s';

/*
|--------------------------------------------------------------------------
| Error Views Directory Path
|--------------------------------------------------------------------------
|
| Leave this BLANK unless you would like to set something other than the default
| application/views/errors/ directory.  Use a full server path with trailing slash.
|
*/
$config['error_views_path'] = '';

/*
|--------------------------------------------------------------------------
| Cache Directory Path
|--------------------------------------------------------------------------
|
| Leave this BLANK unless you would like to set something other than the default
| application/cache/ directory.  Use a full server path with trailing slash.
|
*/
$config['cache_path'] = '';

/*
|--------------------------------------------------------------------------
| Cache Include Query String
|--------------------------------------------------------------------------
|
| Whether to take the URL query string into consideration when generating
| output cache files. Valid options are:
|
|   FALSE      = Disabled
|   TRUE       = Enabled, take all query parameters into account.
|                Please be aware that this may result in numerous cache
|                files generated for the same page over and over again.
|   array('q') = Enabled, but only take into account the specified list
|                of query parameters.
|
*/
$config['cache_query_string'] = FALSE;

/*
|--------------------------------------------------------------------------
| Encryption Key
|--------------------------------------------------------------------------
|
| If you use the Encryption class, you must set an encryption key.
| See the user guide for more info.
|
| https://codeigniter.com/user_guide/libraries/encryption.html
|
*/
$config['encryption_key'] = '';

/*
|--------------------------------------------------------------------------
| Session Variables
|--------------------------------------------------------------------------
|
| 'sess_driver'
|
|   The storage driver to use: files, database, redis, memcached
|
| 'sess_cookie_name'
|
|   The session cookie name, must contain only [0-9a-z_-] characters
|
| 'sess_expiration'
|
|   The number of SECONDS you want the session to last.
|   Setting to 0 (zero) means expire when the browser is closed.
|
| 'sess_save_path'
|
|   The location to save sessions to, driver dependent.
|
|   For the 'files' driver, it's a path to a writable directory.
|   WARNING: Only absolute paths are supported!
|
|   For the 'database' driver, it's a table name.
|   Please read up the manual for the format with other session drivers.
|
|   IMPORTANT: You are REQUIRED to set a valid save path!
|
| 'sess_match_ip'
|
|   Whether to match the user's IP address when reading the session data.
|
|   WARNING: If you're using the database driver, don't forget to update
|            your session table's PRIMARY KEY when changing this setting.
|
| 'sess_time_to_update'
|
|   How many seconds between CI regenerating the session ID.
|
| 'sess_regenerate_destroy'
|
|   Whether to destroy session data associated with the old session ID
|   when auto-regenerating the session ID. When set to FALSE, the data
|   will be later deleted by the garbage collector.
|
| Other session cookie settings are shared with the rest of the application,
| except for 'cookie_prefix' and 'cookie_httponly', which are ignored here.
|
*/
$config['sess_driver'] = 'files';
$config['sess_cookie_name'] = 'website_Cart';
$config['sess_expiration'] = 7200;
$config['sess_save_path'] = FCPATH . 'application/cache/';
$config['sess_match_ip'] = FALSE;
$config['sess_time_to_update'] = 300;
$config['sess_regenerate_destroy'] = FALSE;

/*
|--------------------------------------------------------------------------
| Cookie Related Variables
|--------------------------------------------------------------------------
|
| 'cookie_prefix'   = Set a cookie name prefix if you need to avoid collisions
| 'cookie_domain'   = Set to .your-domain.com for site-wide cookies
| 'cookie_path'     = Typically will be a forward slash
| 'cookie_secure'   = Cookie will only be set if a secure HTTPS connection exists.
| 'cookie_httponly' = Cookie will only be accessible via HTTP(S) (no javascript)
|
| Note: These settings (with the exception of 'cookie_prefix' and
|       'cookie_httponly') will also affect sessions.
|
*/
$config['cookie_prefix']    = '';
$config['cookie_domain']    = '';
$config['cookie_path']        = '/';
$config['cookie_secure']    = FALSE;
$config['cookie_httponly']     = FALSE;

/*
|--------------------------------------------------------------------------
| Standardize newlines
|--------------------------------------------------------------------------
|
| Determines whether to standardize newline characters in input data,
| meaning to replace \r\n, \r, \n occurrences with the PHP_EOL value.
|
| WARNING: This feature is DEPRECATED and currently available only
|          for backwards compatibility purposes!
|
*/
$config['standardize_newlines'] = FALSE;

/*
|--------------------------------------------------------------------------
| Global XSS Filtering
|--------------------------------------------------------------------------
|
| Determines whether the XSS filter is always active when GET, POST or
| COOKIE data is encountered
|
| WARNING: This feature is DEPRECATED and currently available only
|          for backwards compatibility purposes!
|
*/
$config['global_xss_filtering'] = FALSE;

/*
|--------------------------------------------------------------------------
| Cross Site Request Forgery
|--------------------------------------------------------------------------
| Enables a CSRF cookie token to be set. When set to TRUE, token will be
| checked on a submitted form. If you are accepting user data, it is strongly
| recommended CSRF protection be enabled.
|
| 'csrf_token_name' = The token name
| 'csrf_cookie_name' = The cookie name
| 'csrf_expire' = The number in seconds the token should expire.
| 'csrf_regenerate' = Regenerate token on every submission
| 'csrf_exclude_uris' = Array of URIs which ignore CSRF checks
*/
$config['csrf_protection'] = TRUE;
$config['csrf_token_name'] = 'website_token';
$config['csrf_cookie_name'] = 'website_User_settings'; //Do not rename to something that mentions Security
$config['csrf_expire'] = 7200;
$config['csrf_regenerate'] = FALSE;
$config['csrf_exclude_uris'] = array('login');

/*
|--------------------------------------------------------------------------
| Output Compression
|--------------------------------------------------------------------------
|
| Enables Gzip output compression for faster page loads.  When enabled,
| the output class will test whether your server supports Gzip.
| Even if it does, however, not all browsers support compression
| so enable only if you are reasonably sure your visitors can handle it.
|
| Only used if zlib.output_compression is turned off in your php.ini.
| Please do not use it together with httpd-level output compression.
|
| VERY IMPORTANT:  If you are getting a blank page when compression is enabled it
| means you are prematurely outputting something to your browser. It could
| even be a line of whitespace at the end of one of your scripts.  For
| compression to work, nothing can be sent before the output buffer is called
| by the output class.  Do not 'echo' any values with compression enabled.
|
*/
$config['compress_output'] = FALSE;

/*
|--------------------------------------------------------------------------
| Master Time Reference
|--------------------------------------------------------------------------
|
| Options are 'local' or any PHP supported timezone. This preference tells
| the system whether to use your server's local time as the master 'now'
| reference, or convert it to the configured one timezone. See the 'date
| helper' page of the user guide for information regarding date handling.
|
*/
$config['time_reference'] = 'local';

/*
|--------------------------------------------------------------------------
| Rewrite PHP Short Tags
|--------------------------------------------------------------------------
|
| If your PHP installation does not have short tag support enabled CI
| can rewrite the tags on-the-fly, enabling you to utilize that syntax
| in your view files.  Options are TRUE or FALSE (boolean)
|
| Note: You need to have eval() enabled for this to work.
|
*/
$config['rewrite_short_tags'] = FALSE;

/*
|--------------------------------------------------------------------------
| Reverse Proxy IPs
|--------------------------------------------------------------------------
|
| If your server is behind a reverse proxy, you must whitelist the proxy
| IP addresses from which CodeIgniter should trust headers such as
| HTTP_X_FORWARDED_FOR and HTTP_CLIENT_IP in order to properly identify
| the visitor's IP address.
|
| You can use both an array or a comma-separated list of proxy addresses,
| as well as specifying whole subnets. Here are a few examples:
|
| Comma-separated:  '10.0.1.200,192.168.5.0/24'
| Array:        array('10.0.1.200', '192.168.5.0/24')
*/
$config['proxy_ips'] = '';
</code></pre>

## Answers
### Answer ID: 60810503
<p>I think you can work it by the virtual host, and you can follow my practice for your reference:</p>

<p><a href="https://github.com/oliguo/Server-Deployment/blob/master/XAMPP.md#virtual-host-setup" rel="nofollow noreferrer">https://github.com/oliguo/Server-Deployment/blob/master/XAMPP.md#virtual-host-setup</a></p>

<p>Edit the file:</p>

<pre><code>sudo nano /opt/lampp/etc/httpd.conf
</code></pre>

<p>Uncomment:</p>

<pre><code>#Include etc/extra/httpd-vhosts.conf
</code></pre>

<p>Two ways you can follow:</p>

<pre><code>1. By the port way: Like 80 to A site, 81 to B site
2. By changing the host file of your pc, like 127.0.0.1 to A site and B site, the apache will pass the traffic to A site and B site when you visit on your browser.
</code></pre>

<p>Then you edit the httpd-vhosts.conf</p>

<pre><code>sudo nano /opt/lampp/etc/extra/httpd-vhosts.conf
</code></pre>

<p>Port way:</p>

<pre><code>NameVirtualHost *:80

  &lt;VirtualHost *:80&gt;
    DocumentRoot /opt/lampp/htdocs/website_a
    ServerName www.website_a.com
    ErrorLog "/opt/lampp/htdocs/website_a/error_log"
  &lt;/VirtualHost&gt;

  NameVirtualHost *:81
  &lt;VirtualHost *:81&gt;
    DocumentRoot /opt/lampp/htdocs/website_b
    ServerName www.website_b.com
    ErrorLog "/opt/lampp/htdocs/website_b/error_log"
  &lt;/VirtualHost&gt;
</code></pre>

<p>Then you visit www.website_a.com, www.website_b.com:81.</p>

<p>Or you can just change the hostfile way by listening same 80 port if you don't w</p>

<pre><code>NameVirtualHost *:80

  &lt;VirtualHost *:80&gt;
    DocumentRoot /opt/lampp/htdocs/website_a
    ServerName www.website_a.com
    ErrorLog "/opt/lampp/htdocs/website_a/error_log"
  &lt;/VirtualHost&gt;

  NameVirtualHost *:80
  &lt;VirtualHost *:80&gt;
    DocumentRoot /opt/lampp/htdocs/website_b
    ServerName www.website_b.com
    ErrorLog "/opt/lampp/htdocs/website_b/error_log"
  &lt;/VirtualHost&gt;
</code></pre>

<p>And restart the XAMPP.</p>

