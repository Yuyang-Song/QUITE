# URL rewriting via Wordpress Rewrite or .htaccess
[Link to question](https://stackoverflow.com/questions/16664579/url-rewriting-via-wordpress-rewrite-or-htaccess)
**Creation Date:** 1369121850
**Score:** 16
**Tags:** wordpress, .htaccess, url-rewriting
## Question Body
<p><strong>JUMP TO EDIT8 TO SEE HOW I SOLVED THIS</strong><br></p>

<hr>

<p>Let's say I have a Wordpress blog: <code>www.animals.com</code>. I have a certain PHP file in my theme directory: <code>www.animals.com/wp-content/themes/mytheme/db.php</code>. Also, I have a custom template for that page, so I create a new page in the Wordpress administration panel to show <code>db.php</code>: <code>www.animals.com/database</code>.</p>

<p>So if I want to read something about lions, I just go to: <code>www.animals.com/database/?animal=lion</code> (because that's the way I decided to write the PHP, inserting the value from $_GET['animal'] into the query, using PDO etc.).</p>

<p><strong>Now, I would like to access <code>www.animals.com/database/?animal=lion</code> as <code>www.animals.com/lion</code>.</strong></p>

<p>Should I use .htaccess or Wordpress Rewrite? Where should I place my .htaccess, in the root of the Wordpress folder (with wp-config.php and those files) or in my theme directory?</p>

<p>The one from the root has <code>RewriteBase /</code> and stuff from Wordpress by default. What should I write to achieve what I want? Should I put it before or after the existing code?</p>

<p><strong>EDIT</strong>: this is my <strong>public_html</strong> .htaccess and this is what I <strong>really</strong> want to do:
I have a website: <code>www.domain.com</code> and when you type this <code>http://www.domain.com/dios/?dios=agni</code> it shows you the info about the god Agni. I would like to type <code>www.domain.com/dioses/agni</code> to access the info about the god Agni. The PHP file is in <code>www.domain.com/wp-content/themes/smitespain/dios.php</code>
It's not working x_x</p>

<pre><code># BEGIN WordPress
&lt;IfModule mod_rewrite.c&gt;
RewriteEngine On
RewriteBase /
RewriteRule ^dioses/(\w*)$ dios/?dios=$1 [NC,L]
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
&lt;/IfModule&gt;

# END WordPress
</code></pre>

<p><strong>EDIT2</strong>: i'm using multisite <strong>(check EDIT4)</strong>, and again, /database/ /dios/ and /dioses/ are <strong>not</strong> actual folders I created, thats the name for the page I created in Wordpress. The thing is, now it shows the name of the god in the tab title :S that means the variable $_GET['dios'] is set, but it doesnt load the file (dios.php) =/</p>

<p><strong>EDIT3</strong>: I need to access domain.com/dios/?dios=agni specifically, because thats the URL that will let the PHP file (dios.php) to load get_header() from wordpress, so i cant access the file directly</p>

<p><strong>EDIT4</strong>: I decided to remove the multisite thing</p>

<p><strong>EDIT5</strong>: these are the Wordpress pages I have:
<code>domain.com/dioses/</code> for <code>(www.domain.com/wp-content/themes/smitespain/dioses.php)</code><br>
<code>domain.com/dios/?dios=thor</code> for <code>(www.domain.com/wp-content/themes/smitespain/dios.php)</code></p>

<p><strong>EDIT6</strong>: i was reading something in the wordpress codex..and realized that, if i wanna go to <code>domain.com/dioses</code> i can access it by going to <code>domain.com/index.php?pagename=dioses</code> or <code>domain.com/?pagename=dioses</code><br>
So, i added this between the <code>Rewritebase /</code> and the next rule: <code>RewriteRule example/test ?pagename=dioses</code> and <code>domain.com/example/test</code> redirects me to <code>domain.com/dioses</code> but it also changes the url in the address bar :(<br>
The thing is, if i try this: <code>RewriteRule example/test ?pagename=dios&amp;dios=thor</code> it will send me to the page 'dios' without the '?dios=thor'</p>

<p><strong>EDIT7</strong>: i started using wordpress rewrite, i added this to my theme's functions.php:<br></p>

<pre><code>function my_rewrite_rules() {  
    add_rewrite_rule(  
        'blah',
        'index.php?pagename=dios&amp;dios=agni',  
        'top'  
    );  
}  
add_action( 'init', 'my_rewrite_rules' );
</code></pre>

<p>and again..it loads the page dios, without the ?dios=agni</p>

<p><strong>EDIT8</strong>: and finally, I managed to make it work =)<br>
the first thing i needed to know is, the new <code>?dios=XXXX</code> will be no longer available to <code>$_GET['dios']</code> instead, you need to call <code>$wp_query-&gt;query_vars['dios']</code> so i added this to my theme's functions.php</p>

<pre><code>function add_query_vars($new_var) {
$new_var[] = "dios";
return $new_var;
}
add_filter('query_vars', 'add_query_vars');

function add_rewrite_rules($rules) {
$new_rules = array('([^/]+)' =&gt; 'index.php?pagename=dios&amp;dios=$matches[1]');
$rules = $new_rules + $rules;
return $rules;
}
add_filter('rewrite_rules_array', 'add_rewrite_rules');
</code></pre>

<p>i make sure <code>$wp_query-&gt;query_vars['dios']</code> is actually set<br>
then i just add the regular rule</p>

## Answers
### Answer ID: 56556703
<p>URL rewriting wouldn't work for me, neither by calling <code>add_filter('rewrite_rules_array', function() {})</code>, nor by calling <code>add_rewrite_rule()</code>. Apparently that was because filter <code>'rewrite_rules_array'</code> was never triggered when opening frontend website pages, so the rewrites weren't generated. </p>

<p>The solution was to go to admin area and just open page Settings -> Permalinks. I need to do that every time I want to change my rewrites. </p>

<p>I don't know if vanilla Wordpress works like that, this is probably caused by an plugin/theme a have installed.</p>

### Answer ID: 26917741
<p>There is another way to solve it, without touching WordPress.</p>

<p>Add to .htaccess </p>

<pre><code>RewriteRule ^lion /indexw.php?pagename=db&amp;dios=$1 [L,E=URI:/detail/]
</code></pre>

<p>Create file indexw.php:</p>

<pre><code>&lt;?php $_SERVER["REQUEST_URI"] = $_SERVER["REDIRECT_URI"]; include("index.php");
</code></pre>

<p>How it works? mod_rewrite sets REDIRECT_URI as specified in E=URI:value argument.
indexw.php just overwrites REQUEST_URI with correct value (Thanks to Ravi Thapliyal for an insight on this)</p>

### Answer ID: 21851371
<pre><code>RewriteEngine On
RewriteCond %{QUERY_STRING}  ^$
RewriteRule ^www\.animals\.com/lion$ /www.animals.com/database/?animal=lion [R=301,NE,NC,L]
</code></pre>

<p>Just use this code. I hope that it will works.</p>

### Answer ID: 16665304
<p>WordPress puts a global redirect on root for everything unidentified i.e. not an existing file or a folder to its <code>/index.php</code>. You on the other hand now want to redirect them to <code>?animal=unidentified</code>. So, unless the list of animal keywords is fixed any solution proposed could mess up your WordPress.</p>

<p>If you had like 10-odd animals you could add them like below to your .htaccess (at root /)</p>

<pre><code>RewriteEngine on
RewriteBase /

RewriteRule ^(lion|leopard|tiger|dog|cat)/?$ database/?animal=$1 [NC,L]

# WordPress rules come here
</code></pre>

<p>For 40-odd animals I would suggest you to have a directory (need not exist) prefix for your animals.</p>

<pre><code>RewriteRule ^a/(.+?)/?$ database/?animal=$1 [NC,L]
</code></pre>

<p>This would redirect any <code>/a/critter</code> to <code>database/?animal=critter</code> and you won't have to add them to your .htaccess manually any more. You could also have both the rules co-exist so that if you haven't modified .htaccess for <code>/panther</code> yet you could still access it at <code>/a/panther</code>.</p>

<p><em><strong>EDIT:</em></strong><br />
Okay, I looked into it and it isn't possible without writing a PHP script to intercept this request and forward it to <code>index.php</code>. Here's how mutisite works: since, none of your rewrites match it goes to <code>index.php</code>; the entry point for WordPress's php code. Somewhere deep, the code checks the REQUEST_URI header to see if it matches one of your multisites (<code>/dios</code>) and if it does, forwards the request to the page configured (<code>dios.php</code>).</p>

<p>When we do an .htaccess redirect for <code>/dioses/agni</code> we're able to hit <code>index.php</code> (by removing the [L]) but the REQUEST_URI header still remains the same (/dioses/agni) and it has no mulisite configured for it. Hence, the redirection fails.</p>

