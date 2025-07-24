# Object not found! CodeIgniter
[Link to question](https://stackoverflow.com/questions/28466680/object-not-found-codeigniter)
**Creation Date:** 1423697726
**Score:** 0
**Tags:** php, codeigniter-2
## Question Body
<p>Trying to make a simple registration page and it was working until I added 4 more input boxes. And now Im receiving an Object not found.</p>

<p>This is my site atm. <a href="http://68.84.246.160/chat.ty/" rel="nofollow">http://68.84.246.160/chat.ty/</a></p>

<p>Uploaded to GitHub as well. <a href="https://github.com/jamesdlavender/ASSL/tree/master/chat.ty" rel="nofollow">https://github.com/jamesdlavender/ASSL/tree/master/chat.ty</a></p>

<p>view_register.php</p>

<pre><code>&lt;html&gt;
    &lt;head&gt;
        &lt;title&gt;Registration Form&lt;/title&gt;

&lt;style type="text/css"&gt;
    form li {
        list-style: none;
    }

&lt;/style&gt;
    &lt;/head&gt;
    &lt;body&gt;
        &lt;h1&gt;User Registration&lt;/h1&gt;
        &lt;p&gt;Please fill in the details below.&lt;/p&gt;

        &lt;?php

        echo form_open($base_url . 'user/register');

        $username = array(
            'name'      =&gt;      'username',
            'id'        =&gt;      'username',
            'value'     =&gt;      ''

        );
        $name = array(
            'name'      =&gt;      'name',
            'id'        =&gt;      'name',
            'value'     =&gt;      ''

        );
        $email = array(
            'name'      =&gt;      'email',
            'id'        =&gt;      'email',
            'value'     =&gt;      ''

        );
        $password = array(
            'name'      =&gt;      'password',
            'id'        =&gt;      'password',
            'value'     =&gt;      ''

        );
        $password_conf = array(
            'name'      =&gt;      'password_conf',
            'id'        =&gt;      'password_conf',
            'value'     =&gt;      ''

        );       
?&gt;
&lt;ul&gt;
    &lt;li&gt;
    &lt;label&gt;Username&lt;/label&gt;
        &lt;div&gt;
            &lt;?php echo form_input($username); ?&gt;
        &lt;/div&gt;
    &lt;/li&gt;
    &lt;li&gt;
    &lt;label&gt;Name&lt;/label&gt;
        &lt;div&gt;
            &lt;?php echo form_input($name); ?&gt;
        &lt;/div&gt;
    &lt;/li&gt;
    &lt;li&gt;
    &lt;label&gt;Email Address&lt;/label&gt;
        &lt;div&gt;
            &lt;?php echo form_input($email); ?&gt;
        &lt;/div&gt;
    &lt;/li&gt;
    &lt;li&gt;
    &lt;label&gt;Password&lt;/label&gt;
        &lt;div&gt;
            &lt;?php echo form_password($password); ?&gt;
        &lt;/div&gt;
    &lt;/li&gt;
    &lt;li&gt;
    &lt;label&gt;Confirm Password&lt;/label&gt;
        &lt;div&gt;
            &lt;?php echo form_password($password_conf); ?&gt;
        &lt;/div&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;?php echo validation_errors(); ?&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;div&gt;
            &lt;?php echo form_submit(array('name' =&gt; 'register'), 'Register'); ?&gt;

        &lt;/div&gt;
    &lt;/li&gt;
&lt;/ul&gt;        


        &lt;?php echo form_close(); ?&gt;
    &lt;/body&gt;
&lt;/html&gt;
</code></pre>

<p>routes.php</p>

<pre><code>&lt;?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');
/*
| -------------------------------------------------------------------------
| URI ROUTING
| -------------------------------------------------------------------------
| This file lets you re-map URI requests to specific controller functions.
|
| Typically there is a one-to-one relationship between a URL string
| and its corresponding controller class/method. The segments in a
| URL normally follow this pattern:
|
|   example.com/class/method/id/
|
| In some instances, however, you may want to remap this relationship
| so that a different class/function is called than the one
| corresponding to the URL.
|
| Please see the user guide for complete details:
|
|   http://codeigniter.com/user_guide/general/routing.html
|
| -------------------------------------------------------------------------
| RESERVED ROUTES
| -------------------------------------------------------------------------
|
| There area two reserved routes:
|
|   $route['default_controller'] = 'welcome';
|
| This route indicates which controller class should be loaded if the
| URI contains no data. In the above example, the "welcome" class
| would be loaded.
|
|   $route['404_override'] = 'errors/page_missing';
|
| This route will tell the Router what URI segments to use if those provided
| in the URL cannot be matched to a valid route.
|
*/

$route['default_controller'] = "user";
$route['404_override'] = '';


/* End of file routes.php */
/* Location: ./application/config/routes.php */
</code></pre>

<p>user.php</p>

<pre><code>&lt;?php
class User extends CI_Controller {

    function User()
    {
        parent::__construct();

        $this-&gt;view_data['base_url'] = base_url();
    }

    function index()
    {
        $this-&gt;register();

    }

    function register()
    {
        $this-&gt;load-&gt;library('form_validation');

        $this-&gt;form_validation-&gt;set_rules('username', 'Username', 'trim|required|alpha_numeric|min_length[6]');

        if ($this-&gt;form_validation-&gt;run() == FALSE)
        {
            // hasn't been run or there are validation errors
            $this-&gt;load-&gt;view('view_register', $this-&gt;view_data);
        }
        else
        {
            // everything is good - process the form - write the data into the registration database


        }


    }

}
</code></pre>

<p>autoload.php</p>

<pre><code>/*
| -------------------------------------------------------------------
|  Auto-load Libraries
| -------------------------------------------------------------------
| These are the classes located in the system/libraries folder
| or in your application/libraries folder.
|
| Prototype:
|
|   $autoload['libraries'] = array('database', 'session', 'xmlrpc');
*/

$autoload['libraries'] = array('form_validation');


/*
| -------------------------------------------------------------------
|  Auto-load Helper Files
| -------------------------------------------------------------------
| Prototype:
|
|   $autoload['helper'] = array('url', 'file');
*/

$autoload['helper'] = array('url', 'form');


/*
| -------------------------------------------------------------------
|  Auto-load Config files
| -------------------------------------------------------------------
| Prototype:
|
|   $autoload['config'] = array('config1', 'config2');
|
| NOTE: This item is intended for use ONLY if you have created custom
| config files.  Otherwise, leave it blank.
|
*/

$autoload['config'] = array();


/*
| -------------------------------------------------------------------
|  Auto-load Language files
| -------------------------------------------------------------------
| Prototype:
|
|   $autoload['language'] = array('lang1', 'lang2');
|
| NOTE: Do not include the "_lang" part of your file.  For example
| "codeigniter_lang.php" would be referenced as array('codeigniter');
|
*/

$autoload['language'] = array();


/*
| -------------------------------------------------------------------
|  Auto-load Models
| -------------------------------------------------------------------
| Prototype:
|
|   $autoload['model'] = array('model1', 'model2');
|
*/

$autoload['model'] = array();


/* End of file autoload.php */
/* Location: ./application/config/autoload.php */
</code></pre>

<p>config.php</p>

<pre><code>&lt;?php  if ( ! defined('BASEPATH')) exit('No direct script access allowed');

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
| If this is not set then CodeIgniter will guess the protocol, domain and
| path to your installation.
|
*/
$config['base_url'] = '';

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
$config['index_page'] = '';

/*
|--------------------------------------------------------------------------
| URI PROTOCOL
|--------------------------------------------------------------------------
|
| This item determines which server global should be used to retrieve the
| URI string.  The default setting of 'AUTO' works for most servers.
| If your links do not seem to work, try one of the other delicious flavors:
|
| 'AUTO'            Default - auto detects
| 'PATH_INFO'       Uses the PATH_INFO
| 'QUERY_STRING'    Uses the QUERY_STRING
| 'REQUEST_URI'     Uses the REQUEST_URI
| 'ORIG_PATH_INFO'  Uses the ORIG_PATH_INFO
|
*/
$config['uri_protocol'] = 'AUTO';

/*
|--------------------------------------------------------------------------
| URL suffix
|--------------------------------------------------------------------------
|
| This option allows you to add a suffix to all URLs generated by CodeIgniter.
| For more information please see the user guide:
|
| http://codeigniter.com/user_guide/general/urls.html
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
$config['language'] = 'english';

/*
|--------------------------------------------------------------------------
| Default Character Set
|--------------------------------------------------------------------------
|
| This determines which character set is used by default in various methods
| that require a character set to be provided.
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
$config['enable_hooks'] = FALSE;


/*
|--------------------------------------------------------------------------
| Class Extension Prefix
|--------------------------------------------------------------------------
|
| This item allows you to set the filename/classname prefix when extending
| native libraries.  For more information please see the user guide:
|
| http://codeigniter.com/user_guide/general/core_classes.html
| http://codeigniter.com/user_guide/general/creating_libraries.html
|
*/
$config['subclass_prefix'] = 'MY_';


/*
|--------------------------------------------------------------------------
| Allowed URL Characters
|--------------------------------------------------------------------------
|
| This lets you specify with a regular expression which characters are permitted
| within your URLs.  When someone tries to submit a URL with disallowed
| characters they will get a warning message.
|
| As a security measure you are STRONGLY encouraged to restrict URLs to
| as few characters as possible.  By default only these are allowed: a-z 0-9~%.:_-
|
| Leave blank to allow all characters -- but only if you are insane.
|
| DO NOT CHANGE THIS UNLESS YOU FULLY UNDERSTAND THE REPERCUSSIONS!!
|
*/
$config['permitted_uri_chars'] = 'a-z 0-9~%.:_\-';


/*
|--------------------------------------------------------------------------
| Enable Query Strings
|--------------------------------------------------------------------------
|
| By default CodeIgniter uses search-engine friendly segment based URLs:
| example.com/who/what/where/
|
| By default CodeIgniter enables access to the $_GET array.  If for some
| reason you would like to disable it, set 'allow_get_array' to FALSE.
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
$config['allow_get_array']      = TRUE;
$config['enable_query_strings'] = FALSE;
$config['controller_trigger']   = 'c';
$config['function_trigger']     = 'm';
$config['directory_trigger']    = 'd'; // experimental not currently in use

/*
|--------------------------------------------------------------------------
| Error Logging Threshold
|--------------------------------------------------------------------------
|
| If you have enabled error logging, you can set an error threshold to
| determine what gets logged. Threshold options are:
| You can enable error logging by setting a threshold over zero. The
| threshold determines what gets logged. Threshold options are:
|
|   0 = Disables logging, Error logging TURNED OFF
|   1 = Error Messages (including PHP errors)
|   2 = Debug Messages
|   3 = Informational Messages
|   4 = All Messages
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
| application/logs/ folder. Use a full server path with trailing slash.
|
*/
$config['log_path'] = '';

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
| Cache Directory Path
|--------------------------------------------------------------------------
|
| Leave this BLANK unless you would like to set something other than the default
| system/cache/ folder.  Use a full server path with trailing slash.
|
*/
$config['cache_path'] = '';

/*
|--------------------------------------------------------------------------
| Encryption Key
|--------------------------------------------------------------------------
|
| If you use the Encryption class or the Session class you
| MUST set an encryption key.  See the user guide for info.
|
*/
$config['encryption_key'] = '';

/*
|--------------------------------------------------------------------------
| Session Variables
|--------------------------------------------------------------------------
|
| 'sess_cookie_name'        = the name you want for the cookie
| 'sess_expiration'         = the number of SECONDS you want the session to last.
|   by default sessions last 7200 seconds (two hours).  Set to zero for no expiration.
| 'sess_expire_on_close'    = Whether to cause the session to expire automatically
|   when the browser window is closed
| 'sess_encrypt_cookie'     = Whether to encrypt the cookie
| 'sess_use_database'       = Whether to save the session data to a database
| 'sess_table_name'         = The name of the session database table
| 'sess_match_ip'           = Whether to match the user's IP address when reading the session data
| 'sess_match_useragent'    = Whether to match the User Agent when reading the session data
| 'sess_time_to_update'     = how many seconds between CI refreshing Session Information
|
*/
$config['sess_cookie_name']     = 'ci_session';
$config['sess_expiration']      = 7200;
$config['sess_expire_on_close'] = FALSE;
$config['sess_encrypt_cookie']  = FALSE;
$config['sess_use_database']    = FALSE;
$config['sess_table_name']      = 'ci_sessions';
$config['sess_match_ip']        = FALSE;
$config['sess_match_useragent'] = TRUE;
$config['sess_time_to_update']  = 300;

/*
|--------------------------------------------------------------------------
| Cookie Related Variables
|--------------------------------------------------------------------------
|
| 'cookie_prefix' = Set a prefix if you need to avoid collisions
| 'cookie_domain' = Set to .your-domain.com for site-wide cookies
| 'cookie_path'   =  Typically will be a forward slash
| 'cookie_secure' =  Cookies will only be set if a secure HTTPS connection exists.
|
*/
$config['cookie_prefix']    = "";
$config['cookie_domain']    = "";
$config['cookie_path']      = "/";
$config['cookie_secure']    = FALSE;

/*
|--------------------------------------------------------------------------
| Global XSS Filtering
|--------------------------------------------------------------------------
|
| Determines whether the XSS filter is always active when GET, POST or
| COOKIE data is encountered
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
*/
$config['csrf_protection'] = FALSE;
$config['csrf_token_name'] = 'csrf_test_name';
$config['csrf_cookie_name'] = 'csrf_cookie_name';
$config['csrf_expire'] = 7200;

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
| Options are 'local' or 'gmt'.  This pref tells the system whether to use
| your server's local time as the master 'now' reference, or convert it to
| GMT.  See the 'date helper' page of the user guide for information
| regarding date handling.
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
*/
$config['rewrite_short_tags'] = FALSE;


/*
|--------------------------------------------------------------------------
| Reverse Proxy IPs
|--------------------------------------------------------------------------
|
| If your server is behind a reverse proxy, you must whitelist the proxy IP
| addresses from which CodeIgniter should trust the HTTP_X_FORWARDED_FOR
| header in order to properly identify the visitor's IP address.
| Comma-delimited, e.g. '10.0.1.200,10.0.1.201'
|
*/
$config['proxy_ips'] = '';


/* End of file config.php */
/* Location: ./application/config/config.php */
</code></pre>

<p>.htaccess</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
RewriteEngine On
RewriteBase /chat.ty/

#Removes access to the system folder by users.
#Additionally this will allow you to create a System.php controller,
#previously this would not have been possible.
#'system' can be replaced if you have renamed your system folder.
RewriteCond %{REQUEST_URI} ^system.*
RewriteRule ^(.*)$ /index.php?/$1 [L]

#When your application folder isn't in the system folder
#This snippet prevents user access to the application folder
#Submitted by: Fabdrol
#Rename 'application' to your applications folder name.
RewriteCond %{REQUEST_URI} ^application.*
RewriteRule ^(.*)$ /index.php?/$1 [L]

&lt;/IfModule&gt;

&lt;IfModule !mod_rewrite.c&gt;
    # If we don't have mod_rewrite installed, all 404's
    # can be sent to index.php, and everything works as normal.
    # Submitted by: ElliotHaughin

ErrorDocument 404 /index.php
&lt;/IfModule&gt; 
</code></pre>

<p>Any takers? I'm pretty stumped and I'm new with PHP Frameworks. Thanks.</p>

## Answers
### Answer ID: 28467175
<p>Creating a function with the same name as the class is considered as constructor and it's <code>DEPRECATED</code> in <code>php5</code> so try this instead :</p>

<pre><code>class User extends CI_Controller {

    // function User(){
    public function __construct(){
</code></pre>

