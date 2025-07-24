# 000webhost failed no such website after login
[Link to question](https://stackoverflow.com/questions/44017714/000webhost-failed-no-such-website-after-login)
**Creation Date:** 1495004332
**Score:** 1
**Tags:** php, codeigniter
## Question Body
<p>I have uploaded website on 000webhost and dont understand where i am doing wrong. When i login in the empty web page appears saying </p>

<blockquote>
  <p>Nothing on yet</p>
</blockquote>

<p>You can also test : <a href="https://cateringservices.000webhostapp.com/" rel="nofollow noreferrer">https://cateringservices.000webhostapp.com/</a>
id: dell
pass:1234
 I ve LoginN controller and observing that it is not entering in else for redirect or loading view. I dont know why. </p>

<p>My controller LoginN:</p>

<pre><code>&lt;?php
defined('BASEPATH') OR exit('No direct script allowed');
class LoginN extends CI_Controller
{
    function __construct() {
        parent::__construct();
        $this-&gt;load-&gt;library('form_validation');
               $this-&gt;load-&gt;library('session');
        $this-&gt;load-&gt;helper('form');
        $this-&gt;load-&gt;helper('url');
        $this-&gt;load-&gt;database();
        $this-&gt;load-&gt;model('Login_model','login_model');
    } 
    public function index()
    {
        $this-&gt;load-&gt;library('session');
        $this-&gt;form_validation-&gt;set_rules('username','Username','trim|required');
        $this-&gt;form_validation-&gt;set_rules('password','Password','required|callback_basisdata_cek');

        if($this-&gt;form_validation-&gt;run()==false)
        {
            $this-&gt;load-&gt;view('LoginN/login_view');
        }
        else{
              //           $this-&gt;load-&gt;view('user/user');//not loading
            redirect(base_url('IndexController'),'refresh');//not loading
        }
        // $this-&gt;load-&gt;view('user/user');
        //$this-&gt;load-&gt;view('LoginN/login_view');

    }
    public function basisdata_cek()
    {

        $username= $this-&gt;input-&gt;post('username');
        $password=$this-&gt;input-&gt;post('password');
        //echo $username.' '.$password;

        $result=$this-&gt;login_model-&gt;login($username,$password);
        //echo ('fsf'.$result);
        if($result)
        {
            $sess_array = array();
            foreach ($result as $row)
            {
                $sess_array = $arrayName = array('id' =&gt; $row-&gt;id,'username'=&gt; $row-&gt;username);
                $this-&gt;session-&gt;set_userdata('logged_in',$sess_array);

            //  $ci = &amp; get_instance();
                //$ci-&gt;session-&gt;set_userdata("logged_in",$sess_array);
            }
            return true;
        }
        else{
            echo $username.' '.$password;
            $this-&gt;form_validation-&gt;set_message('basisdata_cek','Invalid user or password');
            return false;
        }
    }   

    public function register()
    {   //$this-&gt;load-&gt;library('session');


        if($this-&gt;input-&gt;post('daftar'))
        {
            $this-&gt;login_model-&gt;register();
        //  var_dump(register());
            redirect('LoginN');
        }
        else{
            $this-&gt;load-&gt;view('LoginN/register_view');
        }

    }
}

?&gt;
</code></pre>

<p>my config.php:</p>

<pre><code>&lt;?php
defined('BASEPATH') OR exit('No direct script access allowed');

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
$root = "http://".$_SERVER['HTTP_HOST'];
$root = str_replace(basename($_SERVER['SCRIPT_NAME']),"",$_SERVER['SCRIPT_NAME']);
$config['base_url'] = "http://www.cateringservices.000webhostapp.com/";

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
| URI string.  The default setting of 'REQUEST_URI' works for most servers.
| If your links do not seem to work, try one of the other delicious flavors:
|
| 'REQUEST_URI'    Uses $_SERVER['REQUEST_URI']
| 'QUERY_STRING'   Uses $_SERVER['QUERY_STRING']
| 'PATH_INFO'      Uses $_SERVER['PATH_INFO']
|
| WARNING: If you set this to 'PATH_INFO', URIs will always be URL-decoded!
*/
$config['uri_protocol'] = "REQUEST_URI";

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
$config['language'] = 'english';

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
$config['enable_hooks'] = FALSE;

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
$config['composer_autoload'] = FALSE;

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
$config['permitted_uri_chars'] = '';

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
$config['allow_get_array'] = TRUE;
$config['enable_query_strings'] = FALSE;
$config['controller_trigger'] = 'c';
$config['function_trigger'] = 'm';
$config['directory_trigger'] = 'd';

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
$config['sess_cookie_name'] = 'ci_session';
$config['sess_expiration'] = 7200;
$config['sess_save_path'] = NULL;
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
$config['cookie_path']      = '/';
$config['cookie_secure']    = FALSE;
$config['cookie_httponly']  = FALSE;

/*
|--------------------------------------------------------------------------
| Standardize newlines
|--------------------------------------------------------------------------
|
| Determines whether to standardize newline characters in input data,
| meaning to replace \r\n, \r, \n occurrences with the PHP_EOL value.
|
| This is particularly useful for portability between UNIX-based OSes,
| (usually \n) and Windows (\r\n).
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
$config['csrf_protection'] = FALSE;
$config['csrf_token_name'] = 'csrf_test_name';
$config['csrf_cookie_name'] = 'csrf_cookie_name';
$config['csrf_expire'] = 7200;
$config['csrf_regenerate'] = TRUE;
$config['csrf_exclude_uris'] = array();

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

<p>Routes.php</p>

<pre><code>    &lt;?php
defined('BASEPATH') OR exit('No direct script access allowed');

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
|   https://codeigniter.com/user_guide/general/routing.html
|
| -------------------------------------------------------------------------
| RESERVED ROUTES
| -------------------------------------------------------------------------
|
| There are three reserved routes:
|
|   $route['default_controller'] = 'welcome';
|
| This route indicates which controller class should be loaded if the
| URI contains no data. In the above example, the "welcome" class
| would be loaded.
|
|   $route['404_override'] = 'errors/page_missing';
|
| This route will tell the Router which controller/method to use if those
| provided in the URL cannot be matched to a valid route.
|
|   $route['translate_uri_dashes'] = FALSE;
|
| This is not exactly a route, but allows you to automatically route
| controller and method names that contain dashes. '-' isn't a valid
| class or method name character, so it requires translation.
| When you set this option to TRUE, it will replace ALL dashes in the
| controller and method URI segments.
|
| Examples: my-controller/index -&gt; my_controller/index
|       my-controller/my-method -&gt; my_controller/my_method
*/
$route['default_controller'] = 'LoginN';
//$route['default_controller'] = 'IndexController';

$route['404_override'] = '';
$route['translate_uri_dashes'] = FALSE;
</code></pre>

<p>kindly help....... As i ve to show to someone.</p>

## Answers
### Answer ID: 44018643
<p>First off you have named your class wrong. Filenames and class names should have <strong><em>first letter ONLY Upper case</em></strong> then the rest lower case</p>

<p><a href="https://www.codeigniter.com/user_guide/general/styleguide.html#file-naming" rel="nofollow noreferrer">https://www.codeigniter.com/user_guide/general/styleguide.html#file-naming</a></p>

<p>Filename: Loginn.php</p>

<p><a href="https://www.codeigniter.com/user_guide/general/styleguide.html#class-and-method-naming" rel="nofollow noreferrer">https://www.codeigniter.com/user_guide/general/styleguide.html#class-and-method-naming</a></p>

<pre><code>&lt;?php

class Loginn extends CI_Controller {

}
</code></pre>

<p>Lower case on route like</p>

<pre><code>$route['default_controller'] = 'loginn';
</code></pre>

<p>When redirect should be something like</p>

<pre><code>// Refresh will clear flash data if any set.
redirect(base_url('indexcontroller'), 'refresh');
</code></pre>

<p>Not</p>

<pre><code>redirect(base_url('IndexController'), 'refresh');
</code></pre>

<p>Also might be good to read <a href="https://www.codeigniter.com/user_guide/general/models.html#loading-a-model" rel="nofollow noreferrer">https://www.codeigniter.com/user_guide/general/models.html#loading-a-model</a></p>

### Answer ID: 44017803
<p>Your Login code does not have a valid path and the error is generated by your host that rejects the url because is invalid change the code like this:</p>

<pre><code>if($this-&gt;input-&gt;post('daftar'))
{
    $this-&gt;login_model-&gt;register();
    //  var_dump(register());
    redirect('somepage.php'); // Change your path to any page here
}
</code></pre>

