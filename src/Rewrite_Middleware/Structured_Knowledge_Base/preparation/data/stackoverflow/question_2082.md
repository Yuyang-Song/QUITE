# Wordpress Add custom permalink
[Link to question](https://stackoverflow.com/questions/18249124/wordpress-add-custom-permalink)
**Creation Date:** 1376556100
**Score:** 0
**Tags:** wordpress, url-rewriting, permalinks
## Question Body
<p>I have a dynamic page setup in wordpress which uses a <code>$_GET['id']</code> php variable to make a query to the database. The problem is that my url format looks like the following:</p>

<blockquote>
  <p><a href="http://site.com/business/id?=123" rel="nofollow">http://site.com/business/id?=123</a></p>
</blockquote>

<p>What's the best way to make the url look like:</p>

<blockquote>
  <p><a href="http://site.com/business/business-name-here" rel="nofollow">http://site.com/business/business-name-here</a></p>
</blockquote>

<p>Is it done using rewrite rules in the .htaccess file?
Thanks in advance</p>

## Answers
### Answer ID: 22659979
<p>I've found a great class to do just that by Kyle E try it.</p>

<pre><code>&lt;?php
/*
//Author Kyle E Gentile
//To use this class you must first include the file.  
//After including the file, you need to create an options array.  For example:
$options = array(
    'query_vars' =&gt; array('var1', 'var2'),
    'rules' =&gt; array('(.+?)/(.+?)/(.+?)/?$' =&gt; 'index.php?pagename=$matches[1]&amp;var1=$matches[2]&amp;var2=$matches[3]')
);
//After creating our $option array, 
//we will need to create a new instance of the class as below:
$rewrite = new Add_rewrite_rules($options);
//You must pass the options array, this way. (If you don't there could be problems) 
//Then you can call the filters and action functions as below:
add_action('wp_head', array(&amp;$rewrite, 'flush_rules'));
add_action( 'generate_rewrite_rules', array(&amp;$rewrite, 'add_rewrite_rules') );
add_filter( 'query_vars', array(&amp;$rewrite, 'add_query_vars') );
//That is it.
*/

//prevent duplicate loading of the class if you are using this in multiply plugins
if(!class_exists('add_rewrite_rules')){

    class Add_rewrite_rules{

        var $query_vars;
        var $rules;

        function __construct($options){
            $this-&gt;init($options);
        }

        function init($options){
            foreach($options as $key =&gt; $value){
                $this-&gt;$key = $value;
            }
        }

        function rules_exist(){
            global $wp_rewrite;

            $has_rules = TRUE;

            foreach($this-&gt;rules as $key =&gt; $value){
                if(!in_array($value, $wp_rewrite-&gt;rules)){
                    $has_rules = FALSE;
                }   
            }

            return $has_rules;
        }

        //to be used add_action with the hook 'wp_head'
        //flushing rewrite rules is labor intense so we better test to see if our rules exist first
        //if the rules don't exist flush its like after a night of drinking  
        function flush_rules(){
            global $wp_rewrite;

            if(!$this-&gt;rules_exist()){
                //echo "flushed"; // If want to see this in action uncomment this line and remove this text and you will see it flushed before your eyes
                $wp_rewrite-&gt;flush_rules();
            }
        }

        //filter function to be used with add_filter() with the hook "query_vars"
        function add_query_vars($query_vars){

            foreach($this-&gt;query_vars as $var){
                $query_vars[] = $var;
            }

            return $query_vars;
        }

        //to be used with a the add_action() with the hook "generate_rewrite_rules"
        function add_rewrite_rules(){
            global $wp_rewrite;

            $wp_rewrite-&gt;rules = $this-&gt;rules + $wp_rewrite-&gt;rules;
        }

    }

}
?&gt;
</code></pre>

<p>Add the following function to the init of your plugin / functions file.</p>

<pre><code>public function rewriteRules()
{
//Add the query variables to the list so wordpress doesn't discard them or worse use them to try and find by itself what page to serve.
    $options = array(
        'query_vars' =&gt; array('trainingid', 'vakname'),
        'rules' =&gt;
            array( 'uncategorized/vak/([^/]+)/([^/]+)/?$' =&gt; 'index.php?p=1316&amp;vakname=$matches[1]&amp;level=$matches[2]'
            )
    );

    //I use a autoloader but if you don't you have to include the class.
    //include_once('path/to/AddRewriteRules.php');
    $rewrite = new AddRewriteRules($options);
    add_action('wp_head', array(&amp;$rewrite, 'flush_rules'));
    add_action('generate_rewrite_rules', array(&amp;$rewrite, 'add_rewrite_rules'));
    add_filter('query_vars', array(&amp;$rewrite, 'add_query_vars'));


}
</code></pre>

