# [Ask-Code Igniter]-Load modal doesnt show
[Link to question](https://stackoverflow.com/questions/38988391/ask-code-igniter-load-modal-doesnt-show)
**Creation Date:** 1471409871
**Score:** 0
**Tags:** jquery, ajax, codeigniter, jqxgrid, jqwidget
## Question Body
<p>I have program that load data from database using CI then loaded into JQXgrid Jqwidget, in the JQXgrid I have customize adding button "proceed" this button will show specific data from database. 
<a href="https://i.sstatic.net/VmZly.png" rel="nofollow">This My App User Interface</a>. My plan is use modal from bootstrap to show the data, but for now, the modal when I clicked the "proceed " but not show yet, I'm relatively new in CI, JQXgrid, Jquery and Javascript, an the result should like this.
<a href="https://i.sstatic.net/HvC8q.png" rel="nofollow">Result Show Modal</a>
.So, here it is my code</p>

<p>This Is My View "vwHome.php" :</p>

<pre><code>    &lt;?php
$this-&gt;load-&gt;view('vwHeader');
?&gt;
&lt;!--  
Load Page Specific CSS and JS here
Author : Abhishek R. Kaushik 
Downloaded from http://devzone.co.in
--&gt;
&lt;link href="&lt;?php echo HTTP_CSS_PATH; ?&gt;starter-template.css" rel="stylesheet"&gt;
&lt;link href="&lt;?php echo HTTP_CSS_PATH; ?&gt;jqx.base.css" rel="stylesheet"&gt;
&lt;link href="&lt;?php echo HTTP_CSS_PATH; ?&gt;bootstrap.css" rel="stylesheet"&gt;
&lt;script type="text/javascript" src="&lt;?php echo HTTP_JS_PATH; ?&gt;jquery-1.11.1.min.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo HTTP_JS_PATH; ?&gt;jquery.min.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo HTTP_JS_PATH; ?&gt;bootstrap.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo HTTP_JS_PATH; ?&gt;bootstrap.min.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxcore.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxbuttons.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxscrollbar.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxmenu.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxgrid.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxgrid.sort.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxgrid.selection.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxgrid.columnsresize.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxgrid.pager.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxlistbox.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxdropdownlist.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo JQWIDGET; ?&gt;jqxdata.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="&lt;?php echo HTTP_JS_PATH; ?&gt;demos.js"&gt;&lt;/script&gt;

&lt;style type="text/css"&gt;
    .jqx-grid-column-header {
        font-size:10px;
        font-weight:bold;
    }
&lt;/style&gt;

&lt;script type="text/javascript"&gt;
        $(document).ready(function () {
            // prepare the data
            var source =
            {
                datatype: "json",
                datafields: [
                    { name: 'id'},
                    { name: 'buyer'},
                    { name: 'po_customer'},
                    { name: 'ship_date'},
                    { name: 'type'},
                    { name: 'kode_keramik'},
                    { name: 'nama_keramik'},
                    { name: 'target_kw1'},
                    { name: 'plan_yield'},
                    { name: 'progress'}
                ],
        id: 'id',
                url: '&lt;?php echo base_url().'home/loadDataA'?&gt;',
        root: 'Rows',
                beforeprocessing: function (data) {
                    source.totalrecords = data[0].TotalRows;
                }     
            };
            var dataAdapter = new $.jqx.dataAdapter(source);
            var cellsrenderer = function (row, column, value) {
                return '&lt;div style="text-align: right; margin-top: 5px; font-size: 10px;"&gt;&amp;nbsp;' + value + ' pcs&amp;nbsp;&lt;/div&gt;';
            };
            var cellsrenderer2 = function (row, column, value) {
                return '&lt;div style="text-align: right; margin-top: 5px; font-size: 10px;"&gt;&amp;nbsp;' + value*100 + ' %&amp;nbsp;&lt;/div&gt;';
            };
            var cellsrenderer3 = function (row, column, value) {
                return '&lt;div style="text-align: left; margin-top: 5px; font-size: 10px;"&gt;&amp;nbsp; ' + value + '&amp;nbsp;&lt;/div&gt;';
            };
            var button_renderer = function (row, columnfield, value, defaulthtml, columnproperties) {
            var id = $('#jqxgrid').jqxGrid('getcelltext', row, "id");
            button = '&lt;a href="#modal_details" class="btn btn-xs btn-success view_details" id="'+ id +'"&gt;Proceed&lt;/a&gt;';
            return button;
            };

            $("#jqxgrid").jqxGrid(
            {
                width: '100%',
                source: dataAdapter,
                theme: 'classic',
        pageable: true,
        autoheight: true,
                virtualmode: true,
                rendergridrows: function () {
                    return dataAdapter.records;
                },              
                columns: [
                  { text: 'ID', datafield: 'id', width: 30 ,  cellsrenderer: cellsrenderer3},  
                  { text: 'Action', align: 'center', datafield: 'edit', filterable: false, width: 70, cellsalign: 'center', cellsrenderer: button_renderer, editable: false, exportable: false},  
                  { text: 'Buyer', datafield: 'buyer', width: 75,  cellsrenderer: cellsrenderer3},
                  { text: 'PO Cust.', datafield: 'po_customer', width: 75 ,  cellsrenderer: cellsrenderer3},
                  { text: 'Ship. Date', datafield: 'ship_date', width: 75 ,  cellsrenderer: cellsrenderer3},
                  { text: 'Type', datafield: 'type', width: 50 ,  cellsrenderer: cellsrenderer3},
                  { text: 'Code', datafield: 'kode_keramik', width: 50 ,  cellsrenderer: cellsrenderer3},
                  { text: 'Ceramic Name', datafield: 'nama_keramik', width: 600 ,  cellsrenderer: cellsrenderer3},
                  { text: 'Target KW1', datafield: 'target_kw1', width: 80, cellsrenderer: cellsrenderer},
                  { text: 'Plan Yield', datafield: 'plan_yield', width: 70, cellsrenderer: cellsrenderer2},
                  { text: 'Progress', datafield: 'progress', width: 70, cellsrenderer: cellsrenderer2},
              ]
            });        

            var detailsInitialized = false;
             $("#jqxgrid").bind('rowselect', function (event) {
                var row = event.args.rowindex;
                var id = $("#jqxgrid").jqxGrid('getrowdata', row)['id'];
                var source =
                {
                    url: '&lt;?php echo base_url().'home/loadDataA'?&gt;',
                    async: false,
                    dataType: 'json',
                    data: {id: id},
                    datatype: "json",
                    datafields: [
                                                 { name: 'kurang_kw1' },
                                                 { name: 'hasil_kw1' },
                         { name: 'total_inspek' },
                         { name: 'aktual_yield' },
                         { name: 'aktual_yield' },
                         { name: 'plan_yield' },
                         { name: 'realisasi_glasir' },
                                                 { name: 'realisasi_bakar_ulang' },
                                                 { name: 'total_glasir_awal'},
                                                 { name: 'hasil_glasir_awal'},
                                                 { name: 'hasil_glasir_aktual'},
                                                 { name: 'kurang_glasir_awal'},
                                                 { name: 'kurang_glasir_aktual'},
                                                 { name: 'pva_glasir'},
                                                 { name: 'date_insertedb'}
                    ]    
                };
                var dataAdapter = new $.jqx.dataAdapter(source);
                // initialize jqxGrid
                $("#ordersGrid").jqxGrid(
                {
                                        width:'100%',
                                        columnsheight:'70px',
                    source: dataAdapter,
                    pageable: true,
                    autoheight: true,
                    columns: [
                                                  { text: 'Tgl. Tarik Data', datafield: 'date_insertedb', cellsformat: 'd', width: 130 ,  cellsrenderer: cellsrenderer3},
                                                  { text: 'A. Kurang&lt;br&gt;KW1', datafield: 'kurang_kw1', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'B. Hasil&lt;br&gt;KW1', datafield: 'hasil_kw1', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'C. Total &lt;br&gt;Inspek&lt;br&gt;GK', datafield: 'total_inspek', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'D. Aktual &lt;br&gt;Yield', datafield: 'aktual_yield', width: 80, cellsrenderer: cellsrenderer2},
                                                  { text: 'E. Plan &lt;br&gt;Yield', datafield: 'plan_yield', width: 100, cellsrenderer: cellsrenderer2},
                                                  { text: 'F. Realiasi &lt;br&gt;Glasir', datafield: 'realisasi_glasir', width: 100, cellsrenderer: cellsrenderer},
                                                  { text: 'G. Realisasi &lt;br&gt;Bakar&lt;br&gt;Ulang', datafield: 'realisasi_bakar_ulang', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'H. Total &lt;br&gt;Glasir', datafield: 'total_glasir_awal', cellsformat: 'd', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'I. Hasil &lt;br&gt;Glasir&lt;br&gt;Awal', datafield: 'hasil_glasir_awal', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'J. Hasil &lt;br&gt;Glasir &lt;br&gt;Aktual', datafield: 'hasil_glasir_aktual', width: 100, cellsrenderer: cellsrenderer},
                                                  { text: 'K. Kurang &lt;br&gt;Glasir &lt;br&gt;Awal', datafield: 'kurang_glasir_awal', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'L. Kurang &lt;br&gt;Glasir&lt;br&gt;Aktual', datafield: 'kurang_glasir_aktual', width: 80, cellsrenderer: cellsrenderer},
                                                  { text: 'M. PVA', datafield: 'pva_glasir', width: 80, cellsrenderer: cellsrenderer}
                      ]
                });
              });
        });

        $(document).on('click', ".view_details", function() {

            //alert("aaa");
            var url = "&lt;?php echo base_url().'getGlazeMM/ajax_get_item_list'?&gt;";
            id = this.id;

            $.post(url, {id: id} ,function(data) {

                //var data = "hello";
                var id = $('#jqxgrid').jqxGrid('getcelltextbyid', id, "id");


                var detail_head = '';
                detail_head += "&lt;b&gt;Master ID :&lt;/b&gt; "+id+"&lt;br&gt;";
                detail_head += "&lt;b&gt;Nomor lori :&lt;/b&gt; "+id+"&lt;br&gt;";
                detail_head += "&lt;b&gt;Tanggal Masuk :&lt;/b&gt; "+id+"&lt;br&gt;";
                detail_head += "&lt;b&gt;Waktu Masuk :&lt;/b&gt; "+id+"&lt;br&gt;";
                detail_head += "&lt;b&gt;Waktu Keluar :&lt;/b&gt; "+id+"&lt;br&gt;&lt;br&gt;";



                $('.modal-body').empty();
                $('.modal-body').append( detail_head+data );
                $('#modal_details').modal();


            });

        });
    &lt;/script&gt;

        &lt;h5&gt;Main Data&lt;/h5&gt;
        &lt;div id="jqxgrid"&gt;
            &lt;div class="modal fade" id="modal_details"&gt;
                &lt;div class="modal-dialog" style="width:800px;"&gt;
                    &lt;div class="modal-content"&gt;
                        &lt;div class="modal-header"&gt;
                            &lt;button type="button" class="close" data-dismiss="modal" aria-hidden="true"&gt;&amp;times;&lt;/button&gt;
                            &lt;h4 class="modal-title"&gt;Details&lt;/h4&gt;
                        &lt;/div&gt;
                        &lt;div class="modal-body"&gt;
                            &lt;p&gt;One fine body&amp;hellip;&lt;/p&gt;
                        &lt;/div&gt;
                        &lt;div class="modal-footer"&gt;
                            &lt;button type="button" class="btn btn-primary" data-dismiss="modal"&gt;Close&lt;/button&gt;
                        &lt;/div&gt;
                    &lt;/div&gt;&lt;!-- /.modal-content --&gt;
                &lt;/div&gt;&lt;!-- /.modal-dialog --&gt;
            &lt;/div&gt;&lt;!-- /.modal--&gt;
        &lt;/div&gt;
        &lt;h5&gt;Detail Data&lt;/h5&gt;
        &lt;div id="ordersGrid"&gt;
        &lt;/div&gt;

&lt;hr&gt;
&lt;?php
$this-&gt;load-&gt;view('vwFooter');

?&gt;
</code></pre>

<p>This Is My config.php :</p>

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
/* 
 * ARK Admin V2
 * Code by Abhishek R. Kaushik
 * Downloaded from http://devzone.co.in/
 */
/*
 * Generates Dynamic base_url. 
*/
$config['base_url']    = '';

define('HTTP_CSS_PATH', $config['base_url'].'assets/css/');
define('HTTP_IMAGES_PATH', $config['base_url'].'assets/images/');
define('HTTP_JS_PATH', $config['base_url'].'assets/js/');

define('HTTP_ASSETS_PATH_ADMIN', $config['base_url'].'assets/');

define('HTTP_CSS_PATH_ADMIN', $config['base_url'].'assets/admin/css/');
define('HTTP_IMAGES_PATH_ADMIN', $config['base_url'].'assets/admin/images/');
define('HTTP_JS_PATH_ADMIN', $config['base_url'].'assets/js/');
define('JQWIDGET', $config['base_url'].'assets/jqwidget/');





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
$config['encryption_key'] = 'ARK ADMIN PANEL WITH BOOTSTRAP';

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
$config['sess_expire_on_close'] = TRUE;
$config['sess_encrypt_cookie']  = FALSE;
$config['sess_use_database']    = TRUE;
$config['sess_table_name']      = 'ci_sessions';
$config['sess_match_ip']        = FALSE;
$config['sess_match_useragent'] = FALSE;
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

## Answers
### Answer ID: 39075810
<p>Finally, I can find what I'm wrong doing.
I change this :</p>

<pre><code>&lt;h5&gt;Main Data&lt;/h5&gt;
        &lt;div id="jqxgrid"&gt;
            &lt;div class="modal fade" id="modal_details"&gt;
                &lt;div class="modal-dialog" style="width:800px;"&gt;
                    &lt;div class="modal-content"&gt;
                        &lt;div class="modal-header"&gt;
                            &lt;button type="button" class="close" data-dismiss="modal" aria-hidden="true"&gt;&amp;times;&lt;/button&gt;
                            &lt;h4 class="modal-title"&gt;Details&lt;/h4&gt;
                        &lt;/div&gt;
                        &lt;div class="modal-body"&gt;
                            &lt;p&gt;One fine body&amp;hellip;&lt;/p&gt;
                        &lt;/div&gt;
                        &lt;div class="modal-footer"&gt;
                            &lt;button type="button" class="btn btn-primary" data-dismiss="modal"&gt;Close&lt;/button&gt;
                        &lt;/div&gt;
                    &lt;/div&gt;&lt;!-- /.modal-content --&gt;
                &lt;/div&gt;&lt;!-- /.modal-dialog --&gt;
            &lt;/div&gt;&lt;!-- /.modal--&gt;
        &lt;/div&gt;
        &lt;h5&gt;Detail Data&lt;/h5&gt;
        &lt;div id="ordersGrid"&gt;
        &lt;/div&gt;
</code></pre>

<p>To This One:</p>

<pre><code>&lt;h5&gt;Main Data&lt;/h5&gt;
        &lt;div id="jqxgrid"&gt;
        &lt;/div&gt;
        &lt;h5&gt;Detail Data&lt;/h5&gt;
        &lt;div id="ordersGrid"&gt;
        &lt;/div&gt;
        &lt;div class="modal fade" id="modal_details"&gt;
                &lt;div class="modal-dialog" style="width:800px;"&gt;
                    &lt;div class="modal-content"&gt;
                        &lt;div class="modal-header"&gt;
                            &lt;button type="button" class="close" data-dismiss="modal" aria-hidden="true"&gt;&amp;times;&lt;/button&gt;
                            &lt;h4 class="modal-title"&gt;Data Hasil Dari CDSM&lt;/h4&gt;
                        &lt;/div&gt;
                        &lt;div class="modal-body"&gt;
                            &lt;p&gt;One fine body&amp;hellip;&lt;/p&gt;
                        &lt;/div&gt;
                        &lt;div class="modal-footer"&gt;
                            &lt;button type="button" class="btn btn-primary" data-dismiss="modal"&gt;Close&lt;/button&gt;
                        &lt;/div&gt;
                    &lt;/div&gt;&lt;!-- /.modal-content --&gt;
                &lt;/div&gt;&lt;!-- /.modal-dialog --&gt;
            &lt;/div&gt;&lt;!-- /.modal--&gt;
</code></pre>

